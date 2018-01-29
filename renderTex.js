let fs = require("fs");
let child_process = require("child_process");
let katex = require("katex");
let nunjucks = require("nunjucks").configure({ autoescape: false });
let minify = require("html-minifier").minify;

let tagOfNode = {
	par: "p",
	section: "section",
	subsection: "section",
	enumerate: "ol",
	itemize: "ul",
	item: "li",
	ref: "span"
};

let pythonOutput = child_process.execSync(
	"python parse_tex.py sample.tex sample.json",
	{
		encoding: "utf8"
	}
);
// console.log(pythonOutput);
let tree = JSON.parse(fs.readFileSync("sample.json", { encoding: "utf8" }));
console.log(render(tree)
let html = nunjucks.render("index.njk", { content: render(tree) });
console.log(html)
// let minHTML = minify(html).replace("<p></p>", "");
fs.writeFileSync("index.html", html, "utf8");

function render({ nodeName, id, textContent, childrenSource, childNodes }) {
	switch (nodeName) {
		case "#text":
			return textContent;
		case "math":
			return `<span class="math">${katex.renderToString(
				childrenSource
			)}</span>`;
		case "displaymath":
			return `<div class="displaymath">${katex.renderToString(childrenSource, {
				displayMode: true
			})}</div>`;
		default:
			let tag = tagOfNode[nodeName] || "div";
			let innerHTML = childNodes ? childNodes
				.map(render)
				.join("")
				.trim() : "";
			return innerHTML
				? `<${tag} class="${nodeName}">${innerHTML}</${tag}>`
				: "";
	}
}
