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
	asciidoctor -T custom-html5 -o dist/index.html index.adoc
	asciidoctor -T custom-html5 -o dist/setup-production.html setup-production.adoc
	asciidoctor -T custom-html5 -o dist/setup-development.html setup-development.adoc
	asciidoctor -T custom-html5 -o dist/setup-faqs.html setup-faqs.adoc
	asciidoctor -T custom-html5 -o dist/upgrades-6to6.html upgrades-6to6.adoc
	asciidoctor -T custom-html5 -o dist/upgrades-older.html upgrades-older.adoc
	asciidoctor -T custom-html5 -o dist/upgrades-5to6.html upgrades-5to6.adoc
	asciidoctor -T custom-html5 -o dist/api.html api/api.adoc
	asciidoctor -T custom-html5 -o dist/importers.html importers.adoc
	asciidoctor -T custom-html5 -o dist/webhooks.html webhooks.adoc
	asciidoctor -T custom-html5 -o dist/webhooks-configuration.html webhooks-configuration.adoc
	asciidoctor -T custom-html5 -o dist/changing-elements-status-via-commit-message.html changing-elements-status-via-commit-message.adoc
	asciidoctor -T custom-html5 -o dist/attach-commits-to-elements-via-commit-message.html attach-commits-to-elements-via-commit-message.adoc
	asciidoctor -T custom-html5 -o dist/integrations-github.html integrations-github.adoc
	asciidoctor -T custom-html5 -o dist/integrations-gitlab.html integrations-gitlab.adoc
	asciidoctor -T custom-html5 -o dist/integrations-bitbucket.html integrations-bitbucket.adoc
	asciidoctor -T custom-html5 -o dist/integrations-gogs.html integrations-gogs.adoc
	asciidoctor -T custom-html5 -o dist/integrations-slack.html integrations-slack.adoc
	asciidoctor -T custom-html5 -o dist/backup-and-restore.html backup-and-restore.adoc
	cp -r assets/* dist || exit 1
	cp Caddyfile dist || exit 1
pdf:
	asciidoctor -a allow-uri-read -r asciidoctor-pdf -b pdf -o dist/pdfs/index.pdf index.adoc
	asciidoctor -a allow-uri-read -r asciidoctor-pdf -b pdf -o dist/pdfs/setup-production.pdf setup-production.adoc
	asciidoctor -a allow-uri-read -r asciidoctor-pdf -b pdf -o dist/pdfs/setup-development.pdf setup-development.adoc
	asciidoctor -a allow-uri-read -r asciidoctor-pdf -b pdf -o dist/pdfs/setup-faqs.pdf setup-faqs.adoc
	asciidoctor -a allow-uri-read -r asciidoctor-pdf -b pdf -o dist/pdfs/upgrades-6to6.html upgrades-6to6.adoc
	asciidoctor -a allow-uri-read -r asciidoctor-pdf -b pdf -o dist/pdfs/upgrades-older.html upgrades-older.adoc
	asciidoctor -a allow-uri-read -r asciidoctor-pdf -b pdf -o dist/pdfs/upgrades-5to6.html upgrades-5to6.adoc
	asciidoctor -a allow-uri-read -r asciidoctor-pdf -b pdf -o dist/pdfs/api/api.pdf api/api.adoc
	asciidoctor -a allow-uri-read -r asciidoctor-pdf -b pdf -o dist/pdfs/importers.pdf importers.adoc
	asciidoctor -a allow-uri-read -r asciidoctor-pdf -b pdf -o dist/pdfs/webhooks.pdf webhooks.adoc
	asciidoctor -a allow-uri-read -r asciidoctor-pdf -b pdf -o dist/pdfs/webhooks-configuration.pdf webhooks-configuration.adoc
	asciidoctor -a allow-uri-read -r asciidoctor-pdf -b pdf -o dist/pdfs/changing-elements-status-via-commit-message.pdf changing-elements-status-via-commit-message.adoc
	asciidoctor -a allow-uri-read -r asciidoctor-pdf -b pdf -o dist/pdfs/attach-commits-to-elements-via-commit-message.pdf attach-commits-to-elements-via-commit-message.adoc
	asciidoctor -a allow-uri-read -r asciidoctor-pdf -b pdf -o dist/pdfs/integrations-github.pdf integrations-github.adoc
	asciidoctor -a allow-uri-read -r asciidoctor-pdf -b pdf -o dist/pdfs/integrations-gitlab.pdf integrations-gitlab.adoc
	asciidoctor -a allow-uri-read -r asciidoctor-pdf -b pdf -o dist/pdfs/integrations-bitbucket.pdf integrations-bitbucket.adoc
	asciidoctor -a allow-uri-read -r asciidoctor-pdf -b pdf -o dist/pdfs/integrations-gogs.pdf integrations-gogs.adoc
	asciidoctor -a allow-uri-read -r asciidoctor-pdf -b pdf -o dist/pdfs/integrations-slack.pdf integrations-slack.adoc
	asciidoctor -a allow-uri-read -r asciidoctor-pdf -b pdf -o dist/pdfs/backup-and-restore.pdf backup-and-restore.adoc
