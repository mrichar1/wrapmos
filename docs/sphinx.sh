#!/bin/bash

# Try to ensure we're in the project 'root' for relative paths etc to work.
cd "$(dirname $0)/.."

PATH=bin/:$PATH
SOURCE=docs/source
TARGET=docs/build

sphinx-apidoc -f -T -e -o ${SOURCE}/apidoc wrapmos
travis-sphinx --outdir=${TARGET} build --source=${SOURCE}
# Build docs if this is master branch, and HEAD has a tag associated with it
if [[ $TRAVIS_BRANCH == "master" ]]; then
  echo "Deploying docs to gh-pages..."
  travis-sphinx --outdir=${TARGET} deploy
fi
