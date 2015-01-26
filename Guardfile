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

# This Guardfile currently has dependencies on 2 other files:
# 1. Makefile
# 2. tests/check_JSON_trailing_commas.sh
#
# The method used below extracts the relevant command from Makefile
#
# For example (where filename=index.adoc):
#    `eval "$( grep "#{filename}" Makefile )"`
#
# Evaluates to:
#    `asciidoctor -o dist/index.html index.adoc`
#
# The dependency on Makefile can be removed by using the command literally
# However, every change in every line from Makefile would need to be duplicated here
# With this dependency method, there are very few circumstances where any changes
#   need to be made to this file (see Makefile comments for examples)
#
guard :shell do
  watch(%r{^.+\.adoc}) { |m|
    # Check modified file for JSON trailing commas
    if not system("tests/check_JSON_trailing_commas.sh #{m[0]}")
      n "[#{m[0]}] has at least one suspected JSON trailing comma",
	"Check for JSON trailing comma [#{m[0]}] has failed",
	:pending
    end

    # Determine which filename to use when searching for the render command in Makefile
    if "#{m[0][0,4]}"=="api/"
      filename="api/api.adoc"
    else
      filename="#{m[0]}"
    end

    # Run the command to render the .adoc file if it is in Makefile
    if system("grep #{filename} Makefile")
      # Quotation marks are important since they allow running more than one matched command
      `eval "$( grep "#{filename}" Makefile )"`
      n "[#{filename}] has been found in Makefile and the relevant rendering " +
	"command has been performed",
	"[#{filename}] rendered via. Makefile",
	:success
    else
      n "The command to render [#{filename}] has not been found in Makefile\n" +
	"- please add it there so that rendering can be performed",
	"[#{filename}] not found in Makefile",
	:failed
    end
  }
end
