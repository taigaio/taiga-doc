# A sample Guardfile
# More info at https://github.com/guard/guard#readme

## Uncomment and set this to only include directories you want to watch
# directories %w(app lib config test spec feature)

## Uncomment to clear the screen before every task
# clearing :on

## Guard internally checks for changes in the Guardfile and exits.
## If you want Guard to automatically start up again, run guard in a
## shell loop, e.g.:
##
##  $ while bundle exec guard; do echo "Restarting Guard..."; done
##
## Note: if you are using the `directories` clause above and you are not
## watching the project directory ('.'), the you will want to move the Guardfile
## to a watched dir and symlink it back, e.g.
#
#  $ mkdir config
#  $ mv Guardfile config/
#  $ ln -s config/Guardfile .
#
# and, you'll have to watch "config/Guardfile" instead of "Guardfile"

# Add files and commands to this file, like the example:
#   watch(%r{file/path}) { `command(s)` }
#
require 'asciidoctor'
require 'erb'

# The method used below extracts the relevant command from Makefile
#
# For example:
#    `eval $( grep index.adoc Makefile )`
#
# Evaluates to:
#    `asciidoctor -o dist/index.html index.adoc`
#
# The dependency on Makefile can be removed by using the command literally
# However, every change in every line from Makefile would need to be duplicated here
# With this dependency method, only new lines will need to be included in this file
#
guard :shell do
  watch(/^index\.adoc$/) {
    `eval $( grep index.adoc Makefile )`
  }

  watch(/^setup-production\.adoc$/) {
    `eval $( grep setup-production.adoc Makefile )`
  }

  watch(/^setup-alternatives\.adoc$/) {
    `eval $( grep setup-alternatives.adoc Makefile )`
  }

  watch(%r{^api/.+\.adoc}) {
    `eval $( grep api.adoc Makefile )`
  }

  watch(/^webhooks\.adoc$/) {
    `eval $( grep webhooks.adoc Makefile )`
  }
end
