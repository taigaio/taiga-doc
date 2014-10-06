#!/bin/sh

rm -rf /tmp/taiga-doc-dist
cp dist /tmp/taiga-doc-dist
git checkout gh-pages;
rm -rf dist
mv /tmp/taiga-doc-dist dist
git add --all dist
git commit -a -m "Update doc"
