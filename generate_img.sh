#!/bin/sh
mkdir -p tmp/qa
cp -a qa/* tmp/qa
cp update_script tmp/
cp quickaccess tmp/
cd tmp
tar --owner=root --group=root --exclude=.DS_Store -czvf ../quickaccess-2.1b2.tar.gz *
cd ..
rm -rf tmp
