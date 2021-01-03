#!/bin/bash
cd /var/services/homes/weikun_ict/FatGrap
nohup ./do_work.sh $1 >/dev/null 2>&1 &
ps -aux|grep $1 |grep python|grep -v "grep"
exit 0