#!/usr/bin/env python

import numpy as np
import glob, os, sys, math
from math import hypot
from ROOT import *

from readYields import getYield


def getDirNames(fname):

    tfile = TFile(fname,"READ")

    dirList = [dirKey.ReadObj().GetName() for dirKey in gDirectory.GetListOfKeys() if dirKey.IsFolder() == 1]

    tfile.Close()

    return dirList

def getHnames(fname,tdir):

    tfile = TFile(fname,"READ")
    tfile.cd(tdir)

    hnames = []

    for key in gDirectory.GetListOfKeys():

        obj = key.ReadObj()
        hnames.append(obj.GetName())

    tfile.Close()

    return hnames

def GetUpDownList(fname):

    tfile = TFile(fname,"READ")

    uplist = []
    downlist = []

    for k in tfile.GetListOfKeys():
        histname=k.ReadObj().GetName()
        if "Up" in histname:
            uplist.append(histname)
        if "Down" in histname:
            downlist.append(histname)

    return uplist,downlist

def getSystHist(tfile, hname, syst = "Xsec"):
    if "Env" in syst or "RMS" in syst:
        print("why are you here?")
        return 0
    else:

        upName = hname + '_' + syst + '-Up'
        dnName = hname + '_' + syst + '-Down'

        hNorm = tfile.Get(hname)
        hUp = tfile.Get(upName)
        hDown = tfile.Get(dnName)

        if not hUp and hDown:
            # Replace missing Up with Down
            hUp = hDown
        elif not hDown and hUp:
            # Replace missing Down with Up
            hDown = hUp
        elif not hUp or not hDown:
            return (1,2,3)


        hSyst = hNorm.Clone(hNorm.GetName() + '_' + syst + '_syst')

        hUpVar = hNorm.Clone(hNorm.GetName() + '_' + syst + '_upVar')
        hUpVar.Add(hUp,-1)

        hDownVar = hNorm.Clone(hNorm.GetName() + '_' + syst + '_downVar')
        hDownVar.Add(hDown,-1)

        # find maximum deviations
        for xbin in range(1,hSyst.GetNbinsX()+1):
            for ybin in range(1,hSyst.GetNbinsY()+1):

                # reset bins
                hSyst.SetBinContent(xbin,ybin,0)
                hSyst.SetBinError(xbin,ybin,0)

                maxDev = 0
                maxErr = 0

                #fill with average deviation
                maxDev = 1/2.*(math.fabs(hUpVar.GetBinContent(xbin,ybin))+math.fabs(hDownVar.GetBinContent(xbin,ybin)))

                if hNorm.GetBinContent(xbin,ybin) > 0:
                    maxDev /= hNorm.GetBinContent(xbin,ybin)

                # limit max deviation to 200%
                maxDev = min(maxDev,2.0)

                hSyst.SetBinContent(xbin,ybin,maxDev)
                hSyst.SetBinError(xbin,ybin,maxErr)

        return (hSyst,hUpVar,hDownVar)


def makeSystHists(fileList): #direc,
    if 'signal_' in path:
	    hnames = ["T5qqqqWW_Scan"] # process name
    else:
        hnames = ['EWK', 'DY', 'QCD', 'SingleT', 'TTJets', 'TTV', 'VV', 'WJets']

    # systematic alawys first subdirectory
    print "path =", path
    print path.split("/")
    if "run2" in path:
        systNames = [path.split("/")[1].split("_")[1] + "_" + path.split("/")[1].split("_")[2]]
    else:
        systNames = [path.split("/")[1].split("_")[1]]

    #bindirs =  ['SR_MB','CR_MB','SR_SB','CR_SB']
    #bindirs =  ['SR_MB','CR_MB','SR_SB','CR_SB','Kappa','Rcs_MB','Rcs_SB']

    #from IPython import embed;embed()

    bindirs = getDirNames(fileList[0])
    #print("Found those dirs:", bindirs)
    bindirs = [bin for bin in bindirs if "DL" not in bin]

    #uplist, downlist = GetUpDownList(fileList[0])
    #print(uplist, downlist)
    # dir to store
    sysdir =  "syst/" #direc +
    if not os.path.exists(sysdir): os.makedirs(sysdir)

    #from IPython import embed;embed()

    for fname in fileList:

        tfile = TFile(fname,"UPDATE")
        #tfile = TFile(fname,"READ")
        #sysname = sysdir + os.path.basename(fname)
        #sfile = TFile(sysname,"RECREATE")

        for bindir in bindirs:

            for hname in hnames:
                for syst in systNames:
                    #if "xsec" in syst and "TTJets" in hname and "Kappa" in bindir:
                    #if "Kappa" in bindir and "xsec" in syst:
                    #print(bindir, hname, syst)
                    if bindir != "":
                        (hSyst,hUp,hDown) = getSystHist(tfile, bindir+'/'+ hname, syst)
                    else:
                        (hSyst,hUp,hDown) = getSystHist(tfile, hname, syst)

                    #from IPython import embed;embed()
                    if (hSyst,hUp,hDown) == (1,2,3):
                        # this is a kinda hacky way, but it doesn't take to long. If performance is an issue, look here
                        # only the working systematics get included, the rest is passed
                        # so KappaTT for TTJets is working, but all other processes are skipped
                        # Advantage: generalizes the processing, don't have to check for working configurations
                        continue

                    if hSyst:
                        tfile.cd(bindir)
                        #sfile.mkdir(bindir)
                        #sfile.cd(bindir)
                        hSyst.Write("",TObject.kOverwrite)
                        #print(hname, syst)
                        #hUp.Write("",TObject.kOverwrite)
                        #hDown.Write("",TObject.kOverwrite)

                        #from IPython import embed;embed()

            '''
            # create Syst folder structure
            if not tfile.GetDirectory(bindir+"/Syst"):
            tfile.mkdir(bindir+"/Syst")
            for hname in hnames:
            for syst in systNames:
            tfile.cd(bindir+"/Syst")
            hSyst = getSystHist(tfile, bindir+'/'+ hname, syst)
            hSyst.Write()
            else:
            print 'Already found syst'
            '''

        tfile.Close()
        #from IPython import embed;embed()
    return 1

def combineOtherBkgs(fileList):
    # hardcode MC hists to avoid kappa or repition errors
    bindirs =  ['SR_MB','CR_MB','SR_SB','CR_SB', "SR_SB_NB1i", "CR_SB_NB1i", "SR_SB_NB0", "CR_SB_NB0"]
    other_bkgs = ["DY", "SingleT", "TTV", "VV"]

    for fname in fileList:
        tfile = TFile(fname,"UPDATE")
        for bind in bindirs:
            # start with EWK always, so we have a tObject to add onto

            #systNames = [path.split("/")[1].split("_")[1] + "_" + path.split("/")[1].split("_")[2]]

            if "run2" in path:
                systNames = [path.split("/")[1].split("_")[1] + "_" + path.split("/")[1].split("_")[2]]
            else:
                systNames = [path.split("/")[1].split("_")[1]]

            assert len(systNames)==1
            DY_syst = tfile.Get(bind+"/DY_"+systNames[0]+"_syst").Clone()
            for other in other_bkgs[1:]:
                other_syst = tfile.Get(bind+"/{}_{}_syst".format(other,systNames[0])).Clone()
                #from IPython import embed; embed()
                DY_syst.Add(other_syst)

            tfile.cd(bind)
            DY_syst.SetName("other_bkg_{}_syst".format(systNames[0]))
            DY_syst.Write("",TObject.kOverwrite)
        tfile.Close()
    return 1


if __name__ == "__main__":

    ## remove '-b' option
    _batchMode = False

    if '-b' in sys.argv:
        sys.argv.remove('-b')
        _batchMode = True

    if len(sys.argv) > 1:
        pattern = sys.argv[1]
        print('# pattern is', pattern)
    else:
        print("No pattern given!")
        exit(0)

    # find files matching pattern
    fList = glob.glob(pattern+"*.root")

    for root, dirs, files in os.walk(pattern):

        #print(root, dirs)
        for direc in dirs:
            #if "signal" in direc:
            if "signal" in direc or "syst" in direc:
                path = pattern +"/"+ direc
                for ro,di,fi in os.walk(path):
                    for d in di:
                        if "merged" == d:
                            fileList=[]
                            path = path +"/"+ d
                            print("doing systs for:",path)
                            for r,d,f in os.walk(path):
                                for file in f:
                                    if ".root" in file:
                                        fileList.append(path+"/"+file)

                            makeSystHists(fileList)

                            if "syst" in direc:
                                combineOtherBkgs(fileList)

    print('Finished')
