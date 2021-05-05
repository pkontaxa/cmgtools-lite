#!/bin/sh
input=$1
year=$2
# List all current search bins
python searchBins_0b_with_NW.py | sort | uniq > searchBins.md
# Get a list of all missing bins in target output directory
for dir in grid scan grid-dilep;
do
	ls ${input}/${dir} | grep ".root" | sed "s@.yields.root@@g" |sort |uniq > producedBins_${dir}_${year}.md
	grep -v -x -f producedBins_${dir}_${year}.md searchBins.md | sed "s@_SR@@g" | sed "s@_CR@@g" | sort | uniq > missingBins_${dir}_${year}.md
done
