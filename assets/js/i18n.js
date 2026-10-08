/* Altus site EN→ES translator.
   Driven by the header's `altus-lang` event + localStorage('altus-lang').
   Walks text nodes + select/placeholder/alt attributes, matching on
   whitespace-normalized English and swapping in Spanish. Originals are
   cached so switching back to EN restores exactly. A MutationObserver
   re-applies after React (DC) re-renders. */
(function () {
  var DICT = {

    /* ---- Home: verified Google rating + commitments (replaced unverified figures/quotes) ---- */
    "on Google · 62 reviews": "en Google · 62 reseñas",
    "62 Google reviews": "62 reseñas en Google",
    "Rated 4.6 out of 5 by 62 reviewers on Google.": "Calificado 4.6 de 5 por 62 personas en Google.",
    "Our commitment": "Nuestro compromiso",
    "Every step, in plain language.": "Cada paso, en palabras sencillas.",
    "Our coordinators walk you through each visit and answer your questions before you decide anything.": "Nuestros coordinadores le acompañan en cada visita y responden sus preguntas antes de que usted decida.",
    "Care close to home.": "Atención cerca de casa.",
    "Our research site sits on the JFK Medical Center campus in Lake Worth, part of the community we serve.": "Nuestro sitio de investigación está en el campus del JFK Medical Center en Lake Worth, parte de la comunidad a la que servimos.",
    "Skip to content": "Saltar al contenido",
    /* ---- Header / nav ---- */
    "Expertise": "Especialidades",
    "Volunteers": "Voluntarios",
    "Sponsors": "Patrocinadores",
    "Studies": "Estudios",
    "Team": "Equipo",
    "Enroll today": "Inscríbete hoy",
    "Enroll today →": "Inscríbete hoy →",
    "Enroll today.": "Inscríbete hoy.",

    /* ---- Footer ---- */
    "Advancing diversity through clinical trials, one community at a time. Lake Worth Beach, FL.": "Promoviendo la diversidad a través de ensayos clínicos, una comunidad a la vez. Lake Worth Beach, FL.",
    "Explore": "Explorar",
    "Company": "Compañía",
    "Our Team": "Nuestro equipo",
    "Contact": "Contacto",
    "Follow": "Síguenos",
    "© 2005–2026 Altus Clinical Research. All rights reserved.": "© 2005–2026 Altus Clinical Research. Todos los derechos reservados.",

    /* ---- Breadcrumbs ---- */
    "Home": "Inicio",
    "/ Areas of Expertise": "/ Áreas de especialización",
    "/ Studies": "/ Estudios",
    "/ Volunteers": "/ Voluntarios",
    "/ Sponsors": "/ Patrocinadores",
    "/ Contact": "/ Contacto",
    "/ Our Team": "/ Nuestro equipo",

    /* ---- Home hero ---- */
    "Lake Worth Beach, FL · Now enrolling": "Lake Worth Beach, FL · Inscripción abierta",
    "Advancing": "Promoviendo la",
    "diversity through clinical trials,": "diversidad a través de ensayos clínicos,",
    "one community at a time.": "una comunidad a la vez.",
    "A South Florida research site combining expert teams with trusted community physicians to bring safe, effective treatments to the people who need them.": "Un sitio de investigación del sur de Florida que combina equipos expertos con médicos de confianza de la comunidad para llevar tratamientos seguros y eficaces a quienes los necesitan.",
    "Volunteer for a study →": "Sea voluntario en un estudio →",
    "For sponsors": "Para patrocinadores",
    "across 160+ reviews": "en más de 160 reseñas",

    /* ---- Home stats ---- */
    "160+ reviews": "más de 160 reseñas",
    "therapeutic areas": "áreas terapéuticas",
    "phases of experience": "fases de experiencia",
    "studies enrolling now": "estudios inscribiendo ahora",

    /* ---- Mission ---- */
    "Our mission": "Nuestra misión",
    "We integrate a highly trained research team with the trusted private practices of our partner investigators, driving medical innovation while keeping our community at the center of everything we do.": "Integramos un equipo de investigación altamente capacitado con las consultas privadas de confianza de nuestros investigadores asociados, impulsando la innovación médica mientras mantenemos a nuestra comunidad en el centro de todo lo que hacemos.",

    /* ---- Home: for volunteers / for sponsors cards ---- */
    "For volunteers": "Para voluntarios",
    "Our volunteers play a critical role in advancing treatment for many conditions. We guide you through every step in plain language.": "Nuestros voluntarios desempeñan un papel fundamental en el avance del tratamiento de muchas afecciones. Le guiamos en cada paso con un lenguaje claro.",
    "Free pre-screening with our care team": "Pre-evaluación gratuita con nuestro equipo de atención",
    "Access to studies you won't find elsewhere": "Acceso a estudios que no encontrará en otro lugar",
    "Compassionate care close to home": "Atención compasiva cerca de casa",
    "See if you qualify →": "Vea si califica →",
    "We provide the pharmaceutical industry the highest quality of service while upholding the strictest ethical standards and protocol adherence.": "Brindamos a la industria farmacéutica el más alto nivel de servicio, manteniendo los estándares éticos más estrictos y el cumplimiento del protocolo.",
    "Integrated with established private practices": "Integrados con consultas privadas establecidas",
    "Subject safety & strict protocol adherence": "Seguridad del sujeto y estricto cumplimiento del protocolo",
    "Experienced Phase II–IV research team": "Equipo de investigación con experiencia en Fase II–IV",
    "Explore our facilities →": "Explore nuestras instalaciones →",

    /* ---- How it works ---- */
    "How it works": "Cómo funciona",
    "Joining a study is simple": "Unirse a un estudio es sencillo",
    "Reach out": "Comuníquese",
    "Tell us your area of interest by form or phone.": "Cuéntenos su área de interés por formulario o teléfono.",
    "Pre-screen": "Pre-evaluación",
    "A coordinator reviews eligibility at no cost.": "Un coordinador revisa la elegibilidad sin costo.",
    "Participate": "Participe",
    "Join the study with our team at every visit.": "Únase al estudio con nuestro equipo en cada visita.",
    "Make an impact": "Genere un impacto",
    "Help advance treatments for your community.": "Ayude a avanzar los tratamientos para su comunidad.",

    /* ---- Areas of expertise ---- */
    "Areas of expertise": "Áreas de especialización",
    "Research across the conditions that matter most": "Investigación en las condiciones que más importan",
    "All areas →": "Todas las áreas →",
    "Women's Studies": "Estudios de la mujer",
    "Urology": "Urología",
    "Dermatology": "Dermatología",
    "Vaccines": "Vacunas",
    "Internal Medicine": "Medicina interna",
    "Rheumatology": "Reumatología",
    "Aesthetic Medicine": "Medicina estética",

    /* ---- Currently enrolling (home + studies) ---- */
    "Open enrollment": "Inscripción abierta",
    "Currently enrolling studies": "Estudios con inscripción abierta",
    "Currently enrolling": "Inscribiendo actualmente",
    "View all studies →": "Ver todos los estudios →",
    "Enrolling · Women's": "Inscribiendo · Mujer",
    "Enrolling · Urology": "Inscribiendo · Urología",
    "Coming soon · Women's": "Próximamente · Mujer",
    "Birth Control: Contraceptive Patch": "Anticoncepción: Parche anticonceptivo",
    "Exploring estrogen-free options? A patch trial may be right for you.": "¿Explorando opciones sin estrógeno? Un ensayo de parche podría ser adecuado para usted.",
    "Urinary Incontinence": "Incontinencia urinaria",
    "You may be able to join this study. Additional criteria apply.": "Es posible que pueda unirse a este estudio. Aplican criterios adicionales.",
    "Hot Flash Study": "Estudio de sofocos",
    "Healthy participants may qualify. Additional criteria apply.": "Participantes sanos pueden calificar. Aplican criterios adicionales.",
    "Learn more →": "Más información →",

    /* ---- Reviews ---- */
    "Rated 4.7 out of 5 across 160+ reviews.": "Calificado 4.7 de 5 en más de 160 reseñas.",
    "\"The team explained everything clearly and made me feel completely at ease throughout the trial.\"": "«El equipo explicó todo con claridad y me hizo sentir completamente tranquilo durante todo el ensayo.»",
    "\"Professional, caring, and right in our community. My time and safety always mattered to them.\"": "«Profesionales, atentos y justo en nuestra comunidad. Mi tiempo y mi seguridad siempre les importaron.»",
    "Study Volunteer": "Voluntario del estudio",

    /* ---- Home CTA ---- */
    "Get started": "Comencemos",
    "Ready to take the next step?": "¿Listo para dar el siguiente paso?",
    "Tell us a little about yourself and our team will reach out about current and upcoming studies.": "Cuéntenos un poco sobre usted y nuestro equipo se comunicará acerca de los estudios actuales y futuros.",
    "Call 561-641-0404": "Llame al 561-641-0404",

    /* ---- Expertise page ---- */
    "Seven therapeutic areas, all delivered from one trusted South Florida site. Our investigators conduct Phase II–IV trials with the highest standards of subject safety and protocol adherence.": "Siete áreas terapéuticas, todas desde un sitio de confianza del sur de Florida. Nuestros investigadores realizan ensayos de Fase II–IV con los más altos estándares de seguridad del sujeto y cumplimiento del protocolo.",
    "Contraception, hormone health, uterine fibroids and more, in partnership with our OB/GYN practice.": "Anticoncepción, salud hormonal, fibromas uterinos y más, en colaboración con nuestra consulta de ginecología y obstetricia.",
    "Urinary incontinence, overactive bladder and related conditions, supported by on-site uroflow.": "Incontinencia urinaria, vejiga hiperactiva y afecciones relacionadas, con uroflujometría en el sitio.",
    "Plaque psoriasis, actinic keratosis and other skin conditions evaluated with state-of-the-art tools.": "Psoriasis en placas, queratosis actínica y otras afecciones de la piel evaluadas con herramientas de última generación.",
    "Vaccine trials including meningococcal and COVID-19, with cold-chain storage and IATA-certified staff.": "Ensayos de vacunas, incluidas meningocócica y COVID-19, con almacenamiento en cadena de frío y personal certificado por IATA.",
    "High blood pressure, diabetes and fatty liver, and other chronic conditions managed by our investigators.": "Presión arterial alta, diabetes e hígado graso, y otras afecciones crónicas gestionadas por nuestros investigadores.",
    "Osteoarthritis of the knee and inflammatory conditions, with on-site imaging and DEXA.": "Osteoartritis de rodilla y afecciones inflamatorias, con imágenes y DEXA en el sitio.",
    "Cosmetic and aesthetic dermatology trials evaluating new treatments and devices.": "Ensayos de dermatología cosmética y estética que evalúan nuevos tratamientos y dispositivos.",
    "Not sure which study fits you?": "¿No sabe qué estudio es adecuado para usted?",
    "Our coordinators will help you find the right trial at no cost. Reach out and we'll take it from there.": "Nuestros coordinadores le ayudarán a encontrar el ensayo adecuado sin costo. Comuníquese y nosotros nos encargamos del resto.",
    "Talk to our team →": "Hable con nuestro equipo →",

    /* ---- Studies page ---- */
    "Clinical studies": "Estudios clínicos",
    "Find a study that's right for you": "Encuentre un estudio adecuado para usted",
    "Browse our currently enrolling trials below, or explore the studies we've completed. Pre-screening is always free.": "Explore nuestros ensayos con inscripción abierta a continuación, o vea los estudios que hemos completado. La pre-evaluación siempre es gratuita.",
    "Completed": "Completados",
    "Past studies": "Estudios anteriores",
    "Past studies · Dermatology": "Estudios anteriores · Dermatología",
    "Past studies · Vaccines": "Estudios anteriores · Vacunas",
    "Past studies · Internal Medicine": "Estudios anteriores · Medicina interna",
    "Past studies · Rheumatology": "Estudios anteriores · Reumatología",
    "Past studies · Women's": "Estudios anteriores · Mujer",
    "Past studies · Urology": "Estudios anteriores · Urología",
    "Actinic Keratosis": "Queratosis actínica",
    "COVID-19 Study": "Estudio de COVID-19",
    "Diabetes & Fatty Liver": "Diabetes e hígado graso",
    "High Blood Pressure": "Presión arterial alta",
    "Meningococcal Vaccine": "Vacuna meningocócica",
    "Moderna Vaccine": "Vacuna de Moderna",
    "Osteoarthritis of the Knee": "Osteoartritis de rodilla",
    "Pelvic Pain": "Dolor pélvico",
    "Plaque Psoriasis": "Psoriasis en placas",
    "Psoriasis Study": "Estudio de psoriasis",
    "Uterine Fibroids": "Fibromas uterinos",
    "UTI (Urinary Tract Infections)": "ITU (Infecciones del tracto urinario)",
    "Evaluated a topical treatment for actinic keratosis skin lesions.": "Evaluó un tratamiento tópico para las lesiones cutáneas de queratosis actínica.",
    "Tested a candidate vaccine for the prevention of COVID-19.": "Probó una vacuna candidata para la prevención de la COVID-19.",
    "Investigated a therapy for adults living with diabetes and fatty liver.": "Investigó una terapia para adultos que viven con diabetes e hígado graso.",
    "Enrolled men and women with high blood pressure to assess a new treatment.": "Inscribió a hombres y mujeres con presión arterial alta para evaluar un nuevo tratamiento.",
    "Evaluated a vaccine for the prevention of meningococcal disease.": "Evaluó una vacuna para la prevención de la enfermedad meningocócica.",
    "Assessed an mRNA vaccine candidate in eligible adult participants.": "Evaluó una vacuna candidata de ARNm en participantes adultos elegibles.",
    "Examined an investigational drug for osteoarthritis of the knee.": "Examinó un medicamento en investigación para la osteoartritis de rodilla.",
    "Studied an investigational drug for women experiencing pelvic pain.": "Estudió un medicamento en investigación para mujeres con dolor pélvico.",
    "Enrolled adults with moderate-to-severe plaque psoriasis.": "Inscribió a adultos con psoriasis en placas de moderada a grave.",
    "Evaluated a new treatment for men and women living with psoriasis.": "Evaluó un nuevo tratamiento para hombres y mujeres que viven con psoriasis.",
    "Investigated a treatment option for women with uterine fibroids.": "Investigó una opción de tratamiento para mujeres con fibromas uterinos.",
    "Evaluated a treatment for women with urinary tract infections.": "Evaluó un tratamiento para mujeres con infecciones del tracto urinario.",
    "Completed study": "Estudio completado",
    "See a study you're interested in?": "¿Ve un estudio que le interese?",
    "Reach out and a coordinator will check your eligibility, free and with no obligation.": "Comuníquese y un coordinador verificará su elegibilidad: gratis y sin compromiso.",
    "Get pre-screened →": "Pre-evaluación gratuita →",

    /* ---- Volunteers page ---- */
    "Your participation moves medicine forward": "Su participación hace avanzar la medicina",
    "Volunteers play a critical role in advancing treatment for many conditions. We guide you through every step in plain language, with compassionate care close to home.": "Los voluntarios desempeñan un papel fundamental en el avance del tratamiento de muchas afecciones. Le guiamos en cada paso con un lenguaje claro y atención compasiva cerca de casa.",
    "Browse studies": "Explorar estudios",
    "Free pre-screening": "Pre-evaluación gratuita",
    "A coordinator reviews your eligibility at no cost and with no obligation to continue.": "Un coordinador revisa su elegibilidad sin costo y sin obligación de continuar.",
    "Access to new options": "Acceso a nuevas opciones",
    "Join studies and treatments you won't find through routine care elsewhere.": "Participe en estudios y tratamientos que no encontrará en la atención de rutina en otro lugar.",
    "Care close to home": "Atención cerca de casa",
    "Compassionate, attentive care from a team that treats your time and safety as the priority.": "Atención compasiva y atenta de un equipo que trata su tiempo y su seguridad como la prioridad.",
    "Ready to get started?": "¿Listo para comenzar?",
    "Take the first step today. Pre-screening is always free and there's no obligation to continue.": "Dé el primer paso hoy. La pre-evaluación siempre es gratuita y no hay obligación de continuar.",

    /* ---- Sponsors page ---- */
    "For research sponsors": "Para patrocinadores de investigación",
    "A quality research site, ready for your next study": "Un sitio de investigación de calidad, listo para su próximo estudio",
    "We offer our sponsors a trained and experienced clinical research team. The diverse Palm Beach County suburban population, exceeding 1.3 million, supports FDA standards for ethnically and racially diverse subjects, and our central location near major highways and public transportation keeps access easy for both subjects and sponsor visits.": "Ofrecemos a nuestros patrocinadores un equipo de investigación clínica capacitado y con experiencia. La diversa población suburbana del condado de Palm Beach, que supera los 1.3 millones, respalda los estándares de la FDA para sujetos de diversidad étnica y racial, y nuestra ubicación central cerca de las principales autopistas y el transporte público facilita el acceso tanto para los sujetos como para las visitas de los patrocinadores.",
    "About our research facilities": "Acerca de nuestras instalaciones",
    "5,000 sq. ft. state-of-the-art facility integrated with clinical practice": "Instalación de última generación de 5,000 pies cuadrados integrada con la práctica clínica",
    "Board Certified physicians with years of clinical experience": "Médicos certificados con años de experiencia clínica",
    "Investigators on-site daily": "Investigadores en el sitio a diario",
    "Experienced Certified Clinical Research Coordinators": "Coordinadores de investigación clínica certificados y con experiencia",
    "Access to a 35,000-patient database": "Acceso a una base de datos de 35,000 pacientes",
    "Associated with a large OB/GYN private practice": "Asociados con una gran consulta privada de ginecología y obstetricia",
    "Academic site utilizing Central IRBs": "Sitio académico que utiliza IRB centrales",
    "Proven history of rapid enrollment": "Historial comprobado de inscripción rápida",
    "Secured drug room & study files with restricted access": "Sala de medicamentos y archivos de estudio asegurados con acceso restringido",
    "Locked, explosion-proof refrigerator monitored 24 hours a day": "Refrigerador cerrado y a prueba de explosiones monitoreado las 24 horas del día",
    "IATA Certified staff with daily access to dry ice": "Personal certificado por IATA con acceso diario a hielo seco",
    "Multiple patient exam rooms with gowns & drapes": "Múltiples salas de examen con batas y campos",
    "Sonogram with 4D imaging, digital capture & 52″ display": "Ecógrafo con imágenes 4D, captura digital y pantalla de 52″",
    "GE DEXA machine with digital reporting": "Máquina DEXA de GE con informes digitales",
    "State-of-the-art colposcope & CLIA certified laboratory": "Colposcopio de última generación y laboratorio certificado por CLIA",
    "Private monitoring area with phone, T-1 line, internet & email": "Área de monitoreo privada con teléfono, línea T-1, internet y correo electrónico",
    "Daily DHL & FedEx pick-up; electronic data entry experience": "Recogida diaria de DHL y FedEx; experiencia en entrada electrónica de datos",
    "On-site archiving & 24-hour access to on-call physician": "Archivo en el sitio y acceso las 24 horas a un médico de guardia",
    "Knowledgeable of GCP and NIH standards": "Conocimiento de los estándares de GCP y NIH",
    "HIPAA compliant, centrally located near freeways, hotels & airport": "Cumple con HIPAA, ubicación central cerca de autopistas, hoteles y aeropuerto",
    "Available resources": "Recursos disponibles",
    "Centrifuge": "Centrífuga",
    "Clinical Laboratory": "Laboratorio clínico",
    "Crash Cart": "Carro de paro",
    "DEXA Scanner": "Escáner DEXA",
    "Dry Ice": "Hielo seco",
    "EKG Equipment": "Equipo de electrocardiograma",
    "Fax / Scanner": "Fax / Escáner",
    "Freezer (−20°C)": "Congelador (−20°C)",
    "Freezer (−70°C)": "Congelador (−70°C)",
    "Refrigerator (2–8°C)": "Refrigerador (2–8°C)",
    "Gram Stain Testing": "Pruebas de tinción de Gram",
    "Wright Stain Testing": "Pruebas de tinción de Wright",
    "High Speed Internet": "Internet de alta velocidad",
    "Microscope": "Microscopio",
    "Pharmacy": "Farmacia",
    "Phlebotomy": "Flebotomía",
    "Radiology Equipment": "Equipo de radiología",
    "Secure Medication Storage": "Almacenamiento seguro de medicamentos",
    "Secure Records Retention": "Conservación segura de registros",
    "Ultrasound": "Ultrasonido",
    "Uroflow": "Uroflujometría",
    "Institutional Bio-safety": "Bioseguridad institucional",
    "Committee Certification": "Certificación del comité",
    "Written SOPs": "POE escritos",
    "Interested in placing a study with us? Let's talk about your protocol, timelines, and enrollment goals.": "¿Interesado en colocar un estudio con nosotros? Hablemos sobre su protocolo, cronogramas y objetivos de inscripción.",
    "Discuss your study with us →": "Hablemos de su estudio →",

    /* ---- Team page ---- */
    "Our people": "Nuestra gente",
    "Meet the Altus team": "Conozca al equipo de Altus",
    "Trained, experienced research professionals who adhere to the highest ethical, regulatory, and industry standards, and stay current through ongoing continuing education.": "Profesionales de investigación capacitados y con experiencia que se adhieren a los más altos estándares éticos, regulatorios y de la industria, y se mantienen actualizados mediante educación continua.",
    "Investigator": "Investigador",
    "Medical Director & Principal Investigator": "Director médico e investigador principal",
    "Sub-Investigator": "Subinvestigador",
    "PA-C & Sub-Investigator": "PA-C y subinvestigador",
    "Director of Operations": "Directora de operaciones",
    "Assistant Site Director": "Subdirectora del sitio",
    "Office Manager": "Gerente de oficina",
    "Regulatory Manager": "Gerente regulatorio",
    "Lead Research Coordinator": "Coordinadora principal de investigación",
    "Clinical Research Assistant": "Asistente de investigación clínica",
    "Data Entry / Programmer": "Entrada de datos / Programador",
    "Data Entry Specialist": "Especialista en entrada de datos",
    "Photo": "Foto",

    /* ---- Contact page ---- */
    "First name": "Nombre",
    "Last name": "Apellido",
    "Phone": "Teléfono",
    "Email": "Correo electrónico",
    "Area of interest": "Área de interés",
    "Message (optional)": "Mensaje (opcional)",
    "We'll never share your information. By submitting, you agree to be contacted about studies.": "Nunca compartiremos su información. Al enviar, acepta ser contactado acerca de los estudios.",

    /* ---- Warm variant (single-page concept) ---- */
    "Now enrolling in Lake Worth Beach, FL": "Inscripción abierta en Lake Worth Beach, FL",
    "Advancing diversity through clinical trials,": "Promoviendo la diversidad a través de ensayos clínicos,",
    "3 studies": "3 estudios",
    "A South Florida research site combining expert teams with community physicians to bring safe, effective treatments to the people who need them.": "Un sitio de investigación del sur de Florida que combina equipos expertos con médicos de la comunidad para llevar tratamientos seguros y eficaces a quienes los necesitan.",
    "\"We integrate a highly trained research team with trusted private practices, driving medical innovation while keeping our community at the center of everything we do.\"": "«Integramos un equipo de investigación altamente capacitado con consultas privadas de confianza, impulsando la innovación médica mientras mantenemos a nuestra comunidad en el centro de todo lo que hacemos.»",
    "Phase I–IV": "Fase I–IV",
    "trial experience": "experiencia en ensayos",
    "Experienced Phase I–IV research team": "Equipo de investigación con experiencia en Fase I–IV",
    "Start a conversation →": "Inicie una conversación →",
    "Tell us your area of interest through our form or by phone.": "Cuéntenos su área de interés a través de nuestro formulario o por teléfono.",
    "A coordinator reviews your eligibility, at no cost to you.": "Un coordinador revisa su elegibilidad, sin costo para usted.",
    "Take part in the study with our team supporting every visit.": "Participe en el estudio con nuestro equipo apoyándole en cada visita.",
    "Help advance treatments for your community and beyond.": "Ayude a avanzar los tratamientos para su comunidad y más allá.",
    "Seven therapeutic areas, all delivered from one trusted South Florida site.": "Siete áreas terapéuticas, todas desde un sitio de confianza del sur de Florida.",
    "\"Professional, caring, and right in our community. I always felt my time and safety mattered.\"": "«Profesionales, atentos y justo en nuestra comunidad. Siempre sentí que mi tiempo y mi seguridad importaban.»",
    "A highly trained research team working hand-in-hand with our partner investigators.": "Un equipo de investigación altamente capacitado que trabaja codo a codo con nuestros investigadores asociados.",
    "Principal Investigator": "Investigador principal",
    "Medical Director": "Director médico",
    "Clinical Research Coordinator": "Coordinador de investigación clínica",
    "Patient Care": "Atención al paciente",
    "Sub-Investigator (Partner Physician)": "Subinvestigador (médico asociado)",
    "Partner Physician": "Médico asociado",
    "Regulatory Specialist": "Especialista regulatorio",
    "Compliance": "Cumplimiento",
    "Our team": "Nuestro equipo",
    "© 2026 Altus Clinical Research. All rights reserved.": "© 2026 Altus Clinical Research. Todos los derechos reservados."
  };

  var ATTRS = ["placeholder", "alt", "aria-label", "title"];
  var SKIP = { SCRIPT: 1, STYLE: 1, NOSCRIPT: 1 };
  var lang = "en";
  try {
    var s = localStorage.getItem("altus-lang");
    if (s === "es" || s === "en") lang = s;
  } catch (e) {}

  function norm(v) { return v.replace(/\s+/g, " ").trim(); }

  function applyText(node) {
    if (node.__omEN === undefined) node.__omEN = node.nodeValue;
    var orig = node.__omEN;
    var key = norm(orig);
    if (!key) return;
    if (lang === "es" && DICT[key]) {
      var lead = (orig.match(/^\s*/) || [""])[0];
      var trail = (orig.match(/\s*$/) || [""])[0];
      var next = lead + DICT[key] + trail;
      if (node.nodeValue !== next) node.nodeValue = next;
    } else if (node.nodeValue !== orig) {
      node.nodeValue = orig;
    }
  }

  function applyAttrs(el) {
    for (var i = 0; i < ATTRS.length; i++) {
      var a = ATTRS[i];
      if (!el.hasAttribute(a)) continue;
      var store = "__omA_" + a;
      if (el[store] === undefined) el[store] = el.getAttribute(a);
      var orig = el[store];
      var key = norm(orig);
      if (!key) continue;
      var want = (lang === "es" && DICT[key]) ? DICT[key] : orig;
      if (el.getAttribute(a) !== want) el.setAttribute(a, want);
    }
  }

  function walk(root) {
    var tw = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        if (!n.parentNode || SKIP[n.parentNode.nodeName]) return NodeFilter.FILTER_REJECT;
        return n.nodeValue && n.nodeValue.trim() ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_SKIP;
      }
    });
    var nodes = [], n;
    while ((n = tw.nextNode())) nodes.push(n);
    for (var i = 0; i < nodes.length; i++) applyText(nodes[i]);
    var els = root.querySelectorAll("[placeholder],[alt],[aria-label],[title]");
    for (var j = 0; j < els.length; j++) applyAttrs(els[j]);
  }

  var observer = null;
  function apply() {
    if (observer) observer.disconnect();
    walk(document.body);
    if (observer) observer.observe(document.body, { childList: true, subtree: true, characterData: true });
  }

  function start() {
    apply();
    observer = new MutationObserver(function () {
      observer.disconnect();
      walk(document.body);
      observer.observe(document.body, { childList: true, subtree: true, characterData: true });
    });
    observer.observe(document.body, { childList: true, subtree: true, characterData: true });
  }

  window.addEventListener("altus-lang", function (e) {
    if (e && e.detail) lang = e.detail;
    apply();
  });

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
