#!/bin/bash
source /etc/profile
cd /var/services/homes/weikun_ict/FatGrap
export PYTHONPATH=$PYTHONPATH:/var/services/homes/weikun_ict/FatGrap
fileName=$1
fileName=${fileName%.*}
python example/example.py
