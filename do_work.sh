#!/bin/bash
source /etc/profile
cd /var/services/homes/weikun_ict/FatGrap
export PYTHONPATH=$PYTHONPATH:/var/services/homes/weikun_ict/FatGrap
fileName=$1
fileName=${fileName%.*}
#cmd="nohup python $1 >$fileName.log 2>&1 &"
python $1 > $fileName.log
