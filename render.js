let fs = require("fs");
let katex = require("katex");
nunjucks = require("nunjucks").configure({ autoescape: false });
// let unified = require("unified");
// let rehypeParse = require("rehype-parse");
// let rehypeStringify = require("rehype-stringify");

let capitalize = s => s.charAt(0).toUpperCase() + s.slice(1);

let renderers = {
  // extract renderChildren/innerHTML

  // TODO: Filter mathML
  "#text": n => n.textContent,

  "#document-fragment": renderChildren,

  "#document": renderChildren,

  math: n => {
    let tex = n.source.trim();
    console.assert(
      tex.startsWith("$"),
      'Expected math node source to begin with "$".'
    );
    console.assert(
      tex.endsWith("$"),
      'Expected math node source to end with "$".'
    );
    innerTex = tex.slice(1, -1).trim();
    console.log(`\n\n${innerTex}\n\n`);
    html = katex.renderToString(innerTex);
    return html;
  },

  displaymath: function(n) {
    let tex = n.source.trim();
    console.assert(
      tex.startsWith("$$") || tex.startsWith("\\["),
      'Expected displaymath node source to begin with "$$" or "\\[".'
    );
    console.assert(
      tex.endsWith("$") || tex.endsWith("\\]"),
      'Expected math node source to end with "$$" or with "\\]".'
    );
    innerTex = tex.slice(2, -2).trim();
    console.log(`\n\n${innerTex}\n\n`);
    html = katex.renderToString(innerTex, { displayMode: true });
    return html;
  },

  // lemma: n => {
  //   console.log("lemma");
  //   return renderers.theorem(n);
  // },

  theorem: function(n) {
    // TODO: child containing n.attributes.note
    console.log(n.attributes);
    let number =
      n.ref && n.ref.childNodes && n.ref.childNodes.length > 0
        ? " " + renderChildren(n.ref)
        : "";
    let note = n.attributes.note
      ? ` (${renderChildren(n.attributes.note)})`
      : "";
    let title = `<h3>${capitalize(n.nodeName)}${number}${note}</h3>`;
    return `<div id="${n.id}" class="${n.nodeName}">${title}${renderChildren(
      n
    )}</div>`;
  },

  section: n => {
    let number =
      n.ref && n.ref.childNodes && n.ref.childNodes.length > 0
        ? n.ref.childNodes.map(node).join("")
        : "";
    return `<section id="${n.id}" class="section"><h2>${
      number ? number + ". " : ""
    }${node(n.attributes.title)}</h2>${renderChildren(n)}</div>`;
  },

  document: n =>
    `<div id="${n.id}" class="document">${n.childNodes
      .map(node)
      .join("")}</div>`
};

let DO_NOT_RENDER = [
  "label",
  "documentclass",
  "usepackage",
  "theoremstyle",
  "newtheorem",
  "newcommand",
  "title",
  "maketitle",
  "DeclareMathOperator",
  "setlength",
  "itemsep",
  "bigskip"
];

let THEOREM_ENVS = [
  "theorem",
  "lemma",
  "corollary",
  "definition",
  "remark",
  "remarks",
  "exercise",
  "example"
];

let TAGS = {
  par: "p",
  enumerate: "ol",
  itemize: "ul",
  item: "li",
  textbf: "b",
  textit: "i",
  emph: "i"
};

function node(n) {
  console.log(n.nodeName);
  if (DO_NOT_RENDER.includes(n.nodeName)) {
    return null;
  } else if (n.nodeName in TAGS) {
    let tag = TAGS[n.nodeName];
    return n.childNodes && n.childNodes.length > 0
      ? `<${tag} id=${n.id} class="${n.nodeName}">${renderChildren(n)}</${tag}>`
      : null;
  } else if (THEOREM_ENVS.includes(n.nodeName)) {
    return renderers.theorem(n);
  } else {
    return renderers[n.nodeName](n);
  }
}

function renderChildren(n) {
  return Array.isArray(n.childNodes)
    ? n.childNodes
        .map(node)
        .filter(x => x)
        .join("")
    : node(n.childNodes);
}

function render(jsonFile, templateFile, outFile) {
  let tree = JSON.parse(fs.readFileSync(jsonFile, "utf8"));
  html = nunjucks.render(templateFile, { content: node(tree) });
  if (outFile) {
    fs.writeFileSync(outFile, html, "utf8");
  } else {
    process.stdout.write(html);
  }
}

let [inFile, templateFile, outFile] = process.argv.slice(2);
render(inFile, templateFile, outFile);
