#!/bin/bash

cp public/index.html public/diffMap.html
git commit -m "Update to website" public/index.html public/diffMap.html
git subtree push --prefix=public git@github.com:juris-m/z2csl.git gh-pages
