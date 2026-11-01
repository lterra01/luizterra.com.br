"""Localized editorial architecture for the Luiz Terra authority hub."""

from __future__ import annotations


UI = {
    "en": {
        "insights_heading": "Insights",
        "insights_support": "Executive perspectives on Telecom, CX, BPO, Contact Centers, AI, international markets and technology ecosystems.",
        "all": "All",
        "filters": ["Telecom", "AI & Automation", "CX & BPO", "LATAM", "International Growth"],
        "read_article": "Read Article",
        "view_all": "View all insights",
        "original_edition": "Original edition on LinkedIn",
        "published": "Published",
        "written_by": "Written by",
        "share_linkedin": "Share on LinkedIn",
        "copy_link": "Copy Link",
        "copied": "Link copied",
        "explore_topic": "Explore topic",
        "topic_articles": "Selected insights",
        "topic_themes": "What this topic includes",
        "executive_view": "Executive perspective",
        "decision_framework": "Executive decision framework",
        "questions_heading": "Questions leaders should answer",
        "questions_intro": "A useful decision starts with evidence, ownership and a clear operating consequence. These questions help turn the topic into an actionable review.",
        "question_template": "What should leaders verify about “{theme}” before approving a larger rollout, an operational change or market expansion?",
        "bio": "Executive Bio",
        "download_bio": "Download Executive Bio PDF",
        "strategic_conversation": "Start a Strategic Conversation",
        "topics": "Topics",
        "nav_label": "Main navigation", "home_label": "LT - Luiz Terra home",
        "language_label": "Language versions", "footer_label": "Footer links",
        "breadcrumb": "Breadcrumb", "categories": "Insight categories",
        "primary_actions": "Primary actions", "sectors": "Key sectors and markets",
        "career_stats": "Career statistics", "skills_label": "Skills and expertise",
        "rights": "All rights reserved.", "email": "Email", "schedule": "Schedule a conversation",
        "contact_subject": "Strategic conversation", "collection_label": "eBooks: CX in Practice",
        "ai_agent": "AI Agent",
    },
    "pt": {
        "insights_heading": "Análises",
        "insights_support": "Perspectivas executivas sobre Telecom, CX, BPO, Contact Centers, IA, mercados internacionais e ecossistemas de tecnologia.",
        "all": "Todos",
        "filters": ["Telecom", "IA e Automação", "CX e BPO", "LATAM", "Crescimento Internacional"],
        "read_article": "Ler artigo",
        "view_all": "Ver todas as análises",
        "original_edition": "Edição original no LinkedIn",
        "published": "Publicado",
        "written_by": "Escrito por",
        "share_linkedin": "Compartilhar no LinkedIn",
        "copy_link": "Copiar link",
        "copied": "Link copiado",
        "explore_topic": "Explorar tema",
        "topic_articles": "Artigos selecionados",
        "topic_themes": "O que este tema inclui",
        "executive_view": "Perspectiva executiva",
        "decision_framework": "Roteiro executivo de decisão",
        "questions_heading": "Perguntas que a liderança deve responder",
        "questions_intro": "Uma boa decisão começa com evidências, responsabilidade definida e consequência operacional clara. Estas perguntas ajudam a transformar o tema em uma avaliação prática.",
        "question_template": "O que a liderança deve verificar sobre “{theme}” antes de ampliar a operação, aprovar uma mudança operacional ou expandir para novos mercados?",
        "bio": "Biografia Executiva",
        "download_bio": "Baixar biografia em PDF (inglês)",
        "strategic_conversation": "Iniciar uma conversa estratégica",
        "topics": "Temas",
        "nav_label": "Navegação principal", "home_label": "LT - Página inicial de Luiz Terra",
        "language_label": "Versões de idioma", "footer_label": "Links do rodapé",
        "breadcrumb": "Caminho de navegação", "categories": "Categorias de artigos",
        "primary_actions": "Ações principais", "sectors": "Principais setores e mercados",
        "career_stats": "Indicadores da trajetória profissional", "skills_label": "Competências e especialidades",
        "rights": "Todos os direitos reservados.", "email": "E-mail", "schedule": "Agendar conversa",
        "contact_subject": "Conversa estratégica", "collection_label": "eBooks: CX na Prática",
        "ai_agent": "Assistente de IA",
    },
    "es": {
        "insights_heading": "Análisis",
        "insights_support": "Perspectivas ejecutivas sobre Telecom, CX, BPO, Contact Centers, IA, mercados internacionales y ecosistemas de tecnología.",
        "all": "Todos",
        "filters": ["Telecom", "IA y Automatización", "CX y BPO", "LATAM", "Crecimiento Internacional"],
        "read_article": "Leer artículo",
        "view_all": "Ver todos los análisis",
        "original_edition": "Edición original en LinkedIn",
        "published": "Publicado",
        "written_by": "Escrito por",
        "share_linkedin": "Compartir en LinkedIn",
        "copy_link": "Copiar enlace",
        "copied": "Enlace copiado",
        "explore_topic": "Explorar tema",
        "topic_articles": "Artículos seleccionados",
        "topic_themes": "Qué incluye este tema",
        "executive_view": "Perspectiva ejecutiva",
        "decision_framework": "Marco ejecutivo para la toma de decisiones",
        "questions_heading": "Preguntas que el liderazgo debe responder",
        "questions_intro": "Una buena decisión comienza con evidencia, responsabilidad definida y una consecuencia operativa clara. Estas preguntas ayudan a convertir el tema en una evaluación práctica.",
        "question_template": "¿Qué debe verificar la dirección sobre «{theme}» antes de ampliar la operación, aprobar un cambio operativo o expandirse a nuevos mercados?",
        "bio": "Biografía Ejecutiva",
        "download_bio": "Descargar biografía en PDF (inglés)",
        "strategic_conversation": "Iniciar una conversación estratégica",
        "topics": "Temas",
        "nav_label": "Navegación principal", "home_label": "LT - Página de inicio de Luiz Terra",
        "language_label": "Versiones de idioma", "footer_label": "Enlaces del pie de página",
        "breadcrumb": "Ruta de navegación", "categories": "Categorías de artículos",
        "primary_actions": "Acciones principales", "sectors": "Principales sectores y mercados",
        "career_stats": "Indicadores de la trayectoria profesional", "skills_label": "Competencias y especialidades",
        "rights": "Todos los derechos reservados.", "email": "Correo electrónico", "schedule": "Agendar una conversación",
        "contact_subject": "Conversación estratégica", "collection_label": "eBooks: CX en la Práctica",
        "ai_agent": "Asistente de IA",
    },
}


ARTICLE_TAG_LABELS = {
    "ai amd": {"pt": "AMD com IA", "es": "AMD con IA"},
    "ai answering machine detection": {"pt": "Detecção de secretárias eletrônicas com IA", "es": "Detección de contestadores automáticos con IA"},
    "ai evaluation": {"pt": "Avaliação de IA", "es": "Evaluación de IA"},
    "ai governance": {"pt": "Governança de IA", "es": "Gobernanza de IA"},
    "amd contact center": {"pt": "AMD em contact centers", "es": "AMD en contact centers"},
    "bpo telecom": {"pt": "Telecom para BPO", "es": "Telecom para BPO"},
    "bpo telecom infrastructure": {"pt": "Infraestrutura de telecom para BPO", "es": "Infraestructura de telecomunicaciones para BPO"},
    "brazil bpo": {"pt": "BPO no Brasil", "es": "BPO en Brasil"},
    "brazil contact center": {"pt": "Contact center no Brasil", "es": "Contact center en Brasil"},
    "ccaas latam": {"pt": "CCaaS na América Latina", "es": "CCaaS en Latinoamérica"},
    "ccaas sbc": {"pt": "CCaaS e SBC", "es": "CCaaS y SBC"},
    "ccaas expansion": {"pt": "Expansão de CCaaS", "es": "Expansión de CCaaS"},
    "cx operations": {"pt": "Operações de CX", "es": "Operaciones de CX"},
    "cx stack": {"pt": "Arquitetura de CX", "es": "Arquitectura de CX"},
    "contact center": {"pt": "Contact Center", "es": "Contact Center"},
    "contact center ai": {"pt": "IA em contact centers", "es": "IA en contact centers"},
    "gtm alignment": {"pt": "Alinhamento de entrada no mercado", "es": "Alineación de entrada al mercado"},
    "latam bpo": {"pt": "BPO na América Latina", "es": "BPO en Latinoamérica"},
    "latam cx": {"pt": "CX na América Latina", "es": "CX en Latinoamérica"},
    "latam market entry": {"pt": "Entrada no mercado latino-americano", "es": "Entrada al mercado latinoamericano"},
    "latam nearshore": {"pt": "Nearshore na América Latina", "es": "Nearshore en Latinoamérica"},
    "media observability": {"pt": "Observabilidade de mídia", "es": "Observabilidad del audio"},
    "pstn": {"pt": "PSTN", "es": "PSTN"},
    "portuguese customer service": {"pt": "Atendimento em português", "es": "Atención en portugués"},
    "sbc contact center": {"pt": "SBC para contact centers", "es": "SBC para contact centers"},
    "sip contact center": {"pt": "SIP em contact centers", "es": "SIP en contact centers"},
    "sip interoperability": {"pt": "Interoperabilidade SIP", "es": "Interoperabilidad SIP"},
    "sla": {"pt": "SLA", "es": "SLA"},
    "telecom": {"pt": "Telecom", "es": "Telecom"},
    "voice ai": {"pt": "IA de voz", "es": "IA de voz"},
    "agent desktop": {"pt": "Ambiente de trabalho do agente", "es": "Entorno de trabajo del agente"},
    "agent productivity": {"pt": "Produtividade dos agentes", "es": "Productividad de los agentes"},
    "ai contact center roi": {"pt": "ROI de IA em contact centers", "es": "ROI de IA en contact centers"},
    "analytics": {"pt": "Análise de dados", "es": "Análisis de datos"},
    "automation rate": {"pt": "Taxa de automação", "es": "Tasa de automatización"},
    "call center automation roi": {"pt": "ROI da automação em call centers", "es": "ROI de automatización en call centers"},
    "carrier diversity": {"pt": "Diversidade de operadoras", "es": "Diversidad de operadores"},
    "channel strategy": {"pt": "Estratégia de canais", "es": "Estrategia de canales"},
    "cloud sbc": {"pt": "SBC em nuvem", "es": "SBC en la nube"},
    "cloud contact center sbc": {"pt": "SBC para contact centers em nuvem", "es": "SBC para contact centers en la nube"},
    "co-selling": {"pt": "Vendas conjuntas", "es": "Ventas conjuntas"},
    "contact center sbc": {"pt": "SBC para contact centers", "es": "SBC para contact centers"},
    "contact center architecture": {"pt": "Arquitetura de contact center", "es": "Arquitectura de contact center"},
    "contact center metrics": {"pt": "Indicadores de contact center", "es": "Indicadores de contact center"},
    "contact center technology latam": {"pt": "Tecnologia de contact center na América Latina", "es": "Tecnología de contact center en Latinoamérica"},
    "contact center telecom partner": {"pt": "Parceiro de telecom para contact center", "es": "Socio de telecomunicaciones para contact center"},
    "contact center voice quality": {"pt": "Qualidade de voz no contact center", "es": "Calidad de voz en el contact center"},
    "contact rate": {"pt": "Taxa de contato", "es": "Tasa de contacto"},
    "containment": {"pt": "Resolução no atendimento automatizado", "es": "Resolución en la atención automatizada"},
    "cost per interaction": {"pt": "Custo por interação", "es": "Costo por interacción"},
    "customer effort": {"pt": "Esforço do cliente", "es": "Esfuerzo del cliente"},
    "customer experience": {"pt": "Experiência do cliente", "es": "Experiencia del cliente"},
    "customer service outsourcing brazil": {"pt": "Terceirização de atendimento no Brasil", "es": "Externalización de atención en Brasil"},
    "enterprise ai": {"pt": "IA empresarial", "es": "IA empresarial"},
    "global cx": {"pt": "CX global", "es": "CX global"},
    "international customer experience": {"pt": "Experiência do cliente internacional", "es": "Experiencia del cliente internacional"},
    "international market entry": {"pt": "Entrada em mercados internacionais", "es": "Entrada a mercados internacionales"},
    "jitter": {"pt": "Jitter", "es": "Jitter"},
    "local operating intelligence": {"pt": "Inteligência operacional local", "es": "Inteligencia operativa local"},
    "local telecom partner": {"pt": "Parceiro local de telecom", "es": "Socio local de telecomunicaciones"},
    "managed sbc": {"pt": "SBC gerenciado", "es": "SBC gestionado"},
    "market entry": {"pt": "Entrada em mercados", "es": "Entrada a mercados"},
    "nearshore cx": {"pt": "CX nearshore", "es": "CX nearshore"},
    "nearshore contact center": {"pt": "Contact center nearshore", "es": "Contact center nearshore"},
    "nearshore customer service": {"pt": "Atendimento nearshore", "es": "Atención nearshore"},
    "omnichannel context": {"pt": "Contexto omnicanal", "es": "Contexto omnicanal"},
    "outbound campaigns": {"pt": "Campanhas ativas", "es": "Campañas de llamadas salientes"},
    "packet loss": {"pt": "Perda de pacotes", "es": "Pérdida de paquetes"},
    "partner enablement": {"pt": "Capacitação de parceiros", "es": "Capacitación de socios"},
    "production readiness": {"pt": "Prontidão para produção", "es": "Preparación para producción"},
    "regional resilience": {"pt": "Resiliência regional", "es": "Resiliencia regional"},
    "reseller agreements": {"pt": "Acordos de revenda", "es": "Acuerdos de reventa"},
    "sbc as a service": {"pt": "SBC como serviço", "es": "SBC como servicio"},
    "strategic partnerships": {"pt": "Parcerias estratégicas", "es": "Alianzas estratégicas"},
    "telecom resilience": {"pt": "Resiliência de telecom", "es": "Resiliencia de telecomunicaciones"},
    "voice quality": {"pt": "Qualidade de voz", "es": "Calidad de voz"},
}


EXECUTIVE_BIO = {
    "title": {
        "en": "Luiz Terra: Telecom, CX, BPO & AI Executive | Bio",
        "pt": "Luiz Terra: Executivo em Telecom, CX, BPO e IA | Biografia",
        "es": "Luiz Terra: Ejecutivo en Telecom, CX, BPO e IA | Biografía",
    },
    "description": {
        "en": "Executive biography of Luiz Terra, Head of International Sales at Khomp, with 28+ years across telecom, CX, BPO, contact centers and AI.",
        "pt": "Biografia executiva de Luiz Terra, Head of International Sales na Khomp, com mais de 28 anos em telecom, CX, BPO, contact centers e IA.",
        "es": "Biografía ejecutiva de Luiz Terra, Head of International Sales en Khomp, con más de 28 años en telecom, CX, BPO, contact centers e IA.",
    },
    "position": {
        "en": "International Sales Executive in Telecom, CX, BPO & AI",
        "pt": "Executivo Internacional de Vendas em Telecom, CX, BPO e IA",
        "es": "Ejecutivo Internacional de Ventas en Telecom, CX, BPO e IA",
    },
    "sections": {
        "en": [
            ("Executive summary", [
                "Luiz Terra is an international sales executive with more than 28 years of experience across telecommunications, information technology, Customer Experience, contact centers, BPO and AI-powered communications. His work connects commercial strategy with the operational realities of carrier infrastructure, enterprise communications and customer-service technology.",
                "He develops international markets through enterprise sales, strategic partnerships, channel execution and practical market-entry programs. His perspective comes from working across LATAM, North America, Europe and Africa with operators, BPOs, CCaaS vendors, contact center platforms, integrators and regional technology partners.",
            ]),
            ("Professional journey", [
                "Luiz began his career at CelPlan Technologies and later held regional and executive positions at Acision, Genesys, Altitude Software, Anew Brasil, CX Contact, Resolutte and Vocalcom. These roles covered account leadership, regional sales, technology and revenue responsibility, company management and international expansion.",
                "The journey included a multi-year relocation to Mexico City, commercial development across new LATAM markets, participation in complex telecom and customer-care technology projects, and executive responsibility in both established global vendors and entrepreneurial environments.",
            ]),
            ("Selected business impact", [
                "His experience includes opening and developing international markets, building relationships across telecom and CX ecosystems, leading infrastructure and software sales, and aligning vendors, channels and customers around long-term commercial outcomes. The emphasis is consistently on repeatable execution rather than isolated transactions.",
            ]),
            ("Areas of expertise", [
                "International sales, strategic partnerships, enterprise sales, go-to-market strategy, market entry, SBC, SIP and VoIP, cloud communications, CCaaS, BPO technology, Customer Experience and AI-powered Answering Machine Detection are central to his work.",
            ]),
            ("International market experience", [
                "Luiz has operated across LATAM, North America, Europe and Africa. This exposure supports a practical understanding of localization, partner selection, carrier connectivity, buying cycles, technical enablement and the differences between entering a market and building a sustainable presence in it.",
            ]),
            ("Current role", [
                "As Head of International Sales at Khomp, Luiz leads international commercial development around telecom infrastructure and AI capabilities, including SBC, VoIP and SIP, AI-powered AMD, omnichannel technology and partner-led expansion.",
            ]),
            ("Speaking & industry presence", [
                "Luiz participates in executive conversations, partner meetings and industry events focused on telecom, CX, BPO, contact centers, CCaaS, AI and international go-to-market strategy. He is open to strategic partnerships, market-entry discussions, speaking opportunities and executive networking.",
            ]),
        ],
        "pt": [
            ("Resumo executivo", [
                "Luiz Terra é executivo internacional de vendas com mais de 28 anos de experiência em telecomunicações, tecnologia da informação, Experiência do Cliente, contact centers, BPO e comunicações apoiadas por IA. Sua atuação conecta estratégia comercial às realidades operacionais de infraestrutura de operadoras, comunicações corporativas e tecnologia de atendimento.",
                "Ele desenvolve mercados internacionais por meio de vendas corporativas, parcerias estratégicas, canais de vendas e programas práticos de entrada em mercados. Sua perspectiva resulta da atuação na América Latina, América do Norte, Europa e África junto a operadoras, BPOs, fornecedores de CCaaS, plataformas de contact center, integradores e parceiros regionais.",
            ]),
            ("Trajetória profissional", [
                "Luiz iniciou a carreira na CelPlan Technologies e depois ocupou posições regionais e executivas na Acision, Genesys, Altitude Software, Anew Brasil, CX Contact, Resolutte e Vocalcom. Essas funções abrangeram gestão de contas, vendas regionais, responsabilidades de tecnologia e receita, gestão empresarial e expansão internacional.",
                "A trajetória incluiu mudança por mais de três anos para a Cidade do México, desenvolvimento comercial em novos mercados latino-americanos, participação em projetos complexos de telecom e customer care e responsabilidade executiva em fornecedores globais e ambientes empreendedores.",
            ]),
            ("Impacto empresarial selecionado", [
                "Sua experiência inclui abrir e desenvolver mercados internacionais, construir relacionamentos nos ecossistemas de telecom e CX, liderar vendas de infraestrutura e software e alinhar fornecedores, canais e clientes em torno de resultados comerciais de longo prazo.",
            ]),
            ("Áreas de especialização", [
                "Vendas internacionais, parcerias estratégicas, vendas corporativas, estratégia go-to-market, entrada em mercados, SBC, SIP e VoIP, comunicações em nuvem, CCaaS, tecnologia para BPO, Experiência do Cliente e Answering Machine Detection com IA estão no centro de sua atuação.",
            ]),
            ("Experiência em mercados internacionais", [
                "Luiz atuou na América Latina, América do Norte, Europa e África. Essa experiência sustenta uma visão prática sobre adaptação a cada mercado, seleção de parceiros, conectividade com operadoras, ciclos de compra, capacitação técnica e a diferença entre entrar em um mercado e construir uma presença sustentável.",
            ]),
            ("Função atual", [
                "Como Head of International Sales na Khomp, Luiz lidera o desenvolvimento comercial internacional de infraestrutura de telecom e recursos de IA, incluindo SBC, VoIP e SIP, AMD com IA, tecnologia omnichannel e expansão por parceiros.",
            ]),
            ("Presença em eventos e na indústria", [
                "Luiz participa de conversas executivas, reuniões com parceiros e eventos sobre telecom, CX, BPO, contact centers, CCaaS, IA e estratégia internacional. Está aberto a parcerias estratégicas, discussões de entrada em mercados, oportunidades como palestrante e networking executivo.",
            ]),
        ],
        "es": [
            ("Resumen ejecutivo", [
                "Luiz Terra es un ejecutivo internacional de ventas con más de 28 años de experiencia en telecomunicaciones, tecnología de la información, Experiencia del Cliente, contact centers, BPO y comunicaciones apoyadas por IA. Su trabajo conecta la estrategia comercial con las realidades operativas de la infraestructura de operadores y la tecnología de atención.",
                "Desarrolla mercados internacionales mediante ventas corporativas, alianzas estratégicas, canales de ventas y programas prácticos de entrada a mercados. Su perspectiva proviene de trabajar en Latinoamérica, Norteamérica, Europa y África con operadores, BPOs, proveedores de CCaaS, plataformas de contact center, integradores y socios regionales.",
            ]),
            ("Trayectoria profesional", [
                "Luiz inició su carrera en CelPlan Technologies y posteriormente ocupó posiciones regionales y ejecutivas en Acision, Genesys, Altitude Software, Anew Brasil, CX Contact, Resolutte y Vocalcom. Estas funciones abarcaron gestión de cuentas, ventas regionales, responsabilidad sobre tecnología e ingresos, dirección empresarial y expansión internacional.",
                "La trayectoria incluyó una reubicación de más de tres años en Ciudad de México, desarrollo comercial en nuevos mercados latinoamericanos, participación en proyectos complejos de telecom y customer care y responsabilidad ejecutiva en proveedores globales y entornos emprendedores.",
            ]),
            ("Impacto empresarial seleccionado", [
                "Su experiencia incluye abrir y desarrollar mercados internacionales, construir relaciones en los ecosistemas de telecom y CX, liderar ventas de infraestructura y software y alinear proveedores, canales y clientes alrededor de resultados comerciales sostenibles.",
            ]),
            ("Áreas de especialización", [
                "Ventas internacionales, alianzas estratégicas, ventas corporativas, estrategia go-to-market, entrada a mercados, SBC, SIP y VoIP, comunicaciones cloud, CCaaS, tecnología para BPO, Experiencia del Cliente y Answering Machine Detection con IA son áreas centrales de su trabajo.",
            ]),
            ("Experiencia en mercados internacionales", [
                "Luiz ha trabajado en Latinoamérica, Norteamérica, Europa y África. Esta experiencia aporta una visión práctica sobre adaptación a cada mercado, selección de socios, conectividad con operadores, ciclos de compra, capacitación técnica y la diferencia entre entrar en un mercado y construir una presencia sostenible.",
            ]),
            ("Rol actual", [
                "Como Head of International Sales en Khomp, Luiz lidera el desarrollo comercial internacional de infraestructura telecom y capacidades de IA, incluyendo SBC, VoIP y SIP, AMD con IA, tecnología omnicanal y expansión mediante socios.",
            ]),
            ("Presencia en eventos e industria", [
                "Luiz participa en conversaciones ejecutivas, reuniones con socios y eventos sobre telecom, CX, BPO, contact centers, CCaaS, IA y estrategia internacional. Está abierto a alianzas estratégicas, conversaciones sobre la entrada a mercados, oportunidades como conferenciante y contactos profesionales.",
            ]),
        ],
    },
}


TOPICS = [
    {
        "slug": "sbc-contact-centers",
        "title": {"en": "SBC for Contact Centers", "pt": "SBC para Contact Centers", "es": "SBC en Centros de Contacto"},
        "description": {
            "en": "Executive guidance on Session Border Controllers, SIP interoperability, security, carrier connectivity and resilience for cloud and hybrid contact centers.",
            "pt": "Visão executiva sobre Session Border Controllers, interoperabilidade SIP, segurança, conectividade com operadoras e resiliência em contact centers cloud e híbridos.",
            "es": "Visión ejecutiva sobre Session Border Controllers, interoperabilidad SIP, seguridad, conectividad con operadores y resiliencia en contact centers cloud e híbridos.",
        },
        "perspective": {
            "en": "An SBC is not simply a security appliance at the edge. In contact center environments it is a control point for signaling, media, routing, interoperability, policy and operational visibility. Cloud adoption changes where this control is delivered, but it does not remove the underlying requirement.",
            "pt": "Um SBC não é apenas um appliance de segurança na borda. Em contact centers, ele é um ponto de controle para sinalização, mídia, roteamento, interoperabilidade, políticas e visibilidade operacional. A adoção de cloud muda onde esse controle é entregue, mas não elimina a necessidade.",
            "es": "Un SBC no es solo un dispositivo de seguridad en el borde. En contact centers es un punto de control para señalización, medios, enrutamiento, interoperabilidad, políticas y visibilidad operativa. La adopción cloud cambia dónde se entrega ese control, pero no elimina la necesidad.",
        },
        "themes": {
            "en": ["Session Border Controller", "SIP interoperability", "Carrier connectivity", "Security", "Voice quality", "Cloud and hybrid architecture"],
            "pt": ["Session Border Controller", "Interoperabilidade SIP", "Conectividade com operadoras", "Segurança", "Qualidade de voz", "Arquitetura em nuvem e híbrida"],
            "es": ["Session Border Controller", "Interoperabilidad SIP", "Conectividad con operadores", "Seguridad", "Calidad de voz", "Arquitectura en la nube e híbrida"],
        },
        "articles": ["future-of-sbcs-cloud-contact-centers", "sbc-as-a-service-bpo-ccaas", "sip-voice-quality-resilience-global-contact-centers", "bpos-evaluate-telecom-infrastructure-partners"],
    },
    {
        "slug": "ai-contact-centers",
        "title": {"en": "Contact Center AI: ROI, Automation & Governance", "pt": "IA para Contact Centers: ROI e Governança", "es": "IA para Contact Centers: ROI y Gobernanza"},
        "description": {
            "en": "Practical frameworks for AI ROI, automation, Answering Machine Detection, analytics and operational performance in contact centers.",
            "pt": "Frameworks práticos para ROI de IA, automação, Answering Machine Detection, analytics e desempenho operacional em contact centers.",
            "es": "Frameworks prácticos para ROI de IA, automatización, Answering Machine Detection, analytics y desempeño operativo en contact centers.",
        },
        "perspective": {
            "en": "AI creates value when it changes a measurable operating flow. The relevant question is not whether a model looks impressive, but whether it improves productivity, contact rates, quality, containment, customer outcomes or the speed of a management decision without creating unacceptable risk.",
            "pt": "A IA cria valor quando altera um fluxo operacional mensurável. A pergunta relevante não é se um modelo impressiona, mas se melhora produtividade, taxas de contato, qualidade, contenção, resultados para o cliente ou velocidade de decisão sem criar risco inaceitável.",
            "es": "La IA crea valor cuando modifica un flujo operativo medible. La pregunta relevante no es si un modelo impresiona, sino si mejora productividad, tasas de contacto, calidad, contención, resultados para el cliente o velocidad de decisión sin crear riesgos inaceptables.",
        },
        "themes": {
            "en": ["AI ROI", "Contact center automation", "AI-powered AMD", "Agent productivity", "Analytics", "Quality and governance"],
            "pt": ["Retorno sobre investimento em IA", "Automação em contact centers", "AMD com IA", "Produtividade dos agentes", "Análise de dados", "Qualidade e governança"],
            "es": ["Retorno de la inversión en IA", "Automatización en contact centers", "AMD con IA", "Productividad de los agentes", "Análisis de datos", "Calidad y gobernanza"],
        },
        "articles": ["voice-ai-telecom-discipline", "new-cx-stack-telecom-contact-centers", "ai-contact-centers-roi", "call-center-automation-roi", "ai-powered-amd-outbound-operations"],
    },
    {
        "slug": "latam-nearshore-cx",
        "title": {"en": "LATAM Nearshore CX", "pt": "Nearshore CX na LATAM", "es": "Nearshore CX en LATAM"},
        "description": {
            "en": "Executive perspectives on LATAM nearshore delivery, language, cultural proximity, technology, resilience and customer experience.",
            "pt": "Perspectivas executivas sobre nearshore na LATAM, idiomas, proximidade cultural, tecnologia, resiliência e experiência do cliente.",
            "es": "Perspectivas ejecutivas sobre nearshore en LATAM, idiomas, proximidad cultural, tecnología, resiliencia y experiencia del cliente.",
        },
        "perspective": {
            "en": "LATAM should be evaluated as a portfolio of delivery markets rather than a single low-cost location. Time-zone alignment, multilingual talent, cultural proximity, telecom maturity, management capability and geographic diversification often matter as much as the initial cost model.",
            "pt": "A LATAM deve ser avaliada como um portfólio de mercados de prestação de serviços, e não como um único destino de baixo custo. Fuso horário, talento multilíngue, proximidade cultural, maturidade de telecom, capacidade de gestão e diversificação geográfica frequentemente importam tanto quanto o custo inicial.",
            "es": "LATAM debe evaluarse como un portafolio de mercados de prestación de servicios, no como un único destino de bajo costo. Zona horaria, talento multilingüe, proximidad cultural, madurez de telecomunicaciones, capacidad de gestión y diversificación geográfica suelen importar tanto como el costo inicial.",
        },
        "themes": {
            "en": ["Nearshore CX", "LATAM BPO", "Multilingual delivery", "Cultural proximity", "Regional resilience", "Brazil, Colombia, Mexico and Central America"],
            "pt": ["CX nearshore", "BPO na América Latina", "Atendimento multilíngue", "Proximidade cultural", "Resiliência regional", "Brasil, Colômbia, México e América Central"],
            "es": ["CX nearshore", "BPO en Latinoamérica", "Atención multilingüe", "Proximidad cultural", "Resiliencia regional", "Brasil, Colombia, México y Centroamérica"],
        },
        "articles": ["latam-bridge-us-cx-global-delivery", "nearshore-cx-latam-cost-equation", "brazil-customer-service-outsourcing", "ccaas-market-entry-latam"],
    },
    {
        "slug": "bpo-telecom-infrastructure",
        "title": {"en": "BPO Telecom Infrastructure", "pt": "Infraestrutura de Telecom para BPO", "es": "Infraestructura Telecom para BPO"},
        "description": {
            "en": "How BPOs can evaluate uptime, voice quality, carrier diversity, observability, support, security and scalable telecom architecture.",
            "pt": "Como BPOs podem avaliar disponibilidade, qualidade de voz, diversidade de operadoras, observabilidade, suporte, segurança e arquitetura escalável.",
            "es": "Cómo los BPOs pueden evaluar disponibilidad, calidad de voz, diversidad de operadores, observabilidad, soporte, seguridad y arquitectura escalable.",
        },
        "perspective": {
            "en": "Telecom infrastructure is part of the BPO service promise. Savings from a lower unit price can quickly be lost through poor voice quality, slow troubleshooting, limited carrier options or an architecture that cannot support a new country, campaign or customer requirement.",
            "pt": "A infraestrutura de telecom faz parte da promessa de serviço do BPO. A economia de um preço unitário menor pode ser rapidamente consumida por baixa qualidade de voz, diagnóstico lento de falhas, poucas opções de operadoras ou uma arquitetura que não sustenta um novo país, campanha ou requisito de cliente.",
            "es": "La infraestructura de telecomunicaciones forma parte de la promesa de servicio del BPO. El ahorro de un menor precio unitario puede perderse rápidamente por mala calidad de voz, diagnóstico lento de fallos, pocas opciones de operadores o una arquitectura que no admite un nuevo país, campaña o requisito del cliente.",
        },
        "themes": {
            "en": ["Uptime and SLA", "Carrier diversity", "Voice quality", "Observability", "Security", "Troubleshooting and support"],
            "pt": ["Disponibilidade e SLA", "Diversidade de operadoras", "Qualidade de voz", "Observabilidade", "Segurança", "Diagnóstico de falhas e suporte"],
            "es": ["Disponibilidad y SLA", "Diversidad de operadores", "Calidad de voz", "Observabilidad", "Seguridad", "Diagnóstico de fallos y soporte"],
        },
        "articles": ["bpos-evaluate-telecom-infrastructure-partners", "sip-voice-quality-resilience-global-contact-centers", "sbc-as-a-service-bpo-ccaas", "brazil-customer-service-outsourcing"],
    },
    {
        "slug": "ccaas-latam",
        "title": {"en": "CCaaS in LATAM", "pt": "CCaaS na LATAM", "es": "CCaaS en LATAM"},
        "description": {
            "en": "Market-entry considerations for CCaaS vendors across localization, carriers, PSTN, partnerships, integrations, support and channel strategy in LATAM.",
            "pt": "Considerações de entrada para fornecedores CCaaS sobre localização, operadoras, PSTN, parcerias, integrações, suporte e canais na LATAM.",
            "es": "Consideraciones de entrada para proveedores CCaaS sobre localización, operadores, PSTN, alianzas, integraciones, soporte y canales en LATAM.",
        },
        "perspective": {
            "en": "A translated interface is not a LATAM go-to-market strategy. Sustainable expansion depends on local telecom readiness, regional integrations, commercial coverage, support capability, channel incentives and a clear understanding of how BPOs and enterprises buy in each target market.",
            "pt": "Uma interface traduzida não é uma estratégia go-to-market para a LATAM. A expansão sustentável depende de prontidão de telecom local, integrações regionais, cobertura comercial, capacidade de suporte, incentivos de canal e entendimento de como BPOs e empresas compram em cada mercado.",
            "es": "Una interfaz traducida no es una estrategia go-to-market para LATAM. La expansión sostenible depende de preparación telecom local, integraciones regionales, cobertura comercial, capacidad de soporte, incentivos de canal y comprensión de cómo compran BPOs y empresas en cada mercado.",
        },
        "themes": {
            "en": ["Localization", "PSTN and numbering", "Local partnerships", "BPO ecosystem", "Channel strategy", "Support and integrations"],
            "pt": ["Adaptação ao mercado local", "PSTN e numeração", "Parcerias locais", "Ecossistema de BPO", "Estratégia de canais", "Suporte e integrações"],
            "es": ["Adaptación al mercado local", "PSTN y numeración", "Alianzas locales", "Ecosistema de BPO", "Estrategia de canales", "Soporte e integraciones"],
        },
        "articles": ["ccaas-market-entry-latam", "european-ccaas-local-telecom-partners", "latam-bridge-us-cx-global-delivery", "strategic-partnerships-vs-reseller-agreements"],
    },
    {
        "slug": "international-market-entry",
        "title": {"en": "International Market Entry", "pt": "Entrada em Mercados Internacionais", "es": "Entrada a Mercados Internacionales"},
        "description": {
            "en": "Executive guidance on market entry, strategic partnerships, channel development, localization and international go-to-market execution.",
            "pt": "Visão executiva sobre entrada em mercados, parcerias estratégicas, desenvolvimento de canais, localização e execução internacional.",
            "es": "Visión ejecutiva sobre entrada a mercados, alianzas estratégicas, desarrollo de canales, localización y ejecución internacional.",
        },
        "perspective": {
            "en": "Market entry is a sequence of commitments: selecting a segment, validating demand, enabling the product, building local trust, supporting the first customers and deciding where direct presence is justified. Partnerships matter when they accelerate that sequence with shared accountability.",
            "pt": "Entrada em mercado é uma sequência de compromissos: selecionar um segmento, validar demanda, habilitar o produto, construir confiança local, apoiar os primeiros clientes e decidir onde a presença direta se justifica. Parcerias importam quando aceleram essa sequência com responsabilidade compartilhada.",
            "es": "La entrada a un mercado es una secuencia de compromisos: seleccionar un segmento, validar demanda, habilitar el producto, construir confianza local, apoyar a los primeros clientes y decidir dónde se justifica presencia directa. Las alianzas importan cuando aceleran esa secuencia con responsabilidad compartida.",
        },
        "themes": {
            "en": ["Market selection", "Strategic partnerships", "Channel enablement", "Localization", "Co-selling", "Customer success"],
            "pt": ["Seleção de mercados", "Parcerias estratégicas", "Capacitação de canais", "Adaptação ao mercado local", "Vendas conjuntas", "Sucesso do cliente"],
            "es": ["Selección de mercados", "Alianzas estratégicas", "Capacitación de canales", "Adaptación al mercado local", "Ventas conjuntas", "Éxito del cliente"],
        },
        "articles": ["strategic-partnerships-vs-reseller-agreements", "ccaas-market-entry-latam", "european-ccaas-local-telecom-partners", "latam-bridge-us-cx-global-delivery"],
    },
]


TOPIC_BY_SLUG = {topic["slug"]: topic for topic in TOPICS}


CLUSTER_GUIDANCE = {
    "sbc-contact-centers": {
        "en": [
            "Leadership should review the complete voice service, not an isolated component. That means bringing contact center operations, telecom engineering, security, network, carriers and platform providers into the same decision. The group should agree on critical call flows, expected traffic, recovery objectives, evidence ownership and the commercial consequences of degraded service before comparing architectures.",
            "Validation should include normal traffic, peak conditions and controlled failure. Teams need to observe signaling, media, routing and customer impact while a carrier, region or service component is unavailable. A design is ready when responsibilities are understood, failover is repeatable and operations can explain what happened without depending on a single vendor's interpretation.",
        ],
        "pt": [
            "A liderança deve revisar o serviço completo de voz, não um componente isolado. Isso reúne operação de contact center, engenharia de telecom, segurança, rede, operadoras e plataformas na mesma decisão. O grupo deve alinhar fluxos críticos, tráfego, objetivos de recuperação, responsabilidade pelas evidências e consequências comerciais da degradação antes de comparar arquiteturas.",
            "A validação deve incluir tráfego normal, picos e falhas controladas. As equipes precisam observar sinalização, mídia, roteamento e impacto enquanto uma operadora, região ou componente está indisponível. O desenho está pronto quando responsabilidades são claras, o failover é repetível e a operação consegue explicar o ocorrido sem depender da interpretação de um único fornecedor.",
        ],
        "es": [
            "El liderazgo debe revisar el servicio completo de voz, no un componente aislado. Esto reúne operaciones de contact center, ingeniería telecom, seguridad, red, operadores y plataformas en la misma decisión. El grupo debe acordar flujos críticos, tráfico, objetivos de recuperación, propiedad de la evidencia y consecuencias comerciales antes de comparar arquitecturas.",
            "La validación debe incluir tráfico normal, picos y fallas controladas. Los equipos necesitan observar señalización, medios, rutas e impacto mientras un operador, región o componente no está disponible. El diseño está listo cuando las responsabilidades son claras, el failover es repetible y operaciones puede explicar lo ocurrido sin depender de un solo proveedor.",
        ],
    },
    "ai-contact-centers": {
        "en": [
            "A useful AI decision connects four layers: the customer or agent journey, the operational decision being changed, the model or automation capability and the financial mechanism. If one layer is missing, the project may produce an impressive demonstration without a durable result. Operations, technology, finance, compliance and workforce leaders should share the same definition of success.",
            "Validation should compare representative cohorts and include exception handling. Review who uses the output, how quickly it arrives, what happens when confidence is low and whether quality or customer outcomes deteriorate. Scale only after the operating team can sustain the new process and the benefits ledger shows how capacity, savings or revenue will actually be realized.",
        ],
        "pt": [
            "Uma decisão útil de IA conecta quatro camadas: jornada do cliente ou agente, decisão operacional alterada, recurso de modelo ou automação e mecanismo financeiro. Se uma camada faltar, o projeto pode gerar uma demonstração impressionante sem resultado durável. Operações, tecnologia, finanças, compliance e workforce devem compartilhar a mesma definição de sucesso.",
            "A validação deve comparar grupos representativos e incluir tratamento de exceções. Revise quem usa o resultado, quando ele chega, o que ocorre quando a confiança da classificação é baixa e se a qualidade ou a experiência pioram. Amplie a operação depois que a equipe conseguir sustentar o processo e o registro de benefícios mostrar como gerar capacidade adicional, economia ou receita.",
        ],
        "es": [
            "Una decisión útil de IA conecta cuatro capas: recorrido del cliente o agente, decisión operativa modificada, capacidad del modelo o automatización y mecanismo financiero. Si falta una capa, el proyecto puede generar una demostración impresionante sin resultado durable. Operaciones, tecnología, finanzas, compliance y workforce deben compartir la misma definición de éxito.",
            "La validación debe comparar grupos representativos e incluir el manejo de excepciones. Revise quién usa el resultado, cuándo llega, qué ocurre cuando la confianza de la clasificación es baja y si la calidad o la experiencia empeoran. Amplíe la operación después de que el equipo pueda sostener el proceso y el registro de beneficios muestre cómo generar capacidad adicional, ahorro o ingresos.",
        ],
    },
    "bpo-telecom-infrastructure": {
        "en": [
            "For a BPO, infrastructure decisions should be tied to customer commitments and operating exposure. Procurement, telecom, operations, information security and account leadership need a shared scorecard that connects price with availability, quality, troubleshooting, coverage, scalability and the ability to support customer-specific requirements without uncontrolled complexity.",
            "A practical validation uses a real campaign or service flow and a realistic incident. Confirm route visibility, escalation speed, carrier coordination, evidence quality and recovery capacity. The partner should demonstrate how it will work with the BPO during a difficult hour, because that is when the commercial value of architecture and support becomes visible.",
        ],
        "pt": [
            "Para um BPO, decisões de infraestrutura devem estar ligadas aos compromissos com clientes e à exposição operacional. Compras, telecom, operações, segurança e liderança de contas precisam de scorecard comum que conecte preço a disponibilidade, qualidade, troubleshooting, cobertura, escala e capacidade de atender requisitos específicos sem complexidade descontrolada.",
            "Uma validação prática usa uma campanha ou fluxo real e um incidente plausível. Confirme visibilidade de rota, velocidade de escalonamento, coordenação com operadoras, qualidade das evidências e capacidade de recuperação. O parceiro deve mostrar como atuará junto ao BPO durante uma hora difícil, quando o valor comercial da arquitetura e do suporte aparece.",
        ],
        "es": [
            "Para un BPO, las decisiones de infraestructura deben vincularse con compromisos del cliente y exposición operativa. Compras, telecom, operaciones, seguridad y liderazgo de cuentas necesitan un scorecard común que conecte precio con disponibilidad, calidad, troubleshooting, cobertura, escala y capacidad de soportar requisitos específicos sin complejidad descontrolada.",
            "Una validación práctica utiliza una campaña o flujo real y un incidente plausible. Confirme visibilidad de rutas, velocidad de escalamiento, coordinación con operadores, calidad de evidencia y capacidad de recuperación. El socio debe mostrar cómo trabajará con el BPO durante una hora difícil, cuando aparece el valor comercial de arquitectura y soporte.",
        ],
    },
    "latam-nearshore-cx": {
        "en": [
            "The decision team should translate the customer journey into location requirements. Languages, hours, channels, complexity, seasonality, security, leadership access and recovery needs should be explicit before countries or providers are ranked. This prevents an attractive rate from dominating requirements that are more important to customer experience and continuity.",
            "Validation should combine market due diligence with direct operating evidence. Review recruiting pipelines, supervisor capability, quality practices, telecom architecture, technology integrations and continuity procedures. A controlled transition or pilot should test knowledge transfer and management rhythm, not only whether agents can handle a small sample of contacts.",
        ],
        "pt": [
            "A equipe de decisão deve traduzir a jornada do cliente em requisitos de localização. Idiomas, horários, canais, complexidade, sazonalidade, segurança, acesso à liderança e recuperação precisam estar explícitos antes de classificar países ou fornecedores. Isso evita que uma tarifa atraente domine fatores mais importantes para experiência e continuidade.",
            "A validação combina due diligence de mercado com evidência operacional direta. Revise recrutamento, supervisão, práticas de qualidade, arquitetura de telecom, integrações e continuidade. Uma transição controlada deve testar transferência de conhecimento e ritmo de gestão, não apenas se agentes atendem uma pequena amostra.",
        ],
        "es": [
            "El equipo de decisión debe traducir el recorrido del cliente en requisitos de ubicación. Idiomas, horarios, canales, complejidad, estacionalidad, seguridad, acceso al liderazgo y recuperación deben ser explícitos antes de clasificar países o proveedores. Esto evita que una tarifa atractiva domine factores más importantes para experiencia y continuidad.",
            "La validación combina due diligence de mercado con evidencia operativa directa. Revise reclutamiento, supervisión, calidad, arquitectura telecom, integraciones y continuidad. Una transición controlada debe probar transferencia de conocimiento y ritmo de gestión, no solo si agentes atienden una muestra pequeña.",
        ],
    },
    "ccaas-latam": {
        "en": [
            "Market-entry leadership should maintain one integrated readiness view covering product localization, telecom, legal and commercial dependencies, implementation, partner capability and support. Treating these as separate workstreams often creates late surprises, particularly when an opportunity requires local numbering, integrations or response times that the global operating model does not yet support.",
            "The first customer cohort should be deliberately small and visible. Track sales-cycle friction, technical exceptions, implementation effort, voice quality, support demand and adoption. Use the evidence to refine packaging, partner roles and target segments before expanding to additional countries. Regional scale should be the result of repeatability, not the substitute for it.",
        ],
        "pt": [
            "A liderança de entrada deve manter uma visão integrada de localização do produto, dependências de telecom, legais e comerciais, implantação, capacidade de parceiros e suporte. Tratar tudo como frentes separadas cria surpresas tardias, especialmente quando a oportunidade exige numeração, integrações ou tempos de resposta que o modelo global ainda não suporta.",
            "A primeira coorte de clientes deve ser pequena e visível. Acompanhe atrito comercial, exceções técnicas, esforço de implantação, qualidade de voz, demanda de suporte e adoção. Use a evidência para ajustar oferta, papéis dos parceiros e segmentos antes de expandir. Escala regional deve resultar de repetibilidade.",
        ],
        "es": [
            "El liderazgo de entrada debe mantener una visión integrada de localización del producto, dependencias telecom, legales y comerciales, implementación, capacidad de socios y soporte. Tratar todo como frentes separadas crea sorpresas tardías, especialmente cuando una oportunidad exige numeración, integraciones o tiempos que el modelo global aún no soporta.",
            "La primera cohorte de clientes debe ser pequeña y visible. Siga fricción comercial, excepciones técnicas, esfuerzo de implementación, calidad de voz, demanda de soporte y adopción. Use la evidencia para ajustar oferta, roles y segmentos antes de expandir. La escala regional debe resultar de repetibilidad.",
        ],
    },
    "international-market-entry": {
        "en": [
            "Executives should distinguish access from capability. A partner may open doors, but sustainable entry also requires product fit, technical enablement, implementation capacity, support, customer success and economic alignment. The market plan should state which capability is owned by the vendor, which is owned locally and how the two sides make decisions together.",
            "Validate the partnership through a narrow set of target accounts and use cases. Review discovery quality, technical response, proposal discipline, implementation handoffs and post-sale ownership. Expand the relationship when the joint operating model works repeatedly. This creates stronger trust than announcing broad territorial coverage before execution has been proven.",
        ],
        "pt": [
            "Executivos devem distinguir acesso de capacidade. Um parceiro pode abrir portas, mas entrada sustentável exige aderência do produto, capacitação técnica, implantação, suporte, customer success e alinhamento econômico. O plano deve declarar o que pertence ao fornecedor, o que é responsabilidade local e como as partes decidem juntas.",
            "Valide a parceria com um conjunto restrito de contas e casos. Revise qualidade do discovery, resposta técnica, propostas, passagem para implantação e responsabilidade pós-venda. Expanda quando o modelo operacional conjunto funcionar repetidamente. Isso gera mais confiança do que anunciar ampla cobertura antes de provar execução.",
        ],
        "es": [
            "Los ejecutivos deben distinguir acceso de capacidad. Un socio puede abrir puertas, pero una entrada sostenible exige ajuste del producto, capacitación técnica, implementación, soporte, customer success y alineación económica. El plan debe indicar qué pertenece al proveedor, qué es responsabilidad local y cómo deciden juntos.",
            "Valide la alianza con un conjunto limitado de cuentas y casos. Revise calidad de discovery, respuesta técnica, propuestas, transferencia a implementación y responsabilidad posventa. Expanda cuando el modelo conjunto funcione repetidamente. Esto genera más confianza que anunciar amplia cobertura antes de probar ejecución.",
        ],
    },
}
