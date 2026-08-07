from __future__ import annotations

import html
import json
import textwrap
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from article_library import ARTICLE_UPDATES, NEW_ARTICLES
from content_hub import CLUSTER_GUIDANCE, EXECUTIVE_BIO, TOPICS, TOPIC_BY_SLUG, UI


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
IMAGES = PUBLIC / "images"
BASE_URL = "https://www.luizterra.com.br"
EMAIL = "contact@luizterra.com.br"
LINKEDIN = "https://linkedin.com/in/lterra"
PHOTO = IMAGES / "luiz-terra-executive.jpg"
DATE_PUBLISHED = "2026-07-03"
DATE_MODIFIED = "2026-08-07"
SCHEMA_DATE_CREATED = f"{DATE_PUBLISHED}T00:00:00-03:00"
SCHEMA_DATE_MODIFIED = f"{DATE_MODIFIED}T00:00:00-03:00"


META = {
    "en": {
        "lang": "en",
        "locale": "en_US",
        "path": "",
        "title": "Luiz Terra | International Sales Executive in Telecom, CX, BPO & AI",
        "description": "Luiz Terra is an international sales executive focused on Telecom, CX, BPO, Contact Center, CCaaS and AI-powered communications, with extensive experience developing international markets, strategic partnerships and enterprise business across LATAM, North America, Europe and Africa.",
        "og_title": "Luiz Terra | Telecom, CX, BPO & AI Executive",
        "og_description": "International sales executive helping technology companies, telecom providers and contact center ecosystems expand through strategic partnerships and market-entry execution.",
    },
    "pt": {
        "lang": "pt-BR",
        "locale": "pt_BR",
        "path": "pt/",
        "title": "Luiz Terra | Executivo de Vendas em Telecom, CX, BPO e IA",
        "description": "Luiz Terra é executivo internacional de vendas com mais de 28 anos em Telecom, CX, BPO, CCaaS, SBC e IA na América Latina, América do Norte, Europa e África.",
        "og_title": "Luiz Terra | Executivo em Telecom, CX, BPO e IA",
        "og_description": "Executivo internacional de vendas que conecta tecnologia, telecomunicações e contact centers por meio de parcerias estratégicas e entrada em novos mercados.",
    },
    "es": {
        "lang": "es",
        "locale": "es_ES",
        "path": "es/",
        "title": "Luiz Terra | Ejecutivo de Ventas en Telecom, CX, BPO e IA",
        "description": "Luiz Terra es ejecutivo internacional de ventas con más de 28 años en Telecom, CX, BPO, CCaaS, SBC e IA en Latinoamérica, Norteamérica, Europa y África.",
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
        "bio_cta": "View Executive Bio",
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
        "hero_eyebrow": "São Paulo · América Latina · América do Norte · Europa · África",
        "headline": "Executivo Internacional de Vendas em Telecom, CX, BPO e IA",
        "subheadline": "Ajudo empresas de tecnologia, provedores de telecomunicações e ecossistemas de contact center a expandirem internacionalmente por meio de parcerias estratégicas, vendas corporativas e execução de entrada em novos mercados.",
        "support": "Com mais de 28 anos de experiência na América Latina, América do Norte, Europa e África, meu trabalho conecta infraestrutura de telecom, Contact Center as a Service (CCaaS), Session Border Controller (SBC), AI-powered Answering Machine Detection (AMD) e operações de Business Process Outsourcing (BPO) em estratégias práticas de crescimento.",
        "primary_cta": "Iniciar Conversa Estratégica",
        "secondary_cta": "Conectar no LinkedIn",
        "bio_cta": "Ver Biografia Executiva",
        "current_label": "Current Role",
        "current_text": "Aberto a parcerias estratégicas, conversas sobre entrada em novos mercados, oportunidades como palestrante e networking executivo em Telecom, Customer Experience (CX), BPO e IA.",
        "profile_label": "Perfil Executivo",
        "profile_title": "Crescimento internacional na interseção entre infraestrutura de telecom, CX e IA.",
        "profile": [
            "Luiz Terra construiu sua carreira desde uma função inicial em vendas na CelPlan Technologies até a liderança comercial internacional em Telecom, TI, Customer Experience e ecossistemas de tecnologia para contact center.",
            "Sua experiência passa por operadoras de telecom, BPOs, fornecedores de Contact Center as a Service, plataformas de comunicação em nuvem, integradores e parceiros regionais.",
            "Hoje Luiz lidera vendas internacionais na Khomp, com foco em SBC, VoIP/SIP, AI-powered AMD, plataformas omnichannel e posicionamento internacional de tecnologia brasileira em telecom e IA.",
        ],
        "stats": ["Anos em Telecom, TI e CX", "Regiões Internacionais", "Projeto Telecom de Alto Valor"],
        "impact_label": "Impacto Executivo Selecionado",
        "impact_title": "Impacto comercial construído por expansão, parcerias e vendas de infraestrutura.",
        "career_title": "Linha do tempo reversa de liderança comercial internacional.",
        "expertise_title": "Profundidade comercial em infraestrutura carrier-grade, CCaaS, BPO e IA.",
        "insights_title": "Análises sobre telecom, CX, BPO e IA para decisões de crescimento.",
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
        "bio_cta": "Ver Biografía Ejecutiva",
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
            "pt": "Por que AI-powered AMD se tornou estratégico para operações outbound",
            "es": "Por que AI-powered AMD se volvio estrategico para operaciones outbound",
        },
        "summary": {
            "en": "Answering Machine Detection is no longer just a dialing optimization feature. For modern contact centers, AI-powered AMD can directly impact productivity, compliance, customer experience and operational cost.",
            "pt": "Answering Machine Detection deixou de ser apenas uma função de otimização de discagem. Para contact centers modernos, AI-powered AMD pode impactar produtividade, compliance, experiência do cliente e custo operacional.",
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
            "pt": "Com contact centers migrando para arquiteturas cloud e híbridas, Session Border Controllers continuam críticos para segurança, interoperabilidade, roteamento, resiliência e qualidade de voz.",
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
            "pt": "BPOs precisam de mais do que preço agressivo em telecom. Precisam de confiabilidade, observabilidade, flexibilidade de integração, suporte rápido e capacidade de escalar entre regiões.",
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
            "pt": "América Latina como ponte entre a demanda de CX dos EUA e a entrega global",
            "es": "LATAM como puente entre demanda de CX en EE.UU. y entrega global",
        },
        "summary": {
            "en": "LATAM has become a strategic region for nearshore CX, combining language capabilities, cultural proximity, technical talent and competitive delivery models.",
            "pt": "A América Latina se tornou região estratégica para nearshore CX, combinando capacidades linguísticas, proximidade cultural, talento técnico e modelos competitivos de entrega.",
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
        "category": {"en": "CCaaS Expansion", "pt": "Expansão CCaaS", "es": "Expansión CCaaS"},
        "title": {
            "en": "What European CCaaS vendors need from local telecom partners",
            "pt": "O que fornecedores europeus de CCaaS precisam de parceiros locais de telecom",
            "es": "Que necesitan los vendors europeos de CCaaS de partners telecom locales",
        },
        "summary": {
            "en": "European CCaaS vendors expanding internationally need telecom partners that understand local regulations, SIP interoperability, numbering, carriers, latency and support expectations.",
            "pt": "Fornecedores europeus de CCaaS em expansão internacional precisam de parceiros de telecom que entendam regulação local, interoperabilidade SIP, numeração, operadoras, latência e suporte.",
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
            "pt": "IA em Contact Centers: onde o hype termina e o ROI começa",
            "es": "IA en Contact Centers: donde termina el hype y empieza el ROI",
        },
        "summary": {
            "en": "AI creates value in contact centers when it improves measurable outcomes: answer rates, agent productivity, compliance, routing accuracy, quality monitoring and customer satisfaction.",
            "pt": "IA cria valor em contact centers quando melhora resultados mensuráveis: taxas de atendimento, produtividade de agentes, compliance, roteamento, qualidade e satisfação do cliente.",
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


HOME_FAQ = {
    "en": [
        (
            "Who is Luiz Terra?",
            "Luiz Terra is Head of International Sales at Khomp and an international commercial executive with more than 28 years of experience across telecommunications, IT, customer experience, contact centers, BPO and AI-powered communications.",
        ),
        (
            "What are Luiz Terra's main areas of expertise?",
            "His expertise includes international sales, strategic partnerships, market entry, telecom infrastructure, SBC, VoIP and SIP, CCaaS, BPO technology ecosystems, customer experience and AI-powered Answering Machine Detection.",
        ),
        (
            "In which markets has Luiz Terra worked?",
            "His professional experience covers LATAM, North America, Europe and Africa, connecting global technology vendors with operators, BPOs, contact centers, integrators and regional partners.",
        ),
        (
            "What strategic conversations is Luiz Terra available for?",
            "Luiz is open to conversations about international expansion, channel development, telecom and CX partnerships, AI in contact centers, market entry and speaking opportunities.",
        ),
    ],
    "pt": [
        (
            "Quem é Luiz Terra?",
            "Luiz Terra é Head of International Sales na Khomp e executivo comercial internacional com mais de 28 anos de experiência em telecomunicações, TI, experiência do cliente, contact centers, BPO e comunicações apoiadas por IA.",
        ),
        (
            "Quais são as principais áreas de experiência de Luiz Terra?",
            "Sua experiência inclui vendas internacionais, parcerias estratégicas, entrada em novos mercados, infraestrutura de telecom, SBC, VoIP e SIP, CCaaS, ecossistemas de tecnologia para BPO, CX e Answering Machine Detection com IA.",
        ),
        (
            "Em quais mercados Luiz Terra já atuou?",
            "Sua experiência profissional abrange América Latina, América do Norte, Europa e África, conectando fornecedores globais de tecnologia a operadoras, BPOs, contact centers, integradores e parceiros regionais.",
        ),
        (
            "Para quais conversas estratégicas Luiz Terra está disponível?",
            "Luiz está aberto a conversas sobre expansão internacional, desenvolvimento de canais, parcerias em telecom e CX, IA em contact centers, entrada em mercados e oportunidades como palestrante.",
        ),
    ],
    "es": [
        (
            "¿Quién es Luiz Terra?",
            "Luiz Terra es Head of International Sales en Khomp y ejecutivo comercial internacional con más de 28 años de experiencia en telecomunicaciones, TI, experiencia del cliente, contact centers, BPO y comunicaciones apoyadas por IA.",
        ),
        (
            "¿Cuáles son las principales áreas de experiencia de Luiz Terra?",
            "Su experiencia incluye ventas internacionales, alianzas estratégicas, entrada a nuevos mercados, infraestructura telecom, SBC, VoIP y SIP, CCaaS, tecnología para BPO, CX y Answering Machine Detection con IA.",
        ),
        (
            "¿En qué mercados ha trabajado Luiz Terra?",
            "Su experiencia profesional cubre Latinoamérica, Norteamérica, Europa y África, conectando proveedores globales de tecnología con operadores, BPOs, contact centers, integradores y socios regionales.",
        ),
        (
            "¿Para qué conversaciones estratégicas está disponible Luiz Terra?",
            "Luiz está abierto a conversaciones sobre expansión internacional, desarrollo de canales, alianzas en telecom y CX, IA en contact centers, entrada a mercados y oportunidades como speaker.",
        ),
    ],
}


ARTICLE_LABELS = {
    "en": {
        "why": "Why this topic matters",
        "checklist": "Executive evaluation checklist",
        "next": "A practical path forward",
        "faq": "Frequently asked questions",
        "related": "Related insights",
        "published": "Published",
        "updated": "Updated",
        "reading": "6 min read",
    },
    "pt": {
        "why": "Por que este tema importa",
        "checklist": "Checklist de avaliação executiva",
        "next": "Um caminho prático",
        "faq": "Perguntas frequentes",
        "related": "Insights relacionados",
        "published": "Publicado",
        "updated": "Atualizado",
        "reading": "6 min de leitura",
    },
    "es": {
        "why": "Por qué este tema importa",
        "checklist": "Checklist de evaluación ejecutiva",
        "next": "Un camino práctico",
        "faq": "Preguntas frecuentes",
        "related": "Insights relacionados",
        "published": "Publicado",
        "updated": "Actualizado",
        "reading": "6 min de lectura",
    },
}


INSIGHTS_META = {
    "en": {
        "title": "Telecom, CX, BPO & AI Insights | Luiz Terra",
        "description": "Practical executive insights by Luiz Terra on telecom infrastructure, SBC, CCaaS, BPO, customer experience, international market entry and AI in contact centers.",
    },
    "pt": {
        "title": "Insights de Telecom, CX, BPO e IA | Luiz Terra",
        "description": "Análises práticas de Luiz Terra sobre infraestrutura de telecom, SBC, CCaaS, BPO, experiência do cliente, expansão internacional e IA em contact centers.",
    },
    "es": {
        "title": "Perspectivas sobre Telecom, CX, BPO e IA | Luiz Terra",
        "description": "Análisis prácticos de Luiz Terra sobre infraestructura telecom, SBC, CCaaS, BPO, experiencia del cliente, expansión internacional e IA en contact centers.",
    },
}


ARTICLE_ENHANCEMENTS = {
    "ai-powered-amd-outbound-operations": {
        "en": {
            "checklist": [
                "Detection accuracy for the operation's real call mix, languages and voicemail patterns",
                "Impact on agent occupancy, pacing decisions and abandoned-call risk",
                "Visibility into classifications, confidence levels and false positives",
                "Integration with dialers, CCaaS platforms, SIP infrastructure and routing rules",
                "Compliance controls, test methodology and a measurable operational baseline",
            ],
            "closing": "A useful implementation starts with a controlled sample of real traffic, a shared baseline and clear ownership across operations, telecom and compliance. The goal is not to deploy another isolated AI feature. It is to improve the flow between dialing, classification, routing and agent availability while preserving visibility into every decision.",
            "faq": [
                (
                    "What is AI-powered Answering Machine Detection?",
                    "It is the use of machine-learning techniques and contextual audio analysis to distinguish live answers from voicemail or automated responses during outbound calls. The result is used by dialing and routing systems to decide what should reach an agent.",
                ),
                (
                    "How should a contact center measure AMD value?",
                    "Measure it against a baseline that includes classification accuracy, false positives, agent occupancy, connect rate, abandoned calls and compliance outcomes. Accuracy alone is not enough if the operational flow does not improve.",
                ),
            ],
        },
        "pt": {
            "checklist": [
                "Acurácia para o mix real de chamadas, idiomas e padrões de caixa postal da operação",
                "Impacto na ocupação dos agentes, no pacing e no risco de chamadas abandonadas",
                "Visibilidade sobre classificações, níveis de confiança e falsos positivos",
                "Integração com discadores, plataformas CCaaS, infraestrutura SIP e regras de roteamento",
                "Controles de compliance, metodologia de teste e linha de base operacional mensurável",
            ],
            "closing": "Uma implementação útil começa com uma amostra controlada de tráfego real, uma linha de base compartilhada e responsabilidades claras entre operação, telecom e compliance. O objetivo não é implantar mais um recurso isolado de IA, mas melhorar o fluxo entre discagem, classificação, roteamento e disponibilidade dos agentes, mantendo visibilidade sobre cada decisão.",
            "faq": [
                (
                    "O que é Answering Machine Detection com IA?",
                    "É o uso de aprendizado de máquina e análise contextual de áudio para diferenciar atendimentos humanos de caixas postais ou respostas automatizadas em chamadas outbound. O resultado orienta discadores e sistemas de roteamento.",
                ),
                (
                    "Como um contact center deve medir o valor do AMD?",
                    "A medição deve comparar uma linha de base com acurácia, falsos positivos, ocupação de agentes, taxa de conexão, chamadas abandonadas e resultados de compliance. Acurácia isolada não garante melhoria operacional.",
                ),
            ],
        },
        "es": {
            "checklist": [
                "Precisión para la mezcla real de llamadas, idiomas y patrones de buzón de la operación",
                "Impacto en ocupación de agentes, pacing y riesgo de llamadas abandonadas",
                "Visibilidad de clasificaciones, niveles de confianza y falsos positivos",
                "Integración con marcadores, plataformas CCaaS, infraestructura SIP y reglas de ruteo",
                "Controles de compliance, metodología de prueba y línea base operacional medible",
            ],
            "closing": "Una implementación útil empieza con una muestra controlada de tráfico real, una línea base compartida y responsabilidades claras entre operaciones, telecom y compliance. El objetivo es mejorar el flujo entre marcado, clasificación, ruteo y disponibilidad de agentes, manteniendo visibilidad sobre cada decisión.",
            "faq": [
                (
                    "¿Qué es Answering Machine Detection con IA?",
                    "Es el uso de aprendizaje automático y análisis contextual de audio para diferenciar respuestas humanas de buzones o respuestas automatizadas en llamadas outbound. El resultado orienta a los marcadores y sistemas de ruteo.",
                ),
                (
                    "¿Cómo debe medir un contact center el valor de AMD?",
                    "Debe comparar una línea base con precisión, falsos positivos, ocupación de agentes, tasa de conexión, llamadas abandonadas y resultados de compliance. La precisión aislada no garantiza una mejora operacional.",
                ),
            ],
        },
    },
    "future-of-sbcs-cloud-contact-centers": {
        "en": {
            "checklist": [
                "SIP interoperability across the CCaaS platform, carriers and enterprise environment",
                "Security policy, topology hiding, encryption and protection against voice-specific threats",
                "Routing control, number normalization and support for multi-region operations",
                "High availability, failover behavior and observability of call quality",
                "Operational support with clear escalation paths across vendors and carriers",
            ],
            "closing": "The strongest SBC strategy treats the voice edge as part of the customer experience architecture. Platform, carrier and security teams should validate the same call flows, failure scenarios and operating responsibilities before scale. This reduces the gap between a successful technical test and a resilient production service.",
            "faq": [
                (
                    "Why does a cloud contact center still need an SBC?",
                    "Cloud delivery does not remove the need to secure, normalize, route and observe voice traffic between platforms, carriers and enterprise networks. An SBC provides policy and control at those boundaries.",
                ),
                (
                    "What should be tested before an SBC goes into production?",
                    "Test normal and failure call flows, SIP interoperability, codec behavior, encryption, number formatting, failover, emergency routing where applicable, monitoring and support escalation.",
                ),
            ],
        },
        "pt": {
            "checklist": [
                "Interoperabilidade SIP entre plataforma CCaaS, operadoras e ambiente corporativo",
                "Políticas de segurança, ocultação de topologia, criptografia e proteção da voz",
                "Controle de roteamento, normalização de numeração e operação multirregional",
                "Alta disponibilidade, comportamento de failover e observabilidade da qualidade",
                "Suporte operacional com escalonamento claro entre fornecedores e operadoras",
            ],
            "closing": "A estratégia mais consistente trata o SBC e a borda de voz como parte da arquitetura de experiência do cliente. Times de plataforma, operadoras e segurança devem validar os mesmos fluxos, cenários de falha e responsabilidades antes da escala. Isso reduz a distância entre um teste técnico bem-sucedido e um serviço resiliente em produção.",
            "faq": [
                (
                    "Por que um contact center em nuvem ainda precisa de SBC?",
                    "A nuvem não elimina a necessidade de proteger, normalizar, rotear e observar o tráfego de voz entre plataformas, operadoras e redes corporativas. O SBC aplica políticas e controle nessas fronteiras.",
                ),
                (
                    "O que deve ser testado antes de colocar um SBC em produção?",
                    "Devem ser testados fluxos normais e de falha, interoperabilidade SIP, codecs, criptografia, formatação de números, failover, roteamento de emergência quando aplicável, monitoramento e escalonamento de suporte.",
                ),
            ],
        },
        "es": {
            "checklist": [
                "Interoperabilidad SIP entre plataforma CCaaS, operadores y entorno empresarial",
                "Políticas de seguridad, ocultación de topología, cifrado y protección de la voz",
                "Control de ruteo, normalización de numeración y operación multirregional",
                "Alta disponibilidad, comportamiento de failover y observabilidad de calidad",
                "Soporte operacional con escalamiento claro entre proveedores y operadores",
            ],
            "closing": "La estrategia más consistente trata al SBC y al borde de voz como parte de la arquitectura de experiencia del cliente. Los equipos de plataforma, operadores y seguridad deben validar los mismos flujos, escenarios de falla y responsabilidades antes de escalar.",
            "faq": [
                (
                    "¿Por qué un contact center en la nube todavía necesita un SBC?",
                    "La nube no elimina la necesidad de proteger, normalizar, rutear y observar el tráfico de voz entre plataformas, operadores y redes empresariales. El SBC aplica políticas y control en esas fronteras.",
                ),
                (
                    "¿Qué debe probarse antes de llevar un SBC a producción?",
                    "Deben probarse flujos normales y de falla, interoperabilidad SIP, codecs, cifrado, formato de números, failover, ruteo de emergencia cuando corresponda, monitoreo y escalamiento de soporte.",
                ),
            ],
        },
    },
    "bpos-evaluate-telecom-infrastructure-partners": {
        "en": {
            "checklist": [
                "Service availability, redundancy and recovery objectives matched to client SLAs",
                "Real-time monitoring of routes, carriers, quality indicators and incidents",
                "SIP and SBC expertise across the BPO's CCaaS and dialer environment",
                "Regional carrier coverage, numbering capabilities and regulatory readiness",
                "Commercial transparency, escalation governance and capacity to support growth",
            ],
            "closing": "A disciplined selection process combines architecture review, operational evidence and commercial governance. The partner should demonstrate how incidents are detected, owned and resolved, not only present a coverage map. A pilot with representative traffic helps expose the quality of integration and support before a broader commitment.",
            "faq": [
                (
                    "Which telecom criteria matter most for a BPO?",
                    "Availability, voice quality, routing flexibility, monitoring, fast incident response, SIP expertise, regional coverage and alignment with client SLAs are central criteria.",
                ),
                (
                    "Why is the lowest telecom price not always the best choice?",
                    "Telecom is a production dependency for a BPO. Savings can disappear quickly when outages, poor quality or slow support affect agent productivity, contractual service levels and client retention.",
                ),
            ],
        },
        "pt": {
            "checklist": [
                "Disponibilidade, redundância e objetivos de recuperação alinhados aos SLAs dos clientes",
                "Monitoramento em tempo real de rotas, operadoras, indicadores de qualidade e incidentes",
                "Experiência em SIP e SBC no ambiente de CCaaS e discadores do BPO",
                "Cobertura regional, recursos de numeração e prontidão regulatória",
                "Transparência comercial, governança de escalonamento e capacidade de apoiar crescimento",
            ],
            "closing": "Um processo disciplinado combina revisão de arquitetura, evidências operacionais e governança comercial. O parceiro deve demonstrar como incidentes são detectados, assumidos e resolvidos, e não apenas apresentar um mapa de cobertura. Um piloto com tráfego representativo ajuda a revelar a qualidade da integração e do suporte antes de um compromisso maior.",
            "faq": [
                (
                    "Quais critérios de telecom são mais importantes para um BPO?",
                    "Disponibilidade, qualidade de voz, flexibilidade de roteamento, monitoramento, resposta rápida a incidentes, conhecimento SIP, cobertura regional e alinhamento aos SLAs dos clientes são critérios centrais.",
                ),
                (
                    "Por que o menor preço de telecom nem sempre é a melhor escolha?",
                    "Telecom é uma dependência de produção para o BPO. Uma economia inicial pode desaparecer quando indisponibilidade, baixa qualidade ou suporte lento afetam produtividade, níveis de serviço e retenção de clientes.",
                ),
            ],
        },
        "es": {
            "checklist": [
                "Disponibilidad, redundancia y objetivos de recuperación alineados con los SLA",
                "Monitoreo en tiempo real de rutas, operadores, calidad e incidentes",
                "Experiencia SIP y SBC en el entorno CCaaS y de marcadores del BPO",
                "Cobertura regional, numeración y preparación regulatoria",
                "Transparencia comercial, gobierno de escalamiento y capacidad de crecimiento",
            ],
            "closing": "Un proceso disciplinado combina revisión de arquitectura, evidencia operacional y gobierno comercial. El partner debe demostrar cómo detecta, asume y resuelve incidentes. Un piloto con tráfico representativo ayuda a validar integración y soporte antes de un compromiso mayor.",
            "faq": [
                (
                    "¿Qué criterios telecom son más importantes para un BPO?",
                    "Disponibilidad, calidad de voz, flexibilidad de ruteo, monitoreo, respuesta rápida a incidentes, conocimiento SIP, cobertura regional y alineación con los SLA son criterios centrales.",
                ),
                (
                    "¿Por qué el menor precio telecom no siempre es la mejor elección?",
                    "Telecom es una dependencia de producción para el BPO. El ahorro puede desaparecer cuando fallas, mala calidad o soporte lento afectan productividad, niveles de servicio y retención de clientes.",
                ),
            ],
        },
    },
    "latam-bridge-us-cx-global-delivery": {
        "en": {
            "checklist": [
                "Country selection based on language, talent, regulation and operating model",
                "Telecom quality, carrier diversity and connectivity to the target CCaaS stack",
                "Cultural and time-zone alignment with the customer journeys being served",
                "Local partners for hiring, compliance, facilities and technical operations",
                "A phased market-entry plan with clear service, quality and financial measures",
            ],
            "closing": "LATAM should be evaluated as a portfolio of markets, not as a single operating environment. A practical entry plan selects the right country for the service profile, validates telecom and talent assumptions, and expands after quality and governance are proven. Regional scale comes from repeatable operating discipline rather than from geography alone.",
            "faq": [
                (
                    "Why is LATAM relevant for US customer experience operations?",
                    "The region combines time-zone proximity, multilingual talent, cultural familiarity and established BPO and telecom ecosystems, which can support nearshore customer service and sales models.",
                ),
                (
                    "Is one LATAM market suitable for every CX operation?",
                    "No. Language, talent availability, costs, regulation, telecom maturity and customer needs vary by country. Selection should follow the specific service and risk profile.",
                ),
            ],
        },
        "pt": {
            "checklist": [
                "Seleção do país com base em idioma, talentos, regulação e modelo operacional",
                "Qualidade de telecom, diversidade de operadoras e conexão com o stack de CCaaS",
                "Alinhamento cultural e de fuso horário com as jornadas atendidas",
                "Parceiros locais para contratação, compliance, instalações e operação técnica",
                "Plano de entrada em fases com métricas claras de serviço, qualidade e resultado financeiro",
            ],
            "closing": "A América Latina deve ser avaliada como um portfólio de mercados, e não como um único ambiente operacional. Um plano prático escolhe o país adequado ao perfil do serviço, valida premissas de telecom e talentos e amplia após comprovar qualidade e governança. A escala regional nasce de disciplina operacional repetível.",
            "faq": [
                (
                    "Por que a América Latina é relevante para operações de CX dos EUA?",
                    "A região combina proximidade de fuso horário, talentos multilíngues, familiaridade cultural e ecossistemas maduros de BPO e telecom, favorecendo modelos nearshore de atendimento e vendas.",
                ),
                (
                    "Um único mercado latino-americano serve para qualquer operação de CX?",
                    "Não. Idiomas, disponibilidade de talentos, custos, regulação, maturidade de telecom e necessidades dos clientes variam por país. A escolha deve seguir o perfil específico do serviço e do risco.",
                ),
            ],
        },
        "es": {
            "checklist": [
                "Selección del país según idioma, talento, regulación y modelo operacional",
                "Calidad telecom, diversidad de operadores y conexión con el stack CCaaS",
                "Alineación cultural y horaria con los journeys atendidos",
                "Socios locales para contratación, compliance, instalaciones y operación técnica",
                "Plan de entrada por fases con métricas claras de servicio, calidad y finanzas",
            ],
            "closing": "Latinoamérica debe evaluarse como un portafolio de mercados y no como un único entorno operacional. Un plan práctico elige el país adecuado, valida telecom y talento y amplía después de comprobar calidad y gobierno.",
            "faq": [
                (
                    "¿Por qué Latinoamérica es relevante para operaciones de CX de EE.UU.?",
                    "La región combina proximidad horaria, talento multilingüe, afinidad cultural y ecosistemas establecidos de BPO y telecom, apoyando modelos nearshore de servicio y ventas.",
                ),
                (
                    "¿Un solo mercado latinoamericano sirve para cualquier operación de CX?",
                    "No. Idiomas, talento, costos, regulación, madurez telecom y necesidades del cliente varían por país. La selección debe seguir el perfil de servicio y riesgo.",
                ),
            ],
        },
    },
    "european-ccaas-local-telecom-partners": {
        "en": {
            "checklist": [
                "Local numbering, portability and regulatory requirements in each target country",
                "Carrier relationships and tested SIP interoperability with the CCaaS platform",
                "Latency, media routing, resilience and voice-quality monitoring",
                "Local-language technical support and clear cross-vendor escalation",
                "A channel model that aligns commercial ownership, enablement and customer success",
            ],
            "closing": "Market entry works best when the platform vendor and telecom partner design the offer together. Technical readiness, support responsibilities and channel economics should be explicit before customer acquisition accelerates. This gives enterprise buyers a coherent service instead of a platform contract surrounded by unresolved local dependencies.",
            "faq": [
                (
                    "Why do CCaaS vendors need local telecom partners?",
                    "Local partners help navigate numbering, carrier access, SIP interoperability, regulation, latency, support expectations and the operational details that vary by country.",
                ),
                (
                    "What makes a strong CCaaS and telecom partnership?",
                    "A strong partnership combines tested integration, shared support processes, transparent commercial ownership, local market knowledge and a joint plan for customer success.",
                ),
            ],
        },
        "pt": {
            "checklist": [
                "Numeração local, portabilidade e requisitos regulatórios em cada país-alvo",
                "Relacionamento com operadoras e interoperabilidade SIP testada com a plataforma CCaaS",
                "Latência, roteamento de mídia, resiliência e monitoramento da qualidade de voz",
                "Suporte técnico no idioma local e escalonamento claro entre fornecedores",
                "Modelo de canal que alinhe responsabilidade comercial, capacitação e sucesso do cliente",
            ],
            "closing": "A entrada em mercado funciona melhor quando o fornecedor da plataforma e o parceiro de telecom desenham a oferta em conjunto. Prontidão técnica, responsabilidades de suporte e economia do canal devem estar claras antes de acelerar a aquisição. Assim, o cliente corporativo recebe um serviço coerente, sem dependências locais indefinidas.",
            "faq": [
                (
                    "Por que fornecedores de CCaaS precisam de parceiros locais de telecom?",
                    "Parceiros locais ajudam com numeração, acesso a operadoras, interoperabilidade SIP, regulação, latência, expectativas de suporte e detalhes operacionais que variam em cada país.",
                ),
                (
                    "O que caracteriza uma parceria forte entre CCaaS e telecom?",
                    "Uma parceria forte combina integração testada, processos compartilhados de suporte, responsabilidade comercial transparente, conhecimento do mercado local e plano conjunto para o sucesso do cliente.",
                ),
            ],
        },
        "es": {
            "checklist": [
                "Numeración local, portabilidad y requisitos regulatorios de cada país",
                "Relaciones con operadores e interoperabilidad SIP probada con la plataforma",
                "Latencia, ruteo de medios, resiliencia y monitoreo de calidad",
                "Soporte técnico en idioma local y escalamiento claro entre proveedores",
                "Modelo de canal que alinee propiedad comercial, capacitación y customer success",
            ],
            "closing": "La entrada a mercado funciona mejor cuando el proveedor de plataforma y el partner telecom diseñan la oferta juntos. La preparación técnica, las responsabilidades de soporte y la economía del canal deben estar claras antes de acelerar la adquisición.",
            "faq": [
                (
                    "¿Por qué los proveedores CCaaS necesitan partners telecom locales?",
                    "Los partners locales ayudan con numeración, operadores, interoperabilidad SIP, regulación, latencia, soporte y detalles operacionales que varían por país.",
                ),
                (
                    "¿Qué caracteriza una alianza sólida entre CCaaS y telecom?",
                    "Combina integración probada, procesos compartidos de soporte, propiedad comercial transparente, conocimiento local y un plan conjunto de customer success.",
                ),
            ],
        },
    },
    "ai-contact-centers-roi": {
        "en": {
            "checklist": [
                "A clearly defined business problem and an operational baseline before implementation",
                "Metrics tied to revenue, cost, quality, compliance or customer outcomes",
                "Integration with telecom, CCaaS, CRM, workforce and quality workflows",
                "Human oversight, observability and ownership for exceptions and model drift",
                "A phased rollout that validates value before expanding scope",
            ],
            "closing": "A credible AI roadmap begins with one operational problem, one accountable owner and a small set of measurable outcomes. Teams should validate data quality and workflow integration before scaling. When governance and measurement are built into the implementation, AI becomes part of operating discipline rather than a disconnected demonstration.",
            "faq": [
                (
                    "Which metrics show AI ROI in a contact center?",
                    "The right metrics depend on the use case, but common examples include containment, answer and conversion rates, average handling time, agent occupancy, quality scores, compliance, repeat contacts, customer satisfaction and cost per interaction.",
                ),
                (
                    "Why do contact center AI pilots fail to scale?",
                    "Common causes include vague goals, weak data, poor integration, no operational owner, limited observability and a pilot that is disconnected from the real telecom and customer-service workflow.",
                ),
            ],
        },
        "pt": {
            "checklist": [
                "Problema de negócio claramente definido e linha de base antes da implementação",
                "Métricas ligadas a receita, custo, qualidade, compliance ou resultado para o cliente",
                "Integração com telecom, CCaaS, CRM, workforce e fluxos de qualidade",
                "Supervisão humana, observabilidade e responsáveis por exceções e mudanças do modelo",
                "Implantação em fases que comprove valor antes de ampliar o escopo",
            ],
            "closing": "Um roteiro confiável de IA começa com um problema operacional, um responsável e poucos resultados mensuráveis. Os times devem validar qualidade dos dados e integração aos fluxos antes da escala. Quando governança e medição fazem parte da implementação, a IA se torna disciplina operacional, não apenas demonstração.",
            "faq": [
                (
                    "Quais métricas demonstram ROI de IA em um contact center?",
                    "As métricas dependem do caso de uso, mas podem incluir contenção, taxas de atendimento e conversão, tempo médio, ocupação de agentes, qualidade, compliance, contatos repetidos, satisfação e custo por interação.",
                ),
                (
                    "Por que pilotos de IA em contact centers não conseguem escalar?",
                    "Causas frequentes incluem objetivos vagos, dados fracos, integração insuficiente, ausência de responsável operacional, pouca observabilidade e um piloto desconectado do fluxo real de telecom e atendimento.",
                ),
            ],
        },
        "es": {
            "checklist": [
                "Problema de negocio definido y línea base antes de implementar",
                "Métricas vinculadas a ingresos, costo, calidad, compliance o cliente",
                "Integración con telecom, CCaaS, CRM, workforce y calidad",
                "Supervisión humana, observabilidad y responsables de excepciones",
                "Despliegue por fases que valide valor antes de ampliar el alcance",
            ],
            "closing": "Una hoja de ruta confiable empieza con un problema operacional, un responsable y pocos resultados medibles. Los equipos deben validar datos e integración antes de escalar. Con gobierno y medición, la IA se convierte en disciplina operacional.",
            "faq": [
                (
                    "¿Qué métricas muestran ROI de IA en un contact center?",
                    "Depende del caso, pero pueden incluir contención, tasas de respuesta y conversión, tiempo medio, ocupación, calidad, compliance, contactos repetidos, satisfacción y costo por interacción.",
                ),
                (
                    "¿Por qué los pilotos de IA no logran escalar?",
                    "Causas frecuentes son objetivos vagos, datos débiles, mala integración, falta de responsable operacional, poca observabilidad y desconexión del flujo real de telecom y servicio.",
                ),
            ],
        },
    },
}


def apply_editorial_payload(target: dict, payload: dict) -> None:
    for key, value in payload.items():
        if key not in {"checklist", "closing", "faq"}:
            target[key] = value
    ARTICLE_ENHANCEMENTS[target["slug"]] = {
        lang: {
            "checklist": payload["checklist"][lang],
            "closing": payload["closing"][lang],
            "faq": payload["faq"][lang],
        }
        for lang in ("en", "pt", "es")
    }


for existing_article in ARTICLES:
    payload = ARTICLE_UPDATES.get(existing_article["slug"])
    if payload:
        apply_editorial_payload(existing_article, payload)

for payload in NEW_ARTICLES:
    new_article: dict = {}
    apply_editorial_payload(new_article, payload)
    ARTICLES.append(new_article)


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


def display_date(lang: str, iso_date: str) -> str:
    value = datetime.strptime(iso_date, "%Y-%m-%d")
    if lang == "en":
        return value.strftime("%b %d, %Y").replace(" 0", " ")
    return value.strftime("%d/%m/%Y")


def article_path(lang: str, article: dict) -> str:
    return lang_url(lang, f"insights/{article['slug']}/")


def topic_path(lang: str, topic_slug: str) -> str:
    return lang_url(lang, f"topics/{topic_slug}/")


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
        f'    <link rel="alternate" hreflang="x-default" href="{BASE_URL}{lang_url("en", path)}" />',
    ]
    return "\n".join(links)


def head(
    lang: str,
    page_title: str | None = None,
    description: str | None = None,
    path: str = "",
    page_type: str = "profile",
    article: dict | None = None,
) -> str:
    meta = META[lang]
    title = page_title or meta["title"]
    desc = description or meta["description"]
    og_type = "article" if page_type == "article" else "website"
    preload = (
        '    <link rel="preload" href="/public/images/luiz-terra-executive-520.webp" as="image" type="image/webp" imagesrcset="/public/images/luiz-terra-executive-320.webp 320w, /public/images/luiz-terra-executive-520.webp 520w" imagesizes="(max-width: 768px) 100vw, 340px" fetchpriority="high" />\n'
        if page_type == "profile"
        else ""
    )
    article_meta = ""
    if page_type == "article" and article:
        article_meta = f"""
    <meta property="article:published_time" content="{DATE_PUBLISHED}" />
    <meta property="article:modified_time" content="{DATE_MODIFIED}" />
    <meta property="article:author" content="{LINKEDIN}" />
    <meta property="article:section" content="{esc(article["category"][lang])}" />"""
    og_image = f"{BASE_URL}/public/og/{article['slug']}.png" if page_type == "article" and article else f"{BASE_URL}/public/og-image.png"
    return f"""  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{esc(title)}</title>
    <meta name="description" content="{esc(desc)}" />
    <meta name="author" content="Luiz Terra" />
    <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1" />
    <meta name="msvalidate.01" content="D32D665088441B4D7E0274D9B3AEC1A1" />
    <link rel="canonical" href="{canonical(lang, path)}" />
{hreflang(path)}
    <meta property="og:title" content="{esc(title)}" />
    <meta property="og:description" content="{esc(desc)}" />
    <meta property="og:url" content="{canonical(lang, path)}" />
    <meta property="og:type" content="{og_type}" />
    <meta property="og:site_name" content="Luiz Terra" />
    <meta property="og:locale" content="{meta["locale"]}" />
    <meta property="og:image" content="{og_image}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Luiz Terra, International Sales Executive in Telecom, CX, BPO and AI" />
{article_meta}
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{esc(title)}" />
    <meta name="twitter:description" content="{esc(desc)}" />
    <meta name="twitter:image" content="{og_image}" />
    <link rel="icon" href="/public/favicon.svg" type="image/svg+xml" />
    <link rel="alternate" type="application/rss+xml" title="Luiz Terra Insights" href="{BASE_URL}/feed.xml" />
{preload}{gtag()}
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet" media="print" onload="this.media='all'" />
    <noscript><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet" /></noscript>
    <link rel="stylesheet" href="/styles.css" />
    <script type="application/ld+json">{schema_json(lang, path, page_type, article)}</script>
  </head>"""


def schema_json(lang: str, path: str, page_type: str, article: dict | None) -> str:
    url = canonical(lang, path)
    person = {
        "@type": "Person",
        "@id": f"{BASE_URL}/#luiz-terra",
        "name": "Luiz Terra",
        "description": META[lang]["description"],
        "image": {
            "@type": "ImageObject",
            "url": f"{BASE_URL}/public/images/luiz-terra-executive.jpg",
            "width": 900,
            "height": 900,
        },
        "jobTitle": "Head of International Sales",
        "worksFor": {"@type": "Organization", "name": "Khomp"},
        "email": f"mailto:{EMAIL}",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "São Paulo",
            "addressCountry": "Brazil",
        },
        "url": BASE_URL,
        "sameAs": [LINKEDIN],
        "knowsLanguage": ["Portuguese", "English", "Spanish"],
        "knowsAbout": [
            "Telecom",
            "Telecommunications",
            "Customer Experience",
            "Contact Center",
            "BPO",
            "Business Process Outsourcing",
            "CCaaS",
            "Contact Center as a Service",
            "Session Border Controller",
            "SBC",
            "SIP",
            "VoIP",
            "Cloud Communications",
            "Artificial Intelligence",
            "Answering Machine Detection",
            "AI-powered Answering Machine Detection",
            "Enterprise Sales",
            "Strategic Partnerships",
            "Go-to-Market",
            "Market Entry",
            "International Market Entry",
            "LATAM",
            "Nearshore CX",
        ],
    }
    website = {
        "@type": "WebSite",
        "@id": f"{BASE_URL}/#website",
        "url": f"{BASE_URL}/",
        "name": "Luiz Terra",
        "inLanguage": ["en", "pt-BR", "es"],
        "publisher": {"@id": f"{BASE_URL}/#luiz-terra"},
    }
    graph: list[dict] = [website, person]

    if page_type == "article" and article:
        graph.extend(
            [
                {
                    "@type": "BlogPosting",
                    "@id": f"{url}#article",
                    "mainEntityOfPage": {"@type": "WebPage", "@id": url},
                    "headline": article["title"][lang],
                    "description": article["summary"][lang],
                    "image": f"{BASE_URL}/public/og/{article['slug']}.png",
                    "datePublished": article.get("published", DATE_PUBLISHED),
                    "dateModified": article.get("modified", DATE_MODIFIED),
                    "inLanguage": META[lang]["lang"],
                    "author": {"@id": f"{BASE_URL}/#luiz-terra"},
                    "publisher": {"@id": f"{BASE_URL}/#luiz-terra"},
                    "articleSection": article["category"][lang],
                    "keywords": article["tags"],
                },
                {
                    "@type": "BreadcrumbList",
                    "@id": f"{url}#breadcrumb",
                    "itemListElement": [
                        {
                            "@type": "ListItem",
                            "position": 1,
                            "name": "Luiz Terra",
                            "item": canonical(lang),
                        },
                        {
                            "@type": "ListItem",
                            "position": 2,
                            "name": "Insights",
                            "item": canonical(lang, "insights/"),
                        },
                        {
                            "@type": "ListItem",
                            "position": 3,
                            "name": article["title"][lang],
                            "item": url,
                        },
                    ],
                },
            ]
        )
        faq_items = ARTICLE_ENHANCEMENTS[article["slug"]][lang]["faq"]
        graph.append(
            {
                "@type": "FAQPage",
                "@id": f"{url}#faq",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": question,
                        "acceptedAnswer": {"@type": "Answer", "text": answer},
                    }
                    for question, answer in faq_items
                ],
            }
        )
    elif page_type == "collection":
        graph.append(
            {
                "@type": "CollectionPage",
                "@id": f"{url}#collection",
                "url": url,
                "name": INSIGHTS_META[lang]["title"],
                "description": INSIGHTS_META[lang]["description"],
                "inLanguage": META[lang]["lang"],
                "author": {"@id": f"{BASE_URL}/#luiz-terra"},
                "isPartOf": {"@id": f"{BASE_URL}/#website"},
            }
        )
    elif page_type == "topic" and article:
        graph.extend(
            [
                {
                    "@type": "CollectionPage",
                    "@id": f"{url}#topic",
                    "url": url,
                    "name": article["title"][lang],
                    "description": article["description"][lang],
                    "inLanguage": META[lang]["lang"],
                    "author": {"@id": f"{BASE_URL}/#luiz-terra"},
                    "isPartOf": {"@id": f"{BASE_URL}/#website"},
                },
                {
                    "@type": "BreadcrumbList",
                    "@id": f"{url}#breadcrumb",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": "Luiz Terra", "item": canonical(lang)},
                        {"@type": "ListItem", "position": 2, "name": article["title"][lang], "item": url},
                    ],
                },
            ]
        )
    elif page_type == "bio":
        graph.extend(
            [
                {
                    "@type": "ProfilePage",
                    "@id": f"{url}#profile",
                    "url": url,
                    "name": EXECUTIVE_BIO["title"][lang],
                    "description": EXECUTIVE_BIO["description"][lang],
                    "dateCreated": SCHEMA_DATE_CREATED,
                    "dateModified": SCHEMA_DATE_MODIFIED,
                    "inLanguage": META[lang]["lang"],
                    "mainEntity": {"@id": f"{BASE_URL}/#luiz-terra"},
                    "isPartOf": {"@id": f"{BASE_URL}/#website"},
                },
                {
                    "@type": "BreadcrumbList",
                    "@id": f"{url}#breadcrumb",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": "Luiz Terra", "item": canonical(lang)},
                        {"@type": "ListItem", "position": 2, "name": UI[lang]["bio"], "item": url},
                    ],
                },
            ]
        )
    else:
        graph.extend(
            [
                {
                    "@type": "ProfilePage",
                    "@id": f"{url}#profile",
                    "url": url,
                    "name": META[lang]["title"],
                    "description": META[lang]["description"],
                    "dateCreated": SCHEMA_DATE_CREATED,
                    "dateModified": SCHEMA_DATE_MODIFIED,
                    "inLanguage": META[lang]["lang"],
                    "mainEntity": {"@id": f"{BASE_URL}/#luiz-terra"},
                    "isPartOf": {"@id": f"{BASE_URL}/#website"},
                },
                {
                    "@type": "FAQPage",
                    "@id": f"{url}#faq",
                    "mainEntity": [
                        {
                            "@type": "Question",
                            "name": question,
                            "acceptedAnswer": {"@type": "Answer", "text": answer},
                        }
                        for question, answer in HOME_FAQ[lang]
                    ],
                },
            ]
        )

    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=6)


def nav(lang: str, current_path: str = "") -> str:
    c = COPY[lang]
    menu_label = {"en": "Open navigation menu", "pt": "Abrir menu de navegação", "es": "Abrir menú de navegación"}[lang]
    home = lang_url(lang)
    section = lambda anchor: f"#{anchor}" if current_path == "" else f"{home}#{anchor}"
    nav_items = [
        (section("impact"), c["nav"][0]),
        (section("expertise"), c["nav"][1]),
        (lang_url(lang, "insights/"), c["nav"][2]),
        (lang_url(lang, "executive-bio/"), UI[lang]["bio"]),
        (section("speaking"), c["nav"][3]),
        (section("contact"), c["nav"][4]),
    ]
    links = "\n".join(f'        <a href="{href}">{esc(label)}</a>' for href, label in nav_items)
    lang_links = "\n".join(
        f'          <a href="{lang_url(code, current_path)}" class="{"is-active" if code == lang else ""}" aria-current="{"page" if code == lang else "false"}">{label}</a>'
        for code, label in [("en", "EN"), ("pt", "PT"), ("es", "ES")]
    )
    return f"""    <nav class="site-nav" aria-label="Main navigation">
      <a class="brand" href="{lang_url(lang)}" aria-label="LT - Luiz Terra home">LT</a>
      <button class="nav-toggle" type="button" aria-label="{esc(menu_label)}" aria-expanded="false" aria-controls="nav-links">
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
    featured_articles = [article for article in ARTICLES if article.get("featured")][:6]
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
        f"""            <article data-article-slug="{article["slug"]}" data-category="{esc(article["category"][lang])}">
              <span>{esc(article["category"][lang])}</span>
              <h3>{esc(article["title"][lang])}</h3>
              <p>{esc(article["summary"][lang])}</p>
              <div class="card-meta"><time datetime="{article.get('published', DATE_PUBLISHED)}">{display_date(lang, article.get('published', DATE_PUBLISHED))}</time><span>{esc(article.get('reading', ARTICLE_LABELS[lang]['reading'])[lang] if isinstance(article.get('reading'), dict) else ARTICLE_LABELS[lang]['reading'])}</span></div>
              <a href="{article_path(lang, article)}">{esc(UI[lang]["read_article"])}</a>
            </article>"""
        for article in featured_articles
    )
    topic_cards = "\n".join(
        f"""            <article>
              <span>{idx:02d}</span>
              <h3>{esc(topic["title"][lang])}</h3>
              <p>{esc(topic["description"][lang])}</p>
              <a href="{topic_path(lang, topic['slug'])}">{esc(UI[lang]["explore_topic"])}</a>
            </article>"""
        for idx, topic in enumerate(TOPICS, 1)
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
    home_faq = "\n".join(
        f"""            <details>
              <summary>{esc(question)}</summary>
              <p>{esc(answer)}</p>
            </details>"""
        for question, answer in HOME_FAQ[lang]
    )
    return f"""<!DOCTYPE html>
<html lang="{META[lang]["lang"]}">
{head(lang)}
  <body>
{nav(lang)}
    <main id="top">
      <section class="hero" aria-labelledby="hero-title">
        <div class="hero-grid">
          <div class="hero-copy">
            <p class="eyebrow">{esc(c["hero_eyebrow"])}</p>
            <h1 id="hero-title">Luiz Terra</h1>
            <p class="hero-role">{esc(c["headline"])}</p>
            <p class="hero-subline">{esc(c["subheadline"])}</p>
            <p class="hero-support">{esc(c["support"])}</p>
            <div class="hero-actions" aria-label="Primary actions">
              <a class="button primary" href="mailto:{EMAIL}?subject=Strategic%20conversation">{esc(c["primary_cta"])}</a>
              <a class="button secondary" href="{LINKEDIN}" target="_blank" rel="noopener">{esc(c["secondary_cta"])}</a>
              <a class="button tertiary" href="{lang_url(lang, 'executive-bio/')}">{esc(c["bio_cta"])}</a>
            </div>
          </div>
          <aside class="hero-panel hero-profile" aria-label="Current role">
            <picture>
              <source type="image/webp" srcset="/public/images/luiz-terra-executive-320.webp 320w, /public/images/luiz-terra-executive-520.webp 520w" sizes="(max-width: 768px) 100vw, 340px" />
              <img src="/public/images/luiz-terra-executive.jpg" alt="Luiz Terra, International Sales Executive in Telecom, CX, BPO and AI" width="520" height="520" fetchpriority="high" decoding="async" draggable="false" />
            </picture>
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
          <p class="section-link"><a href="{lang_url(lang, 'insights/')}">{esc(UI[lang]["insights_heading"])} →</a></p>
        </div>
      </section>
      <section class="content-section section-reveal" id="topics" aria-labelledby="topics-title">
        <div class="section-label">{esc(UI[lang]["topics"])}</div>
        <div class="section-body">
          <h2 id="topics-title">{esc(UI[lang]["topics"])}</h2>
          <div class="topic-grid">
{topic_cards}
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
      <section class="content-section section-reveal" id="faq" aria-labelledby="faq-title">
        <div class="section-label">FAQ</div>
        <div class="section-body">
          <h2 id="faq-title">{esc(ARTICLE_LABELS[lang]["faq"])}</h2>
          <div class="faq-list">
{home_faq}
          </div>
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
    filter_by_cluster = {
        "sbc-contact-centers": "telecom",
        "ai-contact-centers": "ai",
        "bpo-telecom-infrastructure": "cx-bpo",
        "latam-nearshore-cx": "latam",
        "ccaas-latam": "international-growth",
        "international-market-entry": "international-growth",
    }
    cards = "\n".join(
        f"""          <article data-article-slug="{article["slug"]}" data-category="{filter_by_cluster.get(article.get('cluster'), 'all')}">
            <span>{esc(article["category"][lang])}</span>
            <h3>{esc(article["title"][lang])}</h3>
            <p>{esc(article["summary"][lang])}</p>
            <div class="card-meta"><time datetime="{article.get('published', DATE_PUBLISHED)}">{display_date(lang, article.get('published', DATE_PUBLISHED))}</time><span>{esc(article.get('reading', {}).get(lang, ARTICLE_LABELS[lang]['reading']))}</span></div>
            <a href="{article_path(lang, article)}">{esc(UI[lang]["read_article"])}</a>
          </article>"""
        for article in ARTICLES
    )
    filters = "\n".join(
        f'<button type="button" data-filter="{key}" aria-pressed="false">{esc(label)}</button>'
        for key, label in zip(["telecom", "ai", "cx-bpo", "latam", "international-growth"], UI[lang]["filters"])
    )
    return f"""<!DOCTYPE html>
<html lang="{META[lang]["lang"]}">
{head(lang, INSIGHTS_META[lang]["title"], INSIGHTS_META[lang]["description"], "insights/", "collection")}
  <body>
{nav(lang, "insights/")}
    <main class="subpage-main">
      <section class="content-section section-reveal is-visible" id="insights" aria-labelledby="insights-title">
        <div class="section-label">Insights</div>
        <div class="section-body">
          <h1 class="subpage-title" id="insights-title">{esc(UI[lang]["insights_heading"])}</h1>
          <p class="article-summary">{esc(UI[lang]["insights_support"])}</p>
          <div class="category-filters" aria-label="Insight categories">
            <button type="button" data-filter="all" aria-pressed="true">{esc(UI[lang]["all"])}</button>
{filters}
          </div>
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


def render_topic(lang: str, topic: dict) -> str:
    articles = [item for slug in topic["articles"] for item in ARTICLES if item["slug"] == slug]
    cards = "\n".join(
        f"""          <article>
            <span>{esc(item["category"][lang])}</span>
            <h3>{esc(item["title"][lang])}</h3>
            <p>{esc(item["summary"][lang])}</p>
            <div class="card-meta"><time datetime="{item.get('published', DATE_PUBLISHED)}">{display_date(lang, item.get('published', DATE_PUBLISHED))}</time><span>{esc(item.get('reading', {}).get(lang, ARTICLE_LABELS[lang]['reading']))}</span></div>
            <a href="{article_path(lang, item)}">{esc(UI[lang]["read_article"])}</a>
          </article>"""
        for item in articles
    )
    themes = "".join(f"<span>{esc(theme)}</span>" for theme in topic["themes"])
    path = f"topics/{topic['slug']}/"
    return f"""<!DOCTYPE html>
<html lang="{META[lang]["lang"]}">
{head(lang, f'{topic["title"][lang]} | Luiz Terra', topic["description"][lang], path, "topic", topic)}
  <body>
{nav(lang, path)}
    <main class="subpage-main topic-main">
      <section class="topic-hero section-reveal is-visible">
        <nav class="article-breadcrumb" aria-label="Breadcrumb"><a href="{lang_url(lang)}">Luiz Terra</a><span aria-hidden="true">/</span><span>{esc(UI[lang]["topics"])}</span></nav>
        <p class="eyebrow">{esc(UI[lang]["topics"])}</p>
        <h1 class="subpage-title">{esc(topic["title"][lang])}</h1>
        <p class="article-summary">{esc(topic["description"][lang])}</p>
      </section>
      <section class="content-section section-reveal is-visible">
        <div class="section-label">{esc(UI[lang]["executive_view"])}</div>
        <div class="section-body">
          <p class="pillar-perspective">{esc(topic["perspective"][lang])}</p>
          <h2>{esc(UI[lang]["topic_themes"])}</h2>
          <div class="chips">{themes}</div>
        </div>
      </section>
      <section class="content-section section-reveal is-visible">
        <div class="section-label">{esc(UI[lang]["topic_articles"])}</div>
        <div class="section-body">
          <h2>{esc(UI[lang]["topic_articles"])}</h2>
          <div class="insight-grid">{cards}</div>
        </div>
      </section>
    </main>
{footer(lang)}
    <script src="/script.js"></script>
  </body>
</html>
"""


def render_executive_bio(lang: str) -> str:
    sections = "\n".join(
        f"""        <section>
          <h2>{esc(heading)}</h2>
          {''.join(f'<p>{esc(paragraph)}</p>' for paragraph in paragraphs)}
        </section>"""
        for heading, paragraphs in EXECUTIVE_BIO["sections"][lang]
    )
    return f"""<!DOCTYPE html>
<html lang="{META[lang]["lang"]}">
{head(lang, EXECUTIVE_BIO["title"][lang], EXECUTIVE_BIO["description"][lang], "executive-bio/", "bio")}
  <body>
{nav(lang, "executive-bio/")}
    <main class="subpage-main article-main">
      <article class="article-page executive-bio-page section-reveal is-visible">
        <nav class="article-breadcrumb" aria-label="Breadcrumb"><a href="{lang_url(lang)}">Luiz Terra</a><span aria-hidden="true">/</span><span>{esc(UI[lang]["bio"])}</span></nav>
        <p class="eyebrow">{esc(UI[lang]["bio"])}</p>
        <h1 class="subpage-title">Luiz Terra</h1>
        <p class="bio-position">{esc(EXECUTIVE_BIO["position"][lang])}</p>
        <div class="bio-actions">
          <a class="button primary" href="mailto:{EMAIL}?subject=Strategic%20conversation">{esc(UI[lang]["strategic_conversation"])}</a>
          <a class="button tertiary" href="/public/luiz-terra-executive-bio.pdf" download>{esc(UI[lang]["download_bio"])}</a>
        </div>
        <div class="article-content bio-content">{sections}</div>
        <section class="related-insights"><h2>{esc(UI[lang]["insights_heading"])}</h2><p><a class="article-back" href="{lang_url(lang, 'insights/')}">{esc(UI[lang]["insights_support"])}</a></p></section>
      </article>
    </main>
{footer(lang)}
    <script src="/script.js"></script>
  </body>
</html>
"""


def render_article(lang: str, article: dict) -> str:
    c = COPY[lang]
    labels = ARTICLE_LABELS[lang]
    enhancement = ARTICLE_ENHANCEMENTS[article["slug"]][lang]
    if article.get("sections"):
        body = "\n".join(
            f"          <h2>{esc(heading)}</h2>\n" + "\n".join(f"          <p>{esc(paragraph)}</p>" for paragraph in paragraphs)
            for heading, paragraphs in article["sections"][lang]
        )
    else:
        body = "\n".join(f"          <p>{esc(p)}</p>" for p in article["body"][lang])
    tags = "".join(f"<span>{esc(tag)}</span>" for tag in article["tags"])
    title = article["title"][lang]
    desc = article["summary"][lang]
    checklist = "\n".join(f"            <li>{esc(item)}</li>" for item in enhancement["checklist"])
    faq = "\n".join(
        f"""          <details>
            <summary>{esc(question)}</summary>
            <p>{esc(answer)}</p>
          </details>"""
        for question, answer in enhancement["faq"]
    )
    related_slugs = article.get("related", [])
    related_articles = [item for slug in related_slugs for item in ARTICLES if item["slug"] == slug][:4]
    if not related_articles:
        related_articles = [item for item in ARTICLES if item["slug"] != article["slug"]][:3]
    topic = TOPIC_BY_SLUG.get(article.get("cluster"))
    cluster_context = ""
    if topic:
        guidance = CLUSTER_GUIDANCE.get(article.get("cluster"), {}).get(lang, [])
        cluster_context = (
            f'<h2>{esc(labels["why"])}</h2>'
            f'<p>{esc(topic["perspective"][lang])}</p>'
            + "".join(f"<p>{esc(paragraph)}</p>" for paragraph in guidance)
        )
    related = "\n".join(
        f"""          <article>
            <span>{esc(item["category"][lang])}</span>
            <h3><a href="{lang_url(lang, f'insights/{item["slug"]}/')}">{esc(item["title"][lang])}</a></h3>
          </article>"""
        for item in related_articles
    )
    return f"""<!DOCTYPE html>
<html lang="{META[lang]["lang"]}">
{head(lang, article.get("seo_title", {}).get(lang, f"{title} | Luiz Terra"), desc, f"insights/{article['slug']}/", "article", article)}
  <body>
{nav(lang, f"insights/{article['slug']}/")}
    <main class="subpage-main article-main">
      <article class="article-page section-reveal is-visible">
        <nav class="article-breadcrumb" aria-label="Breadcrumb">
          <a href="{lang_url(lang)}">Luiz Terra</a>
          <span aria-hidden="true">/</span>
          <a href="{lang_url(lang, 'insights/')}">Insights</a>
        </nav>
        <p class="eyebrow">{esc(article["category"][lang])}</p>
        <h1 class="subpage-title">{esc(title)}</h1>
        <p class="article-summary">{esc(desc)}</p>
        <div class="article-meta">
          <span>{esc(UI[lang]["written_by"])} <a href="{lang_url(lang, 'executive-bio/')}">Luiz Terra</a></span>
          <span>{esc(labels["published"])} <time datetime="{article.get('published', DATE_PUBLISHED)}">{display_date(lang, article.get('published', DATE_PUBLISHED))}</time></span>
          <span>{esc(labels["updated"])} <time datetime="{article.get('modified', DATE_MODIFIED)}">{display_date(lang, article.get('modified', DATE_MODIFIED))}</time></span>
          <span>{esc(article.get('reading', {}).get(lang, labels["reading"]))}</span>
        </div>
        <div class="chips article-tags">{tags}</div>
        <div class="article-content">
          {f'<p class="topic-link"><a href="{topic_path(lang, topic["slug"])}">{esc(UI[lang]["explore_topic"])}: {esc(topic["title"][lang])}</a></p>' if topic else ''}
          {cluster_context}
{body}
          <h2>{esc(labels["checklist"])}</h2>
          <ul class="article-checklist">
{checklist}
          </ul>
          <h2>{esc(labels["next"])}</h2>
          <p>{esc(enhancement["closing"])}</p>
          <p class="article-cta"><a class="button primary" href="mailto:{EMAIL}?subject=Strategic%20conversation">{esc(UI[lang]["strategic_conversation"])}</a></p>
          <h2>{esc(labels["faq"])}</h2>
          <div class="faq-list article-faq">
{faq}
          </div>
        </div>
        <section class="related-insights" aria-labelledby="related-title">
          <h2 id="related-title">{esc(labels["related"])}</h2>
          <div class="related-grid">
{related}
          </div>
        </section>
        <div class="article-actions">
          <a class="article-back" href="{lang_url(lang, 'insights/')}">{esc(c["article_back"])}</a>
          <div class="share-actions" aria-label="{esc(c['share'])}">
            <a class="button secondary share-linkedin" href="https://www.linkedin.com/sharing/share-offsite/?url={canonical(lang, f'insights/{article['slug']}/')}" target="_blank" rel="noopener">in&nbsp; {esc(UI[lang]["share_linkedin"])}</a>
            <button class="button tertiary copy-link" type="button" data-copy-url="{canonical(lang, f'insights/{article['slug']}/')}" data-copy-label="{esc(UI[lang]['copied'])}">↗&nbsp; {esc(UI[lang]["copy_link"])}</button>
          </div>
        </div>
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
        write(ROOT / META[lang]["path"] / "executive-bio" / "index.html", render_executive_bio(lang))
        write(ROOT / META[lang]["path"] / "insights" / "index.html", render_insights_index(lang))
        for article in ARTICLES:
            write(ROOT / META[lang]["path"] / "insights" / article["slug"] / "index.html", render_article(lang, article))
        for topic in TOPICS:
            write(ROOT / META[lang]["path"] / "topics" / topic["slug"] / "index.html", render_topic(lang, topic))


def build_sitemap() -> None:
    pages: list[tuple[str, str]] = [("en", ""), ("pt", ""), ("es", "")]
    for lang in ("en", "pt", "es"):
        pages.append((lang, "executive-bio/"))
        pages.append((lang, "insights/"))
        for article in ARTICLES:
            pages.append((lang, f"insights/{article['slug']}/"))
        for topic in TOPICS:
            pages.append((lang, f"topics/{topic['slug']}/"))

    def sitemap_url(lang: str, path: str) -> str:
        alternates = "\n".join(
            f'    <xhtml:link rel="alternate" hreflang="{code}" href="{BASE_URL}{lang_url(target, path)}" />'
            for code, target in [("en", "en"), ("pt-BR", "pt"), ("es", "es")]
        )
        x_default = f'    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE_URL}{lang_url("en", path)}" />'
        priority = "1.0" if path == "" and lang == "en" else "0.8"
        image = (
            f"""
    <image:image>
      <image:loc>{BASE_URL}/public/images/luiz-terra-executive.jpg</image:loc>
      <image:title>Luiz Terra, International Sales Executive</image:title>
    </image:image>"""
            if path == ""
            else ""
        )
        return f"""  <url>
    <loc>{canonical(lang, path)}</loc>
    <lastmod>{DATE_MODIFIED}</lastmod>
{alternates}
{x_default}
    <priority>{priority}</priority>{image}
  </url>"""

    urls = "\n".join(sitemap_url(lang, path) for lang, path in pages)
    write(
        ROOT / "sitemap.xml",
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml"\n'
        '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
        f"{urls}\n"
        "</urlset>\n",
    )


def build_discovery_files() -> None:
    def rss_date(iso_date: str) -> str:
        return datetime.strptime(iso_date, "%Y-%m-%d").strftime("%a, %d %b %Y 12:00:00 -0300")

    items = "\n".join(
        f"""    <item>
      <title>{esc(article["title"]["en"])}</title>
      <link>{canonical("en", f'insights/{article["slug"]}/')}</link>
      <guid isPermaLink="true">{canonical("en", f'insights/{article["slug"]}/')}</guid>
      <description>{esc(article["summary"]["en"])}</description>
      <pubDate>{rss_date(article.get("published", DATE_PUBLISHED))}</pubDate>
      <category>{esc(article["category"]["en"])}</category>
    </item>"""
        for article in ARTICLES
    )
    write(
        ROOT / "feed.xml",
        f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Luiz Terra Insights</title>
    <link>{BASE_URL}/insights/</link>
    <description>Practical perspectives on international sales, telecom, CX, BPO, CCaaS, SBC and AI-powered contact center operations.</description>
    <language>en</language>
    <lastBuildDate>{rss_date(DATE_MODIFIED)}</lastBuildDate>
{items}
  </channel>
</rss>
""",
    )
    article_links = "\n".join(
        f"- [{article['title']['en']}]({canonical('en', f'insights/{article['slug']}/')}): {article['summary']['en']}"
        for article in ARTICLES
    )
    topic_links = "\n".join(
        f"- [{topic['title']['en']}]({canonical('en', f'topics/{topic['slug']}/')}): {topic['description']['en']}"
        for topic in TOPICS
    )
    write(
        ROOT / "llms.txt",
        f"""# Luiz Terra

> Official professional website of Luiz Terra, Head of International Sales at Khomp and an international sales executive with more than 28 years of experience in telecommunications, IT, CX, BPO, contact centers and AI-powered communications.

## Canonical profiles

- Website: {BASE_URL}/
- Portuguese: {BASE_URL}/pt/
- Spanish: {BASE_URL}/es/
- LinkedIn: {LINKEDIN}
- Executive Bio: {BASE_URL}/executive-bio/

## Areas of expertise

- International sales and market entry
- Strategic partnerships and channel development
- Telecom infrastructure, SBC, VoIP and SIP
- Contact Center as a Service, CX and BPO technology
- AI-powered Answering Machine Detection and contact center AI
- LATAM, North America, Europe and Africa

## Insights

{article_links}

## Topic pages

{topic_links}
""",
    )
    write(ROOT / "a7e3c91d5b604f2e8c739d10ab42e6f5.txt", "a7e3c91d5b604f2e8c739d10ab42e6f5\n")


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


def build_article_og_images() -> None:
    output = PUBLIC / "og"
    output.mkdir(parents=True, exist_ok=True)
    for article in ARTICLES:
        image = Image.new("RGB", (1200, 630), "#0F1117")
        draw = ImageDraw.Draw(image)
        draw.rectangle((60, 60, 1140, 570), outline="#1E3440", width=2)
        draw.rectangle((60, 60, 74, 570), fill="#00C8C8")
        draw.text((112, 106), article["category"]["en"].upper(), fill="#00C8C8", font=load_font(24, True))
        title_font = load_font(50, True)
        y = 168
        for line in wrap_text(draw, article["title"]["en"], title_font, 930)[:5]:
            draw.text((112, y), line, fill="#E8EDF2", font=title_font)
            y += 60
        draw.line((112, 488, 1088, 488), fill="#26323E", width=2)
        draw.text((112, 514), "LUIZ TERRA", fill="#E8EDF2", font=load_font(24, True))
        draw.text((1088, 514), "TELECOM · CX · BPO · AI", fill="#AAB6C4", font=load_font(20), anchor="ra")
        image.save(output / f"{article['slug']}.png", optimize=True)


def build_web_images() -> None:
    if not PHOTO.exists():
        return
    with Image.open(PHOTO) as source:
        image = source.convert("RGB")
        for size in (320, 520):
            resized = image.resize((size, size), Image.Resampling.LANCZOS)
            resized.save(IMAGES / f"luiz-terra-executive-{size}.webp", "WEBP", quality=84, method=6)


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
        Paragraph(f'<b>Location:</b> Sao Paulo, Brazil &nbsp;&nbsp;|&nbsp;&nbsp; <b>Contact:</b> <link href="mailto:{EMAIL}" color="#007C7C">{EMAIL}</link>', styles["small"]),
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
            Paragraph(f'<link href="{BASE_URL}" color="#007C7C">www.luizterra.com.br</link> | <link href="mailto:{EMAIL}" color="#007C7C">{EMAIL}</link>', styles["small"]),
        ]
    )
    def set_pdf_metadata(canvas, _doc) -> None:
        canvas.setTitle("Luiz Terra | International Sales Executive in Telecom, CX, BPO & AI")
        canvas.setAuthor("Luiz Terra")
        canvas.setSubject("Executive biography covering international sales, telecom, CX, BPO, CCaaS, SBC and AI.")
        canvas.setKeywords("Luiz Terra, international sales, telecom, CX, BPO, CCaaS, SBC, AI")

    doc.build(story, onFirstPage=set_pdf_metadata, onLaterPages=set_pdf_metadata)


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
- `/executive-bio/`, `/pt/executive-bio/`, `/es/executive-bio/`
- Six localized topic clusters under `/topics/`, `/pt/topics/` and `/es/topics/`

## Assets

- `public/luiz-terra-executive-bio.pdf`
- `public/og-image.png`
- Article-specific social images under `public/og/`
- `public/favicon.svg`

## Search Discovery

- Canonical and hreflang metadata for English, Brazilian Portuguese and Spanish
- ProfilePage, Person, BlogPosting, BreadcrumbList and FAQPage structured data
- `sitemap.xml` with canonical localized URLs and image discovery
- `feed.xml` for article discovery
- `llms.txt` for AI search and answer-engine context
- IndexNow key file for search-engine notifications

## Editorial Note

The repository still does not include the source text for the 12 previously prepared LinkedIn posts. The six existing Insights were preserved and expanded in place, and seven new long-form articles were added for the requested search topics without creating near-duplicate pages. If the original LinkedIn source becomes available, it should be reviewed editorially before import.

## Manual Checks

- Validate social preview with LinkedIn Post Inspector and WhatsApp after cache propagation.
- Validate structured data after deployment with Google Rich Results Test.
""",
    )


def main() -> None:
    build_web_images()
    build_pages()
    build_sitemap()
    build_discovery_files()
    build_og_image()
    build_article_og_images()
    build_pdf()
    build_readme()


if __name__ == "__main__":
    main()
