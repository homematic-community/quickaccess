#!/bin/sh
mkdir -p tmp/qa
cp -a qa/* tmp/qa
cp update_script tmp/
cp quickaccess tmp/
cd tmp
find . -not -name '.DS_Store' -not -name '*.sha256' -type f -print0 | xargs -0 sha256sum >quickaccess-2.1b3.sha256
tar --owner=root --group=root --exclude=.DS_Store -czvf ../quickaccess-2.1b3.tar.gz *
cd ..
rm -rf tmp
