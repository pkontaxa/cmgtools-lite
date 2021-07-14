#!/usr/bin/env python
"""
import matplotlib
matplotlib.use('Agg')

import glob, os, sys

#from makeYieldPlots import *
import makeYieldPlots_0b as yp
import ROOT as ROOT
import numpy as np
import matplotlib.pyplot as plt


yp._batchMode = False
yp._alpha = 0.8

if __name__ == "__main__":

    yp.CMS_lumi.lumi_13TeV = str(36) + " fb^{-1}"
    # #yp.CMS_lumi.lumi_13TeV = "MC"
    yp.CMS_lumi.extraText = "Simulation"
#
    ## remove '-b' option
    if '-b' in sys.argv:
        sys.argv.remove('-b')
        yp._batchMode = True
#
    if len(sys.argv) > 1:
        pattern = sys.argv[1]
        print '# pattern is', pattern
    # else:
        # print "No pattern given!"
        # exit(0)
#
    basename = os.path.basename(pattern)
    mask = basename.replace("*","X_")
    #print basename, mask
#

    # append / if pattern is a dir
    if os.path.isdir(pattern): pattern += "/"

    # find files matching pattern
    fileList = glob.glob(pattern+"*merge.root")

    #if len(fileList) < 1:
    #    print "Empty file list"
    #    exit(0)

    #noms, ups, downs = [], [], []
    noms, ISRs = [], []

    for file in fileList:
        f=ROOT.TFile(file, "READ")
        t=f.Get("SR_MB")
        hist=t.Get("T5qqqqWW_Scan")
        #from IPython import embed;embed()
        histISR=t.Get("T5qqqqWW_Scan_ISR") #nISRweight
        #histUp = t.Get("T5qqqqWW_Scan_JEC-Up")
        #histDown=t.Get("T5qqqqWW_Scan_JEC-Down")

        #nom_list, up_list, down_list = [], [], []
        nom_list, ISR_list = [], []

        for x in range(hist.GetNbinsX()):
            for y in range(hist.GetNbinsY()):
                nom_list.append(hist.GetBinContent(x,y))
                ISR_list.append(histISR.GetBinContent(x,y))
                #up_list.append(histUp.GetBinContent(x,y))
                #down_list.append(histDown.GetBinContent(x,y))

        noms.append(np.mean(nom_list))
        #print(np.mean(ISR_list))
        ISRs.append(np.mean(ISR_list))
        #ups.append(np.mean(up_list))
        #downs.append(np.mean(down_list))

    xlabels = [f.split("/")[-1].replace(".merge.root", "").replace("_", "\n") for f in fileList]

    fig = plt.figure()
    plt.plot(noms, 'rx', label="nominal")
    #plt.plot(ups, 'bx', label="Up")
    #plt.plot(downs, 'gx', label="Down")
    plt.plot(ISRs, 'bx', label="with ISR weight")
    plt.legend()

    #plt.xticks(ticks=np.arange(0,len(xlabels),1), labels=xlabels, size="small")

    plt.savefig("BinPlots/"+pattern.replace("/","_")+".png")
    """

import glob, os, sys

import makeYieldPlots_0b as yp
yp._batchMode = False
yp._alpha = 0.8

lum = "35.9"
year = 2016
#if len(sys.argv) > 2:
if "2017" in sys.argv[1]:
    lum = "41.9"
    year = 2017
elif "2018" in sys.argv[1]:
    lum = "59.74"
    year = 2018
#    elif "run2" in sys.argv[1]:
#        lum = "137.31"
#        year = "Run II"

yp.CMS_lumi.lumi_13TeV = lum +  " fb^{-1}"
yp.CMS_lumi.extraText = "Preliminary"

doPoisErr = True

def scaleToHist(hists, hRef):

    hTotal = yp.getTotal(hists)

    for hist in hists:
        hist.Divide(hTotal)
        hist.Multiply(hRef)

if __name__ == "__main__":

    ## remove '-b' option
    if '-b' in sys.argv:
        sys.argv.remove('-b')
        yp._batchMode = True
    doSquare = False
    if '-s' in sys.argv:
        sys.argv.remove('-s')
        doSquare = True

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

    # Category
    cat = "SR_MB"

    #BinMask LTX_HTX_NBX_NJX for canvas names
    basename = os.path.basename(pattern)
    #signalBasename = os.path.basename(pattern2)
    #basename = basename.replace("_SR","")
    mask = basename.replace("*","X_")
    #signalMask = signalBasename.replace("*","X_")

    ## Create Yield Storage
    lep = "lep"
    dataString = "data_QCDsubtr"
    print pattern.split("/")
    print pattern.split("/")[2]
    print "WJets" in pattern.split("/")[2]
    if "WJets" in pattern.split("/")[2]:
        lep = "mu"
        data = "data"
    yds = yp.YieldStore(lep + "Yields")
    yds.addFromFiles(pattern,(lep,"sele"))
    yds.showStats()

    ### Store dict in pickle file
    pckname = ""
    pckname = "pickles/" + str(year) + "/" + lep + "/" + cat + "/allSigCentral.pckz"
    if not os.path.exists("pickles"):
        os.makedirs("pickles")
    if not os.path.exists("pickles/" + str(year)):
        os.makedirs("pickles/" + str(year))
    if not os.path.exists("pickles/" + str(year) + "/" + lep):
        os.makedirs("pickles/" + str(year) + "/" + lep)
    if not os.path.exists("pickles/" + str(year) + "/" + lep + "/" + cat):
        os.makedirs("pickles/" + str(year) + "/" + lep + "/" + cat)

    loadDict = "--redo-pickle" in sys.argv # not
    if loadDict and os.path.exists(pckname):
        print "#Loading saved yields from pickle:", pckname
        import cPickle as pickle
        import gzip
        signalYds = pickle.load( gzip.open( pckname, "rb" ) )

    else:
        signalYds = yp.YieldStore("Signal")
        pathSig = pattern
        signalYds.addFromFiles(pathSig,(lep,"sele"))

        print "#Saving yields to pickle:", pckname
        # save to pickle
        import cPickle as pickle
        import gzip
        pickle.dump(signalYds, gzip.open( pckname, "wb" ) )

    nomSamps = ['T5qqqqWW_Scan_mGo1500_mLSP1000']
    #nomSamps = ['VV','DY','TTV','SingleT','WJets','TTsemiLep', 'TTdiLep']
    #ISRSamps = ['T5qqqqWW_Scan_mGo1500_mLSP1000', 'T5qqqqWW_Scan_mGo1500_mLSP1000', 'T5qqqqWW_Scan_mGo1500_mLSP0']
    ISRSamps = ['T5qqqqWW_Scan_ISR_mGo1500_mLSP1000']

    canvs = []

    #from IPython import embed;embed()

    # Totals
    #hDataPred = yp.makeSampHisto(yds,dataString,cat,"Data_prediction"); hDataPred.SetTitle("Data (Pred)")
    hData = yp.makeSampHisto(yds,'T5qqqqWW_Scan_mGo1500_mLSP1000',cat,"nominal"); hData.SetTitle("nominal")
    hMCPred = yp.makeSampHisto(yds,'T5qqqqWW_Scan_ISR_mGo1500_mLSP1000',cat,"ISR"); hMCPred.SetTitle("with ISR")

    # Ratio
    #ratio = yp.getRatio(hTotal,hDataPred)
    ratio = yp.getRatio(hData,hMCPred)

    #ratio.GetYaxis().SetRangeUser(0,5)

    # MC samps
    samps = [(samp,cat) for samp in nomSamps]
    mcHists = yp.makeSampHists(yds,samps)

    #from IPython import embed;embed()

    signalCat = cat.replace("_pos", "").replace("_neg", "")
    signalSamps = [(samp,signalCat) for samp in ISRSamps]
    signalHists = yp.makeSampHists(signalYds,signalSamps)
    print signalHists
    #signalStack = yp.getStack(signalHists)
    #signalLabel = ["T5qqqqWW (1.5, 1.0)", "T5qqqqWW (1.5, 1.0)"]
    #for hist, sample in zip(signalHists, ISRSamps):
        #print "TEST"
        #print hist
        #print sample.replace("_Scan_", " ")

    # Scale MC hists to Prediction
    #scaleToHist(mcHists,hDataPred)

    mcStack = yp.getStack(mcHists)
    hUncert = hMCPred.Clone("uncert")
    hUncert.SetTitle("Stat. Unc.")
    yp.setUnc(hUncert)

    width = 2000 #Previous 1200 Pantelis
    height = 600
    legPos = "Long"

    doPoisErr = False
    if doPoisErr:
        if "SR_MB" in cat:
            histsToPlot = [mcStack] + signalHists + [hUncert]
            ratio = None
        else:
            histsToPlot = [mcStack]  + signalHists + [hUncert,hDataPois]
            ratio = [hPredUnc,ratioPois]
        print(histsToPlot)
        canv = yp.plotHists(cat + "_Expectation_",histsToPlot,ratio,legPos, width, height, logY = True, nCols = len(nomSamps) + 4)
    else:

        histsToPlot = [mcStack] + signalHists + [hData]
        ratio = [ratio]

        canv = yp.plotHists(cat + "_Expectation_",histsToPlot,ratio,legPos, width, height, logY = True, nCols = len(nomSamps) + 2)
        #canv = yp.plotHists(cat + "_Prediction",[mcStack,hData],ratio,legPos, width, height, logY = True, nCols = len(nomSamps) + 1)
        #canv = yp.plotHists(cat,[mcStack],None,legPos, width, height, logY = True, nCols = len(nomSamps))

    cname = "MC_" + cat + "_" +lum.replace('.','p')+"_"+mask

    if doPoisErr: cname += "poisErr_"

    canv.SetName(cname + canv.GetName())

    #canvs.append(canv)

    #print canv.GetName()

    #if not yp._batchMode:
    #    if "q" in raw_input("Enter any key to exit (or 'q' to stop): "): exit(0)

    # Save canvases
    exts = [".pdf",".png",".root"]
    #exts = [".pdf"]
#    print pattern
    odir = "BinPlots/"

    if not os.path.isdir(odir): os.makedirs(odir)

    #for canv in canvs:
    for ext in exts:
        canv.SaveAs(odir+nomSamps[0]+canv.GetName()+pattern.replace('/','_')+ext)
