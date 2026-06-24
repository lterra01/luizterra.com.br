# Luiz Terra Personal Website

Site estático profissional para Luiz Terra, construído em HTML5, CSS e JavaScript vanilla para publicação no GitHub Pages.

## Arquivos

- `index.html`
- `styles.css`
- `script.js`
- `CNAME`
- `README.md`

## Deploy Manual no GitHub Pages

Se o token do GitHub não estiver disponível no ambiente, use:

```bash
cd luizterra.com.br
git init
git add .
git commit -m "Launch Luiz Terra personal website"
git branch -M main
git remote add origin https://github.com/lterra01/luizterra.com.br.git
git push -u origin main
```

Depois, no GitHub:

1. Criar o repositório público `luizterra.com.br` no usuário `lterra01`.
2. Em Settings -> Pages, selecionar Source: `main` branch, `/ (root)`.
3. Confirmar o arquivo `CNAME` com `www.luizterra.com.br`.
4. URL do GitHub Pages: `https://lterra01.github.io/luizterra.com.br`.

## Relatório de DNS

Configure estes registros no painel DNS do registrador do domínio, como registro.br ou equivalente:

| Tipo  | Host/Nome | Valor / Aponta para      | TTL  |
|-------|-----------|--------------------------|------|
| A     | @         | 185.199.108.153          | 3600 |
| A     | @         | 185.199.109.153          | 3600 |
| A     | @         | 185.199.110.153          | 3600 |
| A     | @         | 185.199.111.153          | 3600 |
| CNAME | www       | lterra01.github.io       | 3600 |

A propagação de DNS normalmente leva cerca de 24 a 48 horas. Para verificar, execute `dig www.luizterra.com.br` ou `nslookup www.luizterra.com.br`. Depois que a propagação estiver concluída e o domínio personalizado aparecer como válido no GitHub Pages, ative "Enforce HTTPS" nas configurações de Pages. O certificado Let's Encrypt é provisionado automaticamente e sem custo pelo GitHub Pages.

## Checklist Pós-Lançamento

[ ] DNS verified via `dig www.luizterra.com.br`
[ ] Custom domain confirmed in GitHub Pages settings
[ ] "Enforce HTTPS" toggled ON in GitHub Pages
[ ] Site loads correctly at https://www.luizterra.com.br
[ ] Mobile test at 375px width
[ ] All links tested: email, LinkedIn, cal.read.ai
[ ] Meta description and og:tags reviewed
[ ] Google Search Console: submit sitemap (sitemap.xml optional but recommended - can be a single-page sitemap)
