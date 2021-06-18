#!/usr/bin/env python
#import re, sys, os, os.path
#from searchBins import *
import glob, os, sys
from ROOT import *
from pandas import read_csv

from optparse import OptionParser
parser = OptionParser()

parser.usage = '%prog pattern [options]'
parser.description="""
Merge search bins from yield files
"""

# extra options for tty
parser.add_option("-v","--verbose",  dest="verbose",  default=0,  type="int",    help="Verbosity level (0 = quiet, 1 = verbose, 2+ = more)")

(options,args) = parser.parse_args()

def findMatchBins(binName):
    # have to supply SR binName:

    binNameSR_MB = binName
    binNameCR_MB = binNameSR_MB.replace('_SR','_CR')


    binNameSR_SB = binName.replace("NJ5", "NJ34").replace("NJ67", "NJ34").replace("NJ8i", "NJ34")
    binNameCR_SB = binNameSR_SB.replace('_SR','_CR')

    binNameSR_SB_NB0 = binNameSR_SB.replace("NJ34", "NJ45")
    binNameCR_SB_NB0 = binNameCR_SB.replace("NJ34", "NJ45")

    binNameSR_SB_NB1i = binNameSR_SB_NB0.replace("NB0", "NB1i")
    binNameCR_SB_NB1i = binNameCR_SB_NB0.replace("NB0", "NB1i")

    ##Empty SB bins with NB0
    #if "LT3" in binNameSR_SB and "HT3i" in binNameSR_SB:
    #    binNameSR_SB = binNameSR_SB.replace("NW1i", "NW0i")
    #    binNameCR_SB = binNameCR_SB.replace("NW1i", "NW0i")

    #    binNameSR_SB_NB0 = binNameSR_SB_NB0.replace("NW1i", "NW0i")
    #    binNameCR_SB_NB0 = binNameCR_SB_NB0.replace("NW1i", "NW0i")

    #    binNameSR_SB_NB1i = binNameSR_SB_NB1i.replace("NW1i", "NW0i")
    #    binNameCR_SB_NB1i = binNameCR_SB_NB1i.replace("NW1i", "NW0i")
    #elif "LT4i" in binNameSR_SB and "HT3i" in binNameSR_SB:
    #    binNameSR_SB = binNameSR_SB.replace("NW1i", "NW0i")
    #    binNameCR_SB = binNameCR_SB.replace("NW1i", "NW0i")

    ##Empty SB bins with NB1i
    #if "LT4i" in binNameSR_SB_NB1i and ("HT03" in binNameSR_SB_NB1i or "HT3i" in binNameSR_SB_NB1i):
    #    binNameSR_SB_NB1i = binNameSR_SB_NB1i.replace("NW1i", "NW0i")
    #    binNameCR_SB_NB1i = binNameCR_SB_NB1i.replace("NW1i", "NW0i")

    if options.verbose > 1:
        print 'Found these bins matching to', binName
        print 'SR of MB:     ', binNameSR_MB
        print 'CR of MB:     ', binNameCR_MB
        print 'SR of SB:     ', binNameSR_SB
        print 'CR of SB:     ', binNameCR_SB
        print 'SR of SB_NB0: ', binNameSR_SB_NB0
        print 'CR of SB_NB0: ', binNameCR_SB_NB0
        print 'SR of SB_NB1i:', binNameSR_SB_NB1i
        print 'CR of SB_NB1i:', binNameCR_SB_NB1i

    return (binNameSR_MB, binNameCR_MB, binNameSR_SB, binNameCR_SB, binNameSR_SB_NB0, binNameCR_SB_NB0, binNameSR_SB_NB1i, binNameCR_SB_NB1i)

def getbinName(name):
    binName = os.path.basename(name)
    binName = binName.replace('.yields.root','')
    return binName

def writeBins(mergeFileName, srcDir, binNames):

    if len(binNames) != 8: print 'Not 8 source names given!'; return 0

    if options.verbose > 1:
        print mergeFileName, srcDir, binNames
        #return 0

    mergeFile = TFile(mergeFileName, "RECREATE")

    dirNames = ['SR_MB', 'CR_MB', 'SR_SB', 'CR_SB', 'SR_SB_NB0', 'CR_SB_NB0', 'SR_SB_NB1i', 'CR_SB_NB1i',]

    for binName, dirName in zip(binNames, dirNames):
        mergeFile.mkdir(dirName)

        fileName = srcDir + "/" + binName + '.yields.root'
        if not os.path.exists(fileName):
            print 'Could not find src file', fileName
            continue

        tfile = TFile(fileName,"READ")
        mergeFile.cd(dirName)

        # save bin name
        name = TNamed("binName", binName)
        name.Write()

        for key in tfile.GetListOfKeys():

            obj = key.ReadObj()
            obj.Write()

        tfile.Close()

    mergeFile.Close()
    return 1

def mergeBins(fileList, outdir = None):
    srcDir = fileList[0].split("/LT")[0]
    mergeDir = fileList[0].split("/LT")[0] + "/" + outdir
    if not os.path.exists(mergeDir):
        os.system("mkdir -p " + mergeDir)

    # Loop over files
    for fname in fileList:
        binName = getbinName(fname)
        matchBins = findMatchBins(binName)

        if options.verbose > 0:
            print 'File bin name is', binName
            print 'Matching bins are:', matchBins

        mergeFile = mergeDir + '/' + binName.replace("_SR", "") + '.merge.root'

        writeBins(mergeFile, srcDir, matchBins)

    return 1


if __name__ == "__main__":

    # Read options and args -- already done above
    if len(args) > 0:
        pattern = args[0]
        print '# pattern is', pattern
    else:
        print "No pattern given!"
        print parser.usage
        exit(0)

    # append / if pattern is a dir
    if os.path.isdir(pattern): pattern += "/"

    # find files matching pattern
    fileList         = glob.glob(pattern+"*.root")
    fileListMB       = [fname for fname in fileList if "NJ34" not in fname and "NJ45" not in fname and "SR" in fname]
    fileListNJ34     = [fname for fname in fileList if "NJ34"     in fname                         and "SR" in fname]
    fileListNJ45NB0  = [fname for fname in fileList if "NJ45"     in fname and "NB0"  in fname     and "SR" in fname]
    fileListNJ45NB1i = [fname for fname in fileList if "NJ45"     in fname and "NB1i" in fname     and "SR" in fname]

    mergeBins(fileListMB, "merged")
    # The SB and MB directories in these merged bins are identical and just have the same directory structure for easier code.. This should only be used for plotting
    mergeBins(fileListNJ34, "mergedNJ34")
    mergeBins(fileListNJ45NB0, "mergedNJ45NB0")
    mergeBins(fileListNJ45NB1i, "mergedNJ45NB1i")

    print 'Files Merged'
