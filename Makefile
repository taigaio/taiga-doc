all: doc
doc:
	asciidoctor -o dist/index.html index.adoc
