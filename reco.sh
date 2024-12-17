#!/bin/bash
source /cvmfs/ara.opensciencegrid.org/trunk/centos7/setup.sh
source /home/pgiri/research/software/GeneralAnalysis/For_Analysis_variables/MF_filters/setup.sh
#source /home/mkim/analysis/MF_filters/setup.sh
export OUTPUT_PATH=/data/ana/ARA
export RAW_PATH=/data/exp/ARA
echo " Running ..... "
jobIndex=$1
index2=$jobIndex+1
data=`awk "NR==\$index2" A5.txt`  
#/home/pgiri/research/software/GeneralAnalysis/For_Analysis_variables/MF_filters/Pawan/All_A4.txt`
#python chunk_rpr.py -d $data -p $ped -o $output
python livetime_finder.py -d $data -s 5
echo "Completed"
