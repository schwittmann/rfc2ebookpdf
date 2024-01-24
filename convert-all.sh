#!/bin/bash
rm -f rfc-index.xml
wget https://www.rfc-editor.org/rfc-index.xml
rm -rf RFC-all
mkdir RFC-all
cd RFC-all
wget https://www.rfc-editor.org/in-notes/tar/RFC-all.tar.gz
tar -xzf RFC-all.tar.gz --wildcards --no-anchored 'rfc*txt'
