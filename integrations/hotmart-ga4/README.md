# Hotmart -> GA4: compras confirmadas

## Estado

Ativado em 26/10/2026 em `DELIVERY_MODE=live`, apos validacao separada sem coletar compras ficticias.
URL: `https://luizterra-hotmart-ga4.luizterra-hotmart-ga4.workers.dev/hotmart`.
Para uma nova implantacao de teste, pausar o webhook e usar `validate` explicitamente. O arquivo Wrangler agora preserva o modo real de producao.
Coleta configurada e testes aprovados nao comprovam uma compra genuina nem receita processada no GA4.

## Contrato

- Cloudflare Workers Free + Durable Objects SQLite; nao habilitar plano pago.
- `POST /hotmart`, JSON v2.0.0, cabecalho obrigatorio `X-HOTMART-HOTTOK`.
- Produtos permitidos gerados da fonte `tools/ebook_catalog.py` em `products.json`.
- Produto ficticio do teste padrao da Hotmart e outros IDs nao cadastrados: HTTP 200 `ignored_unregistered_product`, sem persistir nem enviar ao GA4. Isso confirma transporte, nao validacao de uma venda. Novos livros exigem cadastro explicito no catalogo e no webhook.
- `PURCHASE_APPROVED` + `APPROVED`: `purchase`. Boleto/Pix pendente e cancelamentos sao ignorados.
- `PURCHASE_REFUNDED` + `REFUNDED` ou `PURCHASE_CHARGEBACK` + `CHARGEBACK`: um `refund` integral, somente apos compra registrada.
- Valor da oferta em `purchase.price`, sem juros/taxas de `full_price` e sem confundir com comissao.
- Um Durable Object por HMAC da transacao serializa tentativas. Mesmo evento, transacao e modo nao sao enviados duas vezes apos aceite.
- Timeout com resultado desconhecido fica `uncertain`, sem reenvio automatico. HTTP 202 exige revisao, nao comprova entrega.
- Eventos fora da janela de 72 horas do GA4, datas futuras e reembolsos parciais exigem revisao. Nao fazer backfill com data inventada.
- Endpoint sem CORS, corpo maximo 128 KiB, sem logs de payload, compradores, tokens ou respostas do Google.

## Privacidade E Atribuicao

Cloudflare recebe o webhook original, que pode conter dados do comprador. O receptor conserva somente transacao, produto, valor, moeda, horario e estado tecnico. Nao conserva nome, email, CPF, endereco ou dados de pagamento. Somente esse subconjunto financeiro e enviado ao Google.

`client_id` e HMAC numerico por transacao, nunca uma pessoa identificada. Nao ha associacao com sessao, origem, campanha ou usuario real do site. Restringir os relatorios de visitantes ao hostname do site para excluir identidades tecnicas do servidor. Nao usar a contagem de usuarios do relatorio financeiro como quantidade de compradores. O anuncio nao foi conectado a conversoes do Google Ads.

O ledger sanitizado permanece ate uma manutencao explicita; nao apagar antes da janela necessaria de reembolsos/reentregas, pois isso remove a protecao contra duplicatas. Acompanhar limites gratuitos no painel Cloudflare. Exceder limites pode interromper a coleta; nao ha upgrade automatico solicitado por este projeto.

## Segredos

Cadastrar como secrets da Cloudflare, nunca vars em JSON ou codigo publico:

- `HOTMART_HOTTOK`: autenticador existente da Hotmart.
- `GA4_API_SECRET`: chave exclusiva do Measurement Protocol para o fluxo `15196204898`.
- `IDENTITY_SECRET`: aleatorio criptografico persistente. Nao alterar sem plano de migracao do ledger.

`GA4_MEASUREMENT_ID=G-68E95X4DZT` e publico. `DELIVERY_MODE=validate|live` controla o destino. GET `/health` indica prontidao de bindings, nao prova de recebimento de pagamentos.

## Validacao E Deploy

```powershell
pnpm install --frozen-lockfile
pnpm test
pnpm check
pnpm exec wrangler login --device --use-keyring --scopes account:read user:read workers_scripts:write
pnpm exec wrangler deploy
pnpm exec wrangler secret put HOTMART_HOTTOK
pnpm exec wrangler secret put GA4_API_SECRET
pnpm exec wrangler secret put IDENTITY_SECRET
```

As credenciais devem ser inseridas de forma privada, nao em comandos versionados, chat ou capturas. O login oficial do Wrangler usa o cofre do sistema quando disponivel. Autorizacao de publicacao/segredos e obrigatoria antes da ativacao.

1. Implantar inicialmente em `validate` e confirmar `/health`.
   `validate-remote.mjs` testa os tres produtos e a idempotencia. Exige `WORKER_URL` HTTPS, `HOTMART_HOTTOK` privado e recusa rodar se `/health` nao confirmar `ready_validate`. Nao executar testes sinteticos diretamente no endpoint MP de coleta.
2. Configurar Hotmart v2.0.0 para estes tres produtos, apenas aprovado/reembolsado/chargeback.
3. Usar o teste da Hotmart somente enquanto o receptor estiver em `validate`; conferir `validated_not_collected` e nenhuma mensagem de validacao do GA4.
4. Desligar a configuracao de teste da Hotmart antes de mudar para `live`; nunca reenviar historico de testes para producao.
5. Alterar `DELIVERY_MODE` para `live`, publicar e conferir a configuracao final da Hotmart. Nao habilitar pixel nativo de purchase simultaneamente.
6. Aguardar uma venda genuina. Conferir recibo Hotmart, evento aprovado, transacao sem duplicata e valor por produto no GA4 processado. Nenhum teste faz uma compra real.

Para pausar: desativar a configuracao do webhook na Hotmart. Preservar ledger e segredos. Nao apagar historico do Analytics para reverter uma entrega.

## Operacao E Revisao

Na Hotmart, revisar historico de entregas e falhas. No Cloudflare, conferir saude/limites e ledger pelo painel de Durable Objects. Nunca reenviar uma compra com resultado incerto sem reconciliar `transaction_id=hotmart:<transacao>` no GA4. O aceite HTTP do GA4 nao prova processamento. Recibos dos testes nao representam faturamento.

## Referencias

- https://developers.hotmart.com/docs/en/2.0.0/webhook/purchase-webhook/
- https://developers.google.com/analytics/devguides/collection/protocol/ga4/reference
- https://developers.google.com/analytics/devguides/collection/ga4/set-up-ecommerce
- https://developers.cloudflare.com/durable-objects/platform/pricing/

## Registro De Ativacao

- Testes locais: 10 testes do receptor, 13 testes de promocao e 4 testes HTML aprovados; bundle Wrangler validado em dry-run.
- Runtime local workerd/SQLite verificado: sem segredos retorna 503; token ausente retorna 401; boleto pendente retorna 200 ignorado; aprovacao sintetica antiga passa pelo Durable Object e retorna 202 para revisao. Nenhum desses testes enviou purchase ao GA4.
- Cloudflare Free, Durable Object SQLite `TransactionLedger`; sem upgrade pago, sem mudanca no DNS do site, logs e traces desabilitados. Autenticacao Wrangler protegida pelo Windows Credential Manager; escopo especifico `workers_scripts:write`, alem de leitura da conta/usuario.
- Chave GA4 exclusiva `Luiz Terra - Hotmart webhook` criada no fluxo `15196204898`, apos confirmacao do usuario sobre privacidade. Os tres secrets da Cloudflare foram cadastrados sem valores no codigo/publicacao.
- Validacao remota dos tres produtos: `validated_not_collected` e `duplicate_ignored`, somente `/debug/mp/collect`. Nenhuma compra sintetica enviada ao endpoint de coleta.
- Teste oficial Hotmart: tres notificacoes ficticias da transacao `HP16015479281022` (aprovado, reembolsado, chargeback) retornaram `200 - Processado`. Seu produto ficticio nao pertence ao catalogo e foi ignorado; esse recibo comprova transporte, nao pagamento nem receita no Google.
- Configuracao Hotmart `Luiz Terra - eBooks GA4`: ativa, v2.0.0, somente os tres eBooks e os tres eventos financeiros. Produtos e eventos reabertos e conferidos na interface.
- Versao Cloudflare live: `c925769c-5b47-4ce1-99b0-8ef50ef15a69`, publicada a 100%. `/health`: HTTPS 200 `ready_live`; POST sem autenticacao: 401; evento nao financeiro autenticado: 200 ignorado. Nenhum teste de compra foi enviado em live.
- Compra genuina e receita no GA4 processado: ainda nao verificadas.
