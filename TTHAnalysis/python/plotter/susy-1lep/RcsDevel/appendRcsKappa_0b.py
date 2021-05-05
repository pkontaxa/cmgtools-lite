#!/usr/bin/env python
#import re, sys, os, os.path

import glob, os, sys
from math import hypot, sqrt
from ROOT import *
from pandas import read_csv, Series

from readYields import getYield

def getSamples(fname,tdir):

    tfile = TFile(fname,"READ")
    tfile.cd(tdir)

    samples = []

    for key in gDirectory.GetListOfKeys():

        obj = key.ReadObj()
        if "TH" in obj.ClassName():
            samples.append(obj.GetName())

    tfile.Close()

    return samples

def getRcsHist(tfile, hname, band = "SB", merge = True):

    hSR = tfile.Get("SR_" + band + "/" + hname).Clone()
    hCR = tfile.Get("CR_" + band + "/" + hname).Clone()

    #Add Rare Files for WJets calculation in the SB
    if "WJets" in hname and band == "SB":
        for rareSample in ["DY", "SingleT", "TTV", "VV"]:
            tmpHSR = tfile.Get("SR_" + band + "/" + hname.replace("WJets", rareSample))
            tmpHCR = tfile.Get("CR_" + band + "/" + hname.replace("WJets", rareSample))
            hSR.Add(tmpHSR)
            hCR.Add(tmpHCR)

    hRcs = hSR.Clone(hSR.GetName().replace('x_','Rcs_'))
    hRcs.Divide(hCR)
    hRcs.GetYaxis().SetTitle("Rcs")

    # merge means ele/mu values are overwritten by the combined Rcs
    if 'data' in hname: merge = True

    if merge:
        rcs = -999; err = -999;
        #The SB for the WJets Rcs calculation should use the values from muons
        if "WJets" in hname and band == "SB":
            rcs = hRcs.GetBinContent(1,2); err = hRcs.GetBinError(1,2) # mu sele
        else:
            rcs = hRcs.GetBinContent(2,2); err = hRcs.GetBinError(2,2) # lep sele

        hRcs.SetBinContent(1,2,rcs); hRcs.SetBinError(1,2,err) # mu sele
        hRcs.SetBinContent(2,2,rcs); hRcs.SetBinError(2,2,err) # lep sele
        hRcs.SetBinContent(3,2,rcs); hRcs.SetBinError(3,2,err) # ele sele

    return hRcs

def getRcsCorrHist(tfile, hTTbarFraction, hname, band = "SB", merge = True):

    hSR = tfile.Get("SR_" + band + "/"  +  hname)
    hCR = tfile.Get("CR_" + band + "/"  +  hname)

    hUnity = hSR.Clone("Unity")
    hUnity.SetBinContent(1,2,1); hUnity.SetBinError(1,2,0) # mu sele
    hUnity.SetBinContent(2,2,1); hUnity.SetBinError(2,2,0) # lep sele
    hUnity.SetBinContent(3,2,1); hUnity.SetBinError(3,2,0) # ele sele

    hUnity.SetBinContent(1,1,1); hUnity.SetBinError(1,1,0) # mu sele
    hUnity.SetBinContent(2,1,1); hUnity.SetBinError(2,1,0) # lep sele
    hUnity.SetBinContent(3,1,1); hUnity.SetBinError(3,1,0) # ele sele

    if "data" not in hname:
        hRcsTTJets = tfile.Get("Rcs_SB_NB0_TT/TTJets")
    else:
        hRcsTTJets = tfile.Get("Rcs_SB_NB0_TT/data_QCDsubtr")

    hTTPredict = hCR.Clone()
    hTTPredict.Multiply(hRcsTTJets)
    hTTPredict.Multiply(hTTbarFraction)

    hTTbarFractionInverse = hUnity.Clone()
    hTTbarFractionInverse.Add(hTTbarFraction, -1)

    hRcs = hSR.Clone()
    hRcs.Add(hTTPredict, -1)
    hRcs.Divide(hTTbarFractionInverse)
    hRcs.Divide(hCR)

    hRcs.GetYaxis().SetTitle("Rcs")




    # Using events with only muons in the sideband excludes QCD contamination
    if merge:
        rcs = hRcs.GetBinContent(1,2); err = hRcs.GetBinError(1,2) # mu sele

        hRcs.SetBinContent(2,2,rcs); hRcs.SetBinError(2,2,err) # lep sele
        hRcs.SetBinContent(3,2,rcs); hRcs.SetBinError(3,2,err) # ele sele

    return hRcs

def getPredHist(tfile, hname):

    hRcsMB = tfile.Get("Rcs_SB/"+hname)

    if ('data' in hname) or ("background" in hname) or ("poisson" in hname):
        # use EWK template
        hKappa = tfile.Get("Kappa/EWK")
        if not hKappa: hKappa = tfile.Get("Kappa/"+hname)
    else:
        hKappa = tfile.Get("Kappa/"+hname)

    # get yield from CR of MB
    hCR_MB = tfile.Get("CR_MB/"+hname)

    hPred = hCR_MB.Clone(hCR_MB.GetName())#+"_pred")
    #hPred.SetTitle("Predicted yield")

    hPred.Multiply(hRcsMB)
    hPred.Multiply(hKappa)

    return hPred

def readQCDratios(fname = "lp_LTbins_NJ34_f-ratios_MC.txt"):

    fDict = {}

    with open(fname) as ftxt:
        lines = ftxt.readlines()

        for line in lines:
            if line[0] != '#':
                (bin,rat,err) = line.split()
                bin = bin.replace("_NJ34","")
                if 'LT' in bin:
                    fDict[bin] = (float(rat),float(err))

    #print 'Loaded f-ratios from file', fname
    #print fDict

    return fDict

def getPoissonHist(tfile, sample = "background", band = "CR_MB"):
    # sets all bin errors to sqrt(N)

    hist = tfile.Get(band+"/"+sample).Clone(sample+"_poisson")

    if "TH" not in hist.ClassName(): return 0

    for ix in range(1,hist.GetNbinsX()+1):
        for iy in range(1,hist.GetNbinsY()+1):
            hist.SetBinError(ix,iy,sqrt(hist.GetBinContent(ix,iy)))

    return hist


# Systematic error on F-ratio
qcdSysts = {
        'NJ45' : 0.15,
        'NJ68' : 0.30,
        'NJ9'  : 0.50
}

def getQCDsystError(binname):

    # Set 100% syst if NB >= 3
    for nbbin in ['NB3']:
        if nbbin in binname:
            return 1.0

    for njbin in qcdSysts.keys():
        if njbin in binname:
            #print binname, njbin, qcdSysts[njbin]
            return qcdSysts[njbin]
    # If no bin is found, return 100 % uncertainty
    return 1.0

def getQCDsubtrHistos(tfile, sample = "background", band = "CR_MB/", isMC = True, applySyst = True, lep = "ele", year = "2016"):
    ## returns two histograms:
    ## 1. QCD prediction from anti-leptons
    ## 2. Original histo - QCD from prediction

    ## Get fRatios for electrons
    fRatio = 0.3 # default
    fRatioErr = 0.01 # default

    fRatios = {}
    '''Pantelis
    if isMC: fRatios = readQCDratios("fRatios_MC_lumi36p5_Spring16.txt")
    else: fRatios = readQCDratios("fRatios_Data_lumi36p5_Spring16.txt")
    Pantelis'''

    #TTHAnalysis/python/plotter/susy-1lep/RcsDevel/
    if isMC: fRatios = readQCDratios("Lp_LTbins_0b_" + year + "_f-ratios_MC.txt")
    else: fRatios = readQCDratios("Lp_LTbins_0b_" + year + "_f-ratios_MC.txt")

    # read bin name
    binString = tfile.Get(band+"BinName")
    if binString: binName = binString.GetTitle()
    else: binName = tfile.GetName()

    # get bin from filename
    for key in fRatios:
        #print key, binName
        if key in binName:
            (fRatio,fRatioErr) = fRatios[key]
            #print "Found matching ratios for key" , key
            break
        #else: print "No corresp fRatio found! Using default."

    # get QCD syst error pn F
    if applySyst == True:
        systErr = getQCDsystError(binName)

        #print "Fratio\t%f, old error\t%f, new error\t%f" %(fRatio,fRatioErr,hypot(fRatioErr,systErr*fRatio))
        fRatioErr = hypot(fRatioErr,systErr*fRatio)
        # make sure error not bigger than value itself
        fRatioErr = min(fRatioErr,fRatio)

    ## fRatios for muons
    fRatioMu = 0.1; fRatioMuErr = 1.00 * fRatioMu

    ############################
    # Get original histo
    hOrig = tfile.Get(band+sample) # original histogram
    if not hOrig: return 0

    ## 1. QCD prediction
    hQCDpred = hOrig.Clone(sample+"_QCDpred")
    hQCDpred.Reset() # reset counts/errors

    if lep == "ele" :
        # take anti-selected ele yields
        yAnti = hOrig.GetBinContent(3,1); yAntiErr = hOrig.GetBinError(3,1);

        # apply f-ratio
        yQCDFromAnti = fRatio*yAnti
        yQCDFromAntiErr = hypot(yAntiErr*fRatio,yAnti*fRatioErr)
        # make sure error is not bigger than value
        yQCDFromAntiErr = min(yQCDFromAntiErr, yQCDFromAnti)

        # set bin content for ele
        hQCDpred.SetBinContent(3,2,yQCDFromAnti)
        hQCDpred.SetBinError(3,2,yQCDFromAntiErr)

        # set bin content for lep (=ele)
        hQCDpred.SetBinContent(2,2,yQCDFromAnti)
        hQCDpred.SetBinError(2,2,yQCDFromAntiErr)
    elif lep == "lep":

        ## Electrons
        # take anti-selected ele yields
        yAntiEle = hOrig.GetBinContent(3,1); yAntiEleErr = hOrig.GetBinError(3,1);

        # apply f-ratio
        yQCDFromAntiEle = fRatio*yAntiEle
        yQCDFromAntiEleErr = hypot(yAntiEleErr*fRatio,yAntiEle*fRatioErr)
        # make sure error is not bigger than value
        yQCDFromAntiEleErr = min(yQCDFromAntiEleErr, yQCDFromAntiEle)

        # set bin content for ele
        hQCDpred.SetBinContent(3,2,yQCDFromAntiEle)
        hQCDpred.SetBinError(3,2,yQCDFromAntiEleErr)

        ## Muons
        # take anti-selected mu yields
        yAntiMu = hOrig.GetBinContent(1,1); yAntiMuErr = hOrig.GetBinError(1,1);

        # apply f-ratio
        yQCDFromAntiMu = fRatioMu*yAntiMu
        yQCDFromAntiMuErr = hypot(yAntiMuErr*fRatioMu,yAntiMu*fRatioMuErr)
        # make sure error is not bigger than value
        yQCDFromAntiMuErr = min(yQCDFromAntiMuErr, yQCDFromAntiMu)

        # set bin content for mu
        hQCDpred.SetBinContent(1,2,yQCDFromAntiMu)
        hQCDpred.SetBinError(1,2,yQCDFromAntiMuErr)

        # set bin content for lep (=mu+ele)
        yQCDFromAntiLep = yQCDFromAntiEle + yQCDFromAntiMu
        yQCDFromAntiLepErr = hypot(yQCDFromAntiEleErr,yQCDFromAntiMuErr)
        yQCDFromAntiLepErr = min(yQCDFromAntiLepErr,yQCDFromAntiLep)

        hQCDpred.SetBinContent(2,2,yQCDFromAntiLep)
        hQCDpred.SetBinError(2,2,yQCDFromAntiLepErr)
    elif lep == "mu":
        ## Muons
        # take anti-selected mu yields
        yAntiMu = hOrig.GetBinContent(1,1); yAntiMuErr = hOrig.GetBinError(1,1);

        # apply f-ratio
        yQCDFromAntiMu = fRatioMu*yAntiMu
        yQCDFromAntiMuErr = hypot(yAntiMuErr*fRatioMu,yAntiMu*fRatioMuErr)
        # make sure error is not bigger than value
        yQCDFromAntiMuErr = min(yQCDFromAntiMuErr, yQCDFromAntiMu)

        # set bin content for mu
        hQCDpred.SetBinContent(1,2,yQCDFromAntiMu)
        hQCDpred.SetBinError(1,2,yQCDFromAntiMuErr)

        # set bin content for lep (=ele)
        hQCDpred.SetBinContent(2,2,yQCDFromAntiMu)
        hQCDpred.SetBinError(2,2,yQCDFromAntiMuErr)
    else:
        print "QCD estimate not yet implemented for", lep
        return 0

    ############################
    ## 2. histo with QCD subtracted
    hQCDsubtr = hOrig.Clone(sample+"_QCDsubtr")

    # do QCD subtraction only in Control Region
    if 'CR' in band:
        # subtract prediction from histo
        hQCDsubtr.Add(hQCDpred,-1)

    return (hQCDpred,hQCDsubtr)

def replaceEmptyDataBinsWithMC(fileList):
    # hists to make QCD estimation
    bindirs =  ['CR_MB','SR_SB','CR_SB']
    print ''
    print "Replacing empty data bins with MC for CR_MB, SR_SB, CR_SB, 100% error"
    for fname in fileList:
        tfile = TFile(fname,"UPDATE")
        if 1==1:
            for bindir in bindirs:
                try:
                    histData = tfile.Get(bindir+"/data").Clone()
                except ReferenceError:
                    continue
                histBkg = tfile.Get(bindir+"/background").Clone()

                #if "TH" not in histData.ClassName() or 'TH' in histBkg.ClassName(): return 0

                ix = 2
                iy = 2
                if histData.GetBinContent(ix, iy) == 0:
                    print '!!! ATTENTION: replacing', fname, bindir, "bin number", ix, iy, "data", histData.GetBinContent(ix, iy), "with MC", histBkg.GetBinContent(ix,iy), 'alsp replacing sorrounding bins e, mu sel !!!'
                    histData.SetBinContent(ix, iy, histBkg.GetBinContent(ix,iy))
                    histData.SetBinError(ix, iy, histBkg.GetBinContent(ix,iy))
                    histData.SetBinContent(ix+1, iy, histBkg.GetBinContent(ix+1,iy))
                    histData.SetBinError(ix+1, iy, histBkg.GetBinContent(ix+1,iy))
                    histData.SetBinContent(ix-1, iy, histBkg.GetBinContent(ix-1,iy))
                    histData.SetBinError(ix-1, iy, histBkg.GetBinContent(ix-1,iy))

                if histData:
                    tfile.cd(bindir)
                    # overwrite old hist
                    histData.Write("",TObject.kOverwrite)
                tfile.cd()
        tfile.Close()
    print ''



def blindDataBins(fileList):
    # hists to make QCD estimation
    #bindirs =  ['SR_MB']
    bindirs =  []
    print ''
    print "Replacing empty data bins with MC for CR_MB, SR_SB, CR_SB, 100% error"
    for fname in fileList:
        tfile = TFile(fname,"UPDATE")
        if 1==1:
            for bindir in bindirs:
                ix = 2
                iy = 2
                try:
                    histData = tfile.Get(bindir+"/data").Clone()
                except ReferenceError:
                    continue
                print '!!! ATTENTION: Blinding DATA'
                histData.SetBinContent(ix, iy, 0)
                histData.SetBinError(ix, iy, 0)
                histData.SetBinContent(ix+1, iy, 0)
                histData.SetBinError(ix+1, iy, 0)
                histData.SetBinContent(ix-1, iy, 0)
                histData.SetBinError(ix-1, iy, 0)

                if histData:
                    tfile.cd(bindir)
                    # overwrite old hist
                    histData.Write("",TObject.kOverwrite)
                tfile.cd()
        tfile.Close()
    print ''

def makeQCDsubtraction(fileList, samples, year):
    # hists to make QCD estimation
    bindirs =  ['SR_MB','CR_MB','SR_SB','CR_SB','SR_SB_NB0','CR_SB_NB0','SR_SB_NB1i','CR_SB_NB1i']

    #print "Making QCD subtraction for", samples

    # Apply systematic error on F-ratio?
    applySyst = True

    for fname in fileList:
        tfile = TFile(fname,"UPDATE")

        for sample in samples:
            for bindir in bindirs:

                if 'data' in sample: isMC = False
                else: isMC = True

                #hNew = getQCDsubtrHisto(tfile,sample,bindir+"/",isMC)
                ret  = getQCDsubtrHistos(tfile,sample,bindir+"/",isMC, applySyst, "lep", year)
                #print ret

                if not ret:
                    print 'Could not create new histo for', sample, 'in bin', bindir
                else:
                    (hQCDpred,hQCDsubtr) = ret
                    tfile.cd(bindir)
                    #hNew.Write()
                    hQCDpred.Write("",TObject.kOverwrite)
                    hQCDsubtr.Write("",TObject.kOverwrite)
                tfile.cd()

        tfile.Close()

def makePoissonErrors(fileList, samples = ["background","QCD","EWK"]):
    # hists to make make poisson errors
    print "Making poisson hists for:", samples

    bindirs =  ['SR_MB','CR_MB','SR_SB','CR_SB']

    for fname in fileList:
        tfile = TFile(fname,"UPDATE")

        for sample in samples:
            for bindir in bindirs:

                hist = getPoissonHist(tfile,sample,bindir)

                if hist:
                    tfile.cd(bindir)
                    # overwrite old hist
                    hist.Write("",TObject.kOverwrite)#"",TObject.kOverwrite)
                tfile.cd()

        tfile.Close()

def makeKappaHists(fileList, samples = []):

    # get process names from file if not given
    if samples == []: samples = getSamples(fileList[0],'SR_MB')

    #print "Making Rcs and Kappa hists for:", samples

    bindirs =  ['SR_MB','CR_MB','SR_SB','CR_SB']
    #print bindirs

    for fname in fileList:
        #tfileMB = TFile(fname,"UPDATE")
        #tfileSB = TFile(fname.replace("NJ5", "NJ34").replace("NJ67", "NJ34").replace("NJ8i", "NJ34"),"UPDATE")

        #getQCDpred(tfile, 'MB')

        # create Rcs/Kappa dir struct
        if not tfile.GetDirectory("Rcs_MB"):
            tfile.mkdir("Rcs_MB")
            tfile.mkdir("Rcs_SB")
            tfile.mkdir("Kappa")

            # store SB/MB names
            sbname = tfile.Get("SR_SB/BinName")
            if sbname:
                #print sbname
                sbname.SetName("SBname")
                tfile.cd("Kappa")
                sbname.Write("",TObject.kOverwrite)

            mbname = tfile.Get("SR_MB/BinName")
            if mbname:
                mbname.SetName("MBname")
                tfile.cd("Kappa")
                mbname.Write("",TObject.kOverwrite)

            for sample in samples:

                hRcsMB = getRcsHist(tfile, sample, 'MB')
                hRcsSB = getRcsHist(tfile, sample, 'SB')

                # make kappa
                hKappa = hRcsMB.Clone(hRcsMB.GetName().replace('Rcs','Kappa'))
                hKappa.Divide(hRcsSB)

                hKappa.GetYaxis().SetTitle("Kappa")

                tfile.cd("Rcs_MB")
                hRcsMB.Write("",TObject.kOverwrite)

                tfile.cd("Rcs_SB")
                hRcsSB.Write("",TObject.kOverwrite)

                tfile.cd("Kappa")
                hKappa.Write("",TObject.kOverwrite)

        else:
            pass
            #print 'Already found Rcs and Kappa'

        '''
        yList = []
        print 'Yields for', sample
        for bindir in bindirs:
        yList.append(getYield(tfile,sample,bindir))

        print yList
        '''

        tfile.Close()

    return 1

def makeKappaTTHists(fileList, samples = []):
    # get process names from file if not given
    if samples == []: samples = list(set([sample for sample in getSamples(fileList[0],'CR_MB') if "_syst" not in sample and ("TTJets" in sample or sample == "data_QCDsubtr")]))

    print "Making kappa_tt and Rcs tt for:", samples

    bindirs = ['SR_MB','CR_MB','SR_SB_NB0','CR_SB_NB0', 'SR_SB_NB1i', 'CR_SB_NB1i']

    for fname in fileList:
        tfile = TFile(fname, "UPDATE")

        #Create direcotry for RCS and Kappa
        if not tfile.GetDirectory("Rcs_MB_TT"):
            tfile.mkdir("Rcs_MB_TT")
            tfile.mkdir("Rcs_SB_NB0_TT")
            tfile.mkdir("Rcs_SB_NB1i_TT")
            tfile.mkdir("KappaTT")
            tfile.mkdir("KappaB")
            tfile.mkdir("KappaBTT")

        # store SB/MB names
        sbname = tfile.Get("SR_SB/BinName")
        if sbname:
            sbname.SetName("SBname")
            tfile.cd("KappaTT")
            sbname.Write("",TObject.kOverwrite)
            tfile.cd("KappaB")
            sbname.Write("",TObject.kOverwrite)
            tfile.cd("KappaBTT")
            sbname.Write("",TObject.kOverwrite)

        mbname = tfile.Get("SR_MB/BinName")
        if mbname:
            mbname.SetName("MBname")
            tfile.cd("KappaTT")
            mbname.Write("",TObject.kOverwrite)
            tfile.cd("KappaB")
            mbname.Write("",TObject.kOverwrite)
            tfile.cd("KappaBTT")
            mbname.Write("",TObject.kOverwrite)

        for sample in samples:
            if sample == "data_QCDsubtr":
                hRcsSB_NB1i_data = getRcsHist(tfile, sample, 'SB_NB1i')
                tfile.cd("Rcs_SB_NB1i_TT")
                hRcsSB_NB1i_data.SetName(sample)
                hRcsSB_NB1i_data.Write("",TObject.kOverwrite)
            else:
                ewkSample = sample.replace("TTJets", "EWK")

                hRcsMB = getRcsHist(tfile, sample, 'MB', True)
                hRcsSB_NB0 = getRcsHist(tfile, sample, 'SB_NB0', True)
                hRcsSB_NB1i = getRcsHist(tfile, ewkSample, 'SB_NB1i', True)

                hKappaB = hRcsSB_NB0.Clone(hRcsSB_NB0.GetName().replace('Rcs','KappaB'))
                hKappaB.Divide(hRcsSB_NB1i)

                hKappaTT = hRcsMB.Clone(hRcsMB.GetName().replace('Rcs','KappaTT'))
                hKappaTT.Divide(hRcsSB_NB0)

                tfile.cd("Rcs_MB_TT")
                hRcsMB.SetName(sample)
                hRcsMB.Write("",TObject.kOverwrite)

                tfile.cd("Rcs_SB_NB0_TT")
                hRcsSB_NB0.SetName(sample)
                hRcsSB_NB0.Write("",TObject.kOverwrite)

                tfile.cd("Rcs_SB_NB1i_TT")
                hRcsSB_NB1i.SetName(sample)
                hRcsSB_NB1i.Write("",TObject.kOverwrite)

                tfile.cd("KappaB")
                hKappaB.SetName(sample)
                hKappaB.Write("",TObject.kOverwrite)

                tfile.cd("KappaTT")
                hKappaTT.SetName(sample)
                hKappaTT.Write("",TObject.kOverwrite)

                hKappaBTT = hKappaB.Clone()
                hKappaBTT.Multiply(hKappaTT)
                tfile.cd("KappaBTT")
                hKappaBTT.SetName(sample)
                hKappaBTT.Write("",TObject.kOverwrite)
        tfile.Close()
    return 1

def makeKappaWHists(fileList, samples = [], ttbarFractionCsv = "templateFits_0b_2016_EXT_nominal.csv"):
    # get process names from file if not given
    if samples == []: samples = list(set([sample for sample in getSamples(fileList[0],'CR_MB') if "_syst" not in sample and ("WJets" in sample or sample == "data")]))

    print "Making Rcs W and KappaW hists for:", samples

    bindirs =  ['SR_MB','CR_MB','SR_SB','CR_SB']

    ttbarFractionDf = read_csv(ttbarFractionCsv, index_col = "bin")

    for fname in fileList:
        tfile = TFile(fname,"UPDATE")

        #Create direcotry for RCS and Kappa
        if not tfile.GetDirectory("Rcs_MB_W"):
            tfile.mkdir("Rcs_MB_W")
            tfile.mkdir("Rcs_SB_W")
            tfile.mkdir("KappaW")
            tfile.mkdir("Rcs_MB_KappaW")

        # store SB/MB names
        sbname = tfile.Get("SR_SB/BinName")
        if sbname:
            sbname.SetName("SBname")
            tfile.cd("KappaW")
            sbname.Write("",TObject.kOverwrite)

        mbname = tfile.Get("SR_MB/BinName")
        if mbname:
            mbname.SetName("MBname")
            tfile.cd("KappaW")
            mbname.Write("",TObject.kOverwrite)

        binNameMB = tfile.Get("SR_MB/binName").GetTitle().replace("_SR", "").replace("_CR", "")
        binNameSB = tfile.Get("SR_SB/binName").GetTitle().replace("_SR", "").replace("_CR", "")

        ttbarFraction = ttbarFractionDf.loc[binNameSB, "TTJetsIncl_fraction"]
        ttbarFractionErr = ttbarFractionDf.loc[binNameSB, "TTJetsIncl_fraction_err"]

        hTTbarFraction = tfile.Get("CR_SB/" + sample).Clone()
        hTTbarFraction.SetBinContent(1,2,ttbarFraction); hTTbarFraction.SetBinError(1,2,ttbarFractionErr) # mu sele
        hTTbarFraction.SetBinContent(2,2,ttbarFraction); hTTbarFraction.SetBinError(2,2,ttbarFractionErr) # lep sele
        hTTbarFraction.SetBinContent(3,2,ttbarFraction); hTTbarFraction.SetBinError(3,2,ttbarFractionErr) # ele sele

        hTTbarFraction.SetBinContent(1,1,ttbarFraction); hTTbarFraction.SetBinError(1,1,ttbarFractionErr) # mu sele
        hTTbarFraction.SetBinContent(2,1,ttbarFraction); hTTbarFraction.SetBinError(2,1,ttbarFractionErr) # lep sele
        hTTbarFraction.SetBinContent(3,1,ttbarFraction); hTTbarFraction.SetBinError(3,1,ttbarFractionErr) # ele sele

        for sample in samples:
            if sample == "data":
                hRcsSB_data = getRcsCorrHist(tfile, hTTbarFraction, "data", 'SB', True)
                tfile.cd("Rcs_SB_W")
                hRcsSB_data.SetName("data")
                hRcsSB_data.Write("",TObject.kOverwrite)

            else:
                hRcsMB = getRcsHist(tfile, sample, 'MB', True)
                hRcsSB = getRcsHist(tfile, sample, 'SB', True)

                hKappa = hRcsMB.Clone()
                hKappa.Divide(hRcsSB)

                if hKappa.GetBinContent(1, 2) < 1e-5:
                    fname2017 = fname.replace("2018", "2017")
                    tfile2017 = TFile(fname2017, "UPDATE")

                    hKappa2017 = tfile2017.Get("KappaW/" + sample)
                    kappa2017 = hKappa2017.GetBinContent(1, 2)
                    kappaErr2017 = hKappa2017.GetBinError(1, 2)

                    #kappaDiff = 0.011625170396101147 # This is the weighted average of (kappaW_2017 - kappaW_2018)/kappaW_2017 for all bins
                    kappaDiff = 0.062799 # This is the peak position of (kappaW_2017 - kappaW_2018)/kappaW_2017 for all bins assuming a gaussian distribution
                    kappaErr2017 = (kappaErr2017 * kappaErr2017 + kappaDiff*kappa2017 * kappaDiff*kappa2017)**0.5

                    print "\n\nWarning!!! The bin %s does not have any WJets MC..\nTaking value from 2017 instead!" % binNameMB
                    print "File changed from:\n", fname, "\nto\n", fname2017
                    print "Assign additional uncertainty of %.3f * %.3f = %.3f" % (kappa2017, kappaDiff, kappa2017 * kappaDiff)
                    print "\n\n"

                    hKappa.SetBinContent(1, 2, kappa2017)
                    hKappa.SetBinContent(2, 2, kappa2017)
                    hKappa.SetBinContent(3, 2, kappa2017)

                    hKappa.SetBinError(1, 2, kappaErr2017)
                    hKappa.SetBinError(2, 2, kappaErr2017)
                    hKappa.SetBinError(3, 2, kappaErr2017)

                    # For plotting, also get the Rcs_MB_W(MC) and Rcs_SB_W(MC) from 2017

                    hRcsSB2017 = tfile2017.Get("Rcs_SB_W/" + sample)
                    rcsSB2017 = hRcsSB2017.GetBinContent(1, 2)
                    rcsSBErr2017 = hRcsSB2017.GetBinError(1, 2)

                    hRcsSB.SetBinContent(1, 2, rcsSB2017)
                    hRcsSB.SetBinContent(2, 2, rcsSB2017)
                    hRcsSB.SetBinContent(3, 2, rcsSB2017)

                    hRcsSB.SetBinError(1, 2, rcsSBErr2017)
                    hRcsSB.SetBinError(2, 2, rcsSBErr2017)
                    hRcsSB.SetBinError(3, 2, rcsSBErr2017)

                    hRcsMB2017 = tfile2017.Get("Rcs_MB_W/" + sample)
                    rcsMB2017 = hRcsMB2017.GetBinContent(1, 2)
                    rcsMBErr2017 = hRcsMB2017.GetBinError(1, 2)

                    hRcsMB.SetBinContent(1, 2, rcsMB2017)
                    hRcsMB.SetBinContent(2, 2, rcsMB2017)
                    hRcsMB.SetBinContent(3, 2, rcsMB2017)

                    hRcsMB.SetBinError(1, 2, rcsMBErr2017)
                    hRcsMB.SetBinError(2, 2, rcsMBErr2017)
                    hRcsMB.SetBinError(3, 2, rcsMBErr2017)

                    tfile2017.Close()
                hKappa.GetYaxis().SetTitle("KappaW")

                tfile.cd("Rcs_MB_W")
                hRcsMB.SetName(sample)
                hRcsMB.Write("",TObject.kOverwrite)

                tfile.cd("Rcs_SB_W")
                hRcsSB.SetName(sample)
                hRcsSB.Write("",TObject.kOverwrite)

                tfile.cd("KappaW")
                hKappa.SetName(sample)
                hKappa.Write("",TObject.kOverwrite)

        tfile.Close()
    return 1

def makePredictTTHists(fileList, samples = [], ttbarFractionCsv = "templateFits_0b_2016_EXT_nominal.csv"):

    # get process names from file
    if samples == []: samples = [sample for sample in getSamples(fileList[0],'CR_MB') if "TTJets" in sample]

    print "Making predictions for", samples

    for fname in fileList:
        tfile = TFile(fname,"UPDATE")

        ttbarFractionDf = read_csv(ttbarFractionCsv, index_col = "bin")

        #tfile.cd("SR_MB_predict")
        for sample in samples:
            # Read in the relevant histograms
            try:
                hRcsSB_NB1i_data = tfile.Get("Rcs_SB_NB1i_TT/data_QCDsubtr").Clone()
            except ReferenceError:
                continue
            hKappaB = tfile.Get("KappaB/" + sample)
            hKappaTT = tfile.Get("KappaTT/" + sample)

            tfile.cd("Rcs_SB_NB0_TT")
            hRcsSB_NB0_data = hRcsSB_NB1i_data.Clone()
            hRcsSB_NB0_data.Multiply(hKappaB)
            hRcsSB_NB0_data.SetName("data_QCDsubtr")
            hRcsSB_NB0_data.Write("",TObject.kOverwrite)

            tfile.cd("Rcs_MB_TT")
            hRcsMB_data = hRcsSB_NB1i_data.Clone()
            hRcsMB_data.Multiply(hKappaB)
            hRcsMB_data.Multiply(hKappaTT)
            hRcsMB_data.SetName("data_QCDsubtr")
            hRcsMB_data.Write("",TObject.kOverwrite)

            binNameMB = tfile.Get("SR_MB/binName").GetTitle().replace("_SR", "").replace("_CR", "")
            ttbarFraction = ttbarFractionDf.loc[binNameMB, "TTJetsIncl_fraction"]
            ttbarFractionErr = ttbarFractionDf.loc[binNameMB, "TTJetsIncl_fraction_err"]
            hTTbarFraction = tfile.Get("CR_SB/TTJets")
            hTTbarFraction.SetBinContent(1,2,ttbarFraction); hTTbarFraction.SetBinError(1,2,ttbarFractionErr) # mu sele
            hTTbarFraction.SetBinContent(2,2,ttbarFraction); hTTbarFraction.SetBinError(2,2,ttbarFractionErr) # lep sele
            hTTbarFraction.SetBinContent(3,2,ttbarFraction); hTTbarFraction.SetBinError(3,2,ttbarFractionErr) # ele sele

            tfile.cd("SR_MB")
            hTTJetsPred = tfile.Get("CR_MB/data_QCDsubtr")
            hTTJetsPred.Multiply(hRcsSB_NB1i_data)
            hTTJetsPred.Multiply(hKappaB)
            hTTJetsPred.Multiply(hKappaTT)
            hTTJetsPred.Multiply(hTTbarFraction)
            hTTJetsPred.SetName(sample + "_pred")
            hTTJetsPred.Write("",TObject.kOverwrite)
        tfile.Close()

    return 1

def makePredictWHists(fileList, samples = [], ttbarFractionCsv = "templateFits_0b_2016_EXT_nominal.csv"):

    # get process names from file
    if samples == []: samples = [sample for sample in getSamples(fileList[0],'CR_MB') if "WJets" in sample]

    print "Making predictions for", samples

    for fname in fileList:
        tfile = TFile(fname,"UPDATE")

        ttbarFractionDf = read_csv(ttbarFractionCsv, index_col = "bin")

        # create Rcs/Kappa dir struct
        #tfile.mkdir("SR_MB_predict")
        #tfile.mkdir("Rcs_SB_NB0_W")
        #tfile.mkdir("Rcs_MB_W")

        binNameMB = tfile.Get("SR_MB/binName").GetTitle().replace("_SR", "")
        binNameSB = tfile.Get("SR_SB/binName").GetTitle().replace("_SR", "")
        for sample in samples:
            # Read in the relevant histograms
            try:
                hRcsSB_data = tfile.Get("Rcs_SB_W/data").Clone()
            except ReferenceError:
                continue
            hKappa = tfile.Get("KappaW/" + sample)

            tfile.cd("Rcs_MB_W")
            hRcsMB_data = hRcsSB_data.Clone()
            hRcsMB_data.Multiply(hKappa)
            hRcsMB_data.SetName("data")
            hRcsMB_data.Write("",TObject.kOverwrite)


            wjetsFraction = ttbarFractionDf.loc[binNameSB, "WJetsIncl_fraction"]
            wjetsFractionErr = ttbarFractionDf.loc[binNameSB, "WJetsIncl_fraction_err"]
            hWJetsFraction = tfile.Get("CR_SB/WJets").Clone()
            hWJetsFraction.SetBinContent(1,2,wjetsFraction); hWJetsFraction.SetBinError(1,2,wjetsFractionErr) # mu sele
            hWJetsFraction.SetBinContent(2,2,wjetsFraction); hWJetsFraction.SetBinError(2,2,wjetsFractionErr) # lep sele
            hWJetsFraction.SetBinContent(3,2,wjetsFraction); hWJetsFraction.SetBinError(3,2,wjetsFractionErr) # ele sele

            tfile.cd("SR_MB")
            hWJetsPred = tfile.Get("CR_MB/data")
            hWJetsPred.Multiply(hRcsSB_data)
            hWJetsPred.Multiply(hKappa)
            hWJetsPred.Multiply(hWJetsFraction)
            hWJetsPred.SetName(sample + "_pred")
            hWJetsPred.Write("",TObject.kOverwrite)

        tfile.Close()

    return 1

def makePredictHists(fileList, samples = []):

    # get process names from file
    if samples == []: samples = getSamples(fileList[0],'SR_MB')

    print "Making predictions for", samples

    for fname in fileList:
        tfile = TFile(fname,"UPDATE")

        # create Rcs/Kappa dir struct
        if not tfile.GetDirectory("SR_MB_predict"):
            tfile.mkdir("SR_MB_predict")
            binString = tfile.Get("SR_MB/BinName").Clone()
            if binString: binName = binString.GetTitle()
            else: binName = tfile.GetName()
            #print binString
            tfile.cd("SR_MB_predict")
            binString.Write("",TObject.kOverwrite)
            for sample in samples:

                hPredict = getPredHist(tfile,sample)

                if hPredict:
                    tfile.cd("SR_MB_predict")
                    hPredict.Write("",TObject.kOverwrite)
                    #print "Wrote prediction of", sample

                else:
                    print "Failed to make prediction for", sample
        else:
            pass

        tfile.Close()

    return 1

def makeClosureHists(fileList, samples = []):
    if samples == []: samples = getSamples(fileList[0],'SR_MB')

    print "Making closure hists for", samples

    bindirs =  ['SR_MB','CR_MB','SR_SB','CR_SB']

    for fname in fileList:
        tfile = TFile(fname,"UPDATE")

        # create Closure dir
        if not tfile.GetDirectory("Closure"):
            tfile.mkdir("Closure")

        for sample in samples:

            hPred = tfile.Get("SR_MB_predict/"+sample)#+"_pred")
            hObs = tfile.Get("SR_MB/"+sample)

            hDiff = hObs.Clone(hObs.GetName())#+"_diff")
            hDiff.Add(hPred,-1)

            #hDiff.GetYaxis().SetTitle("Observed - Predicted/Observed")
            hDiff.Divide(hObs)

            tfile.cd("Closure")
            hDiff.Write("",TObject.kOverwrite)

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
        print '# pattern is', pattern
    else:
        print "No pattern given!"
        exit(0)


    # append / if pattern is a dir
    if os.path.isdir(pattern): pattern += "/"

    # find files matching pattern
    fileList = glob.glob(pattern+"*merge.root")

    if len(fileList) < 1:
        print "Empty file list"
        exit(0)

    ##################
    # Sample names
    ##################
    # all sample names
    allSamps = getSamples(fileList[0],'SR_MB')
    print 'Found these samples:', allSamps

    # make poisson errors for
    poisSamps = []#"background","QCD","EWK"]
    poisSamps = [s for s in poisSamps if s in allSamps]
    # do qcd prediciton for:

    qcdPredSamps =  ["background","data","QCD","background_poisson","QCD_poisson"]
    #qcdPredSamps =  ["background","QCD","background_poisson","QCD_poisson"]
    qcdPredSamps = [s for s in qcdPredSamps if s in allSamps]
    # samples to make full prediciton
    predSamps = allSamps + ["background_poisson","QCD_poisson"]
    predSaps = [s for s in predSamps if s in allSamps]

    #replaceEmptyDataBinsWithMC(fileList)
    blindDataBins(fileList)

    if "2016" in pattern:
        year = "2016_EXT"
    elif "2017" in pattern:
        year = "2017"
    elif "2018" in pattern:
        year = "2018"
    else:
        print "This code expects the year to be part of the pattern!"
        print "Please rename the input directory to contain information about the year!"
        exit()

    ttbarCsvFile =  "TemplateFit/templateFits_0b_" + year + "_nominal.csv"
    if "grid-dilep" in pattern:
        ttbarCsvFile =  "TemplateFit/templateFits_0b_" + year + "_dilep-corr.csv"

    #makePoissonErrors(fileList, poisSamps)
    makeQCDsubtraction(fileList, qcdPredSamps, year = year.replace("_EXT", ""))
    if "--do-qcd" in sys.argv:
        exit()
    print "QCD Estimate done!"

    makeKappaTTHists(fileList)#, predSamps)
    makePredictTTHists(fileList, ttbarFractionCsv = ttbarCsvFile)#, predSamps)
    print "Rcs Calculation for TTJets prediciton done!"

    makeKappaWHists(fileList, ttbarFractionCsv = ttbarCsvFile)#, predSamps)
    makePredictWHists(fileList, ttbarFractionCsv = ttbarCsvFile)#, predSamps)
    print "Rcs Calculation for WJets prediciton done!"

    print 'Finished'
