# eBook bonus and private courtesy vouchers

## Commercial rules

- Released catalogue: CX na Operacao (8811187), Indicadores de Atendimento na Pratica (8811999), Qualidade e Feedback no Atendimento (8812046), IA no Atendimento: do Piloto a Operacao (8836219), Voz e Telecom para CX (8836306), Vendas Consultivas em Telecom e CX (8836331).
- Each existing Hotmart product includes its Portuguese, English and Spanish PDFs at the unchanged R$ 9.99 price. The six translated PDFs were added and the three-file lists reopened on 29 October 2026.
- The three additional titles also include PT/EN/ES at R$ 9.99 each. Their cover-only replacements were saved and the lists reopened before release approval on 29 October 2026. Bonus recipients may choose two distinct titles from all six, not the entire catalogue.
- An approved first AI Agent purchase or paid Fiverr consulting order grants any two different titles, once per customer across both services. Renewals and further orders do not grant another bonus.
- Verify eligibility manually in the relevant platform before issuing a purchase grant. A browser click, prepared message, GA4 event or generated payment is not payment approval.
- Hotmart does not support a 100% checkout coupon. Courtesy vouchers are private invitations, valid for 30 days, individual and single-use. They are not Hotmart discounts and must never be entered into checkout.
- Fiverr order, payment, messages and delivery remain on Fiverr. Do not ask Fiverr customers to email, pay elsewhere, or use an off-platform redemption channel.
- Delivery is manual and has no extra charge. Do not send the entire catalogue when the grant covers two. Each chosen title includes all three language editions.

Official coupon guidance: https://suportehotmart.zendesk.com/hc/pt-br/articles/360015325411-Como-criar-cupons-de-desconto-para-o-meu-produto

## Private files

Paid manuscripts and packs are outside this public repository. The private international edition release folder contains `pdf/`, `delivery/`, `manifest.json`, sources and upload evidence. Never copy them into `public/`, Git, a public Drive share or an Analytics payload.

The default voucher storage is `%USERPROFILE%\.codex\private\luizterra-vouchers`. The SQLite ledger stores code, customer and purchase hashes, grant dates, the two title IDs, redemption reservation and delivery confirmation. Clear codes exist only in the private invitation. Keep this directory in a restricted private backup. The CLI refuses storage within a Git checkout or common web root.

Use a stable opaque customer reference maintained privately. The same person must keep the same reference across Hotmart and Fiverr; otherwise the manual one-per-customer check cannot work. The reference is not an email or a name. The CLI does not identify customers or verify payments itself.

## Issue an invitation

From the repository root, use the configured Python runtime:

```powershell
python tools/voucher_registry.py issue --customer-ref prospect-001 --source courtesy
```

The command prints only a grant ID, expiry and private invitation path, not the clear code. Assign that reference to one selected recipient in the private operating record before sending the invitation. Expiry is exactly 30 days from issue (UTC).

For a bonus, first verify the purchase status, identity and prior grant manually. Use an opaque private order reference and explicitly attest that you checked approved payment:

```powershell
python tools/voucher_registry.py issue --customer-ref customer-001 --source mini-expert --order-ref hotmart-order-001 --confirmed-approved
python tools/voucher_registry.py issue --customer-ref customer-002 --source fiverr --order-ref fiverr-order-001 --confirmed-approved
```

These are independent command examples, not real customers or receipts. Never run both for the same person. For Fiverr, keep the invitation and selection inside the paid order's messages.

## Reserve and deliver

1. Receive the choice of exactly two distinct catalogue titles. On the website, preparing a message does not send it, reserve a voucher or approve a request.
2. Check the original grant and customer reference. Put only the received code in a private text file; do not pass clear codes as command arguments or commit them.
3. Reserve the selection atomically:

```powershell
python tools/voucher_registry.py redeem --customer-ref customer-001 --code-file C:\private-redemption\received-code.txt --titles cx-na-operacao qualidade-e-feedback-no-atendimento
```

4. Attach the two chosen trilingual packs through the authorised private channel. If delivery fails, resume the same reserved grant, not a new redemption or a new code. A reservation is not a delivery receipt.
5. Only after successful delivery, record its actual channel:

```powershell
python tools/voucher_registry.py delivered --grant-id GRANT_ID_FROM_ISSUE --channel private-email
```

Use `--channel fiverr-order` for a Fiverr grant; the CLI refuses off-platform email delivery for that source. Do not confirm delivery before sending and checking the attachments. A repeated delivery-confirmation command is rejected.

## Measurement boundaries

- Existing `ebook_*` and `mini_expert_*` events retain their identities.
- `fiverr_landing_view`, `fiverr_product_view`, `fiverr_landing_click` and `fiverr_offer_click` measure interest, never a paid Fiverr order.
- `bonus_landing_view`, `bonus_landing_click`, `bonus_request_prepare` and `bonus_contact_click` measure intent only. They contain no voucher, customer reference, order ID, email, transaction, revenue or message body.
- Courtesy delivery never emits `purchase` and never creates artificial revenue. This change does not connect Fiverr payments or AI Agent renewals to GA4.
- The financial receiver uses only the released eBook catalogue. New titles require their own release verification and a coordinated allowlist/webhook deployment; the bonus alone does not broaden collection. Never resend financial events for a promotion.

## Prepared Additions

The 29 October volumes on AI operations, voice/telecom and consultative selling are held as drafts in `tools/ebook_launches.py`. Follow `docs/EBOOK_LAUNCH_2026-10-29.md` before making them redeemable. Existing invitations and private ledger entries are preserved; do not issue replacement grants or reset their validity merely because the catalogue expands.
