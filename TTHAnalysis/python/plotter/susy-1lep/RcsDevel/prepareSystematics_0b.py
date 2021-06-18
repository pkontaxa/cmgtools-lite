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

#def writeBins(mergeFileName, srcDir, binNames):
def writeBins(systName16, mergeDir):

    systematic = systName16.split("/")[1]
    binFileName = systName16.split("/")[2]
    systName17 = systName16.replace("2016", "2017")
    systName18 = systName16.replace("2016", "2018")

    #skip isr for nowq
    if "ISR" in systematic:
        return 1

    if "syst_" in systName16:
        fileName16 = systName16.split("/")[0] + "/grid/" + binFileName
        fileName17 = systName17.split("/")[0] + "/grid/" + binFileName
        fileName18 = systName18.split("/")[0] + "/grid/" + binFileName
    elif "signal_" in systName16:
        fileName16 = systName16.split("/")[0] + "/scan/" + binFileName
        fileName17 = systName17.split("/")[0] + "/scan/" + binFileName
        fileName18 = systName18.split("/")[0] + "/scan/" + binFileName
    else:
        print "Check your " + systName16 + "! It should be a systematic variation!"

    if "2016" not in fileName16:
        print "Your input dir is supposed to contain 2016 in order to fetch the correct files and get the correct target dir!"
        exit()

    if not os.path.exists(fileName16):
        print 'Could not find src file', fileName16
        exit()
    if not os.path.exists(fileName17):
        print 'Could not find src file', fileName17
        exit()
    if not os.path.exists(fileName18):
        print 'Could not find src file', fileName18
        exit()


    tFile16 = TFile.Open(fileName16, "READ")
    systFile16 = TFile.Open(systName16, "READ")

    systNameRun2_16 = mergeDir + "/" + systematic + "_2016"
    systFileRun2_16 = TFile.Open(systNameRun2_16 + "/" + binFileName, "RECREATE")

    systHistList16 = systFile16.GetListOfKeys()
    nominalHistList16 = tFile16.GetListOfKeys()

    if not os.path.exists(systNameRun2_16):
        os.makedirs(systNameRun2_16)

    tFile17 = TFile.Open(fileName17, "READ")
    systFile17 = TFile.Open(systName17, "READ")

    systNameRun2_17 = mergeDir + "/" + systematic + "_2017"
    systFileRun2_17 = TFile.Open(systNameRun2_17 + "/" + binFileName, "RECREATE")

    systHistList17 = systFile17.GetListOfKeys()
    nominalHistList17 = tFile17.GetListOfKeys()

    if not os.path.exists(systNameRun2_17):
        os.makedirs(systNameRun2_17)

    tFile18 = TFile.Open(fileName18, "READ")
    systFile18 = TFile.Open(systName18, "READ")

    systNameRun2_18 = mergeDir + "/" + systematic + "_2018"
    systFileRun2_18 = TFile.Open(systNameRun2_18 + "/" + binFileName, "RECREATE")

    systHistList18 = systFile18.GetListOfKeys()
    nominalHistList18 = tFile18.GetListOfKeys()

    if not os.path.exists(systNameRun2_18):
        os.makedirs(systNameRun2_18)

    for key16, key17, key18 in zip(nominalHistList16, nominalHistList17, nominalHistList18):

        keyName = key16.GetName()
        #print keyName
        if "data" in keyName or "background" in keyName or "TTdiLep" in keyName or "TTsemiLep" in keyName:
            continue

        nominalHist16 = key16.ReadObj()
        nominalHist17 = key17.ReadObj()
        nominalHist18 = key18.ReadObj()

        systName = systematic.split("_")[1]

        systUpHist16 = systHistList16.FindObject(keyName + "_" + systName + "-Up").ReadObj()
        systDownHist16 = systHistList16.FindObject(keyName + "_" + systName + "-Down").ReadObj()

        nominalHistRun2_16 = nominalHist16.Clone()
        nominalHistRun2_16.Add(nominalHist17)
        nominalHistRun2_16.Add(nominalHist18)

        systUpHistRun2_16 = systUpHist16.Clone()
        systUpHistRun2_16.Add(nominalHist17)
        systUpHistRun2_16.Add(nominalHist18)

        systDownHistRun2_16 = systDownHist16.Clone()
        systDownHistRun2_16.Add(nominalHist17)
        systDownHistRun2_16.Add(nominalHist18)

        systFileRun2_16.cd()
        nominalHistRun2_16.SetName(nominalHistRun2_16.GetName().replace("-", "_2016-"))
        nominalHistRun2_16.Write()

        systUpHistRun2_16.SetName(systUpHistRun2_16.GetName().replace("-", "_2016-"))
        systUpHistRun2_16.Write()

        systDownHistRun2_16.SetName(systDownHistRun2_16.GetName().replace("-", "_2016-"))
        systDownHistRun2_16.Write()

        systUpHist17 = systHistList17.FindObject(keyName + "_" + systName + "-Up").ReadObj()
        systDownHist17 = systHistList17.FindObject(keyName + "_" + systName + "-Down").ReadObj()

        nominalHistRun2_17 = nominalHist17.Clone()
        nominalHistRun2_17.Add(nominalHist16)
        nominalHistRun2_17.Add(nominalHist18)

        systUpHistRun2_17 = systUpHist17.Clone()
        systUpHistRun2_17.Add(nominalHist16)
        systUpHistRun2_17.Add(nominalHist18)

        systDownHistRun2_17 = systDownHist17.Clone()
        systDownHistRun2_17.Add(nominalHist16)
        systDownHistRun2_17.Add(nominalHist18)

        systFileRun2_17.cd()
        nominalHistRun2_17.SetName(nominalHistRun2_17.GetName().replace("-", "_2017-"))
        nominalHistRun2_17.Write()
        systFileRun2_17.cd()
        systUpHistRun2_17.SetName(systUpHistRun2_17.GetName().replace("-", "_2017-"))
        systUpHistRun2_17.Write()
        systFileRun2_17.cd()
        systDownHistRun2_17.SetName(systDownHistRun2_17.GetName().replace("-", "_2017-"))
        systDownHistRun2_17.Write()

        systUpHist18 = systHistList18.FindObject(keyName + "_" + systName + "-Up").ReadObj()
        systDownHist18 = systHistList18.FindObject(keyName + "_" + systName + "-Down").ReadObj()

        nominalHistRun2_18 = nominalHist18.Clone()
        nominalHistRun2_18.Add(nominalHist16)
        nominalHistRun2_18.Add(nominalHist17)

        systUpHistRun2_18 = systUpHist18.Clone()
        systUpHistRun2_18.Add(nominalHist16)
        systUpHistRun2_18.Add(nominalHist17)

        systDownHistRun2_18 = systDownHist18.Clone()
        systDownHistRun2_18.Add(nominalHist16)
        systDownHistRun2_18.Add(nominalHist17)

        systFileRun2_18.cd()
        nominalHistRun2_18.SetName(nominalHistRun2_18.GetName().replace("-", "_2018-"))
        nominalHistRun2_18.Write()
        systFileRun2_18.cd()
        systUpHistRun2_18.SetName(systUpHistRun2_18.GetName().replace("-", "_2018-"))
        systUpHistRun2_18.Write()
        systFileRun2_18.cd()
        systDownHistRun2_18.SetName(systDownHistRun2_18.GetName().replace("-", "_2018-"))
        systDownHistRun2_18.Write()

    tFile16.Close()
    tFile17.Close()
    tFile18.Close()

    systFile16.Close()
    systFile17.Close()
    systFile18.Close()

    systFileRun2_16.Close()
    systFileRun2_17.Close()
    systFileRun2_18.Close()

    return 1

def mergeBins(fileList, outdir = None):
    srcDir = fileList[0].split("/LT")[0]
    mergeDir = fileList[0].split("/")[0]
    if outdir != None:
        mergeDir = mergeDir + "/" + outdir
    mergeDir = mergeDir.replace("2016", "run2_prepSyst")
    print "MergeDir", mergeDir
    if not os.path.exists(mergeDir):
        os.system("mkdir -p " + mergeDir)

    # Loop over files
    for fname in fileList:

        if options.verbose > 0:
            print 'File bin name is', binName

        writeBins(fname, mergeDir)
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
    fileList = glob.glob(pattern+"*.root")

    mergeBins(fileList)
    print 'Systematics files Prepared'
