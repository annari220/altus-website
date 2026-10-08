#!/usr/bin/env python3
"""One-time import of WordPress posts and long-form pages.

Usage: python3 tools/import_wp.py path/to/altus-wp-export.json
Writes content/articles.json (metadata) and content/articles/<slug>.html
(cleaned body HTML). Links to altusresearch.com become {{ROOT}}-relative so
they work on any host. Images keep their /wp-content/uploads/ paths.
"""
import html
import json
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, Comment

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "content"
SKIP_POSTS = {"dlm-internal", "paid-vs-unpaid-clinical-trial-patients-does-money-encourage-better-results"}
# Long-form WordPress *pages* that read as articles (kept at their nested paths).
ARTICLE_PAGES = {
    "/volunteers/what-to-expect-when-you-volunteer-for-a-clinical-trial-in-palm-beach-fl/",
    "/areas-of-expertise/clinical-trials-near-me-in-palm-beach-fl/",
    "/areas-of-expertise/internal-medicine/internal-medicine-clinical-research-in-palm-springs-fl/",
    "/areas-of-expertise/aesthetic-medicine/aesthetic-medicine-clinical-research-in-boynton-beach-fl/",
}
ALLOWED = {"p", "h2", "h3", "h4", "ul", "ol", "li", "a", "strong", "em", "b", "i", "blockquote", "br",
           "img", "figure", "figcaption", "table", "thead", "tbody", "tr", "th", "td"}
SITE = re.compile(r"^https?://(www\.)?altusresearch\.com")


def clean(raw):
    s = BeautifulSoup(raw, "html.parser")
    for c in s.find_all(string=lambda t: isinstance(t, Comment)):
        c.extract()
    for t in s(["script", "style", "form", "noscript", "iframe", "svg", "button", "input"]):
        t.decompose()
    for h in s.find_all("h1"):
        h.name = "h2"
    for h in s.find_all(["h5", "h6"]):
        h.name = "h4"
    for el in list(s.find_all(True)):
        if el.name not in ALLOWED:
            el.unwrap()
            continue
        keep = {}
        if el.name == "a" and not el.get("href", "").strip():
            el.unwrap()
            continue
        if el.name == "a" and el.get("href"):
            href = el["href"].strip()
            href = SITE.sub("", href)
            if href == "":
                href = "/"
            if href == "volunteer-page-url":
                href = "/volunteers/"
            if href.startswith("tel:"):
                href = "tel:+15616410404"
            if href.startswith("/"):
                if href.startswith("/pages/") or href.startswith("/dlm-internal"):
                    href = "/contact-us/"
                href = "{{ROOT}}" + href.lstrip("/")
            keep["href"] = href
            if href.startswith("http"):
                keep["target"] = "_blank"
                keep["rel"] = "noopener"
        if el.name == "img":
            src = SITE.sub("", el.get("src", ""))
            if not src.startswith("/wp-content/"):
                el.decompose()
                continue
            keep = {"src": "{{ROOT}}" + src.lstrip("/"), "alt": el.get("alt", ""), "loading": "lazy",
                    "decoding": "async"}
            if el.get("width") and el.get("height"):
                keep["width"], keep["height"] = el["width"], el["height"]
        el.attrs = keep
    # drop empty paragraphs / headings
    for el in s.find_all(["p", "h2", "h3", "h4", "li"]):
        if not el.get_text(strip=True) and not el.find("img"):
            el.decompose()
    out = str(s)
    out = re.sub(r"\n{3,}", "\n\n", out).strip()
    out = out.replace("&nbsp;", " ")
    return out


def main(path):
    d = json.load(open(path, encoding="utf-8"))
    media = {m["id"]: m for m in d["media"]}
    (OUT / "articles").mkdir(parents=True, exist_ok=True)
    meta = []
    items = [("post", p) for p in d["posts"] if p["slug"] not in SKIP_POSTS]
    items += [("page", p) for p in d["pages"]
              if SITE.sub("", p["link"]) in ARTICLE_PAGES]
    for kind, it in items:
        link = SITE.sub("", it["link"])
        y = it.get("yoast_head_json") or {}
        img = None
        fm = it.get("featured_media")
        if fm and fm in media:
            img = SITE.sub("", media[fm]["source_url"]).lstrip("/")
        elif y.get("og_image"):
            img = SITE.sub("", y["og_image"][0]["url"]).lstrip("/")
        if img and not (ROOT / img).exists():
            img = None
        body = clean(it["content"]["rendered"])
        slug = link.strip("/").replace("/", "__")
        (OUT / "articles" / f"{slug}.html").write_text(body + "\n", encoding="utf-8")
        title = html.unescape(it["title"]["rendered"]).strip()
        desc = html.unescape(y.get("description") or "")
        if not desc:
            desc = re.sub(r"\s+", " ", BeautifulSoup(body, "html.parser").get_text(" ")).strip()[:155]
        meta.append({"kind": kind, "path": link, "file": f"{slug}.html", "title": title,
                     "desc": desc, "date": it["date"][:10], "modified": it["modified"][:10], "img": img})
    meta.sort(key=lambda m: m["date"], reverse=True)
    (OUT / "articles.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"imported {len(meta)} articles ({sum(m['kind']=='post' for m in meta)} posts)")
    print("missing image:", [m["path"] for m in meta if not m["img"]])


if __name__ == "__main__":
    main(sys.argv[1])
