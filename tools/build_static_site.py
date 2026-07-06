from __future__ import annotations

import html
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
IMAGES = PUBLIC / "images"
BASE_URL = "https://www.luizterra.com.br"
EMAIL = "contact@luizterra.com.br"
LINKEDIN = "https://linkedin.com/in/lterra"
PHOTO = IMAGES / "luiz-terra-executive.jpg"


META = {
    "en": {
        "lang": "en",
        "path": "",
        "title": "Luiz Terra | International Sales Executive in Telecom, CX, BPO & AI",
        "description": "Luiz Terra is an international sales executive with 28+ years of experience in Telecom, CX, BPO, Contact Center, CCaaS, SBC and AI-powered communication solutions across LATAM, North America, Europe and Africa.",
        "og_title": "Luiz Terra | Telecom, CX, BPO & AI Executive",
        "og_description": "International sales executive helping technology companies, telecom providers and contact center ecosystems expand through strategic partnerships and market-entry execution.",
    },
    "pt": {
        "lang": "pt-BR",
        "path": "pt/",
        "title": "Luiz Terra | Executivo Internacional de Vendas em Telecom, CX, BPO e IA",
        "description": "Luiz Terra e um executivo internacional de vendas com 28+ anos de experiencia em Telecom, CX, BPO, Contact Center, CCaaS, SBC e solucoes de comunicacao com IA na LATAM, America do Norte, Europa e Africa.",
        "og_title": "Luiz Terra | Executivo em Telecom, CX, BPO e IA",
        "og_description": "Executivo internacional de vendas que ajuda empresas de tecnologia, provedores de telecomunicacoes e ecossistemas de contact center a expandirem por meio de parcerias estrategicas e entrada em novos mercados.",
    },
    "es": {
        "lang": "es",
        "path": "es/",
        "title": "Luiz Terra | Ejecutivo Internacional de Ventas en Telecom, CX, BPO e IA",
        "description": "Luiz Terra es un ejecutivo internacional de ventas con 28+ anos de experiencia en Telecom, CX, BPO, Contact Center, CCaaS, SBC y soluciones de comunicacion con IA en LATAM, Norteamerica, Europa y Africa.",
        "og_title": "Luiz Terra | Ejecutivo en Telecom, CX, BPO e IA",
        "og_description": "Ejecutivo internacional de ventas que ayuda a empresas de tecnologia, proveedores de telecomunicaciones y ecosistemas de contact center a expandirse mediante alianzas estrategicas y entrada a nuevos mercados.",
    },
}


COPY = {
    "en": {
        "nav": ["Impact", "Expertise", "Insights", "Speaking", "Contact"],
        "hero_eyebrow": "Sao Paulo · LATAM · North America · Europe · Africa",
        "headline": "International Sales Executive in Telecom, CX, BPO & AI",
        "subheadline": "I help technology companies, telecom providers and contact center ecosystems expand internationally through strategic partnerships, enterprise sales and market-entry execution.",
        "support": "With 28+ years across LATAM, North America, Europe and Africa, my work connects telecom infrastructure, Contact Center as a Service (CCaaS), Session Border Controller (SBC), AI-powered Answering Machine Detection (AMD) and Business Process Outsourcing (BPO) operations into practical growth strategies.",
        "primary_cta": "Start a Strategic Conversation",
        "secondary_cta": "Connect on LinkedIn",
        "bio_cta": "Download Executive Bio",
        "current_label": "Current Role",
        "current_text": "Open to strategic partnerships, market-entry conversations, speaking opportunities and executive networking across Telecom, Customer Experience (CX), BPO and AI.",
        "profile_label": "Executive Profile",
        "profile_title": "International growth at the intersection of telecom infrastructure, CX and AI.",
        "profile": [
            "Luiz Terra built his career from an early sales role at CelPlan Technologies into international commercial leadership across Telecom, IT, Customer Experience and contact center technology ecosystems.",
            "His work spans telecom operators, BPOs, Contact Center as a Service vendors, cloud communication platforms, integrators and regional partners. That perspective helps connect enterprise sales, market-entry execution and partner-led growth in markets with different buying behaviors.",
            "Today Luiz leads international sales at Khomp, with focus on SBC, VoIP/SIP, AI-powered AMD, omnichannel platforms and the international positioning of Brazilian telecom and AI technology.",
        ],
        "stats": ["Years in Telecom, IT and CX", "International Regions", "Landmark Telecom Deal"],
        "impact_label": "Selected Business Impact",
        "impact_title": "Commercial impact built through expansion, partnerships and infrastructure sales.",
        "career_title": "A reverse timeline of international commercial leadership.",
        "expertise_title": "Commercial depth across carrier infrastructure, CCaaS, BPO and AI positioning.",
        "insights_title": "Thought leadership topics for telecom, CX, BPO and AI growth conversations.",
        "read_more": "Read article",
        "speaking_label": "Speaking & Industry Presence",
        "speaking_title": "Industry conversations across telecom, CX, BPO, CCaaS and international GTM.",
        "speaking_intro": "Luiz has participated in international business meetings, partner events and industry conversations across LATAM, North America and Europe, with focus on Telecom, CX, BPO, CCaaS, SBC, AI-powered AMD and international go-to-market strategies.",
        "ecosystem_label": "Selected Ecosystem References Across Luiz Terra's Career",
        "ecosystem_title": "Professional context across international telecom, CX, BPO and technology ecosystems.",
        "ecosystem_intro": "Selected companies, platforms and market ecosystems Luiz Terra has interacted with, worked around or been exposed to throughout his international career in Telecom, CX, BPO, Contact Center and technology partnerships.",
        "ecosystem_disclaimer": "References shown for professional context only. They do not necessarily imply current commercial relationships, endorsements or formal partnerships.",
        "contact_label": "Strategic Conversations",
        "contact_title": "Interested in market-entry, partnerships or AI-powered contact center solutions?",
        "contact_lead": "Interested in strategic partnerships, market-entry discussions, telecom infrastructure, BPO technology ecosystems or AI-powered contact center solutions?",
        "footer": "Telecom | CX | BPO | AI | International Sales · Sao Paulo, Brazil",
        "article_back": "Back to insights",
        "share": "Share this article",
    },
    "pt": {
        "nav": ["Impacto", "Expertise", "Insights", "Palestras", "Contato"],
        "hero_eyebrow": "Sao Paulo · LATAM · America do Norte · Europa · Africa",
        "headline": "Executivo Internacional de Vendas em Telecom, CX, BPO e IA",
        "subheadline": "Ajudo empresas de tecnologia, provedores de telecomunicacoes e ecossistemas de contact center a expandirem internacionalmente por meio de parcerias estrategicas, vendas corporativas e execucao de entrada em novos mercados.",
        "support": "Com 28+ anos na LATAM, America do Norte, Europa e Africa, meu trabalho conecta infraestrutura de telecom, Contact Center as a Service (CCaaS), Session Border Controller (SBC), AI-powered Answering Machine Detection (AMD) e operacoes de Business Process Outsourcing (BPO) em estrategias praticas de crescimento.",
        "primary_cta": "Iniciar Conversa Estrategica",
        "secondary_cta": "Conectar no LinkedIn",
        "bio_cta": "Baixar Bio Executiva",
        "current_label": "Current Role",
        "current_text": "Aberto a parcerias estrategicas, conversas sobre entrada em novos mercados, oportunidades como palestrante e networking executivo em Telecom, Customer Experience (CX), BPO e IA.",
        "profile_label": "Perfil Executivo",
        "profile_title": "Crescimento internacional na intersecao entre infraestrutura telecom, CX e IA.",
        "profile": [
            "Luiz Terra construiu sua carreira desde uma funcao inicial em vendas na CelPlan Technologies ate lideranca comercial internacional em Telecom, IT, Customer Experience e ecossistemas de tecnologia para contact center.",
            "Sua experiencia passa por operadoras de telecom, BPOs, fornecedores de Contact Center as a Service, plataformas de comunicacao em nuvem, integradores e parceiros regionais.",
            "Hoje Luiz lidera vendas internacionais na Khomp, com foco em SBC, VoIP/SIP, AI-powered AMD, plataformas omnichannel e posicionamento internacional de tecnologia brasileira em telecom e IA.",
        ],
        "stats": ["Anos em Telecom, IT e CX", "Regioes Internacionais", "Projeto Telecom de Alto Valor"],
        "impact_label": "Impacto Executivo Selecionado",
        "impact_title": "Impacto comercial construido por expansao, parcerias e vendas de infraestrutura.",
        "career_title": "Linha do tempo reversa de lideranca comercial internacional.",
        "expertise_title": "Profundidade comercial em infraestrutura carrier-grade, CCaaS, BPO e IA.",
        "insights_title": "Topicos de autoridade em telecom, CX, BPO e IA para conversas de crescimento.",
        "read_more": "Ler artigo",
        "speaking_label": "Palestras e Presenca na Industria",
        "speaking_title": "Conversas de mercado em telecom, CX, BPO, CCaaS e GTM internacional.",
        "speaking_intro": "Luiz participou de reunioes internacionais de negocio, eventos de parceiros e conversas da industria na LATAM, America do Norte e Europa, com foco em Telecom, CX, BPO, CCaaS, SBC, AI-powered AMD e estrategias internacionais de go-to-market.",
        "ecosystem_label": "Referencias de Ecossistema Selecionadas na Carreira de Luiz Terra",
        "ecosystem_title": "Contexto profissional em ecossistemas internacionais de telecom, CX, BPO e tecnologia.",
        "ecosystem_intro": "Empresas, plataformas e ecossistemas de mercado com os quais Luiz Terra interagiu, trabalhou ao redor ou teve exposicao ao longo de sua carreira internacional em Telecom, CX, BPO, Contact Center e parcerias tecnologicas.",
        "ecosystem_disclaimer": "Referencias exibidas apenas para contexto profissional. Elas nao implicam necessariamente relacoes comerciais atuais, endossos ou parcerias formais.",
        "contact_label": "Conversas Estrategicas",
        "contact_title": "Interesse em entrada de mercado, parcerias ou solucoes de contact center com IA?",
        "contact_lead": "Interesse em parcerias estrategicas, discussoes de entrada em novos mercados, infraestrutura telecom, ecossistemas de tecnologia BPO ou solucoes de contact center com IA?",
        "footer": "Telecom | CX | BPO | IA | Vendas Internacionais · Sao Paulo, Brazil",
        "article_back": "Voltar para insights",
        "share": "Compartilhar artigo",
    },
    "es": {
        "nav": ["Impacto", "Expertise", "Insights", "Speaker", "Contacto"],
        "hero_eyebrow": "Sao Paulo · LATAM · Norteamerica · Europa · Africa",
        "headline": "Ejecutivo Internacional de Ventas en Telecom, CX, BPO e IA",
        "subheadline": "Ayudo a empresas de tecnologia, proveedores de telecomunicaciones y ecosistemas de contact center a expandirse internacionalmente mediante alianzas estrategicas, ventas corporativas y ejecucion de entrada a nuevos mercados.",
        "support": "Con 28+ anos en LATAM, Norteamerica, Europa y Africa, mi trabajo conecta infraestructura telecom, Contact Center as a Service (CCaaS), Session Border Controller (SBC), AI-powered Answering Machine Detection (AMD) y operaciones de Business Process Outsourcing (BPO) en estrategias practicas de crecimiento.",
        "primary_cta": "Iniciar Conversacion Estrategica",
        "secondary_cta": "Conectar en LinkedIn",
        "bio_cta": "Descargar Bio Ejecutiva",
        "current_label": "Current Role",
        "current_text": "Abierto a alianzas estrategicas, conversaciones sobre entrada a nuevos mercados, oportunidades como speaker y networking ejecutivo en Telecom, Customer Experience (CX), BPO e IA.",
        "profile_label": "Perfil Ejecutivo",
        "profile_title": "Crecimiento internacional en la interseccion de infraestructura telecom, CX e IA.",
        "profile": [
            "Luiz Terra construyo su carrera desde una funcion inicial de ventas en CelPlan Technologies hasta liderazgo comercial internacional en Telecom, IT, Customer Experience y ecosistemas tecnologicos de contact center.",
            "Su trabajo abarca operadores telecom, BPOs, proveedores de Contact Center as a Service, plataformas de comunicacion en la nube, integradores y socios regionales.",
            "Hoy Luiz lidera ventas internacionales en Khomp, con foco en SBC, VoIP/SIP, AI-powered AMD, plataformas omnichannel y posicionamiento internacional de tecnologia brasilena en telecom e IA.",
        ],
        "stats": ["Anos en Telecom, IT y CX", "Regiones Internacionales", "Proyecto Telecom de Alto Valor"],
        "impact_label": "Impacto Ejecutivo Seleccionado",
        "impact_title": "Impacto comercial construido mediante expansion, alianzas y ventas de infraestructura.",
        "career_title": "Linea de tiempo inversa de liderazgo comercial internacional.",
        "expertise_title": "Profundidad comercial en infraestructura carrier-grade, CCaaS, BPO e IA.",
        "insights_title": "Temas de liderazgo intelectual en telecom, CX, BPO e IA para conversaciones de crecimiento.",
        "read_more": "Leer articulo",
        "speaking_label": "Speaking y Presencia en la Industria",
        "speaking_title": "Conversaciones de mercado en telecom, CX, BPO, CCaaS y GTM internacional.",
        "speaking_intro": "Luiz ha participado en reuniones internacionales de negocio, eventos de partners y conversaciones de industria en LATAM, Norteamerica y Europa, con foco en Telecom, CX, BPO, CCaaS, SBC, AI-powered AMD y estrategias internacionales de go-to-market.",
        "ecosystem_label": "Referencias de Ecosistema Seleccionadas en la Carrera de Luiz Terra",
        "ecosystem_title": "Contexto profesional en ecosistemas internacionales de telecom, CX, BPO y tecnologia.",
        "ecosystem_intro": "Empresas, plataformas y ecosistemas de mercado con los que Luiz Terra ha interactuado, trabajado alrededor o tenido exposicion a lo largo de su carrera internacional en Telecom, CX, BPO, Contact Center y alianzas tecnologicas.",
        "ecosystem_disclaimer": "Referencias mostradas solo para contexto profesional. No implican necesariamente relaciones comerciales actuales, endosos o alianzas formales.",
        "contact_label": "Conversaciones Estrategicas",
        "contact_title": "Interes en entrada a mercados, alianzas o soluciones de contact center con IA?",
        "contact_lead": "Interes en alianzas estrategicas, discusiones de entrada a nuevos mercados, infraestructura telecom, ecosistemas tecnologicos BPO o soluciones de contact center con IA?",
        "footer": "Telecom | CX | BPO | IA | Ventas Internacionales · Sao Paulo, Brazil",
        "article_back": "Volver a insights",
        "share": "Compartir articulo",
    },
}


IMPACTS = {
    "en": [
        ("International Expansion", "Opened, developed and managed business opportunities across LATAM, North America, Europe and Africa."),
        ("Telecom & CX Ecosystem", "Built commercial relationships with telecom operators, BPOs, CCaaS vendors, contact center platforms and technology partners."),
        ("Telecom Infrastructure Sales", "Led strategic sales involving SBC, VoIP/SIP, cloud telecom, AI-powered AMD and carrier-grade communication solutions."),
        ("Landmark Deals", "Participated in complex international projects, including high-value telecom and customer-care technology deals."),
        ("Strategic Partnerships", "Developed partner-led growth strategies with technology vendors, integrators and regional market specialists."),
    ],
    "pt": [
        ("Expansao Internacional", "Abriu, desenvolveu e gerenciou oportunidades de negocio na LATAM, America do Norte, Europa e Africa."),
        ("Ecossistema Telecom & CX", "Construiu relacoes comerciais com operadoras, BPOs, fornecedores de CCaaS, plataformas de contact center e parceiros tecnologicos."),
        ("Vendas de Infraestrutura Telecom", "Liderou vendas estrategicas envolvendo SBC, VoIP/SIP, cloud telecom, AI-powered AMD e solucoes de comunicacao carrier-grade."),
        ("Projetos de Alto Valor", "Participou de projetos internacionais complexos, incluindo tecnologia telecom e customer-care de alto valor."),
        ("Parcerias Estrategicas", "Desenvolveu estrategias de crescimento via parceiros com vendors, integradores e especialistas regionais."),
    ],
    "es": [
        ("Expansion Internacional", "Abrio, desarrollo y gestiono oportunidades de negocio en LATAM, Norteamerica, Europa y Africa."),
        ("Ecosistema Telecom & CX", "Construyo relaciones comerciales con operadores, BPOs, proveedores CCaaS, plataformas de contact center y socios tecnologicos."),
        ("Ventas de Infraestructura Telecom", "Lidero ventas estrategicas con SBC, VoIP/SIP, cloud telecom, AI-powered AMD y soluciones carrier-grade."),
        ("Proyectos de Alto Valor", "Participo en proyectos internacionales complejos, incluyendo tecnologia telecom y customer-care de alto valor."),
        ("Alianzas Estrategicas", "Desarrollo estrategias de crecimiento mediante partners con vendors, integradores y especialistas regionales."),
    ],
}


ARTICLES = [
    {
        "slug": "ai-powered-amd-outbound-operations",
        "category": {"en": "AI & Contact Center", "pt": "IA & Contact Center", "es": "IA & Contact Center"},
        "title": {
            "en": "Why AI-powered AMD is becoming strategic for outbound operations",
            "pt": "Por que AI-powered AMD se tornou estrategico para operacoes outbound",
            "es": "Por que AI-powered AMD se volvio estrategico para operaciones outbound",
        },
        "summary": {
            "en": "Answering Machine Detection is no longer just a dialing optimization feature. For modern contact centers, AI-powered AMD can directly impact productivity, compliance, customer experience and operational cost.",
            "pt": "Answering Machine Detection deixou de ser apenas uma funcao de otimizacao de discagem. Para contact centers modernos, AI-powered AMD pode impactar produtividade, compliance, experiencia do cliente e custo operacional.",
            "es": "Answering Machine Detection dejo de ser solo una funcion de optimizacion de discado. Para contact centers modernos, AI-powered AMD puede impactar productividad, compliance, experiencia del cliente y costo operativo.",
        },
        "body": {
            "en": [
                "Outbound operations are under pressure to improve answer rates, reduce wasted agent time and maintain disciplined compliance. In that environment, AMD becomes a strategic layer in the operating model rather than a technical checkbox.",
                "AI-powered AMD can help contact centers distinguish live answers from machines with more context, improving pacing decisions and the use of agent capacity. The business value appears when better detection supports productivity, quality and customer experience at the same time.",
                "For BPOs and enterprise contact centers, the evaluation should connect detection accuracy with observability, routing logic, compliance controls and integration with the broader dialing and CCaaS stack.",
            ],
            "pt": [
                "Operacoes outbound precisam melhorar taxas de atendimento, reduzir tempo improdutivo de agentes e manter disciplina de compliance. Nesse contexto, AMD deixa de ser detalhe tecnico e passa a fazer parte do modelo operacional.",
                "AI-powered AMD ajuda contact centers a distinguir atendimentos reais de caixas postais com mais contexto, melhorando decisoes de pacing e uso da capacidade de agentes.",
                "Para BPOs e contact centers corporativos, a avaliacao deve conectar acuracia, observabilidade, regras de roteamento, controles de compliance e integracao com o stack de discagem e CCaaS.",
            ],
            "es": [
                "Las operaciones outbound necesitan mejorar tasas de respuesta, reducir tiempo improductivo de agentes y mantener disciplina de compliance. En ese contexto, AMD deja de ser un detalle tecnico y se vuelve parte del modelo operativo.",
                "AI-powered AMD ayuda a los contact centers a distinguir respuestas reales de buzones con mas contexto, mejorando decisiones de pacing y uso de capacidad de agentes.",
                "Para BPOs y contact centers corporativos, la evaluacion debe conectar precision, observabilidad, reglas de enrutamiento, controles de compliance e integracion con el stack de discado y CCaaS.",
            ],
        },
        "tags": ["AMD", "AI", "Outbound", "Contact Center"],
    },
    {
        "slug": "future-of-sbcs-cloud-contact-centers",
        "category": {"en": "Telecom Infrastructure", "pt": "Infraestrutura Telecom", "es": "Infraestructura Telecom"},
        "title": {
            "en": "The future of SBCs in cloud contact centers",
            "pt": "O futuro dos SBCs em contact centers em nuvem",
            "es": "El futuro de los SBCs en contact centers en la nube",
        },
        "summary": {
            "en": "As contact centers move to cloud and hybrid architectures, Session Border Controllers remain critical for security, interoperability, routing, resilience and voice quality.",
            "pt": "Com contact centers migrando para arquiteturas cloud e hibridas, Session Border Controllers continuam criticos para seguranca, interoperabilidade, roteamento, resiliencia e qualidade de voz.",
            "es": "A medida que los contact centers migran a arquitecturas cloud e hibridas, los Session Border Controllers siguen siendo criticos para seguridad, interoperabilidad, ruteo, resiliencia y calidad de voz.",
        },
        "body": {
            "en": [
                "Cloud contact centers still depend on reliable voice paths, secure borders and interoperability between platforms, carriers and enterprise environments. SBCs sit at that operational boundary.",
                "The strategic question is not whether voice becomes cloud-native, but how companies maintain quality, routing control and security while integrating multiple providers and regions.",
                "For vendors, BPOs and operators, SBC strategy should be evaluated together with carrier relationships, SIP interoperability, monitoring, failover design and support responsiveness.",
            ],
            "pt": [
                "Contact centers em nuvem ainda dependem de rotas de voz confiaveis, bordas seguras e interoperabilidade entre plataformas, carriers e ambientes corporativos. SBCs atuam exatamente nessa fronteira operacional.",
                "A questao estrategica nao e se voz se torna cloud-native, mas como manter qualidade, controle de roteamento e seguranca ao integrar provedores e regioes.",
                "Para vendors, BPOs e operadoras, estrategia de SBC deve ser avaliada junto com relacoes carrier, interoperabilidade SIP, monitoramento, failover e suporte.",
            ],
            "es": [
                "Los contact centers en la nube siguen dependiendo de rutas de voz confiables, bordes seguros e interoperabilidad entre plataformas, carriers y entornos corporativos.",
                "La pregunta estrategica no es si la voz se vuelve cloud-native, sino como mantener calidad, control de ruteo y seguridad al integrar proveedores y regiones.",
                "Para vendors, BPOs y operadores, la estrategia de SBC debe evaluarse junto con relaciones carrier, interoperabilidad SIP, monitoreo, failover y soporte.",
            ],
        },
        "tags": ["SBC", "SIP", "Cloud Telecom", "CCaaS"],
    },
    {
        "slug": "bpos-evaluate-telecom-infrastructure-partners",
        "category": {"en": "BPO Technology", "pt": "Tecnologia para BPO", "es": "Tecnologia para BPO"},
        "title": {
            "en": "How BPOs should evaluate telecom infrastructure partners",
            "pt": "Como BPOs devem avaliar parceiros de infraestrutura telecom",
            "es": "Como los BPOs deben evaluar partners de infraestructura telecom",
        },
        "summary": {
            "en": "BPOs need more than aggressive pricing from telecom vendors. They need reliability, observability, integration flexibility, fast support and a partner capable of scaling across regions.",
            "pt": "BPOs precisam de mais do que preco agressivo em telecom. Precisam de confiabilidade, observabilidade, flexibilidade de integracao, suporte rapido e capacidade de escalar entre regioes.",
            "es": "Los BPOs necesitan mas que precios agresivos en telecom. Necesitan confiabilidad, observabilidad, flexibilidad de integracion, soporte rapido y capacidad de escalar entre regiones.",
        },
        "body": {
            "en": [
                "BPO operations depend on telecom infrastructure as a core production layer. When that layer fails, service levels, agent productivity and client trust are affected quickly.",
                "Evaluation should include uptime, routing flexibility, monitoring, support escalation, SIP expertise and the ability to operate across different regulatory and carrier environments.",
                "The strongest partners combine technical depth with commercial discipline, helping BPOs scale without turning telecom into a constant operational bottleneck.",
            ],
            "pt": [
                "Operacoes BPO dependem de infraestrutura telecom como camada central de producao. Quando essa camada falha, SLAs, produtividade e confianca do cliente sao afetados rapidamente.",
                "A avaliacao deve incluir disponibilidade, flexibilidade de roteamento, monitoramento, escalonamento de suporte, conhecimento SIP e capacidade de operar em ambientes regulatorios e carriers distintos.",
                "Os melhores parceiros combinam profundidade tecnica e disciplina comercial para ajudar BPOs a escalar sem transformar telecom em gargalo operacional.",
            ],
            "es": [
                "Las operaciones BPO dependen de infraestructura telecom como capa central de produccion. Cuando falla, niveles de servicio, productividad y confianza del cliente se afectan rapidamente.",
                "La evaluacion debe incluir disponibilidad, flexibilidad de ruteo, monitoreo, escalamiento de soporte, conocimiento SIP y capacidad de operar en entornos regulatorios y carriers distintos.",
                "Los mejores partners combinan profundidad tecnica y disciplina comercial para ayudar a BPOs a escalar sin convertir telecom en un cuello de botella.",
            ],
        },
        "tags": ["BPO", "Telecom Infrastructure", "Partners", "Operations"],
    },
    {
        "slug": "latam-bridge-us-cx-global-delivery",
        "category": {"en": "Market Entry", "pt": "Entrada em Mercado", "es": "Entrada a Mercado"},
        "title": {
            "en": "LATAM as a bridge between US CX demand and global delivery",
            "pt": "LATAM como ponte entre demanda de CX dos EUA e entrega global",
            "es": "LATAM como puente entre demanda de CX en EE.UU. y entrega global",
        },
        "summary": {
            "en": "LATAM has become a strategic region for nearshore CX, combining language capabilities, cultural proximity, technical talent and competitive delivery models.",
            "pt": "A LATAM se tornou regiao estrategica para nearshore CX, combinando capacidades linguisticas, proximidade cultural, talento tecnico e modelos competitivos de entrega.",
            "es": "LATAM se volvio una region estrategica para nearshore CX, combinando capacidades linguisticas, proximidad cultural, talento tecnico y modelos competitivos de entrega.",
        },
        "body": {
            "en": [
                "US demand for CX capacity continues to push companies toward delivery models that balance cost, quality, language and cultural alignment. LATAM is central to that conversation.",
                "The opportunity is not only labor arbitrage. It includes technical talent, regional telecom maturity, multilingual operations and the ability to connect nearshore delivery with global platforms.",
                "Companies entering LATAM need local partnerships, telecom readiness and a realistic understanding of country-by-country execution requirements.",
            ],
            "pt": [
                "A demanda dos EUA por capacidade de CX continua levando empresas a buscar modelos que equilibrem custo, qualidade, idioma e alinhamento cultural. A LATAM e central nessa conversa.",
                "A oportunidade nao e apenas custo. Inclui talento tecnico, maturidade telecom, operacoes multilingues e capacidade de conectar entrega nearshore com plataformas globais.",
                "Empresas que entram na LATAM precisam de parcerias locais, prontidao telecom e entendimento realista das exigencias de execucao por pais.",
            ],
            "es": [
                "La demanda de CX en EE.UU. sigue empujando a empresas hacia modelos que equilibran costo, calidad, idioma y alineacion cultural. LATAM es central en esa conversacion.",
                "La oportunidad no es solo costo. Incluye talento tecnico, madurez telecom, operaciones multilingues y capacidad de conectar entrega nearshore con plataformas globales.",
                "Las empresas que entran a LATAM necesitan alianzas locales, preparacion telecom y entendimiento realista de ejecucion pais por pais.",
            ],
        },
        "tags": ["LATAM", "CX", "Nearshore", "Market Entry"],
    },
    {
        "slug": "european-ccaas-local-telecom-partners",
        "category": {"en": "CCaaS Expansion", "pt": "Expansao CCaaS", "es": "Expansion CCaaS"},
        "title": {
            "en": "What European CCaaS vendors need from local telecom partners",
            "pt": "O que vendors europeus de CCaaS precisam de parceiros telecom locais",
            "es": "Que necesitan los vendors europeos de CCaaS de partners telecom locales",
        },
        "summary": {
            "en": "European CCaaS vendors expanding internationally need telecom partners that understand local regulations, SIP interoperability, numbering, carriers, latency and support expectations.",
            "pt": "Vendors europeus de CCaaS em expansao internacional precisam de parceiros telecom que entendam regulacao local, interoperabilidade SIP, numeracao, carriers, latencia e suporte.",
            "es": "Vendors europeos de CCaaS en expansion internacional necesitan partners telecom que entiendan regulacion local, interoperabilidad SIP, numeracion, carriers, latencia y soporte.",
        },
        "body": {
            "en": [
                "International CCaaS expansion often looks simple from the platform layer and complex at the telecom edge. Numbering, carriers, latency and SIP details can define customer experience.",
                "Local telecom partners reduce execution risk when they understand both regulatory context and the operational expectations of enterprise contact centers.",
                "The best market-entry plans align platform capability, local telecom readiness, support model and commercial channel strategy before the first large opportunity appears.",
            ],
            "pt": [
                "A expansao internacional de CCaaS parece simples na camada de plataforma e complexa na borda telecom. Numeracao, carriers, latencia e detalhes SIP podem definir a experiencia do cliente.",
                "Parceiros telecom locais reduzem risco de execucao quando entendem tanto o contexto regulatorio quanto as expectativas operacionais de contact centers corporativos.",
                "Os melhores planos alinham plataforma, prontidao telecom local, modelo de suporte e estrategia comercial antes da primeira grande oportunidade.",
            ],
            "es": [
                "La expansion internacional de CCaaS parece simple en la capa de plataforma y compleja en el borde telecom. Numeracion, carriers, latencia y detalles SIP pueden definir la experiencia.",
                "Los partners telecom locales reducen riesgo de ejecucion cuando entienden el contexto regulatorio y las expectativas operativas de contact centers empresariales.",
                "Los mejores planes alinean plataforma, preparacion telecom local, modelo de soporte y estrategia comercial antes de la primera gran oportunidad.",
            ],
        },
        "tags": ["CCaaS", "Telecom Partners", "Europe", "SIP"],
    },
    {
        "slug": "ai-contact-centers-roi",
        "category": {"en": "AI ROI", "pt": "ROI em IA", "es": "ROI en IA"},
        "title": {
            "en": "AI in Contact Centers: where the hype ends and ROI starts",
            "pt": "IA em Contact Centers: onde o hype termina e o ROI comeca",
            "es": "IA en Contact Centers: donde termina el hype y empieza el ROI",
        },
        "summary": {
            "en": "AI creates value in contact centers when it improves measurable outcomes: answer rates, agent productivity, compliance, routing accuracy, quality monitoring and customer satisfaction.",
            "pt": "IA cria valor em contact centers quando melhora resultados mensuraveis: taxas de atendimento, produtividade de agentes, compliance, roteamento, qualidade e satisfacao do cliente.",
            "es": "La IA crea valor en contact centers cuando mejora resultados medibles: tasas de respuesta, productividad, compliance, ruteo, calidad y satisfaccion del cliente.",
        },
        "body": {
            "en": [
                "AI initiatives in contact centers should start with operational outcomes, not with generic automation narratives. The strongest cases improve measurable parts of the business.",
                "Relevant outcomes include answer rates, agent productivity, compliance control, routing accuracy, quality monitoring and customer satisfaction. Those metrics connect technology to executive priorities.",
                "The practical path is to integrate AI into existing telecom, CCaaS and BPO operating models with clear ownership, observability and realistic change management.",
            ],
            "pt": [
                "Iniciativas de IA em contact centers devem comecar por resultados operacionais, nao por narrativas genericas de automacao. Os melhores casos melhoram partes mensuraveis do negocio.",
                "Resultados relevantes incluem taxas de atendimento, produtividade, compliance, roteamento, monitoramento de qualidade e satisfacao do cliente.",
                "O caminho pratico e integrar IA aos modelos existentes de telecom, CCaaS e BPO com ownership claro, observabilidade e gestao realista de mudanca.",
            ],
            "es": [
                "Las iniciativas de IA en contact centers deben empezar por resultados operativos, no por narrativas genericas de automatizacion. Los mejores casos mejoran partes medibles del negocio.",
                "Resultados relevantes incluyen tasas de respuesta, productividad, compliance, ruteo, monitoreo de calidad y satisfaccion del cliente.",
                "El camino practico es integrar IA a modelos existentes de telecom, CCaaS y BPO con ownership claro, observabilidad y gestion realista del cambio.",
            ],
        },
        "tags": ["AI", "ROI", "Contact Center", "CX"],
    },
]


CAREER = [
    ("Current", "Khomp", "Head of International Sales", "Leading global expansion with focus on SBC, AI-powered AMD, Genesys AppFoundry and international channel development."),
    ("North America", "Vocalcom", "VP Sales LATAM", "Drove LATAM sales for cloud technology solutions from a North America context."),
    ("Prior", "Resolutte", "CTO & CRO", "Led technology and revenue responsibilities for communication and CX enhancement solutions."),
    ("Prior", "CX Contact", "CEO", "Directed executive leadership for a contact center and customer experience operation."),
    ("Entrepreneurial", "Anew Brasil", "General Director & Board Member / CEO", "Founded the Brazilian arm, achieved significant revenue growth and won the CCEE public tender."),
    ("Mexico City", "Altitude Software", "Commercial Director, Latin America", "Relocated for 3+ years, expanded into new countries and presented on contact center virtualization in Bogota."),
    ("Brazil", "Genesys", "Senior Sales Manager", "Served telecom, outsourcing and financial sectors while participating in the strategic GMK merger integration."),
    ("LATAM", "Acision", "Key Account Manager, Latin America", "Secured significant contracts and introduced new products for the region."),
    ("Early career", "CelPlan Technologies", "Sales Assistant", "Started in sales with a USA-based company before moving into broader regional responsibility."),
]


ECOSYSTEM = [
    ("MEO/Altice", "Europe"),
    ("Concentrix", "Global"),
    ("Teleperformance", "Global"),
    ("Enghouse", "Global"),
    ("TIGO", "LATAM"),
    ("Genesys", "Global"),
    ("Five9", "North America"),
    ("Atento", "LATAM"),
    ("Vocalcom", "Global"),
    ("InConcert CX", "Global"),
    ("Collab", "Global"),
]


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def lang_url(lang: str, path: str = "") -> str:
    prefix = META[lang]["path"]
    if path:
        return f"/{prefix}{path}".replace("//", "/")
    return "/" if lang == "en" else f"/{prefix}"


def canonical(lang: str, path: str = "") -> str:
    return f"{BASE_URL}{lang_url(lang, path)}"


def gtag() -> str:
    return """    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-68E95X4DZT"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', 'G-68E95X4DZT');
    </script>"""


def hreflang(path: str = "") -> str:
    links = [
        f'    <link rel="alternate" hreflang="en" href="{BASE_URL}{lang_url("en", path)}" />',
        f'    <link rel="alternate" hreflang="pt-BR" href="{BASE_URL}{lang_url("pt", path)}" />',
        f'    <link rel="alternate" hreflang="es" href="{BASE_URL}{lang_url("es", path)}" />',
        f'    <link rel="alternate" hreflang="x-default" href="{BASE_URL}/" />',
    ]
    return "\n".join(links)


def head(lang: str, page_title: str | None = None, description: str | None = None, path: str = "") -> str:
    meta = META[lang]
    title = page_title or meta["title"]
    desc = description or meta["description"]
    return f"""  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{esc(title)}</title>
    <meta name="description" content="{esc(desc)}" />
    <link rel="canonical" href="{canonical(lang, path)}" />
{hreflang(path)}
    <meta property="og:title" content="{esc(meta["og_title"])}" />
    <meta property="og:description" content="{esc(meta["og_description"])}" />
    <meta property="og:url" content="{canonical(lang, path)}" />
    <meta property="og:type" content="website" />
    <meta property="og:image" content="{BASE_URL}/public/og-image.png" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Luiz Terra, International Sales Executive in Telecom, CX, BPO and AI" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{esc(meta["og_title"])}" />
    <meta name="twitter:description" content="{esc(meta["og_description"])}" />
    <meta name="twitter:image" content="{BASE_URL}/public/og-image.png" />
    <link rel="icon" href="/public/favicon.svg" type="image/svg+xml" />
{gtag()}
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="/styles.css" />
    <script type="application/ld+json">{schema_json()}</script>
  </head>"""


def schema_json() -> str:
    return """{
      "@context": "https://schema.org",
      "@type": "Person",
      "name": "Luiz Terra",
      "jobTitle": "Head of International Sales",
      "worksFor": {"@type": "Organization", "name": "Khomp"},
      "address": {"@type": "PostalAddress", "addressLocality": "Sao Paulo", "addressCountry": "Brazil"},
      "email": "mailto:contact@luizterra.com.br",
      "url": "https://www.luizterra.com.br",
      "sameAs": ["https://linkedin.com/in/lterra"],
      "knowsAbout": ["Telecom", "Contact Center", "BPO", "Customer Experience", "CCaaS", "SBC", "VoIP", "SIP", "AI-powered AMD", "International Sales", "Strategic Partnerships", "Market Entry"]
    }"""


def nav(lang: str, current_path: str = "") -> str:
    c = COPY[lang]
    home = lang_url(lang)
    section = lambda anchor: f"#{anchor}" if current_path == "" else f"{home}#{anchor}"
    nav_items = [
        (section("impact"), c["nav"][0]),
        (section("expertise"), c["nav"][1]),
        (lang_url(lang, "insights/"), c["nav"][2]),
        (section("speaking"), c["nav"][3]),
        (section("contact"), c["nav"][4]),
    ]
    links = "\n".join(f'        <a href="{href}">{esc(label)}</a>' for href, label in nav_items)
    lang_links = "\n".join(
        f'          <a href="{lang_url(code, current_path)}" class="{"is-active" if code == lang else ""}" aria-current="{"page" if code == lang else "false"}">{label}</a>'
        for code, label in [("en", "EN"), ("pt", "PT"), ("es", "ES")]
    )
    return f"""    <nav class="site-nav" aria-label="Main navigation">
      <a class="brand" href="{lang_url(lang)}" aria-label="Luiz Terra home">LT</a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav-links">
        <span></span>
        <span></span>
      </button>
      <div class="nav-links" id="nav-links">
{links}
        <div class="language-switcher" aria-label="Language versions">
{lang_links}
        </div>
        <a class="nav-cta" href="mailto:{EMAIL}?subject=Strategic%20conversation">{esc(c["primary_cta"])}</a>
      </div>
    </nav>"""


def footer(lang: str) -> str:
    c = COPY[lang]
    return f"""    <footer class="site-footer">
      <div>
        <p>© 2026 Luiz Terra. All rights reserved.</p>
        <small>{esc(c["footer"])}</small>
      </div>
      <div class="footer-links" aria-label="Footer links">
        <a href="mailto:{EMAIL}">{EMAIL}</a>
        <a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a>
      </div>
    </footer>"""


def render_home(lang: str) -> str:
    c = COPY[lang]
    impact_cards = "\n".join(
        f"""            <article>
              <span>{idx:02d}</span>
              <h3>{esc(title)}</h3>
              <p>{esc(body)}</p>
            </article>"""
        for idx, (title, body) in enumerate(IMPACTS[lang], 1)
    )
    profile = "\n".join(f"            <p>{esc(p)}</p>" for p in c["profile"])
    career = "\n".join(
        f"""            <article>
              <time>{esc(time)}</time>
              <div>
                <h3>{esc(company)}</h3>
                <p class="role">{esc(role)}</p>
                <p>{esc(text)}</p>
              </div>
            </article>"""
        for time, company, role, text in CAREER
    )
    insights = "\n".join(
        f"""            <article data-article-slug="{article["slug"]}">
              <span>{esc(article["category"][lang])}</span>
              <h3>{esc(article["title"][lang])}</h3>
              <p>{esc(article["summary"][lang])}</p>
              <a href="{lang_url(lang, f'insights/{article["slug"]}/')}">{esc(c["read_more"])}</a>
            </article>"""
        for article in ARTICLES
    )
    ecosystem = "\n".join(
        f'            <article><strong>{esc(name)}</strong><span>{esc(region)}</span></article>'
        for name, region in ECOSYSTEM
    )
    presence = [
        "Contact center and telecom events in LATAM",
        "International partner meetings across North America and Europe",
        "Executive discussions with BPOs, CCaaS vendors and telecom operators",
        "Topics: AI in contact centers, SBC strategy, cloud telecom, BPO technology partnerships and international GTM",
    ]
    presence_cards = "\n".join(f"            <article>{esc(item)}</article>" for item in presence)
    return f"""<!DOCTYPE html>
<html lang="{META[lang]["lang"]}">
{head(lang)}
  <body>
{nav(lang)}
    <main id="top">
      <section class="hero section-reveal" aria-labelledby="hero-title">
        <div class="hero-grid">
          <div class="hero-copy">
            <p class="eyebrow">{esc(c["hero_eyebrow"])}</p>
            <h1 id="hero-title">{esc(c["headline"])}</h1>
            <p class="hero-subline">{esc(c["subheadline"])}</p>
            <p class="hero-support">{esc(c["support"])}</p>
            <div class="hero-actions" aria-label="Primary actions">
              <a class="button primary" href="mailto:{EMAIL}?subject=Strategic%20conversation">{esc(c["primary_cta"])}</a>
              <a class="button secondary" href="{LINKEDIN}" target="_blank" rel="noopener">{esc(c["secondary_cta"])}</a>
              <a class="button tertiary" href="/public/luiz-terra-executive-bio.pdf" download>{esc(c["bio_cta"])}</a>
            </div>
          </div>
          <aside class="hero-panel hero-profile" aria-label="Current role">
            <img src="/public/images/luiz-terra-executive.jpg" alt="Luiz Terra, International Sales Executive in Telecom, CX, BPO and AI" width="520" height="520" draggable="false" />
            <div>
              <span>{esc(c["current_label"])}</span>
              <strong>Head of International Sales at Khomp</strong>
              <p>{esc(c["current_text"])}</p>
            </div>
          </aside>
        </div>
        <div class="ticker" aria-label="Key sectors and markets">
          <div class="ticker-track">
            {"".join(f"<span>{esc(item)}</span>" for item in ["Telecom Infrastructure", "Contact Center", "CCaaS", "SBC", "AI-powered AMD", "BPO Technology", "VoIP/SIP", "Strategic Partnerships", "LATAM", "North America", "Europe", "Africa"] * 2)}
          </div>
        </div>
      </section>
      <section class="content-section section-reveal" id="about" aria-labelledby="about-title">
        <div class="section-label">{esc(c["profile_label"])}</div>
        <div class="section-body">
          <h2 id="about-title">{esc(c["profile_title"])}</h2>
          <div class="copy-stack">
{profile}
          </div>
          <div class="stats" aria-label="Career statistics">
            <article><strong>28+</strong><span>{esc(c["stats"][0])}</span></article>
            <article><strong>4</strong><span>{esc(c["stats"][1])}</span></article>
            <article><strong>USD 2M+</strong><span>{esc(c["stats"][2])}</span></article>
          </div>
        </div>
      </section>
      <section class="content-section section-reveal" id="impact" aria-labelledby="impact-title">
        <div class="section-label">{esc(c["impact_label"])}</div>
        <div class="section-body">
          <h2 id="impact-title">{esc(c["impact_title"])}</h2>
          <div class="impact-grid">
{impact_cards}
          </div>
        </div>
      </section>
      <section class="content-section section-reveal" id="career" aria-labelledby="career-title">
        <div class="section-label">Career</div>
        <div class="section-body">
          <h2 id="career-title">{esc(c["career_title"])}</h2>
          <div class="timeline">
{career}
          </div>
        </div>
      </section>
      <section class="content-section section-reveal" id="expertise" aria-labelledby="expertise-title">
        <div class="section-label">Expertise</div>
        <div class="section-body">
          <h2 id="expertise-title">{esc(c["expertise_title"])}</h2>
          <div class="chips" aria-label="Skills and expertise">
            {"".join(f"<span>{esc(item)}</span>" for item in ["International Sales", "Strategic Partnerships", "Market Entry", "SBC", "AI-Powered AMD", "CCaaS", "BPO Ecosystem", "VoIP/SIP", "Cloud Telecom", "CRM & CX"])}
          </div>
          <div class="focus-grid">
            <article><span aria-hidden="true">◎</span><h3>Global SBC &amp; Carrier Partnerships</h3><p>Building trust with operators, carriers and partners where infrastructure, reliability and sales timing matter.</p></article>
            <article><span aria-hidden="true">◇</span><h3>AI in Contact Center</h3><p>Positioning AMD and CCaaS capabilities for markets that demand measurable operational impact.</p></article>
            <article><span aria-hidden="true">↗</span><h3>International Market Entry</h3><p>Opening and developing markets across North America, Europe, LATAM and Africa with channel-led execution.</p></article>
          </div>
        </div>
      </section>
      <section class="content-section section-reveal" id="insights" aria-labelledby="insights-title">
        <div class="section-label">Insights</div>
        <div class="section-body">
          <h2 id="insights-title">{esc(c["insights_title"])}</h2>
          <div class="insight-grid" id="insight-grid">
{insights}
          </div>
        </div>
      </section>
      <section class="content-section section-reveal" id="speaking" aria-labelledby="speaking-title">
        <div class="section-label">{esc(c["speaking_label"])}</div>
        <div class="section-body">
          <h2 id="speaking-title">{esc(c["speaking_title"])}</h2>
          <p class="section-intro">{esc(c["speaking_intro"])}</p>
          <div class="presence-grid">
{presence_cards}
          </div>
        </div>
      </section>
      <section class="content-section section-reveal" id="clients" aria-labelledby="clients-title">
        <div class="section-label">{esc(c["ecosystem_label"])}</div>
        <div class="section-body">
          <h2 id="clients-title">{esc(c["ecosystem_title"])}</h2>
          <p class="section-intro">{esc(c["ecosystem_intro"])}</p>
          <div class="account-grid">
{ecosystem}
          </div>
          <p class="reference-note">{esc(c["ecosystem_disclaimer"])}</p>
        </div>
      </section>
      <section class="contact-section section-reveal" id="contact" aria-labelledby="contact-title">
        <div class="contact-card">
          <p class="eyebrow">{esc(c["contact_label"])}</p>
          <h2 id="contact-title">{esc(c["contact_title"])}</h2>
          <p class="contact-lead">{esc(c["contact_lead"])}</p>
          <div class="contact-options">
            <a id="email-link" href="mailto:{EMAIL}" data-user="contact" data-domain="luizterra.com.br"><span aria-hidden="true">✉</span><strong>Email</strong><small id="email-text">{EMAIL}</small></a>
            <a href="{LINKEDIN}" target="_blank" rel="noopener"><span aria-hidden="true">in</span><strong>LinkedIn</strong><small>linkedin.com/in/lterra</small></a>
            <a href="https://cal.read.ai/lterra01" target="_blank" rel="noopener"><span aria-hidden="true">↗</span><strong>Schedule</strong><small>cal.read.ai/lterra01</small></a>
          </div>
        </div>
      </section>
    </main>
{footer(lang)}
    <script src="/script.js"></script>
  </body>
</html>
"""


def render_insights_index(lang: str) -> str:
    c = COPY[lang]
    cards = "\n".join(
        f"""          <article data-article-slug="{article["slug"]}">
            <span>{esc(article["category"][lang])}</span>
            <h3>{esc(article["title"][lang])}</h3>
            <p>{esc(article["summary"][lang])}</p>
            <a href="{lang_url(lang, f'insights/{article["slug"]}/')}">{esc(c["read_more"])}</a>
          </article>"""
        for article in ARTICLES
    )
    return f"""<!DOCTYPE html>
<html lang="{META[lang]["lang"]}">
{head(lang, f"Insights | {META[lang]['title']}", META[lang]["description"], "insights/")}
  <body>
{nav(lang, "insights/")}
    <main class="subpage-main">
      <section class="content-section section-reveal is-visible" id="insights" aria-labelledby="insights-title">
        <div class="section-label">Insights</div>
        <div class="section-body">
          <h1 class="subpage-title" id="insights-title">{esc(c["insights_title"])}</h1>
          <div class="insight-grid">
{cards}
          </div>
        </div>
      </section>
    </main>
{footer(lang)}
    <script src="/script.js"></script>
  </body>
</html>
"""


def render_article(lang: str, article: dict) -> str:
    c = COPY[lang]
    body = "\n".join(f"          <p>{esc(p)}</p>" for p in article["body"][lang])
    tags = "".join(f"<span>{esc(tag)}</span>" for tag in article["tags"])
    title = article["title"][lang]
    desc = article["summary"][lang]
    return f"""<!DOCTYPE html>
<html lang="{META[lang]["lang"]}">
{head(lang, f"{title} | Luiz Terra", desc, f"insights/{article['slug']}/")}
  <body>
{nav(lang, f"insights/{article['slug']}/")}
    <main class="subpage-main article-main">
      <article class="article-page section-reveal is-visible">
        <a class="article-back" href="{lang_url(lang, 'insights/')}">{esc(c["article_back"])}</a>
        <p class="eyebrow">{esc(article["category"][lang])}</p>
        <h1 class="subpage-title">{esc(title)}</h1>
        <p class="article-summary">{esc(desc)}</p>
        <div class="chips article-tags">{tags}</div>
        <div class="article-content">
{body}
        </div>
        <a class="button secondary" href="mailto:{EMAIL}?subject={esc(title).replace(' ', '%20')}">{esc(c["share"])}</a>
      </article>
    </main>
{footer(lang)}
    <script src="/script.js"></script>
  </body>
</html>
"""


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def build_pages() -> None:
    write(ROOT / "index.html", render_home("en"))
    write(ROOT / "en" / "index.html", render_home("en"))
    write(ROOT / "pt" / "index.html", render_home("pt"))
    write(ROOT / "es" / "index.html", render_home("es"))
    for lang in ("en", "pt", "es"):
        write(ROOT / META[lang]["path"] / "insights" / "index.html", render_insights_index(lang))
        for article in ARTICLES:
            write(ROOT / META[lang]["path"] / "insights" / article["slug"] / "index.html", render_article(lang, article))


def build_sitemap() -> None:
    paths = ["/", "/en/", "/pt/", "/es/"]
    for lang in ("en", "pt", "es"):
        paths.append(lang_url(lang, "insights/"))
        for article in ARTICLES:
            paths.append(lang_url(lang, f"insights/{article['slug']}/"))
    unique = []
    for path in paths:
        if path not in unique:
            unique.append(path)
    urls = "\n".join(
        f"""  <url>
    <loc>{BASE_URL}{path}</loc>
    <lastmod>2026-07-03</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{"1.0" if path == "/" else "0.8"}</priority>
  </url>"""
        for path in unique
    )
    write(ROOT / "sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')


def load_font(size: int, bold: bool = False):
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        test = f"{current} {word}".strip()
        if draw.textbbox((0, 0), test, font=font)[2] <= width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def build_og_image() -> None:
    PUBLIC.mkdir(exist_ok=True)
    image = Image.new("RGB", (1200, 630), "#0F1117")
    draw = ImageDraw.Draw(image)
    teal = "#00C8C8"
    text = "#E8EDF2"
    muted = "#AAB6C4"
    divider = "#1E2530"
    draw.rectangle((72, 92, 1128, 538), outline=divider, width=2)
    if PHOTO.exists():
        photo = Image.open(PHOTO).convert("RGB")
        side = min(photo.size)
        left = (photo.width - side) // 2
        top = max(0, (photo.height - side) // 3)
        photo = photo.crop((left, top, left + side, top + side)).resize((250, 250))
        image.paste(photo, (92, 132))
        draw.rectangle((92, 132, 342, 382), outline=teal, width=4)
        text_x = 390
    else:
        draw.rectangle((92, 112, 250, 270), outline=teal, width=5)
        draw.text((171, 178), "LT", fill=teal, font=load_font(58, True), anchor="mm")
        text_x = 300
    draw.text((text_x, 128), "LUIZ TERRA", fill=teal, font=load_font(34, True))
    title_font = load_font(58, True)
    y = 206
    for line in wrap_text(draw, "International Sales Executive in Telecom, CX, BPO & AI", title_font, 760):
        draw.text((text_x, y), line, fill=text, font=title_font)
        y += 66
    draw.text((text_x, 394), "Strategic Partnerships · Market Entry · Telecom Infrastructure", fill=muted, font=load_font(26))
    draw.text((92, 486), "LATAM · North America · Europe · Africa", fill=teal, font=load_font(24, True))
    image.save(PUBLIC / "og-image.png")


def build_pdf() -> None:
    PUBLIC.mkdir(exist_ok=True)
    pdf_path = PUBLIC / "luiz-terra-executive-bio.pdf"
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        rightMargin=0.55 * inch,
        leftMargin=0.55 * inch,
        topMargin=0.48 * inch,
        bottomMargin=0.42 * inch,
    )
    styles = {
        "title": ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=24, leading=28, textColor=colors.HexColor("#0F1117"), spaceAfter=4),
        "subtitle": ParagraphStyle("subtitle", fontName="Helvetica-Bold", fontSize=13, leading=16, textColor=colors.HexColor("#007C7C"), spaceAfter=10),
        "body": ParagraphStyle("body", fontName="Helvetica", fontSize=8.6, leading=11.3, textColor=colors.HexColor("#1E2530"), spaceAfter=5),
        "section": ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=9.8, leading=12, textColor=colors.HexColor("#007C7C"), spaceBefore=6, spaceAfter=4),
        "small": ParagraphStyle("small", fontName="Helvetica", fontSize=8.2, leading=10, textColor=colors.HexColor("#334155")),
    }
    story = [
        Paragraph("Luiz Terra", styles["title"]),
        Paragraph("International Sales Executive in Telecom, CX, BPO & AI", styles["subtitle"]),
        Paragraph("<b>Location:</b> Sao Paulo, Brazil &nbsp;&nbsp;|&nbsp;&nbsp; <b>Contact:</b> contact@luizterra.com.br", styles["small"]),
        Spacer(1, 0.09 * inch),
        Paragraph("Executive Summary", styles["section"]),
        Paragraph(
            "Luiz Terra is an international sales executive with 28+ years of experience across Telecom, IT, Customer Experience, Contact Center, BPO and AI-powered communication solutions. He helps technology companies, telecom providers and contact center ecosystems expand internationally through strategic partnerships, enterprise sales and market-entry execution.",
            styles["body"],
        ),
    ]
    expertise = [
        "International Sales & Revenue Growth",
        "Strategic Partnerships",
        "Telecom Infrastructure",
        "SBC, VoIP/SIP and Cloud Communications",
        "CCaaS, CX and BPO Technology Ecosystems",
        "AI-powered Answering Machine Detection",
        "Market Entry across LATAM, North America, Europe and Africa",
    ]
    impact = [
        "28+ years of executive and commercial experience",
        "Business exposure across LATAM, North America, Europe and Africa",
        "Experience with telecom operators, BPOs, CCaaS vendors, contact center platforms and technology partners",
        "Participation in complex international telecom and customer-care technology projects",
        "Track record in partner-led growth, enterprise sales and market expansion",
    ]
    table_data = [
        [Paragraph("Areas of Expertise", styles["section"]), Paragraph("Business Impact", styles["section"])],
        [
            Paragraph("<br/>".join(f"• {item}" for item in expertise), styles["body"]),
            Paragraph("<br/>".join(f"• {item}" for item in impact), styles["body"]),
        ],
    ]
    table = Table(table_data, colWidths=[3.35 * inch, 3.35 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
                ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#D8E2EA")),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D8E2EA")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    story.extend([table, Spacer(1, 0.08 * inch)])
    story.extend(
        [
            Paragraph("Current Role", styles["section"]),
            Paragraph("Head of International Sales at Khomp", styles["body"]),
            Paragraph("Professional Focus", styles["section"]),
            Paragraph(
                "Strategic partnerships, market-entry conversations, speaking opportunities and executive networking across Telecom, CX, BPO, Contact Center, CCaaS, SBC and AI.",
                styles["body"],
            ),
            Spacer(1, 0.12 * inch),
            Paragraph("www.luizterra.com.br | contact@luizterra.com.br", styles["small"]),
        ]
    )
    doc.build(story)


def build_readme() -> None:
    write(
        ROOT / "README.md",
        """# Luiz Terra Executive Website

Static executive website for Luiz Terra, published with GitHub Pages.

## Current Positioning

International Sales Executive in Telecom, CX, BPO and AI, focused on strategic partnerships, market-entry conversations, speaking opportunities and executive networking across LATAM, North America, Europe and Africa.

## Routes

- `/` - English home and x-default
- `/en/` - English version
- `/pt/` - Portuguese version
- `/es/` - Spanish version
- `/insights/`, `/pt/insights/`, `/es/insights/`
- Localized article pages under each insights route

## Assets

- `public/luiz-terra-executive-bio.pdf`
- `public/og-image.png`
- `public/favicon.svg`

## Editorial Note

The repository does not currently include the 12 previously prepared LinkedIn posts. The site uses the six approved insight topics already present in the website content and provides localized article routes for them. When the 12 posts are available, add them to the article data in `tools/build_static_site.py` and regenerate the static pages.

## Manual Checks

- Validate social preview with LinkedIn Post Inspector and WhatsApp after cache propagation.
- Add an executive photo at `public/images/luiz-terra-executive.jpg` if a final approved headshot is provided.
""",
    )


def main() -> None:
    build_pages()
    build_sitemap()
    build_og_image()
    build_pdf()
    build_readme()


if __name__ == "__main__":
    main()
