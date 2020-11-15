#!/bin/bash
path=/home/$USER/analyze_pp
url_pandoc=https://github.com/jgm/pandoc/releases/download/2.11.1.1/pandoc-2.11.1.1-1-amd64.deb
url_python_file=https://raw.githubusercontent.com/3n3a/eneas_pluspoints_parser/main/analyze.py
url_python_req=https://raw.githubusercontent.com/3n3a/eneas_pluspoints_parser/main/requirements.txt

apt install -y wget python3 python3-pip python3-venv

mkdir -p $path
cd $path

wget $url_pandoc
wget $url_python_file
wget $url_python_req

dpkg -i pandoc-*.deb
rm -rf pandoc-*.deb

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
echo "installed everything...hopefully.\nexecute analyzer.py [file] - have fun"
