#!/bin/sh
input=$1
year=$2
# List all current search bins
python searchBins_0b_with_NW.py | sort | uniq > searchBins.md
# Get a list of all missing bins in target output directory
for dir in  grid signal_btagLF syst_JEC syst_TTxsec syst_btagHF grid-dilep signal_JEC syst_DLConst syst_PU syst_Wpol syst_btagLF scan signal_btagHF syst_DLSlope syst_TTVxsec syst_Wxsec syst_lepSF;
do
	ls ${input}/${dir} | grep ".root" | sed "s@.yields.root@@g" |sort |uniq > producedBins_${dir}_${year}.md
	grep -v -x -f producedBins_${dir}_${year}.md searchBins.md | sed "s@_SR@@g" | sed "s@_CR@@g" | sort | uniq > missingBins_${dir}_${year}.md
done
