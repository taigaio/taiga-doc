#!/bin/sh

# Not exiting for the JSON trailing commas check since just a warning, not an error
tests/check_JSON_trailing_commas.sh

make || exit 1
rm -rf /tmp/taiga-doc-dist || exit 1
cp -r dist /tmp/taiga-doc-dist || exit 1
git checkout gh-pages || exit 1
rm -rf dist || exit 1
mv /tmp/taiga-doc-dist dist || exit 1
git add --all dist || exit 1
git commit -a -m "Update doc" || exit 1
