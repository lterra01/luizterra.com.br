"""Verified additions; unreleased drafts never become public offers."""

import re


RELEASE_CHECKS = (
    "author_release_approved", "hotmart_terms_accepted", "delivery_read_back",
    "sales_active", "checkout_verified",
)

NEW_EBOOKS = [
    {
        "id": "ia-no-atendimento-do-piloto-a-operacao", "hotmart_id": "8836219",
        "name": "IA no Atendimento: do Piloto à Operação", "volume": 4,
        "titles": {"pt": "IA no Atendimento: do Piloto à Operação", "en": "AI in Customer Service: From Pilot to Operations", "es": "IA en la Atención: del Piloto a la Operación"},
        "pages": 25, "worksheets": 4, "modified": "2026-10-29",
        "price": "9.99", "price_label": "R$ 9,99", "checkout": "https://pay.hotmart.com/P108249096W",
        "cover": "/public/ebooks/ia-no-atendimento-do-piloto-a-operacao.webp",
        "release_state": "released", "checks": {name: True for name in RELEASE_CHECKS},
        "summary": {
            "pt": "Defina escopo, fontes e permissões; avalie respostas e organize a transferência humana antes de ampliar um piloto de IA.",
            "en": "Define scope, sources and permissions; evaluate answers and organise human handover before expanding an AI pilot.",
            "es": "Defina alcance, fuentes y permisos; evalúe respuestas y organice la derivación humana antes de ampliar un piloto de IA.",
        },
        "topics": {
            "pt": ["Conhecimento, ferramentas e supervisão", "Caso simulado com 200 solicitações", "Quatro fichas de avaliação e continuidade"],
            "en": ["Knowledge, tools and supervision", "Simulated case with 200 requests", "Four evaluation and continuity worksheets"],
            "es": ["Conocimiento, herramientas y supervisión", "Caso simulado con 200 solicitudes", "Cuatro fichas de evaluación y continuidad"],
        },
    },
    {
        "id": "voz-e-telecom-para-cx", "hotmart_id": "8836306",
        "name": "Voz e Telecom para CX", "volume": 5,
        "titles": {"pt": "Voz e Telecom para CX", "en": "Voice and Telecom for CX", "es": "Voz y Telecom para CX"},
        "pages": 25, "worksheets": 4, "modified": "2026-10-29",
        "price": "9.99", "price_label": "R$ 9,99", "checkout": "https://pay.hotmart.com/A108249258G",
        "cover": "/public/ebooks/voz-e-telecom-para-cx.webp",
        "release_state": "released", "checks": {name: True for name in RELEASE_CHECKS},
        "summary": {
            "pt": "Conecte atendimento, Telecom e fornecedores com evidências de qualidade de voz, incidentes e continuidade do serviço.",
            "en": "Connect service teams, telecom and suppliers through evidence of voice quality, incidents and service continuity.",
            "es": "Conecte atención, Telecom y proveedores mediante evidencias de calidad de voz, incidencias y continuidad del servicio.",
        },
        "topics": {
            "pt": ["Sinalização, áudio e jornada de atendimento", "Disponibilidade sem contar eventos sobrepostos duas vezes", "Quatro fichas de incidente e continuidade"],
            "en": ["Signalling, audio and the service journey", "Availability without double-counting overlapping events", "Four incident and continuity worksheets"],
            "es": ["Señalización, audio y recorrido de atención", "Disponibilidad sin duplicar intervalos superpuestos", "Cuatro fichas de incidencias y continuidad"],
        },
    },
    {
        "id": "vendas-consultivas-em-telecom-e-cx", "hotmart_id": "8836331",
        "name": "Vendas Consultivas em Telecom e CX", "volume": 6,
        "titles": {"pt": "Vendas Consultivas em Telecom e CX", "en": "Consultative Selling in Telecom and CX", "es": "Ventas Consultivas en Telecom y CX"},
        "pages": 25, "worksheets": 4, "modified": "2026-10-29",
        "price": "9.99", "price_label": "R$ 9,99", "checkout": "https://pay.hotmart.com/F108249305B",
        "cover": "/public/ebooks/vendas-consultivas-em-telecom-e-cx.webp",
        "release_state": "released", "checks": {name: True for name in RELEASE_CHECKS},
        "summary": {
            "pt": "Estruture descoberta, responsabilidades de parceiros, pilotos e propostas, separando intenção comercial de resultado confirmado.",
            "en": "Structure discovery, partner responsibilities, pilots and proposals, separating commercial intent from confirmed outcomes.",
            "es": "Estructure descubrimiento, responsabilidades de socios, pilotos y propuestas, separando intención y resultado confirmado.",
        },
        "topics": {
            "pt": ["Descoberta e hipótese de valor", "Parceiros e expansão internacional", "Caso simulado de funil e quatro fichas"],
            "en": ["Discovery and value hypotheses", "Partners and international expansion", "Simulated funnel case and four worksheets"],
            "es": ["Descubrimiento e hipótesis de valor", "Socios y expansión internacional", "Caso simulado de embudo y cuatro fichas"],
        },
    },
]


def released_additions(candidates=None):
    """Fail closed if a candidate claims release without every required receipt."""
    released = []
    for book in NEW_EBOOKS if candidates is None else candidates:
        if book["release_state"] not in {"prepared", "draft", "released"}:
            raise ValueError(f"Unknown release state: {book['id']}")
        if book["release_state"] != "released":
            continue
        if not all(book["checks"].get(name) is True for name in RELEASE_CHECKS):
            raise ValueError(f"Unverified eBook release: {book['id']}")
        if not re.fullmatch(r"[0-9]+", book.get("hotmart_id") or ""):
            raise ValueError(f"Missing verified Hotmart ID: {book['id']}")
        if not re.fullmatch(r"https://pay\.hotmart\.com/[A-Z][0-9]+[A-Z]", book.get("checkout") or ""):
            raise ValueError(f"Missing verified checkout: {book['id']}")
        released.append({key: value for key, value in book.items() if key not in {"release_state", "checks"}})
    return released
