# Competitive Coding Environment

### KACTL Export to Code Snippet Utility

```js
(function () {
	code = document.querySelector("#read-only-cursor-text-area").value;
	code = code.replace(/#pragma[^\n]+\n+/g, "");
	code = code.replaceAll("$", "\\$");
	path = "kactl/" + window.location.href.split("/content/")[1];
	// https://github.com/kth-competitive-programming/kactl/blob/main/content/data-structures/FenwickTree.h -> kactl/data-structures/FenwickTree.h
	o = {
		scope: "cpp",
		prefix: path,
		body: code
			.split("\n")
			.concat("", "$0")
			.sort((a, b) => b.startsWith("#") - a.startsWith("#")),
	};
	s = `"${path}": ` + JSON.stringify(o, null, "\t");
	copy(s);
})();
```
