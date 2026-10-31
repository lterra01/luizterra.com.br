# Validacao SEO - 31/10/2026

## Escopo

Revisao dos avisos de dados estruturados recebidos do Google Search Console,
HTML estatico, disponibilidade HTTPS, descoberta, metadados e imagens responsivas.
Metricas privadas de Search Console e GA4 ficam fora deste repositorio publico.
Os checkouts, precos, bonus, credenciais e receptor financeiro nao foram alterados.

## Avisos E Correcao

- Os emails de 31/10/2026 apontam campos recomendados, nao erros criticos.
- O catalogo descreve uma colecao de seis livros diferentes. Agora usa
  `CollectionPage`, `ItemList` e `Book`, com nomes e descricoes no idioma da pagina,
  IDs Hotmart verdadeiros e ofertas existentes. Nao simula uma pagina de um unico
  produto para obter rich results de uma categoria.
- A pagina individual de CX na Operacao preserva `Book` + `Product`, oferta,
  descricao, autor e identidade real. Marca Luiz Terra e SKU Hotmart adicionados.
- Nao foram inventadas notas, avaliacoes, ISBNs, GTINs, transportadoras nem regras
  internacionais de devolucao. A ausencia de `review` e `aggregateRating` continua
  legitima sem avaliacoes reais visiveis. `shippingDetails` nao e preenchido com
  frete fisico ficticio para PDFs. Condicoes de reembolso permanecem no texto da
  oferta e no checkout, sem generalizar uma regra a todos os paises.
- Breadcrumbs estruturados adicionados as paginas comerciais.
- Oito artigos recebem titulos de busca mais objetivos, sem mudar seus H1s,
  textos, URLs ou datas de publicacao. Metadescricao inglesa da home encurtada.
- Capas promocionais ganham variantes de 320, 640 e 960 px com `srcset` e `sizes`.
  Originais de 1254 px, imagens sociais e PDFs pagos permanecem preservados.

## Exclusoes Esperadas

Nao remover redirecionamentos HTTP/HTTPS ou apex/www, nem criar conteudo duplicado
para tentar indexar aliases. `/en/` permanece com canonical para `/`. O feed RSS
nao e uma pagina comercial que precise de indexacao. Esses casos ficam fora do
sitemap de paginas canonicas e nao devem motivar uma falsa validacao de correcao.

## Validacao Repetivel

```powershell
python -B tools/build_catalog_assets.py --responsive-only
python -B -c "import sys; sys.path.insert(0,'tools'); import build_static_site as b; b.build_pages(); b.build_sitemap(); b.build_discovery_files(); b.build_readme()"
python -B -m unittest discover -s tools -p 'test_*.py'
node --test tools/test_ebook_promotion.js tools/test_mini_expert.js tools/test_commerce.js integrations/hotmart-ga4/test.mjs
python -B tools/seo_audit.py --output <private-output>/local.json
python -B tools/seo_audit.py --live --output <private-output>/public.json
```

O auditor percorre o sitemap e verifica status/final URL, canonical, robots meta e
HTTP, permissao Googlebot, H1, idioma, metadados, JSON-LD parseavel, alternates
reciprocos, titulos/descricoes duplicados, arquivos referenciados e imagens. No
modo live compara os assets e o sitemap publicos com os artefatos locais. Nao
executa JavaScript, nao gera pageviews e nao envia eventos financeiros.

O limite de comprimento de titulo/descricao e uma heuristica editorial, nao um
limite oficial de caracteres nem uma pontuacao de ranking do Google. O auditor
nao substitui o Rich Results Test, inspecao de URL, analise editorial ou dados
de experiencia real dos usuarios.

## Medicao E Limites

- Visitas e engajamento no GA4: manter o filtro de hostname proprio.
- Receita por eBook: manter categoria do item, sem filtro de hostname, porque o
  evento server-side nao possui uma sessao atribuida.
- Cliques em checkout, exposicoes e escolhas da apresentacao nao sao compras.
  Nao somar eventos com finalidades diferentes como se fossem pessoas distintas.
- QA e acessos do proprietario podem existir no historico. Nesta revisao os testes
  de interface usam bloqueio de coleta apenas na aba temporaria de QA, sem mudar
  configuracoes de producao nem filtros do Google.
- Uma linha agregada de receita nao prova venda genuina nem ausencia de duplicidade.
  A conciliacao exige a transacao aprovada na Hotmart e o mesmo transaction_id no GA4.
- PageSpeed/Lighthouse e teste de laboratorio de uma pagina. Core Web Vitals de
  campo podem permanecer sem dados; ausencia de dados nao significa aprovacao.
- Sitemap processado, IndexNow aceito e solicitacao de indexacao sao recibos
  separados. Nenhum deles garante indexacao, posicao, cliques ou vendas.

## Publicacao E Reversao

Publicar na branch principal e conferir o workflow de Pages antes de testar o
dominio. Depois, usar o auditor live e Rich Results Test nas paginas alteradas.
Solicitacoes ao Search Console devem ser individuais e sem contornar CAPTCHA.

Para reverter, aplicar `git revert` ao commit desta revisao e aguardar novo deploy
do Pages. Nao apagar dados, dimensoes ou historico do Analytics. As capas originais
e as rotas canonicas anteriores continuam presentes.

## Referencias Oficiais

- https://developers.google.com/search/docs/appearance/structured-data/product-snippet
- https://developers.google.com/search/docs/appearance/structured-data/merchant-listing
- https://developers.google.com/search/docs/appearance/structured-data/review-snippet
- https://support.google.com/webmasters/answer/7440203
- https://www.indexnow.org/documentation
