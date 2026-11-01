"use strict";

const fs = require("node:fs");
const path = require("node:path");
const PDFLib = require("../public/vendor/pdf-lib-1.17.1/pdf-lib.min.js");
const { create } = require("../growth-pdf.js");

async function main() {
  const payload = JSON.parse(fs.readFileSync(0, "utf8"));
  const outputIndex = process.argv.indexOf("--output-dir");
  const outputDir = outputIndex >= 0 ? path.resolve(process.argv[outputIndex + 1]) : null;
  if (outputDir) fs.mkdirSync(outputDir, { recursive: true });
  const results = [];
  for (const item of payload.cases) {
    if (!/^[a-z0-9-]+$/.test(item.id)) throw new Error("Unsupported fixture identifier");
    const result = await create(PDFLib, item.data);
    const pdf = await PDFLib.PDFDocument.load(result.bytes);
    const output = outputDir ? path.join(outputDir, `${item.id}.pdf`) : null;
    if (output) fs.writeFileSync(output, result.bytes);
    results.push({ id: item.id, pages: pdf.getPageCount(), fieldNames: result.fieldNames, layout: result.layout,
      ...(output ? { output } : {}), ...(payload.includeBytes ? { pdf: Buffer.from(result.bytes).toString("base64") } : {}) });
  }
  process.stdout.write(JSON.stringify(results));
}

main().catch((error) => { process.stderr.write(`${error.message}\n`); process.exitCode = 1; });
