all: doc
doc:
	asciidoc -b html5 -o dist/index.html index.asc
