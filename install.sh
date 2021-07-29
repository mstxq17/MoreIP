#!/bin/sh
pip3 install -r requirements.txt
cp moreIP.py /usr/local/bin/mip
chmod +x /usr/local/bin/mip
echo "install Success!"
