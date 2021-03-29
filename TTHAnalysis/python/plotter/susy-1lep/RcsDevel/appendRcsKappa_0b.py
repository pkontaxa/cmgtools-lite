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

    hSR = tfile.Get("SR_"+band+"/"+hname)
    hCR = tfile.Get("CR_"+band+"/"+hname)

    hRcs = hSR.Clone(hSR.GetName().replace('x_','Rcs_'))
    hRcs.Divide(hCR)
    hRcs.GetYaxis().SetTitle("Rcs")

    # merge means ele/mu values are overwritten by the combined Rcs
    if 'data' in hname: merge = True

    if merge:
        rcs = hRcs.GetBinContent(2,2); err = hRcs.GetBinError(2,2) # lep sele

        hRcs.SetBinContent(1,2,rcs); hRcs.SetBinError(1,2,err) # mu sele
        hRcs.SetBinContent(3,2,rcs); hRcs.SetBinError(3,2,err) # ele sele

    return hRcs

def getRcsCorrHist(tfile, tfileTT, ttbarFraction, hname, band = "SB", merge = True, charge = "neg"):

    hSR = tfile.Get("SR_" + band + "/"  +  hname)
    dataSR = hSR.GetBinContent(1, 2)
    hCR = tfile.Get("CR_" + band + "/"  +  hname)#tfile.Get("CR_" + band + "/"  +  hname)
    dataCR = hCR.GetBinContent(1, 2)

    if "data" not in hname:
        hRcsTTJets = tfileTT.Get("Rcs_SB_NB0_TT_forWJets/TTJets")
    else:
        hRcsTTJets = tfileTT.Get("Rcs_SB_NB0_TT_forWJets/data_QCDsubtr")

    ttRcsSB_NB0 = hRcsTTJets.GetBinContent(2, 2)
    print "rcs_tt = ", hRcsTTJets.GetBinContent(1, 2), hRcsTTJets.GetBinContent(2, 2), hRcsTTJets.GetBinContent(3, 2)

    hTTPredict = hCR.Clone()
    hTTPredict.Multiply(hRcsTTJets)
    hTTPredict.Scale(ttbarFraction)

    hRcs = hSR.Clone()
    hRcs.Add(hTTPredict, -1)
    hRcs.Scale(1. / (1 - ttbarFraction))
    hRcs.Divide(hCR)

    rcssb = (dataSR - ttbarFraction * ttRcsSB_NB0 * dataCR) / (1 - ttbarFraction) / dataCR
    print "getRcsCorrHist = ({:.8f} - {:.8f} * {:.8f} * {:.8f}) / (1 - {:.8f}) / {:.8f} = {:.8}".format(dataSR, ttbarFraction, ttRcsSB_NB0, dataCR, ttbarFraction, dataCR, rcssb)

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
            print binname, njbin, qcdSysts[njbin]
            return qcdSysts[njbin]
    # If no bin is found, return 100 % uncertainty
    return 1.0

def getQCDsubtrHistos(tfile, sample = "background", band = "CR_MB/", isMC = True, applySyst = True, lep = "ele"):
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
    if isMC: fRatios = readQCDratios("Lp_LTbins_0b_2016_f-ratios_MC.txt")
    else: fRatios = readQCDratios("Lp_LTbins_0b_2016_f-ratios_MC.txt")

    # read bin name
    binString = tfile.Get(band+"BinName")
    if binString: binName = binString.GetTitle()
    else: binName = tfile.GetName()

    # get bin from filename
    for key in fRatios:
        #print key, binName
        if key in binName:
            (fRatio,fRatioErr) = fRatios[key]
            print "Found matching ratios for key" , key
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

def makeQCDsubtraction(fileList, samples):
    # hists to make QCD estimation
    bindirs =  ['SR_MB','CR_MB','SR_SB','CR_SB']

    print "Making QCD subtraction for", samples

    # Apply systematic error on F-ratio?
    applySyst = True

    for fname in fileList:
        tfile = TFile(fname,"UPDATE")

        for sample in samples:
            for bindir in bindirs:

                if 'data' in sample: isMC = False
                else: isMC = True

                #hNew = getQCDsubtrHisto(tfile,sample,bindir+"/",isMC)
                ret  = getQCDsubtrHistos(tfile,sample,bindir+"/",isMC, applySyst, "lep")
                print ret

                if not ret:
                    print 'Could not create new histo for', sample, 'in bin', bindir
                else:
                    (hQCDpred,hQCDsubtr) = ret
                    tfile.cd(bindir)
                    #hNew.Write()
                    hQCDpred.Write()
                    hQCDsubtr.Write()
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
                    hist.Write()#"",TObject.kOverwrite)
                tfile.cd()

        tfile.Close()

def makeKappaHists(fileList, samples = []):

    # get process names from file if not given
    if samples == []: samples = getSamples(fileList[0],'SR_MB')

    #print "Making Rcs and Kappa hists for:", samples

    bindirs =  ['SR_MB','CR_MB','SR_SB','CR_SB']
    #print bindirs

    for fname in fileList:
        tfileMB = TFile(fname,"UPDATE")
        tfileSB = TFile(fname.replace("NJ5", "NJ34").replace("NJ67", "NJ34").replace("NJ8i", "NJ34"),"UPDATE")

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
                sbname.Write()

            mbname = tfile.Get("SR_MB/BinName")
            if mbname:
                mbname.SetName("MBname")
                tfile.cd("Kappa")
                mbname.Write()

            for sample in samples:

                hRcsMB = getRcsHist(tfile, sample, 'MB')
                hRcsSB = getRcsHist(tfile, sample, 'SB')

                # make kappa
                hKappa = hRcsMB.Clone(hRcsMB.GetName().replace('Rcs','Kappa'))
                hKappa.Divide(hRcsSB)

                hKappa.GetYaxis().SetTitle("Kappa")

                tfile.cd("Rcs_MB")
                hRcsMB.Write()

                tfile.cd("Rcs_SB")
                hRcsSB.Write()

                tfile.cd("Kappa")
                hKappa.Write()

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
    if samples == []: samples = getSamples(fileList[0],'SR_MB')

    #print "Making kappa_tt and Rcs tt for:", samples

    bindirs = ['SR_MB','CR_MB','SR_SB','CR_SB']
    outDir = "RcsKappa"
    outputDirName = fileList[0].split("/merged")[0] + "/" + outDir
    if not os.path.exists(outputDirName):
        os.makedirs(outputDirName)

    for fname in fileList:
        tfile = TFile(fname.replace("merged", outDir).replace("_forTTJets", ""), "RECREATE")
        tfileMB = TFile(fname, "READ")
        print tfileMB

        fnameSB_NB0 = fname
        # Exceptions for merged bins to avoid empty bin in the sideband:
        if "LT4i" in fnameSB_NB0 and "HT3i" in fnameSB_NB0 and "NW1i" in fnameSB_NB0:
            fnameSB_NB0 = fnameSB_NB0.replace("NW1i", "NW0i")
        elif "LT4i" in fnameSB_NB0 and "HT0_" in fnameSB_NB0 and "NW1i" in fnameSB_NB0:
            fnameSB_NB0 = fnameSB_NB0.replace("NW1i", "NW0i")
        fnameSB_NB0  = fnameSB_NB0.replace("NJ5", "NJ45").replace("NJ67", "NJ45").replace("NJ8i", "NJ45")
        fnameSB_NB1i = fnameSB_NB0.replace("NB0", "NB1i")

        ###if 'LT4i' in fnameSB_NB1i and 'HT3i' in fnameSB_NB1i and 'NB1i' in fnameSB_NB1i and 'NW1i' in fnameSB_NB1i:
        ###    fnameSB_NB1i = fnameSB_NB1i.replace('LT4i', 'LT3i')
        ###    fnameSB_NB1i = fnameSB_NB1i.replace('LT4i', 'LT3')

        tfileSB_NB0  = TFile(fnameSB_NB0, "READ")
        tfileSB_NB1i = TFile(fnameSB_NB1i, "READ")

        # Account for different KappaB in the empty bins for WJets for both charges
        # Use Kappa for correction of using merged bins in the sideband for the WJets bins for both charges
        fnameSB_NB0_forWJets = fnameSB_NB0
        fnameSB_NB1i_forWJets = fnameSB_NB1i
        if "LT2" in fnameSB_NB1i and "HT2i" in fnameSB_NB1i and "NW1i" in fnameSB_NB1i:
            fnameSB_NB0_forWJets = fnameSB_NB1i.replace("NW1i", "NW0i")
            fnameSB_NB1i_forWJets = fnameSB_NB1i.replace("NW1i", "NW0i")
        elif "LT3" in fnameSB_NB1i and "HT3i" in fnameSB_NB1i and "NW1i" in fnameSB_NB1i:
            fnameSB_NB0_forWJets = fnameSB_NB1i.replace("NW1i", "NW0i")
            fnameSB_NB1i_forWJets = fnameSB_NB1i.replace("NW1i", "NW0i")
        elif "LT4i" in fnameSB_NB1i and "HT3i" in fnameSB_NB1i and "NW1i" in fnameSB_NB1i:
            fnameSB_NB0_forWJets = fnameSB_NB1i.replace("NW1i", "NW0i")
            fnameSB_NB1i_forWJets = fnameSB_NB1i.replace("NW1i", "NW0i")

        if "LT4i" in fnameSB_NB1i and "HT0" in fnameSB_NB1i and "NW0_" in fnameSB_NB1i:#This specific bin might not be needed TODO
            fnameSB_NB0_forWJets = fnameSB_NB1i.replace("NW0", "NW0i")
            fnameSB_NB1i_forWJets = fnameSB_NB1i.replace("NW0", "NW0i")
        elif "LT3" in fnameSB_NB1i and "HT3i" in fnameSB_NB1i:
            fnameSB_NB0_forWJets = fnameSB_NB1i.replace("LT3", "LT3i")
            fnameSB_NB1i_forWJets = fnameSB_NB1i.replace("LT3", "LT3i")

        tfileSB_NB0_forWJets  = TFile(fnameSB_NB0_forWJets, "READ")
        tfileSB_NB1i_forWJets = TFile(fnameSB_NB1i_forWJets, "READ")

        print tfileSB_NB0
        print tfileSB_NB1i
        #print tfileSB_NB0_forWJets_neg
        #print tfileSB_NB0_forWJets_pos
        #print tfileSB_NB1i_forWJets_neg
        #print tfileSB_NB1i_forWJets_pos

        #Copy the relevant histograms for easier plotting
        for cat in bindirs:
            if "MB" in cat:
                tmpFile = tfileMB
            else:
                tmpFile = tfileSB_NB0
            tfile.mkdir(cat)
            tfile.cd(cat)
            for sample in samples:
                tmpHist = tmpFile.Get(cat + "/" + sample)
                tmpHist.Write()

        #Create direcotry for RCS and Kappa
        tfile.mkdir("Rcs_MB_TT")
        #tfile.mkdir("Rcs_SB_data_TT")
        tfile.mkdir("Rcs_SB_NB0_TT")
        tfile.mkdir("Rcs_SB_NB1i_TT")
        tfile.mkdir("Rcs_SB_NB0_TT_forWJets")
        tfile.mkdir("Rcs_SB_NB1i_TT_forWJets")
        tfile.mkdir("KappaTT")
        tfile.mkdir("KappaB")

        tfile.mkdir("KappaB_forWJets")
        #tfile.mkdir("Rcs_MB_KappaB_KappaTT")

        # store SB/MB names
        sbname = tfile.Get("SR_SB/BinName")
        if sbname:
            sbname.SetName("SBname")
            tfile.cd("KappaTT")
            sbname.Write()
            tfile.cd("KappaB")
            sbname.Write()

        mbname = tfile.Get("SR_MB/BinName")
        if mbname:
            mbname.SetName("MBname")
            tfile.cd("KappaTT")
            mbname.Write()
            tfile.cd("KappaB")
            mbname.Write()

        hRcsSB_NB1i_data = getRcsHist(tfileSB_NB1i, "data_QCDsubtr", 'SB')
        print "hRcsSB_NB1i_data", hRcsSB_NB1i_data.GetBinContent(2, 2)
        hRcsSB_NB1i_data_forWJets = getRcsHist(tfileSB_NB1i_forWJets, "data_QCDsubtr", 'SB')

        hRcsMB = getRcsHist(tfileMB, "TTJets", 'MB', True)
        hRcsSB_NB0 = getRcsHist(tfileSB_NB0, "TTJets", 'MB', True)
        hRcsSB_NB1i = getRcsHist(tfileSB_NB1i, "EWK", 'SB', True)

        hKappaB = hRcsSB_NB0.Clone(hRcsSB_NB0.GetName().replace('Rcs','KappaB'))
        hKappaB.Divide(hRcsSB_NB1i)
        hKappaB.GetYaxis().SetTitle("KappaB")

        hRcsSB_NB0_forWJets = getRcsHist(tfileSB_NB0_forWJets, "TTJets", 'MB', True)
        hRcsSB_NB1i_forWJets = getRcsHist(tfileSB_NB1i_forWJets, "EWK", 'SB', True)
        hKappaB_forWJets = hRcsSB_NB0.Clone(hRcsSB_NB0_forWJets.GetName().replace('Rcs','KappaB'))
        hKappaB_forWJets.Divide(hRcsSB_NB1i_forWJets)
        hKappaB_forWJets.GetYaxis().SetTitle("KappaB_forWJets")

        hKappaTT = hRcsMB.Clone(hRcsMB.GetName().replace('Rcs','KappaTT'))
        hKappaTT.Divide(hRcsSB_NB0)
        hKappaTT.GetYaxis().SetTitle("KappaTT")

        #TESTING AREA
        """
        ttMB_SR = tfileMB.Get("SR_MB/" + "TTJets").GetBinContent(2, 2)
        ttMB_CR = tfileMB.Get("CR_MB/" + "TTJets").GetBinContent(2, 2)

        ttSB_NB0_SR = tfileSB_NB0.Get("SR_SB/" + "TTJets").GetBinContent(2, 2)
        ttSB_NB0_CR = tfileSB_NB0.Get("CR_SB/" + "TTJets").GetBinContent(2, 2)

        #ttSB_NB1i_SR = tfileSB_NB1i.Get("SR_SB/" + "TTJets").GetBinContent(2, 2)
        #ttSB_NB1i_CR = tfileSB_NB1i.Get("CR_SB/" + "TTJets").GetBinContent(2, 2)

        ttSB_NB1i_SR = tfileSB_NB1i.Get("SR_SB/" + "TTJets").GetBinContent(2, 2)
        ttSB_NB1i_CR = tfileSB_NB1i.Get("CR_SB/" + "TTJets").GetBinContent(2, 2)

        ewkSB_NB1i_SR = tfileSB_NB1i.Get("SR_SB/" + "EWK").GetBinContent(2, 2)
        ewkSB_NB1i_CR = tfileSB_NB1i.Get("CR_SB/" + "EWK").GetBinContent(2, 2)

        dataMB_SR = tfileMB.Get("SR_SB/" + "TTJets").GetBinContent(2, 2)
        dataMB_CR = tfileMB.Get("CR_SB/" + "TTJets").GetBinContent(2, 2)

        if ttMB_CR == 0:
            print "WARNING, 0 YIELD IN MB CR"
            ttMB_CR = -999

        if ttSB_NB0_CR == 0:
            print "WARNING, 0 YIELD IN 0b SB CR"
            ttSB_NB0_CR = -999

        if ttSB_NB1i_CR == 0:
            print "WARNING, 0 YIELD IN 1ib SB CR"
            ttSB_NB1i_CR = -999

        RcsMB_MC = ttMB_SR / ttMB_CR
        RcsSB_NB0_MC = ttSB_NB0_SR / ttSB_NB0_CR
        RcsSB_NB1i_MC = ewkSB_NB1i_SR / ewkSB_NB1i_CR

        if RcsSB_NB1i_MC == 0:
            print "WARNING YOUR RcsSB_NB1i_MC == 0!!"
            KappaB = -999
        else:
            KappaB = RcsSB_NB0_MC / RcsSB_NB1i_MC

        ##if RcsSB_NB0_MC == 0:
            #print "WARNING YOUR RcsSB_NB0_MC == 0!!"
            #KappaTT = -999
        #else:
        KappaTT = RcsMB_MC / RcsSB_NB0_MC

        hrcsmb_mc      = hRcsMB.GetBinContent(2, 2)
        hrcssb_nb0_mc  = hRcsSB_NB0.GetBinContent(2, 2)
        hrcssb_nb1i_mc = hRcsSB_NB1i.GetBinContent(2, 2)
        hkappab = hKappaB.GetBinContent(2, 2)
        hkappatt = hKappaTT.GetBinContent(2, 2)
        print "RcsMB_MC      \t\t\t\t= {:.8f} / {:.8f}\t= {:.8f} =? {:.8f} : ".format(ttMB_SR, ttMB_CR, RcsMB_MC, hrcsmb_mc) + "ERROR!!!" * (RcsMB_MC != hrcsmb_mc)
        print "RcsSB_NB0_MC  \t\t\t\t= {:.8f} / {:.8f}\t= {:.8f} =? {:.8f} : ".format(ttSB_NB0_SR, ttSB_NB0_CR, RcsSB_NB0_MC, hrcssb_nb0_mc) + "ERROR!!!" * (RcsSB_NB0_MC != hrcssb_nb0_mc)
        print "RcsSB_NB1i_MC \t\t\t\t= {:.8f} / {:.8f}\t= {:.8f} =? {:.8f} : ".format(ttSB_NB1i_SR, ttSB_NB1i_CR, RcsSB_NB1i_MC, hrcssb_nb1i_mc) + "ERROR!!!" * (RcsSB_NB1i_MC != hrcssb_nb1i_mc)
        print "KappaB  = RcsSB_NB0_MC / RcsSB_NB1i_MC\t= {:.8f} / {:.8f} = {:.8f} =? {:.8f} : ".format(RcsSB_NB0_MC, RcsSB_NB1i_MC , KappaB, hkappab) + "ERROR!!!" * (KappaB != hkappab)
        print "KappaTT = RcsMB_MC     / RcsSB_NB0_MC\t= {:.8f} / {:.8f} = {:.8f} =? {:.8f} : ".format(RcsMB_MC, RcsSB_NB0_MC , KappaTT, hkappatt) + "ERROR!!!" * (KappaTT != hkappatt)
        print "KappaB * RcsSBNB1i = {} * {} = {} =? {} = rcssbnb0".format(KappaB, RcsSB_NB1i_MC, KappaB * RcsSB_NB1i_MC, RcsSB_NB0_MC)
        print ""
        #TTBAR MANUAL CALCULATION IS EXACTLY THE SAME AS USING TH2 histograms!
        #TESTING AREA
        """

        tfile.cd("Rcs_MB_TT")
        hRcsMB.SetName("TTJets")
        hRcsMB.Write()

        tfile.cd("Rcs_SB_NB0_TT")
        hRcsSB_NB0.SetName("TTJets")
        hRcsSB_NB0.Write()

        tfile.cd("Rcs_SB_NB1i_TT")
        hRcsSB_NB1i.SetName("TTJets")
        hRcsSB_NB1i.Write()

        tfile.cd("KappaB")
        hKappaB.SetName("TTJets")
        hKappaB.Write()

        # Extra KappaB for considering the merged bins in WJets sideband
        tfile.cd("KappaB_forWJets")
        hKappaB_forWJets.SetName("TTJets")
        hKappaB_forWJets.Write()

        tfile.cd("Rcs_SB_NB0_TT_forWJets")
        hRcsSB_NB0_MC_forWJets= hRcsSB_NB1i.Clone()
        hRcsSB_NB0_MC_forWJets.Multiply(hKappaB_forWJets)
        hRcsSB_NB0_MC_forWJets.SetName("TTJets")
        hRcsSB_NB0_MC_forWJets.Write()

        tfile.cd("KappaTT")
        hKappaTT.SetName("TTJets")
        hKappaTT.Write()

        tfile.cd("SR_MB")
        hTTJetsPred = tfileMB.Get("CR_MB/data_QCDsubtr")
        print "hTTJetsPred = ", hTTJetsPred.GetBinContent(2, 2)
        hTTJetsPred.Multiply(hRcsSB_NB1i_data)
        print "hTTJetsPred = ", hTTJetsPred.GetBinContent(2, 2)
        hTTJetsPred.Multiply(hKappaB)
        print "hTTJetsPred = ", hTTJetsPred.GetBinContent(2, 2)
        hTTJetsPred.Multiply(hKappaTT)
        print "hTTJetsPred = ", hTTJetsPred.GetBinContent(2, 2)
        hTTJetsPred.SetName("TTJets" + "_pred")
        hTTJetsPred.Write()
        print "hTTJetsPred = ", hTTJetsPred.GetBinContent(2, 2)

        tfile.cd("Rcs_SB_NB1i_TT")
        hRcsSB_NB1i_data.SetName("data_QCDsubtr")
        hRcsSB_NB1i_data.Write()

        tfile.cd("Rcs_SB_NB0_TT")
        hRcsSB_NB0_data = hRcsSB_NB1i_data.Clone()
        hRcsSB_NB0_data.Multiply(hKappaB)
        hRcsSB_NB0_data.SetName("data_QCDsubtr")
        hRcsSB_NB0_data.Write()

        # Extra KappaB for considering the merged bins in WJets sideband
        tfile.cd("Rcs_SB_NB0_TT_forWJets")
        hRcsSB_NB0_data_forWJets= hRcsSB_NB1i_data.Clone()
        hRcsSB_NB0_data_forWJets.Multiply(hKappaB_forWJets)
        hRcsSB_NB0_data_forWJets.SetName("data_QCDsubtr")
        hRcsSB_NB0_data_forWJets.Write()

        tfile.Close()
        tfileMB.Close()
        tfileSB_NB0.Close()
        tfileSB_NB1i.Close()
    return 1

def makeKappaWHists(fileList, samples = [], ttbarFractionCsv = "templateFits_0b_newBinning_2016.csv"):

    # get process names from file if not given
    if samples == []: samples = getSamples(fileList[0],'SR_MB')

    #print "Making Rcs W and KappaW hists for:", samples

    bindirs =  ['SR_MB','CR_MB','SR_SB','CR_SB']
    #print bindirs
    outDir = "RcsKappa"
    outputDirName = fileList[0].split("/merged")[0] + "/" + outDir
    if not os.path.exists(outputDirName):
        os.makedirs(outputDirName)

    ttbarFractionDf = read_csv(ttbarFractionCsv, index_col = "bin")

    for fname in fileList:
        #print fname
        tfile = TFile(fname.replace("merged", outDir).replace("_forWJets", "").replace("_neg", "").replace("_pos", ""), "UPDATE")
        for charge in ["neg", "pos"]:
            if charge == "pos":
                fname = fname.replace("neg", "pos")
            #tfile = TFile(fname,"UPDATE")
            tfileMB = TFile(fname,"READ")
            fnameSB = fname.replace("NJ5", "NJ34").replace("NJ67", "NJ34").replace("NJ8i", "NJ34")
            # Exceptions for merged bins to avoid empty bin in the sideband:
            if "LT2" in fnameSB and "HT2i" in fnameSB and "NW1i" in fnameSB:
                fnameSB = fnameSB.replace("NW1i", "NW0i")
            #elif "LT3" in fnameSB and "HT3i" in fnameSB and "NW1i" in fnameSB:
                #fnameSB = fnameSB.replace("NW1i", "NW0i")
            elif "LT4i" in fnameSB and "HT3i" in fnameSB and "NW1i" in fnameSB:
                fnameSB = fnameSB.replace("NW1i", "NW0i")
            elif "LT4i" in fnameSB and "HT0" in fnameSB and "NW0_" in fnameSB:#This might not be needed
                fnameSB = fnameSB.replace("NW0", "NW0i")
            elif "LT3" in fnameSB and "HT3i" in fnameSB:
                fnameSB = fnameSB.replace("LT3", "LT3i")
            tfileSB = TFile(fnameSB, "READ")
            #tfileTT = TFile(fname.replace("merged", outDir).replace("_forWJets", "").replace("_forWJets_pos", ""), "Update"fname.replace("merged", outDir).replace("_WJets", "").replace("_neg", "").replace("_pos", ""), "READ")

            #if fnameSB == "yield_0b_2016v7/grid/merged/LT3_HT3i_NB0_NJ34_forWJets_NW0_neg.merge.root" or \
            #        fnameSB == "yield_0b_2016v7/grid/merged/LT3_HT3i_NB0_NJ34_forWJets_NW0i_neg.merge.root" or \
            #        fnameSB == "yield_0b_2016v7/grid/merged/LT4i_HT0_NB0_NJ34_forWJets_NW0_pos.merge.root" or \
            #        fnameSB == "yield_0b_2016v7/grid/merged/LT4i_HT0_NB0_NJ34_forWJets_NW0_neg.merge.root":
            #    continue

            #if not tfile.GetDirectory("Rcs_MB_W" + charge):
            #Copy the relevant histograms for easier plotting
            for cat in bindirs:
                if "MB" in cat:
                    tmpFile = tfileMB
                else:
                    tmpFile = tfileSB
                tfile.mkdir(cat + "_" + charge)
                tfile.cd(cat + "_" + charge)
                for sample in samples:
                    tmpHist = tmpFile.Get(cat + "/" + sample)
                    tmpHist.Write()

            #Create direcotry for RCS and Kappa
            tfile.mkdir("Rcs_MB_W" + charge)
            tfile.mkdir("Rcs_SB_W" + charge)
            #tfile.mkdir("Rcs_SB_data_W" + charge)
            tfile.mkdir("KappaW_" + charge)
            tfile.mkdir("Rcs_MB_KappaW_" + charge)

            # store SB/MB names
            sbname = tfile.Get("SR_SB/BinName")
            if sbname:
                sbname.SetName("SBname")
                tfile.cd("KappaW_" + charge)
                sbname.Write()

            mbname = tfile.Get("SR_MB/BinName")
            if mbname:
                mbname.SetName("MBname")
                tfile.cd("KappaW_" + charge)
                mbname.Write()

            tfile.cd("CR_MB_" + charge)

            binName = fnameSB.split("/")[-1].replace(".merge.root", "").replace("_forWJets", "").replace("_neg", "").replace("_pos", "")
            #ttbarFraction = 0.3
            #if binName in ttbarFractionDf.index:
            #    ttbarFraction = ttbarFractionDf.loc[binName, "TTJets" + charge.replace("pos", "Pos").replace("neg", "Neg") + "_fraction"]
            ttbarFraction = ttbarFractionDf.loc[binName, "TTJets" + charge.replace("pos", "Pos").replace("neg", "Neg") + "_fraction"]
            print "ttbarFraction = ", ttbarFraction
            hRcsMB = getRcsHist(tfileMB, "WJets", 'MB', True)

            # just testing, do not use for real
            #hRcsMB = getRcsHist(tfileMB, "WJets", 'MB', False)
            ##rcs = hRcsMB.GetBinContent(1,2); err = hRcsMB.GetBinError(1,2) # mu sele
            ##hRcsMB.SetBinContent(2,2,rcs); hRcsMB.SetBinError(2,2,err) # lep sele
            ##hRcsMB.SetBinContent(3,2,rcs); hRcsMB.SetBinError(3,2,err) # ele sele

            hRcsSB = getRcsCorrHist(tfileSB, tfile, ttbarFraction, "EWK", 'SB', True, charge)
            hRcsSB_data = getRcsCorrHist(tfileSB, tfile, ttbarFraction, "data", 'SB', True, charge)


            hKappa = hRcsMB.Clone()
            hKappa.Divide(hRcsSB)

            hRcsMb_KappaW = hRcsSB_data.Clone(hRcsSB_data.GetName().replace('Rcs', 'Rcs_MB_KappaW'))
            hRcsMb_KappaW.Multiply(hKappa)

            hKappa.GetYaxis().SetTitle("KappaW_" + charge)

            ### TESTING AREA
            print tfile
            print tfileMB
            print tfileSB
            wSR_MB = tfileMB.Get("SR_MB/WJets").GetBinContent(2, 2)
            wCR_MB = tfileMB.Get("CR_MB/WJets").GetBinContent(2, 2)
            backgroundSR_SB = tfileSB.Get("SR_SB/EWK").GetBinContent(1, 2)
            backgroundCR_SB = tfileSB.Get("CR_SB/EWK").GetBinContent(1, 2)

            rcsMB = wSR_MB / wCR_MB
            #rcsSB = backgroundSR_SB / backgroundCR_SB

            ttjets = tfileSB.Get("CR_SB/EWK").GetBinContent(1, 2)
            ttRcsSB_NB0 = tfile.Get("Rcs_SB_NB0_TT_forWJets/TTJets").GetBinContent(2, 2)
            ttRcsSB_NB0_data = tfile.Get("Rcs_SB_NB0_TT_forWJets/data_QCDsubtr").GetBinContent(2, 2)
            #ttRcsSB_NB1i = tfile.Get("Rcs_SB_NB1i_TT/TTJets").GetBinContent(2, 2)
            #ttKappaB = tfile.Get("KappaB/TTJets").GetBinContent(2, 2)
            #nTTBar = ttKappaB * ttRcsSB_NB1i * ttjets
            nTTBar = ttRcsSB_NB0 * ttjets

            hrcsmb = hRcsMB.GetBinContent(2, 2)
            hrcssb = hRcsSB.GetBinContent(1, 2)
            hkappaw = hKappa.GetBinContent(1, 2)
            rcsSB_data = hRcsSB_data.GetBinContent(1, 2)
            print hKappa.GetBinContent(1, 2),hKappa.GetBinContent(2, 2),hKappa.GetBinContent(3, 2)

            print "rcsMB    = {:.8f} / {:.8f} = {:.8f} =? {:.8f}".format(wSR_MB, wCR_MB, rcsMB, hrcsmb)

            rcsSB = (backgroundSR_SB - ttbarFraction * nTTBar) / (1 - ttbarFraction) / backgroundCR_SB
            print "rcsSB_MC = ({:.8f} - {:.8f} * {:.8f} * {:.8f}) / (1 - {:.8f}) / {:.8f} = {:.8} =? {:.8f}".format(backgroundSR_SB, ttbarFraction, ttRcsSB_NB0, ttjets, ttbarFraction, backgroundCR_SB, rcsSB, hrcssb)
            kappaw = rcsMB / rcsSB
            print "KappaW   = {:.8f} / {:.8f} = {:.8f} =? {:.8f}".format(rcsMB, rcsSB, kappaw, hkappaw)
            print hrcsmb / hrcssb

            dataSR_SB = tfileSB.Get("SR_SB/data").GetBinContent(1, 2)
            dataCR_SB = tfileSB.Get("CR_SB/data").GetBinContent(1, 2)
            print "dataCR_SB =", dataCR_SB
            print "rcsSB_MC = ({:.8f} - {:.8f} * {:.8f} * {:.8f}) / (1 - {:.8f}) / {:.8f} = {:.8} =? {:.8f}".format(backgroundSR_SB, ttbarFraction, ttRcsSB_NB0, ttjets, ttbarFraction, backgroundCR_SB, rcsSB, hrcssb)
            rcssb_data = (dataSR_SB - ttbarFraction * ttRcsSB_NB0_data * dataCR_SB) / (1 - ttbarFraction) / dataCR_SB
            print "rcsSB_data = ({:.8f} - {:.8f} * {:.8f} * {:.8f}) / (1 - {:.8f}) / {:.8f} = {:.8} =? {:.8f}".format(dataSR_SB, ttbarFraction, ttRcsSB_NB0_data, dataCR_SB, ttbarFraction, dataCR_SB, rcssb_data, rcsSB_data)
            print ""
            ### TESTING AREA

            tfile.cd("Rcs_MB_W" + charge)
            hRcsMB.SetName("WJets")
            hRcsMB.Write()

            tfile.cd("Rcs_SB_W" + charge)
            hRcsSB.SetName("WJets")
            hRcsSB.Write()

            tfile.cd("Rcs_SB_W" + charge)
            hRcsSB_data.SetName("data")
            hRcsSB_data.Write()

            tfile.cd("KappaW_" + charge)
            hKappa.SetName("WJets")
            hKappa.Write()

            #tfile.cd("Rcs_MB_KappaW_" + charge)
            #hKappa.SetName("Rcs_MB_KappaW")
            #hKappa.Write()

            hWJetsPred = tfileMB.Get("CR_MB/data")
            hWJetsPred.Multiply(hRcsSB_data)
            hWJetsPred.Multiply(hKappa)
            tfile.cd("SR_MB")
            hWJetsPred.SetName("WJets_pred_" + charge)
            hWJetsPred.Write()

            tfileMB.Close()
            tfileSB.Close()
        tfile.Close()
        print ""

    return 1

def makePredictHists(fileList, samples = []):

    # get process names from file
    if samples == []: samples = getSamples(fileList[0],'SR_MB')

    print "Making predictions for", samples

    for fname in fileList:
        tfile = TFile(fname.replace("merged", outDir).replace("_forWJets", "").replace("_neg", "").replace("_pos", ""), "UPDATE")
        #tfile = TFile(fname,"UPDATE")

        # create Rcs/Kappa dir struct
        if not tfile.GetDirectory("SR_MB_predict"):
            tfile.mkdir("SR_MB_predict")
            binString = tfile.Get("SR_MB/BinName").Clone()
            if binString: binName = binString.GetTitle()
            else: binName = tfile.GetName()
            #print binString
            tfile.cd("SR_MB_predict")
            binString.Write()
            for sample in samples:

                hPredict = getPredHist(tfile,sample)

                if hPredict:
                    tfile.cd("SR_MB_predict")
                    hPredict.Write()
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
            hDiff.Write()

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

    fileListTT = [fname for fname in fileList if ("NJ45" not in fname and "TTJets" in fname)]
    #fileListW = [fname for fname in fileList if ("NJ34" not in fname and "WJets" in fname and "neg" in fname and "LT12"not in fname and "LT3i" not in fname)]
    fileListW = [fname for fname in fileList if ("NJ34" not in fname and "WJets" in fname and "neg" in fname)]
    print fileListTT
    print fileListW

    #makePoissonErrors(fileList, poisSamps)
    if '--do-qcd' in sys.argv:
        makeQCDsubtraction(fileList, qcdPredSamps)
        exit()
    makeKappaTTHists(fileListTT)#, predSamps)
    print "Rcs Calculation for TTbar prediciton done!"
    makeKappaWHists(fileListW)#, predSamps)
    #makePredictHists(fileListW)#, predSamps)
    ####makeClosureHists(fileList, predSamps)

    print 'Finished'
