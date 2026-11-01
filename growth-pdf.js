(function () {
  "use strict";

  const wrapText = (value, font, size, width) => {
    const lines = [];
    for (const paragraph of String(value).split("\n")) {
      let line = "";
      for (const word of paragraph.split(/\s+/).filter(Boolean)) {
        const candidate = line ? `${line} ${word}` : word;
        if (font.widthOfTextAtSize(candidate, size) <= width) {
          line = candidate;
        } else {
          if (line) lines.push(line);
          line = "";
          for (const character of word) {
            if (font.widthOfTextAtSize(line + character, size) > width && line) {
              lines.push(line);
              line = "";
            }
            line += character;
          }
        }
      }
      lines.push(line);
    }
    return lines;
  };

  const create = async (PDFLib, data) => {
    const { PDFDocument, StandardFonts, rgb, PDFName, PDFString } = PDFLib;
    const document = await PDFDocument.create();
    const regular = await document.embedFont(StandardFonts.Helvetica);
    const bold = await document.embedFont(StandardFonts.HelveticaBold);
    const form = document.getForm();
    const width = 595.28;
    const height = 841.89;
    const margin = 46;
    const span = width - 2 * margin;
    const colour = (hex) => rgb(...hex.match(/\w\w/g).map((value) => parseInt(value, 16) / 255));
    const ink = colour("183b32");
    const muted = colour("52665f");
    const green = colour("153f35");
    const mint = colour("b8e5d4");
    const blue = colour("245e83");
    const line = colour("ccd9d2");
    const paper = colour("f4f7f5");
    const white = rgb(1, 1, 1);
    const layout = [];
    document.setTitle(`${data.copy.heading} | ${data.topic}`);
    document.setAuthor("Luiz Terra");
    document.setSubject(data.topic);
    document.setCreator("Luiz Terra - CX in Practice");
    document.setProducer("Luiz Terra CX Action Plan / pdf-lib");
    document.catalog.set(PDFName.of("Lang"), PDFString.of(data.language));

    const rect = (page, x, top, w, h, fill, border) => page.drawRectangle({
      x, y: height - top - h, width: w, height: h,
      ...(fill ? { color: fill } : { color: white }),
      ...(border ? { borderColor: border, borderWidth: 0.7 } : {}),
    });
    const rule = (page, top, x = margin, w = span) => page.drawLine({
      start: { x, y: height - top }, end: { x: x + w, y: height - top }, color: line, thickness: 0.7,
    });
    const text = (page, value, top, { x = margin, w = span, size = 11, face = regular, color = ink, leading = size * 1.4 } = {}) => {
      const lines = wrapText(value, face, size, w);
      const bottom = top + lines.length * leading;
      if (bottom > height - 24 || x < 0 || x + w > width + 0.1) throw new Error("PDF text exceeds the page bounds");
      lines.forEach((value, index) => page.drawText(value, { x, y: height - top - size - index * leading, size, font: face, color }));
      layout.push({ page: document.getPages().indexOf(page) + 1, text: String(value), top, bottom, x, width: w });
      return bottom;
    };
    const field = (page, name, label, x, top, w, h = 26, multiline = false) => {
      text(page, label, top, { x, w, size: 8, color: muted });
      const input = form.createTextField(name);
      input.setMaxLength(multiline ? 700 : 70);
      if (multiline) input.enableMultiline();
      input.addToPage(page, { x, y: height - top - 15 - h, width: w, height: h, font: regular,
        textColor: ink, backgroundColor: white, borderColor: line, borderWidth: 0.65 });
      input.setFontSize(10);
      input.setText("");
      layout.push({ page: document.getPages().indexOf(page) + 1, field: name, top: top + 15, bottom: top + 15 + h, x, width: w });
    };
    const footer = (page, number) => {
      rule(page, 793);
      text(page, "LUIZ TERRA", 805, { size: 8, face: bold });
      text(page, "www.luizterra.com.br", 805, { x: 200, w: 220, size: 8, color: muted });
      text(page, `${number} / 3`, 805, { x: width - margin - 40, w: 40, size: 8, color: muted });
    };
    const runningHeader = (page, section) => {
      rect(page, 0, 0, width, 9, green);
      text(page, "CX / LUIZ TERRA", 32, { size: 8, face: bold, color: blue });
      text(page, section, 60, { size: 27, face: bold, leading: 31 });
      text(page, data.topic, 100, { size: 12, color: muted });
      rule(page, 133);
    };

    const cover = document.addPage([width, height]);
    rect(cover, 0, 0, width, 230, green);
    rect(cover, margin, 35, 36, 36, null, mint);
    text(cover, "LT", 43, { x: margin + 8, w: 28, size: 17, face: bold, color: green });
    text(cover, "LUIZ TERRA", 42, { x: 96, w: 200, size: 12, face: bold, color: white });
    text(cover, data.copy.label, 89, { size: 9, face: bold, color: mint });
    text(cover, data.copy.heading, 119, { size: 35, face: bold, color: white, leading: 41 });
    text(cover, data.copy.pdf_subtitle, 177, { size: 12, color: mint, leading: 17 });
    text(cover, data.topic, 260, { size: 23, face: bold, leading: 28 });
    text(cover, `${data.copy.pdf_generated}: ${data.dateLabel}`, 301, { size: 9, color: muted });
    text(cover, data.plan.maintenance ? data.copy.maintenance : data.copy.pdf_basis, 329, { size: 10, color: muted, leading: 14 });
    let cursor = 391;
    for (const [index, action] of data.plan.actions.entries()) {
      text(cover, String(index + 1).padStart(2, "0"), cursor, { w: 40, size: 22, face: bold, color: blue });
      const bottom = text(cover, action[1], cursor + 1, { x: 96, w: span - 50, size: 13, face: bold, leading: 18 });
      rule(cover, Math.max(cursor + 65, bottom + 17));
      cursor = Math.max(cursor + 88, bottom + 34);
    }
    rect(cover, margin, 690, span, 64, paper);
    text(cover, data.copy.cadence, 703, { x: margin + 15, w: span - 30, size: 12, face: bold });
    text(cover, data.copy.pdf_cadence_note, 726, { x: margin + 15, w: span - 30, size: 9, color: muted, leading: 12 });
    footer(cover, 1);

    const actionsPage = document.addPage([width, height]);
    runningHeader(actionsPage, data.copy.pdf_actions_heading);
    for (const [index, action] of data.plan.actions.entries()) {
      const top = 158 + index * 194;
      text(actionsPage, String(index + 1).padStart(2, "0"), top, { w: 34, size: 18, face: bold, color: blue });
      text(actionsPage, action[1], top, { x: 89, w: span - 43, size: 13, face: bold, leading: 17 });
      text(actionsPage, data.copy.evidence, top + 49, { size: 8, face: bold, color: blue });
      text(actionsPage, action[2], top + 66, { size: 10, leading: 14, color: muted });
      field(actionsPage, `owner_${index + 1}`, data.copy.pdf_owner, margin, top + 106, 328);
      field(actionsPage, `due_${index + 1}`, data.copy.pdf_due, 390, top + 106, width - margin - 390);
      rule(actionsPage, top + 174);
    }
    if (data.plan.actions.length < 3) {
      const notesTop = 164 + data.plan.actions.length * 194;
      field(actionsPage, "execution_notes", data.copy.pdf_execution_notes, margin, notesTop, span, 715 - notesTop, true);
    }
    text(actionsPage, data.copy.pdf_fields_note, 759, { size: 8, color: muted, leading: 11 });
    footer(actionsPage, 2);

    const review = document.addPage([width, height]);
    runningHeader(review, data.copy.pdf_review_heading);
    text(review, data.copy.pdf_review_intro, 151, { size: 10, color: muted });
    rect(review, margin, 197, span, 27, green);
    text(review, "#", 204, { x: margin + 10, w: 25, size: 9, face: bold, color: white });
    text(review, data.copy.evidence, 204, { x: 91, w: 285, size: 9, face: bold, color: white });
    text(review, data.copy.pdf_progress, 204, { x: 402, w: 110, size: 9, face: bold, color: white });
    for (const [index, action] of data.plan.actions.entries()) {
      const top = 224 + index * 70;
      if (index % 2 === 0) rect(review, margin, top, span, 70, paper);
      text(review, String(index + 1).padStart(2, "0"), top + 17, { x: margin + 10, w: 30, size: 11, face: bold, color: blue });
      text(review, action[2], top + 13, { x: 91, w: 289, size: 9, leading: 13, color: muted });
      const progress = form.createTextField(`progress_${index + 1}`);
      progress.setMaxLength(28);
      progress.addToPage(review, { x: 402, y: height - top - 45, width: width - margin - 414, height: 25, font: regular,
        backgroundColor: white, textColor: ink, borderColor: line, borderWidth: 0.65 });
      progress.setFontSize(9);
      progress.setText("");
    }
    const reviewNotesTop = 250 + data.plan.actions.length * 70;
    field(review, "review_notes", data.copy.pdf_notes, margin, reviewNotesTop, span, 529 - reviewNotesTop, true);
    field(review, "review_date", data.copy.pdf_review_date, margin, 563, 180);
    text(review, data.copy.pdf_next, 633, { size: 12, face: bold });
    text(review, data.relatedTitle, 659, { size: 14, face: bold, leading: 18 });
    text(review, data.copy.pdf_related_note, 706, { size: 9, color: muted, leading: 12 });
    const linkTop = text(review, "www.luizterra.com.br", 741, { size: 10, face: bold, color: blue }) - 14;
    review.node.addAnnot(document.context.register(document.context.obj({
      Type: "Annot", Subtype: "Link", Rect: [margin, height - linkTop - 15, margin + 160, height - linkTop + 2],
      Border: [0, 0, 0], A: { Type: "Action", S: "URI", URI: PDFString.of(data.relatedUrl) },
    })));
    footer(review, 3);
    form.updateFieldAppearances(regular);
    return { bytes: await document.save(), layout, fieldNames: form.getFields().map((field) => field.getName()) };
  };

  const api = { create, wrapText };
  if (typeof module === "object" && module.exports) module.exports = api;
  else window.CxPlanPdf = api;
})();
