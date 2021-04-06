#!/bin/sh
# Get a list of all missing bins in target output directory
ls ${1}/grid/ | grep ".root" | sed "s@.yields.root@@g" |sort |uniq > producedBins_grid.md
ls ${1}/scan/ | grep ".root" | sed "s@.yields.root@@g" |sort |uniq > producedBins_scan.md
ls ${1}/grid-dilep/ | grep ".root" | sed "s@.yields.root@@g" |sort |uniq > producedBins_grid-dilep.md

# List all current search bins
python searchBins_0b_with_NW.py | sort | uniq > searchBins.md

# Produce a file with only the missing bins which can be read in by searchBins.py as a missingBins list which delets all bins from the cutDict to only produce the missing bins
grep -v -x -f producedBins_grid.md searchBins.md | sed "s@_SR@@g" | sed "s@_CR@@g" | sort | uniq > missingBins_grid.md
grep -v -x -f producedBins_scan.md searchBins.md | sed "s@_SR@@g" | sed "s@_CR@@g" | sort | uniq > missingBins_scan.md
grep -v -x -f producedBins_grid-dilep.md searchBins.md | sed "s@_SR@@g" | sed "s@_CR@@g" | sort | uniq > missingBins_grid-dilep.md
