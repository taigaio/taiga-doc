#!/bin/sh

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2021-present Kaleidos INC

# Not exiting for the JSON trailing commas check since just a warning, not an error
tests/check_JSON_trailing_commas.sh

make doc || exit 1
make pdf || exit 1
rm -rf /tmp/taiga-doc-dist || exit 1
cp -r dist /tmp/taiga-doc-dist || exit 1
git checkout gh-pages || exit 1
git pull || exit 1
git reset --hard || exit 1
find . ! -path "./.git/*" -a ! -name .git -a ! -name CNAME -delete
mv /tmp/taiga-doc-dist/* . || exit 1
git add --all . || exit 1
git commit -a -m "Update doc" || exit 1
git push || exit 1
git checkout main || exit 1
