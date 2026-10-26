# Medicao da apresentacao do eBook

Inicio desta instrumentacao: 26/10/2026. Destino explicito: GA4 `G-68E95X4DZT`.
Campanha inicial: `cx_na_operacao_launch_v1`. Atualizacao multiproduto: colecao `cx-na-pratica`, anuncio `cx_na_pratica_collection_v1`.
Fonte canonica: `tools/ebook_catalog.py`, com os tres IDs Hotmart, precos e URLs verificados em 26/10/2026.

## Eventos E Definicoes

| Evento | Acionamento | Unidade |
|---|---|---|
| `ebook_introduction_view` | A apresentacao foi aberta e esta visivel. | Uma exibicao |
| `ebook_offer_continue` | Clique para conhecer a colecao ou um dos produtos na apresentacao. | Uma escolha pela oferta |
| `ebook_site_continue` | Continuar no site, X, Escape ou clique no fundo externo. | Uma escolha por seguir navegando |
| `ebook_landing_view` | A pagina de oferta do eBook foi carregada. | Uma visualizacao da oferta, incluindo recargas |
| `ebook_landing_click` | Link para a landing page, com `placement` identificando faixa ou apresentacao. | Clique separado; nao somar as escolhas |
| `ebook_checkout_click` | Clique para abrir o checkout da Hotmart. | Intencao de compra, nao pagamento |
| `ebook_catalog_view` | A pagina da colecao foi carregada. | Uma visualizacao da colecao |
| `ebook_product_view` | Pelo menos metade do card do produto ficou visivel. | Uma exposicao por card e carregamento |

Exibicao e escolhas levam `ebook_ad_id`. As escolhas tambem levam `interaction_method`: `offer_button`, `continue_button`, `close_icon`, `escape`, `backdrop` ou `other_close`.

Interacoes com um produto levam `ebook_id`, `ebook_title` e, quando disponivel, `hotmart_product_id`. Exibicao/fechamento da apresentacao multiproduto e visita ao catalogo levam `ebook_collection_id`, sem atribuir a colecao inteira a um livro. Os proximos eBooks devem reutilizar os nomes de eventos e informar seus proprios IDs. O relatorio inclui o prefixo `ebook_`, nao um produto fixo. O observador mede exposicao do card, nao leitura ou compra. Sem IntersectionObserver nao se inventa uma exposicao.

A mesma exibicao emite no maximo uma escolha. Seguir para a oferta fecha a apresentacao, mas nao gera simultaneamente uma escolha pelo site. A navegacao tem limite de espera de 700 ms e nao depende da disponibilidade do Analytics. Cliques modificados para abrir uma nova aba preservam o comportamento do navegador.

## Indicadores

- Taxa de interesse na oferta = contagem de `ebook_offer_continue` / contagem de `ebook_introduction_view` x 100.
- Taxa de continuidade no site = contagem de `ebook_site_continue` / contagem de `ebook_introduction_view` x 100.
- Distribuicao das decisoes = contagem de cada escolha / soma das duas escolhas x 100.

Use o mesmo periodo, anuncio e filtros no numerador e denominador. Nao some `ebook_landing_click` a `ebook_offer_continue`: o clique do modal pode emitir ambos para finalidades diferentes.
As taxas da apresentacao multiproduto sao da colecao/campanha. Nao dividir escolhas de um livro por exposicoes inexistentes daquele livro no modal. Para comparar interesse por produto, consultar exposicoes `ebook_product_view` e cliques `ebook_checkout_click`, com o mesmo produto e `placement`; nao tratar a divisao como conversao paga atribuida.

As taxas por exibicao nao sao taxas de pessoas exclusivas. `sessionStorage` limita a apresentacao na sessao da aba e nao equivale a uma sessao do GA4. O relatorio de usuarios pode ter sobreposicao quando a mesma pessoa recebe mais de uma exibicao.

Nao ha evento de escolha quando a pessoa simplesmente fecha a aba ou sai da pagina sem decidir. Bloqueadores, falta de consentimento, perda de rede e atraso de processamento tambem podem reduzir a coleta. As duas taxas por exibicao nao precisam somar 100%. Nao inferir uma compra, receita ou abandono de checkout a partir destes eventos.

## Configuracao No Google Analytics

- Propriedade identificada na interface: Site Pessoal - Luiz Terra, ID `544154510`, conta `399962631`.
- Dimensoes personalizadas de escopo Evento cadastradas em 26/10/2026: `eBook Identificador do anuncio` (`ebook_ad_id`) e `eBook Metodo de interacao` (`interaction_method`).
- Dimensoes adicionadas para os relatorios multiproduto: `eBook ID do produto` (`ebook_id`), `eBook Titulo` (`ebook_title`) e `eBook Posicao do CTA` (`placement`).
- No relatorio de Eventos, comparar os tres eventos da apresentacao. Para a decomposicao, usar as dimensoes do anuncio e do metodo de interacao.
- Nao marcar a escolha por continuar no site como evento principal. Esta entrega nao cria conversoes de compra nem altera conversoes do Google Ads.
- A coleta nao e retroativa. As escolhas de fechamento nao eram medidas antes desta alteracao.

## Validacao

1. Executar `node --test tools/test_ebook_promotion.js` e os testes Python do eBook.
2. Publicar e confirmar o JavaScript no dominio real.
3. Ativar depuracao somente no navegador de teste via Google Tag Assistant.
4. Fazer uma exibicao e uma escolha por vez; verificar nome, anuncio e metodo no DebugView da propriedade correta.
5. Conferir os relatorios processados posteriormente. DebugView e recebimento em tempo real nao comprovam consolidacao historica nem engajamento de clientes reais.

### Resultado Da Validacao Em 26/10/2026

- Codigo publicado no commit `1d9c755`; workflow do GitHub Pages `40370150695` concluido com sucesso. JavaScript e pagina PT retornaram HTTP 200 com os novos eventos e atributos.
- Nove testes JavaScript e tres testes Python aprovados.
- Fluxo Web `15196204898` confirmado na interface com ID `G-68E95X4DZT`.
- Tag Assistant e DebugView confirmaram `ebook_introduction_view`, `ebook_offer_continue` e `ebook_site_continue` na propriedade `544154510`.
- Parametros recebidos conferidos no DebugView: `ebook_ad_id=cx_na_operacao_launch_v1`; `interaction_method=offer_button` e `interaction_method=continue_button` nas respectivas escolhas.
- Os acessos de validacao usaram URLs com `qa=ebook-...-20261026` e depuracao restrita ao navegador de teste. Os numeros do DebugView incluem QA, nao representam alcance ou interesse comercial de visitantes. Para analise de desempenho, excluir trafego de teste e usar relatorios processados com filtros consistentes.
- A navegacao para a landing page e a continuidade na pagina principal foram verificadas no dominio publico. Fechamentos alternativos e prevencao de duplicidade foram cobertos pelos testes locais.
- Relatorios historicos processados e vendas nao foram validados nesta entrega.

## Relatorios De Acompanhamento

Os tres relatorios nativos do GA4 e suas definicoes estao documentados em `docs/GA4_REPORTS.md`. Novas dimensoes nao preenchem dados anteriores. Permitir o processamento do Google antes de avaliar a ausencia de linhas; nao tratar uma tabela vazia no periodo anterior ao lancamento como falha ou resultado comercial zero.

## Compras Confirmadas E Receita

O receptor em `integrations/hotmart-ga4/` e separado dos eventos do navegador. Aceita apenas notificacoes Hotmart autenticadas para os produtos cadastrados. `PURCHASE_APPROVED` com status `APPROVED` gera `purchase`; gerar boleto/Pix ou chegar a uma pagina de obrigado nao basta. Reembolso integral e chargeback geram um unico `refund` da compra conhecida. Reembolso parcial e eventos antigos precisam de revisao.

O valor enviado e `purchase.price.value` na moeda da oferta: nao e a comissao do produtor, nem inclui juros/taxas de `full_price`. Nao fixar R$ 9,99 no servidor: descontos devem aparecer pelo valor efetivo da notificacao. O relatorio financeiro mede os produtos vendidos, nao o saldo liquido a receber da Hotmart.

Dados do comprador sao descartados antes de persistir ou enviar ao Google. O identificador tecnico HMAC e por transacao, nao por pessoa. Nao associa a venda a uma sessao real do site, canal, anuncio ou clique. Eventos do servidor podem criar identidades tecnicas no total geral da propriedade; relatorios especificos de visitas ao site devem restringir ao hostname proprio. Nao anunciar um funil atribuido ou ROAS sem uma futura integracao consentida de client_id/session_id.

Modo `validate` usa somente `/debug/mp/collect`, sem registrar vendas no GA4. Modo `live` envia eventos financeiros reais. Nunca enviar notificacao sintetica de teste para o endpoint de coleta em producao. Autenticacao HTTP, validacao do payload, aceite do GA4 e compra processada no relatorio sao provas diferentes. O estado operacional atualizado fica no README da integracao.

## Referencias

- https://developers.google.com/analytics/devguides/collection/ga4/events
- https://developers.google.com/tag-platform/gtagjs/reference/parameters
- https://support.google.com/analytics/answer/7201382?hl=pt-BR
