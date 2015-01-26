#!/bin/sh

# This script is used in two ways:
# 1. To check a single .adoc file as soon as it is modified (via. Guardfile)
# 2. To check all of the .adoc files when the docs are being build (via. build-docs.sh)
#
if [ ${#} -eq 0 ]; then
    CHECK_FILES="."
else
    CHECK_FILES="${1}"
fi

# Get excludes file if found
# Looks for the file in the same directory as this script, with prefix "exclude-from_" and removal of ".sh" suffix
# I.e. `check_JSON_trailing_commas.sh` => `exclude-from_check_JSON_trailing_commas`
SCRIPT_FILENAME=$( basename "${0}" )
EXCLUDE_FROM_FILE=$( echo "${0}" | sed 's:'"${SCRIPT_FILENAME}"':'"exclude-from_${SCRIPT_FILENAME}"':' | sed 's:.sh::' )
if [ -r "${EXCLUDE_FROM_FILE}" ]; then
    EXCLUDE_FROM="--exclude-from=${EXCLUDE_FROM_FILE}"
else
    EXCLUDE_FROM=
fi

# Files to search in
INCLUDE_GLOB="*.adoc"

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
if [ -z "${EXCLUDE_FROM}" ]; then
    CHECK_JSON=$( grep -r -Pzo -l --include="${INCLUDE_GLOB}" ',([^\\]\s*}['\'']?\s?\\?$)' "${CHECK_FILES}" )
else
    CHECK_JSON=$( grep -r -Pzo -l --include="${INCLUDE_GLOB}" "${EXCLUDE_FROM}" ',([^\\]\s*}['\'']?\s?\\?$)' "${CHECK_FILES}" )
fi

# Show files if found
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
