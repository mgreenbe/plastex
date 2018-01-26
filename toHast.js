let fs = require("fs");
let katex = require("katex");

let tree = JSON.parse(fs.readFileSync("tree.json", "utf8"));

let renderers = {
  // extract renderChildren/innerHTML

  // TODO: Filter mathML
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
    return {
      type: "element",
      tagName: "span",
      properties: { className: "inlineMath" },
      children: [
        {
          type: "text",
          value: tex.slice(1, -1)
        }
      ]
    };
  },

  "#text": n => ({
    type: "text",
    value: n.textContent
  }),

  label: n => null,

  par: function(n) {
    return {
      type: "element",
      tagName: "p",
      properties: { className: "par" },
      children: n.childNodes.map(child => this[child.nodeName](child))
    };
  },

  theorem: function(n) {
    let dataRef =
      n.ref.length > 0
        ? n.ref.childNodes &&
          n.ref.childNodes.map(child => this[child.nodeName](child)).join("")
        : null;
    let elt = {
      type: "element",
      tagName: "div",
      properties: Object.assign(
        { id: n.id, className: "theorem" },
        dataRef ? { "data-ref": dataRef } : {}
      ),
      children: n.childNodes.map(child => this[child.nodeName](child))
    };
    // TODO: child containing n.attributes.note
    let innerHTML = n.childNodes
      .map(child => this[child.nodeName](child))
      .join("");
    return `<div id="${n.id}" class="theorem"${
      dataRef ? " " + dataRef : ""
    }>${innerHTML}</div>`;
  }
};

let th = tree.childNodes[0];
let p = th.childNodes[0];
let t = p.childNodes[1];
let m = p.childNodes[2];

console.log(renderers.theorem(th));
