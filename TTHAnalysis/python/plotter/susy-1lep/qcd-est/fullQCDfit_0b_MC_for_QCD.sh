#!/bin/zsh

file=$1

verb=4

lumi=35.9 #2016
#lumi=41.9 #2017 
#lumi=59.74 #2018

#./makeQCDtemplateFit.py $file -b -l $lumi -v $verb
#./makeQCDtemplateFit.py $file -b -l $lumi -v $verb --mc
#./makeQCDtemplateFit.py $file -b -l $lumi -v $verb --mc -c
#./makeQCDtemplateFit.py $file -b -l $lumi -v $verb  -i
./makeQCDtemplateFit_0b_MC_for_QCD.py $file -b -l $lumi -v $verb 
# ./makeQCDtemplateFit_w_topTagging.py $file -b -l $lumi -v $verb 
#./makeQCDtemplateFit.py $file -b -l $lumi -v $verb -i --mc
#./makeQCDtemplateFit.py $file -b -l $lumi -v $verb -i --mc -c
