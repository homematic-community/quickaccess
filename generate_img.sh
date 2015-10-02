#!/bin/sh
mkdir -p tmp/qa
cp -a qa/* tmp/qa
cp update_script tmp/
cp quickaccess tmp/
cd tmp
tar -czvf ../quickaccess-2.0b5.tar.gz *
cd ..
rm -rf tmp
