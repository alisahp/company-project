#!/bin/bash
yum install python-pip git centos-release-scl scl-utils-build -y
yum install  python33 gcc python3 -y

if [ ! -d "$HOME/common_scripts" 2>/dev/null ]; then
  git clone -b master https://github.com/fuchicorp/common_scripts.git "$HOME/common_scripts"
fi
cd  "$HOME/common_scripts/bastion-scripts/"
python3 -m pip install -r "$HOME/common_scripts/bastion-scripts/requirements.txt"
python3 sync-users.py