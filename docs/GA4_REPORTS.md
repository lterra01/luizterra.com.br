# Relatorios Nativos Do Google Analytics

Criados em 26/10/2026 na propriedade `Site Pessoal - Luiz Terra` (`544154510`), conta `399962631`, fluxo Web `15196204898`, medicao `G-68E95X4DZT`.

Acesso autenticado: Google Analytics > Relatorios > Luiz Terra - Performance > Acompanhamento. A colecao `16208104030` contem os quatro relatorios abaixo. Publicar a colecao disponibiliza o menu aos usuarios ja autorizados da propriedade; nao publica os dados no website.

## 01 eBooks - Interesse e checkout

- ID do relatorio: `16208056745`. Modelo: Eventos.
- Filtro permanente: Nome do evento comeca com `ebook_`, sem restringir ao primeiro produto.
- Metricas: contagem de eventos, total de usuarios e contagem de eventos por usuario ativo.
- Dimensoes selecionaveis: nome do evento, ID do produto, titulo do eBook, campanha da apresentacao, metodo de interacao, posicao do CTA e caminho da pagina.
- Eventos: `ebook_introduction_view`, `ebook_offer_continue`, `ebook_site_continue`, `ebook_landing_view`, `ebook_catalog_view`, `ebook_product_view`, `ebook_landing_click` e `ebook_checkout_click`.
- A soma dos eventos nao representa pessoas, compras nem um funil sequencial de conversao. Um clique da apresentacao pode gerar `ebook_offer_continue` e `ebook_landing_click`; nao soma-los como duas decisoes. Nao somar usuarios de linhas com possivel sobreposicao.
- Taxas de interesse e continuidade: usar as contagens das respectivas escolhas divididas pelas exibicoes da apresentacao, com a mesma colecao, campanha, periodo e filtros. A apresentacao da colecao nao e uma exposicao atribuida a um unico produto. Acesso direto a uma oferta nao exige exibicao da apresentacao.
- Este relatorio mede intencao, nao pagamento ou receita. A visualizacao da pagina nao significa leitura completa; o clique para o checkout nao significa pagamento. Compras ficam no relatorio 04.

Os proximos eBooks devem reutilizar os nomes de eventos e informar seu proprio `ebook_id`, `ebook_title` e ID Hotmart no catalogo `tools/ebook_catalog.py`. O JavaScript resolve o produto mais proximo; a colecao usa `ebook_collection_id`, sem atribuir outros produtos ao CX na Operacao.

## 04 eBooks - Compras e receita

- ID do relatorio: `16208361514`. Modelo: Compras de e-commerce. Salvo e adicionado a colecao publicada em 26/10/2026.
- Filtro permanente: Categoria do item corresponde a RegEx `^eBook$`. Novos livros com a mesma categoria podem aparecer sem recriar o relatorio.
- Metricas: itens comprados, receita do item e valor do reembolso do item. Sem colunas de carrinho ou visualizacao de item que nao estao instrumentadas como e-commerce.
- Dimensoes nativas: nome do item, ID, categoria, marca e afiliacao, entre outras do modelo.
- Webhook autenticado ativado em 26/10/2026. As linhas financeiras dependem das vendas genuinas aprovadas e do processamento do Google. Consulte `integrations/hotmart-ga4/README.md` para os recibos de ativacao. Uma tabela vazia hoje nao comprova ausencia de vendas na Hotmart.
- A receita e a da oferta do produto; nao e comissao liquida nem saldo da Hotmart. Conferir separadamente reembolsos e a definicao nativa de receita do item; nao subtrair o reembolso duas vezes.
- O identificador do servidor e tecnico, por transacao, nao um visitante. Nao usar usuarios, pais ou canal deste fluxo como compradores reais ou atribuicao do anuncio. Nao ha ROAS implementado.

## 02 Site - Engajamento por pagina

- ID do relatorio: `16207905711`. Modelo: Paginas e telas.
- Filtro permanente: Nome do host corresponde a `^(www\.)?luizterra\.com\.br$`, salvo em 26/10/2026. Exclui localhost, checkout externo e identidades tecnicas sem hostname.
- Metricas: visualizacoes, usuarios ativos, visualizacoes por usuario ativo, tempo medio de engajamento por usuario ativo e contagem de eventos.
- Dimensoes: titulo e caminho da pagina, agrupamento de conteudo, categoria do dispositivo e idioma.
- Permite verificar quais artigos, temas, biografia e ofertas recebem atencao. Tempo de engajamento e a medida nativa do GA4, nao uma estimativa de leitura integral.
- Contagem de eventos tem seletor de evento; `scroll` pode ser consultado quando disponivel. A rolagem automatica do GA4 nao mede cada secao da pagina nem todos os percentuais de profundidade.

## 03 Site - Visitas e aquisicao

- ID do relatorio: `16208060617`. Modelo: Aquisicao de trafego.
- Filtro permanente: Nome do host corresponde a `^(www\.)?luizterra\.com\.br$`, salvo em 26/10/2026. Mantem visitas do dominio proprio separadas das notificacoes financeiras do servidor.
- Metricas: sessoes, sessoes engajadas, taxa de engajamento, tempo medio de engajamento por sessao, total de usuarios, novos usuarios e visualizacoes.
- Dimensoes: canal da sessao, origem/midia, origem, meio, plataforma de origem, campanha, pais, dispositivo e pagina de destino.
- A origem usa escopo da sessao, nao a origem do primeiro usuario. Os dados cobrem todos os canais; Organic Search e apenas uma linha, nao o total do site.
- Usuarios nao equivalem necessariamente a pessoas identificadas; sessoes e visualizacoes sao unidades distintas. Nao somar usuarios de pais, dispositivo ou canal sem considerar sobreposicao.

## Uso E Limites

- Selecione o mesmo periodo e comparacao nos relatorios. O periodo padrao observado na validacao foi os 28 dias completos anteriores, ate ontem. O periodo anterior ao lancamento nao possui os novos eventos de eBook. Receita nao deve receber o filtro de hostname dos relatorios de visitas, pois chega do servidor sem uma pagina/sessao atribuida.
- Use o seletor de dimensao e a dimensao secundaria para relacionar produto e evento. Para avaliar a apresentacao, prefira eventos de exibicao e escolha, nao a soma de todos os eventos do produto.
- As dimensoes personalizadas podem precisar de 24 a 48 horas de processamento e nao preenchem dados retroativamente. `(not set)` pode incluir eventos anteriores ao envio dos novos parametros.
- Os relatorios podem incluir acessos do proprietario e de QA. URLs de teste usam `qa=ebook-...-20261026`; o parametro identifica acessos de teste, mas pode nao acompanhar toda a navegacao subsequente. Nao interpretar os testes como interesse real. Nao foram alterados filtros de coleta, consentimento ou conversoes do Google Ads.
- Os relatorios sao alimentados pelo GA4 existente. Bloqueadores, consentimento, perda de rede e processamento podem limitar cobertura. Nenhuma ferramenta garante coleta de todas as visitas.
- Para acompanhamento imediato, a Visao geral em tempo real e o DebugView continuam sendo superfices separadas. Os tres relatorios criados usam dados processados, nao atualizacao segundo a segundo.

## Verificacao E Reversao

- Os tres relatorios foram salvos, adicionados na ordem 01, 02 e 03 a uma colecao e publicados no menu da propriedade. Foram reabertos pelo menu e tiveram os nomes, metricas e dimensoes conferidos.
- O relatorio 04 foi acrescentado depois, com ordem final 01, 02, 03, 04. Os filtros permanentes de hostname dos relatorios 02 e 03 foram salvos, confirmados na colecao publicada e reabertos. O relatorio financeiro usa sua categoria, sem filtro de hostname.
- A instrumentacao de produto e `ebook_landing_view` possui testes JavaScript e HTML. A validacao do site publico e do recebimento no GA4 deve ser registrada separadamente da simples criacao dos relatorios.
- Para ocultar os relatorios do menu, despublicar `Luiz Terra - Performance` na Biblioteca. Os relatorios e dados de origem permanecem preservados.
- Para reverter o codigo, usar `git revert` no commit de instrumentacao multiproduto, sem redefinir nem apagar dados do Analytics. Nao excluir dimensoes ou historico para desfazer uma mudanca de exibicao.

## Referencias

- https://support.google.com/analytics/answer/13844077
- https://support.google.com/analytics/answer/10460557
- https://support.google.com/analytics/answer/14239696
