# Notes regarding keeping Makefile & Guardfile in sync
# - Guardfile is configured to extract commands from this Makefile
# - If decision is made to break this dependency, all commands from this
#   Makefile should be duplicated in the Guardfile
# - Thereafter, every single change will need to be applied in both files
#
# Guardfile *DOES require* modification if:
# - A new .adoc file is added to this file
# - The path/name of an existing .adoc file is changed
#
# Guardfile *DOES NOT require* modification if:
# - Any other part of an existing command is changed, i.e.:
#   - OK: Modifying asciidoctor command line switches
#   - OK: Changing path/name for HTML output
#
all: doc
doc:
	asciidoctor -o dist/index.html index.adoc
	asciidoctor -o dist/setup-production.html setup-production.adoc
	asciidoctor -o dist/setup-alternatives.html setup-alternatives.adoc
	asciidoctor -o dist/api.html api/api.adoc
	asciidoctor -o dist/webhooks.html webhooks.adoc
