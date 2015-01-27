# Notes regarding keeping Makefile & Guardfile in sync
# - Guardfile is configured to extract commands from this Makefile
# - If decision is made to break this dependency, all commands from this
#   Makefile should be duplicated in the Guardfile
# - Thereafter, every single change will need to be applied in both files
#
# *DO NOT*:
# - Write the whole path/name of one of the .adoc files in any comment
#
# M:1 vs. 1:1 .adoc files:
# - 1:1 is where 1 .adoc file is rendered to 1 output file
# - M:1 is where 1 .adoc file references many other .adoc files, but rendered
#   to only 1 output file (such as api.adoc)
#
# Guardfile *DOES require* modification if:
# - A new M:1 .adoc file is added to this file
# - The path/name of an existing M:1 .adoc file is changed
#
# Guardfile *DOES NOT require* modification if:
# - A new 1:1 .adoc file is added to this file
# - The path/name of an existing 1:1 .adoc file is changed
# - More than 1 command is used to render an existing .adoc file
# - Any other part of an existing command is changed, i.e.:
#   - OK: Modifying asciidoctor command line switches
#   - OK: Changing path/name for HTML output
#
all: doc
doc:
	asciidoctor -o dist/index.html index.adoc
	asciidoctor -o dist/setup-production.html setup-production.adoc
	asciidoctor -o dist/setup-development.html setup-development.adoc
	asciidoctor -o dist/setup-alternatives.html setup-alternatives.adoc
	asciidoctor -o dist/api.html api/api.adoc
	asciidoctor -o dist/webhooks.html webhooks.adoc
