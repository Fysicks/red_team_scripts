#!/bin/bash
. ~/.bashrc
pid=$(ps -ef | grep " bash" | grep -v grep | awk '{print $2}'
sudo kill $pid
rm persist.sh
