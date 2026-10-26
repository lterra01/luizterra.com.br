# Medicao da apresentacao do eBook

Inicio desta instrumentacao: 26/10/2026. Destino explicito: GA4 `G-68E95X4DZT`.
Produto: `cx-na-operacao`. Anuncio: `cx_na_operacao_launch_v1`.

## Eventos E Definicoes

| Evento | Acionamento | Unidade |
|---|---|---|
| `ebook_introduction_view` | A apresentacao foi aberta e esta visivel. | Uma exibicao |
| `ebook_offer_continue` | Clique em Conhecer o eBook dentro da apresentacao. | Uma escolha pela oferta |
| `ebook_site_continue` | Continuar no site, X, Escape ou clique no fundo externo. | Uma escolha por seguir navegando |
| `ebook_landing_click` | Link para a landing page, com `placement` identificando faixa ou apresentacao. | Clique separado; nao somar as escolhas |
| `ebook_checkout_click` | Clique para abrir o checkout da Hotmart. | Intencao de compra, nao pagamento |

Exibicao e escolhas levam `ebook_ad_id`. As escolhas tambem levam `interaction_method`: `offer_button`, `continue_button`, `close_icon`, `escape`, `backdrop` ou `other_close`.

A mesma exibicao emite no maximo uma escolha. Seguir para a oferta fecha a apresentacao, mas nao gera simultaneamente uma escolha pelo site. A navegacao tem limite de espera de 700 ms e nao depende da disponibilidade do Analytics. Cliques modificados para abrir uma nova aba preservam o comportamento do navegador.

## Indicadores

- Taxa de interesse na oferta = contagem de `ebook_offer_continue` / contagem de `ebook_introduction_view` x 100.
- Taxa de continuidade no site = contagem de `ebook_site_continue` / contagem de `ebook_introduction_view` x 100.
- Distribuicao das decisoes = contagem de cada escolha / soma das duas escolhas x 100.

Use o mesmo periodo, anuncio e filtros no numerador e denominador. Nao some `ebook_landing_click` a `ebook_offer_continue`: o clique do modal pode emitir ambos para finalidades diferentes.

As taxas por exibicao nao sao taxas de pessoas exclusivas. `sessionStorage` limita a apresentacao na sessao da aba e nao equivale a uma sessao do GA4. O relatorio de usuarios pode ter sobreposicao quando a mesma pessoa recebe mais de uma exibicao.

Nao ha evento de escolha quando a pessoa simplesmente fecha a aba ou sai da pagina sem decidir. Bloqueadores, falta de consentimento, perda de rede e atraso de processamento tambem podem reduzir a coleta. As duas taxas por exibicao nao precisam somar 100%. Nao inferir uma compra, receita ou abandono de checkout a partir destes eventos.

## Configuracao No Google Analytics

- Propriedade identificada na interface: Site Pessoal - Luiz Terra, ID `544154510`, conta `399962631`.
- Dimensoes personalizadas de escopo Evento cadastradas em 26/10/2026: `eBook Identificador do anuncio` (`ebook_ad_id`) e `eBook Metodo de interacao` (`interaction_method`).
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

## Referencias

- https://developers.google.com/analytics/devguides/collection/ga4/events
- https://developers.google.com/tag-platform/gtagjs/reference/parameters
- https://support.google.com/analytics/answer/7201382?hl=pt-BR
