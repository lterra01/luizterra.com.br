"""Private, manual eBook grants. This does not verify payments or emit GA4 events.

The ledger and invitation files must stay outside Git checkouts and web roots.
Use opaque customer references, never names, emails or payment credentials.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import secrets
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path

TITLE_IDS = {
    "cx-na-operacao", "indicadores-de-atendimento-na-pratica",
    "qualidade-e-feedback-no-atendimento",
}
DEFAULT_ROOT = Path.home() / ".codex" / "private" / "luizterra-vouchers"


def utc_now():
    return datetime.now(timezone.utc)


def digest(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def opaque_ref(value):
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_:-]{2,79}", value):
        raise ValueError("Use an opaque 3-80 character reference, without names or email addresses.")
    return value


def private_root(path):
    path = Path(path).expanduser().resolve()
    if any((parent / ".git").exists() for parent in (path, *path.parents)):
        raise ValueError("The private ledger cannot be stored inside a Git checkout.")
    if any(part.lower() in {"public", "wwwroot", "htdocs"} for part in path.parts):
        raise ValueError("The private ledger cannot be stored in a web root.")
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    return path


@contextmanager
def connect(root):
    db = sqlite3.connect(private_root(root) / "ledger.sqlite3", timeout=10)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("""CREATE TABLE IF NOT EXISTS grants (
        id TEXT PRIMARY KEY, code_hash TEXT UNIQUE NOT NULL,
        customer_hash TEXT UNIQUE NOT NULL, source TEXT NOT NULL,
        order_hash TEXT UNIQUE, issued_at TEXT NOT NULL, expires_at TEXT NOT NULL,
        redeemed_at TEXT, selected_titles TEXT,
        delivered_at TEXT, delivery_channel TEXT
    )""")
    db.commit()
    try:
        with db:
            yield db
    finally:
        db.close()


def issue(root, customer_ref, source="courtesy", order_ref=None, approved=False, now=None):
    if source not in {"courtesy", "mini-expert", "fiverr"}:
        raise ValueError("Unknown grant source.")
    customer_ref = opaque_ref(customer_ref)
    if source != "courtesy" and (not approved or not order_ref):
        raise ValueError("Manually verify approved payment and supply its opaque reference first.")
    if order_ref:
        opaque_ref(order_ref)
    now = now or utc_now()
    expires = now + timedelta(days=30)
    code = "LTCX-" + secrets.token_hex(12).upper()
    grant_id = secrets.token_hex(8)
    root = private_root(root)
    with connect(root) as db:
        try:
            db.execute("INSERT INTO grants (id, code_hash, customer_hash, source, order_hash, issued_at, expires_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (grant_id, digest(code), digest(customer_ref), source,
                        digest(source + ":" + order_ref) if order_ref else None,
                        now.isoformat(), expires.isoformat()))
        except sqlite3.IntegrityError as exc:
            raise ValueError("A grant already exists for this customer or purchase. Do not grant again for renewals.") from exc
    invitation = root / (grant_id + "-convite-privado.txt")
    # The clear code is written once to a private invitation, never to stdout or GA4.
    invitation.write_text(
        "CORTESIA PRIVADA - LUIZ TERRA\n\n"
        f"Código individual: {code}\nVálido até: {expires.isoformat()} (UTC)\n\n"
        "Escolha 2 títulos diferentes: CX na Operação; Indicadores de Atendimento na Prática; "
        "Qualidade e Feedback no Atendimento. Cada título inclui português, inglês e espanhol.\n"
        "Sem cobrança. Uso único, pessoal e interno autorizado. Sem revenda ou redistribuição.\n"
        "Escolha os títulos em https://www.luizterra.com.br/pt/bonus/ e envie a solicitação "
        "e este código somente no contato privado. A entrega é manual após conferir validade e uso. "
        "Não funciona no checkout da Hotmart.\n"
        + ("Clientes Fiverr: solicitação, código e entrega somente nas mensagens do pedido Fiverr.\n"
           if source == "fiverr" else "Contato privado: contact@luizterra.com.br.\n"),
        encoding="utf-8",
    )
    return {"grant_id": grant_id, "expires_at": expires.isoformat(), "invitation": str(invitation)}


def redeem(root, code, titles, customer_ref, now=None):
    if len(titles) != 2 or len(set(titles)) != 2 or not set(titles) <= TITLE_IDS:
        raise ValueError("Select exactly two distinct catalogue titles.")
    customer_ref = opaque_ref(customer_ref)
    code = code.strip().upper()
    if not re.fullmatch(r"LTCX-[0-9A-F]{24}", code):
        raise ValueError("Invalid voucher format.")
    now = now or utc_now()
    with connect(root) as db:
        db.execute("BEGIN IMMEDIATE")
        row = db.execute("SELECT * FROM grants WHERE code_hash = ?", (digest(code),)).fetchone()
        if row is None or row["customer_hash"] != digest(customer_ref):
            raise ValueError("Voucher and customer reference do not match.")
        if row["redeemed_at"]:
            raise ValueError("Voucher already redeemed.")
        if datetime.fromisoformat(row["expires_at"]) <= now:
            raise ValueError("Voucher expired.")
        db.execute("UPDATE grants SET redeemed_at = ?, selected_titles = ? WHERE id = ? AND redeemed_at IS NULL",
                   (now.isoformat(), json.dumps(sorted(titles)), row["id"]))
    return {"grant_id": row["id"], "status": "reserved_pending_manual_delivery", "titles": sorted(titles)}


def confirm_delivery(root, grant_id, channel, now=None):
    now = now or utc_now()
    with connect(root) as db:
        db.execute("BEGIN IMMEDIATE")
        row = db.execute("SELECT * FROM grants WHERE id = ?", (grant_id,)).fetchone()
        if row is None or not row["redeemed_at"]:
            raise ValueError("Reserve the selected titles before confirming delivery.")
        if row["delivered_at"]:
            raise ValueError("Delivery was already confirmed.")
        expected = "fiverr-order" if row["source"] == "fiverr" else "private-email"
        if channel != expected:
            raise ValueError(f"Required delivery channel: {expected}.")
        db.execute("UPDATE grants SET delivered_at = ?, delivery_channel = ? WHERE id = ?",
                   (now.isoformat(), channel, grant_id))
    return {"grant_id": grant_id, "status": "delivery_manually_confirmed", "channel": channel}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    commands = parser.add_subparsers(dest="command", required=True)
    new = commands.add_parser("issue")
    new.add_argument("--customer-ref", required=True)
    new.add_argument("--source", choices=("courtesy", "mini-expert", "fiverr"), default="courtesy")
    new.add_argument("--order-ref")
    new.add_argument("--confirmed-approved", action="store_true")
    use = commands.add_parser("redeem")
    use.add_argument("--customer-ref", required=True)
    use.add_argument("--code-file", type=Path, required=True,
                     help="Private text file containing only the code; do not pass a code in shell history.")
    use.add_argument("--titles", nargs=2, required=True, choices=sorted(TITLE_IDS))
    delivered = commands.add_parser("delivered")
    delivered.add_argument("--grant-id", required=True)
    delivered.add_argument("--channel", choices=("fiverr-order", "private-email"), required=True)
    args = parser.parse_args()
    try:
        if args.command == "issue":
            result = issue(args.root, args.customer_ref, args.source, args.order_ref, args.confirmed_approved)
        elif args.command == "redeem":
            result = redeem(args.root, args.code_file.read_text(encoding="utf-8").strip(), args.titles, args.customer_ref)
        else:
            result = confirm_delivery(args.root, args.grant_id, args.channel)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
