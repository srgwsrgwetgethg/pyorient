#!/bin/bash
#
# Copyright 2020 Niko Usai <usai.niko@gmail.com>, http://mogui.it; Marc Auberer, https://marc-auberer.de
#
# this file is part of pyorient
#
# Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
#  limitations under the License.
#

set -e

PARENT_DIR=$(dirname $(cd "$(dirname "$0")"; pwd))
DOCS_DIR="$PARENT_DIR/docs"

GHPAGES_DIR="$DOCS_DIR/build/html"


if [ ! -d "$GHPAGES_DIR" ]; then
  echo "--- Cloning repo ---"
  git clone https://marcauberer:$GH_TOKEN@github.com/marcauberer/pyorient.git $GHPAGES_DIR
  cd $GHPAGES_DIR
  git checkout gh-pages
  git config user.email "pyorient-ci@example.com"
  git config user.name "pyorient CI"
else
  echo "--- Already cloned repository ---"
fi

# Update branch
cd $GHPAGES_DIR
git checkout gh-pages
git pull

# generate docs
cd $DOCS_DIR
make html

# push them
cd $GHPAGES_DIR
git commit -a -m 'regenerate docs'
git push origin gh-pages
