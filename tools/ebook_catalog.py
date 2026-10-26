"""Public catalogue facts verified against the released Hotmart offers."""

from ebook_content import EBOOK

COLLECTION_PATH = "ebooks/"
COLLECTION_ID = "cx-na-pratica"

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
        "cover": "/public/ebooks/indicadores-de-atendimento-na-pratica.webp", "modified": "2026-10-26",
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
        "cover": "/public/ebooks/qualidade-e-feedback-no-atendimento.webp", "modified": "2026-10-26",
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

COLLECTION_COPY = {
    "pt": {
        "title": "CX na Prática: 3 eBooks de Luiz Terra | R$ 9,99 cada",
        "description": "Conheça os três eBooks de Luiz Terra sobre rotinas, indicadores, qualidade e feedback no atendimento. PDFs em português, R$ 9,99 cada, pela Hotmart.",
        "intro": "Três guias para quem supervisiona ou coordena o atendimento. Escolha o tema que sua operação precisa trabalhar agora.",
        "label": "EBOOKS DE LUIZ TERRA", "language": "Conteúdo em português · PDF · edição 1.0",
        "volume": "Volume", "pages": "páginas", "worksheets": "fichas de trabalho", "buy": "Comprar na Hotmart",
        "details": "O que você encontra", "each": "cada · pagamento único", "collection": "Conhecer a coleção",
        "related": "Continue a coleção", "related_text": "Aprofunde a medição dos resultados e o desenvolvimento da equipe com os outros dois volumes.",
        "note": "Cada eBook é vendido separadamente. Pagamento e acesso pela Hotmart. Prazo de reembolso de 7 dias, conforme as condições da oferta.",
        "modal_title": "CX na Prática", "modal_text": "Rotinas, indicadores e qualidade: três eBooks para apoiar decisões no atendimento.",
        "bar": "CX na Prática · 3 eBooks de Luiz Terra", "close": "Fechar apresentação dos eBooks", "continue": "Continuar no site",
    },
    "en": {
        "title": "CX na Prática: 3 eBooks by Luiz Terra | R$ 9.99 each",
        "description": "Explore Luiz Terra's three Portuguese-language eBooks on customer service routines, metrics, quality and feedback. PDF editions sold individually on Hotmart.",
        "intro": "Three guides for customer service supervisors and coordinators. Choose the topic your operation needs to work on next.",
        "label": "EBOOKS BY LUIZ TERRA", "language": "Portuguese-language content · PDF · edition 1.0",
        "volume": "Volume", "pages": "pages", "worksheets": "worksheets", "buy": "Buy on Hotmart",
        "details": "Inside this eBook", "each": "each · one-time payment", "collection": "Explore the collection",
        "related": "Continue the collection", "related_text": "Explore service measurement and team development in the other two volumes.",
        "note": "Each eBook is sold separately. Payment and access through Hotmart. A 7-day refund period applies under the offer terms. All three books are in Portuguese.",
        "modal_title": "CX na Prática", "modal_text": "Routines, metrics and quality: three Portuguese-language eBooks to support customer service decisions.",
        "bar": "CX na Prática · 3 eBooks by Luiz Terra", "close": "Close the eBook introduction", "continue": "Continue to the site",
    },
    "es": {
        "title": "CX na Prática: 3 eBooks de Luiz Terra | R$ 9,99 cada uno",
        "description": "Conozca los tres eBooks de Luiz Terra sobre rutinas, indicadores, calidad y feedback en atención al cliente. PDFs en portugués, vendidos por separado en Hotmart.",
        "intro": "Tres guías para supervisores y coordinadores de atención. Elija el tema que su operación necesita trabajar ahora.",
        "label": "EBOOKS DE LUIZ TERRA", "language": "Contenido en portugués · PDF · edición 1.0",
        "volume": "Volumen", "pages": "páginas", "worksheets": "fichas de trabajo", "buy": "Comprar en Hotmart",
        "details": "Dentro del eBook", "each": "cada uno · pago único", "collection": "Conocer la colección",
        "related": "Continúe la colección", "related_text": "Profundice en la medición de resultados y el desarrollo del equipo con los otros dos volúmenes.",
        "note": "Cada eBook se vende por separado. Pago y acceso a través de Hotmart. Plazo de reembolso de 7 días, según las condiciones de la oferta. Los tres libros están en portugués.",
        "modal_title": "CX na Prática", "modal_text": "Rutinas, indicadores y calidad: tres eBooks en portugués para apoyar decisiones en la atención.",
        "bar": "CX na Prática · 3 eBooks de Luiz Terra", "close": "Cerrar presentación de los eBooks", "continue": "Continuar al sitio",
    },
}
