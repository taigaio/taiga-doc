#!/bin/sh

# This script is used in two ways:
# 1. To check a single .adoc file as soon as it is modified (via. Guardfile)
# 2. To check all of the .adoc files when the docs are being build (via. build-docs.sh)
#
INCLUDE_GLOB="*.adoc"

if [ $# -eq 0 ]; then
    CHECK_FILE="."
else
    CHECK_FILE="${1}"
fi

# REGEX     EXPLANATION
# ,         Match the suspected JSON trailing comma
# (...)     Bracket around the rest of the search string so that it can be used as the Perl replace string, $1 (not implemented, yet)
# [^\\]     Match beginning of next line
# \s*       Match 0 or more spaces from the beginning of the line
# }         Match the JSON end brace
# ['\'']?   Match the possible single quote here (has to be escaped due to the whole regex being enclosed in single quotes)
# \s?       Match the possible space here
# \\?       Match the possible backslash here
# $         Match end of line
#
CHECK_JSON=$( rgrep -Pzo -l --include="${INCLUDE_GLOB}" ',([^\\]\s*}['\'']?\s?\\?$)' "${CHECK_FILE}" )
if [ -z "${CHECK_JSON}" ]; then
    exit 0
else
    echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    echo "WARNING: (${INCLUDE_GLOB}) file(s) with suspected JSON trailing commas"
    echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    echo "${CHECK_JSON}"
    echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    echo
    exit 1
fi
