"""Public catalogue facts verified against the released Hotmart offers."""

import hashlib

from ebook_content import EBOOK
from ebook_launches import released_additions

COLLECTION_PATH = "ebooks/"
COLLECTION_ID = "cx-na-pratica"
DELIVERY_LANGUAGES = ["pt-BR", "en", "es"]

BOOK_TITLES = {
    "cx-na-operacao": {"pt": "CX na Operação", "en": "CX in Operations", "es": "CX en la Operación"},
    "indicadores-de-atendimento-na-pratica": {"pt": "Indicadores de Atendimento na Prática", "en": "Customer Service Metrics in Practice", "es": "Indicadores de Atención al Cliente en la Práctica"},
    "qualidade-e-feedback-no-atendimento": {"pt": "Qualidade e Feedback no Atendimento", "en": "Customer Service Quality and Feedback", "es": "Calidad y Feedback en la Atención al Cliente"},
}

EBOOKS = [
    {
        **EBOOK, "hotmart_id": "8811187", "volume": 1, "pages": 27, "worksheets": 4,
        "summary": {
            "pt": "Sete rotinas para organizar o atendimento, preservar o contexto e acompanhar o próximo passo de cada caso.",
            "en": "Seven routines to organise customer service, preserve context and follow up on the next step in each case.",
            "es": "Siete rutinas para organizar la atención, preservar el contexto y dar seguimiento al próximo paso de cada caso.",
        },
        "topics": {
            "pt": ["Motivo do contato e reincidência", "Passagem de casos e falhas de voz", "Responsáveis, prazos e acompanhamento"],
            "en": ["Contact reasons and repeat contacts", "Case handoffs and voice failures", "Ownership, deadlines and follow-up"],
            "es": ["Motivo del contacto y reincidencia", "Transferencia de casos y fallas de voz", "Responsables, plazos y seguimiento"],
        },
    },
    {
        "id": "indicadores-de-atendimento-na-pratica", "hotmart_id": "8811999", "volume": 2,
        "name": "Indicadores de Atendimento na Prática", "pages": 25, "worksheets": 3,
        "checkout": "https://pay.hotmart.com/I108198534I", "price": "9.99", "price_label": "R$ 9,99",
        "cover": "/public/ebooks/indicadores-de-atendimento-na-pratica.webp", "modified": "2026-10-29",
        "summary": {
            "pt": "Defina bases de medição, confira os dados e interprete indicadores antes de decidir o que mudar na operação.",
            "en": "Define measurement baselines, check the data and interpret service metrics before deciding what to change.",
            "es": "Defina bases de medición, verifique los datos e interprete indicadores antes de decidir qué cambiar en la operación.",
        },
        "topics": {
            "pt": ["TMA, abandono e nível de serviço", "Backlog, CSAT e resolução no primeiro contato", "Caso simulado com cálculos abertos"],
            "en": ["Handling time, abandonment and service level", "Backlog, CSAT and first-contact resolution", "Simulated case with transparent calculations"],
            "es": ["TMO, abandono y nivel de servicio", "Backlog, CSAT y resolución en el primer contacto", "Caso simulado con cálculos abiertos"],
        },
    },
    {
        "id": "qualidade-e-feedback-no-atendimento", "hotmart_id": "8812046", "volume": 3,
        "name": "Qualidade e Feedback no Atendimento", "pages": 25, "worksheets": 4,
        "checkout": "https://pay.hotmart.com/O108198605F", "price": "9.99", "price_label": "R$ 9,99",
        "cover": "/public/ebooks/qualidade-e-feedback-no-atendimento.webp", "modified": "2026-10-29",
        "summary": {
            "pt": "Avalie atendimentos com critérios observáveis e transforme os achados em feedback e desenvolvimento da equipe.",
            "en": "Evaluate service interactions using observable criteria and turn findings into feedback and team development.",
            "es": "Evalúe la atención con criterios observables y transforme los hallazgos en feedback y desarrollo del equipo.",
        },
        "topics": {
            "pt": ["Critérios, pontuação e itens não aplicáveis", "Calibração entre avaliadores", "Feedback, microtreinos e acompanhamento"],
            "en": ["Criteria, scoring and not-applicable items", "Calibration between evaluators", "Feedback, micro-training and follow-up"],
            "es": ["Criterios, puntuación e ítems no aplicables", "Calibración entre evaluadores", "Feedback, microentrenamientos y seguimiento"],
        },
    },
]

ADDITIONS = released_additions()
for addition in ADDITIONS:
    BOOK_TITLES[addition["id"]] = addition["titles"]
    EBOOKS.append({key: value for key, value in addition.items() if key != "titles"})

CATALOG_REVISION = hashlib.sha256("\n".join(book["id"] for book in EBOOKS).encode("utf-8")).hexdigest()[:12]
COLLECTION_AD_ID = f"cx_na_pratica_collection_{CATALOG_REVISION}" if ADDITIONS else "cx_na_pratica_collection_v1"
COLLECTION_SESSION_KEY = f"luiz-terra-ebook-collection-{CATALOG_REVISION}-introduced" if ADDITIONS else "luiz-terra-ebook-collection-v1-introduced"

COLLECTION_COPY = {
    "pt": {
        "title": "CX na Prática: eBooks, AI Agent e Consultoria | Luiz Terra",
        "description": "eBooks de CX em português, inglês e espanhol por R$ 9,99 cada. Conheça o AI Agent e a consultoria de Luiz Terra na Fiverr, com dois eBooks de bônus.",
        "intro": "Três formas de trabalhar os desafios do atendimento: guias práticos, um assistente de IA e uma análise consultiva revisada por Luiz Terra.",
        "label": "EBOOKS · AI AGENT · CONSULTORIA", "language": "Cada eBook inclui português, inglês e espanhol · PDFs completos · edição 1.0",
        "volume": "Volume", "pages": "páginas", "worksheets": "fichas de trabalho", "buy": "Comprar na Hotmart",
        "details": "O que você encontra", "each": "cada · pagamento único", "collection": "Conhecer a coleção",
        "related": "Continue a coleção", "related_text": "Explore os demais volumes para conectar atendimento, medição e decisões da operação.",
        "note": "Cada título é vendido separadamente por R$ 9,99 e inclui os três idiomas. Pagamento e acesso pela Hotmart. Reembolso em 7 dias, conforme as condições da oferta. AI Agent e consultoria são serviços independentes.",
        "modal_title": "CX na Prática", "modal_text": "eBooks em três idiomas, AI Agent e consultoria. Ao contratar um dos serviços, escolha dois eBooks de bônus.",
        "bar": f"CX na Prática · {len(EBOOKS)} eBooks de Luiz Terra", "close": "Fechar apresentação dos eBooks", "continue": "Continuar no site",
    },
    "en": {
        "title": "CX in Practice: eBooks, AI Agent and Consulting | Luiz Terra",
        "description": "Customer service eBooks in English, Spanish and Portuguese at R$ 9.99 per title. Explore Luiz Terra's AI Agent and Fiverr consulting with two bonus eBooks.",
        "intro": "Three ways to work on customer service challenges: practical guides, an AI assistant and a consulting analysis reviewed by Luiz Terra.",
        "label": "EBOOKS · AI AGENT · CONSULTING", "language": "Every eBook includes English, Spanish and Portuguese · complete PDFs · edition 1.0",
        "volume": "Volume", "pages": "pages", "worksheets": "worksheets", "buy": "Buy on Hotmart",
        "details": "Inside this eBook", "each": "each · one-time payment", "collection": "Explore the collection",
        "related": "Continue the collection", "related_text": "Explore the other volumes to connect customer service, measurement and operating decisions.",
        "note": "Each title is sold separately at R$ 9.99 and includes all three languages. Payment and access through Hotmart. A 7-day refund period applies under the offer terms. AI Agent and consulting are separate services.",
        "modal_title": "CX in Practice", "modal_text": "eBooks in three languages, an AI Agent and consulting. Buy either service and choose two bonus eBooks.",
        "bar": f"CX na Prática · {len(EBOOKS)} eBooks by Luiz Terra", "close": "Close the eBook introduction", "continue": "Continue to the site",
    },
    "es": {
        "title": "CX en la Práctica: eBooks, AI Agent y Consultoría | Luiz Terra",
        "description": "eBooks de atención en español, inglés y portugués por R$ 9,99 cada título. Conozca el AI Agent y la consultoría de Luiz Terra en Fiverr, con dos eBooks de regalo.",
        "intro": "Tres formas de trabajar los retos de atención: guías prácticas, un asistente de IA y un análisis consultivo revisado por Luiz Terra.",
        "label": "EBOOKS · AI AGENT · CONSULTORÍA", "language": "Cada eBook incluye español, inglés y portugués · PDFs completos · edición 1.0",
        "volume": "Volumen", "pages": "páginas", "worksheets": "fichas de trabajo", "buy": "Comprar en Hotmart",
        "details": "Dentro del eBook", "each": "cada uno · pago único", "collection": "Conocer la colección",
        "related": "Continúe la colección", "related_text": "Explore los demás volúmenes para conectar atención, medición y decisiones operativas.",
        "note": "Cada título se vende por separado por R$ 9,99 e incluye los tres idiomas. Pago y acceso por Hotmart. Reembolso en 7 días, según la oferta. AI Agent y consultoría son servicios independientes.",
        "modal_title": "CX en la Práctica", "modal_text": "eBooks en tres idiomas, AI Agent y consultoría. Contrate cualquiera de los servicios y elija dos eBooks de regalo.",
        "bar": f"CX na Prática · {len(EBOOKS)} eBooks de Luiz Terra", "close": "Cerrar presentación de los eBooks", "continue": "Continuar al sitio",
    },
}
