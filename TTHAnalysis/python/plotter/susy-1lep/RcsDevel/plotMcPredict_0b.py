#!/usr/bin/env python

import sys,os

import makeYieldPlots_0b as yp

yp._batchMode = False
yp._alpha = 0.8

lum = "35.9"
year = 2016
if len(sys.argv) > 2:
    if "2017" in sys.argv[1]:
        lum = "41.9"
        year = 2017
    elif "2018" in sys.argv[1]:
        lum = "59.74"
        year = 2018

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

    if len(sys.argv) > 2:
        pattern = sys.argv[1]
        pattern2 = sys.argv[2]
        print '# pattern is', pattern
    else:
        print "No pattern given!"
        exit(0)

    #BinMask LTX_HTX_NBX_NJX for canvas names
    basename = os.path.basename(pattern)
    signalBasename = os.path.basename(pattern2)
    #basename = basename.replace("_SR","")
    mask = basename.replace("*","X_")
    signalMask = signalBasename.replace("*","X_")

    ## Create Yield Storage
    yds = yp.YieldStore("lepYields")
    yds.addFromFiles(pattern,("lep","sele"))
    yds.showStats()

    #signalYds = yp.YieldStore("Signal")
    #signalYds.addFromFiles(pattern2,("lep","sele"))
    #signalYds.showStats()

    ##TESTING
    ## Store dict in pickle file
    storeDict = True
    pckname = "pickles_{}/allSigCentral.pckz".format(year)

    signalYds = yp.YieldStore("Signal")
    pathSig = pattern2
    signalYds.addFromFiles(pathSig,("lep","sele"))
    #if storeDict == True and os.path.exists(pckname):
    #    print "#Loading saved yields from pickle:", pckname

    #    import cPickle as pickle
    #    import gzip
    #    signalYds = pickle.load( gzip.open( pckname, "rb" ) )
    #else:
    #    signalYds = yp.YieldStore("Signal")
    #    pathSig = pattern2
    #    signalYds.addFromFiles(pathSig,("lep","sele"))

    #    print "#Saving yields to pickle:", pckname
    #    # save to pickle
    #    import cPickle as pickle
    #    import gzip
    #    pickle.dump( signalYds, gzip.open( pckname, "wb" ) )



    ##mcSamps = ['QCD','VV','DY','TTV','SingleT','WJets','TTJets']#
    #mcSamps = ['VV','DY','TTV','SingleT','WJets','TTJets', 'T5qqqqWW_Scan_mGo1500_mLSP1000']#
    mcSamps = ['VV','DY','TTV','SingleT','WJets','TTJets']#
    #signalSamples = ['T5qqqqWW_Scan_mGo1500_mLSP1000', 'T5qqqqWW_Scan_mGo1900_mLSP100']
    signalSamples = ['T5qqqqWW_Scan_mGo1500_mLSP1000', 'T5qqqqWW_Scan_mGo1900_mLSP100', 'T5qqqqWW_Scan_mGo2100_mLSP1800', 'T5qqqqWW_Scan_mGo1050_mLSP900']
    #signalSamples = ['T5qqqqWW_Scan_mGo1500_mLSP1000', 'T5qqqqWW_Scan_mGo1900_mLSP100', 'T5qqqqWW_Scan_mGo2150_mLSP1750', 'T5qqqqWW_Scan_mGo2100_mLSP1800', 'T5qqqqWW_Scan_mGo2150_mLSP1800', 'T5qqqqWW_Scan_mGo1050_mLSP900', 'T5qqqqWW_Scan_mGo1800_mLSP200', 'T5qqqqWW_Scan_mGo2400_mLSP1400', 'T5qqqqWW_Scan_mGo2550_mLSP200']

    # update colors
    #yp.colorDict["T5qqqqWW_Scan_mGo1500_mLSP1000"] = yp.kCyan
    #yp.colorDict["T5qqqqWW_Scan_mGo1900_mLSP100"] = yp.kMagenta

    # Category
    #cat = "CR_MB"
    #cats = ["SR_MB_predict"]
    cat = "CR_MB"
    #cats = ["SR_MB"]
    #cats = ["CR_SB"]
    #cats = ["SR_SB"]
    if len(sys.argv) > 3:
        cat = sys.argv[3]

    canvs = []

    #for cat in cats:

    # Totals
    hDataPred = yp.makeSampHisto(yds,"data_QCDsubtr",cat,"Data_prediction"); hDataPred.SetTitle("Data (Pred)")

    hData = yp.makeSampHisto(yds,"data_QCDsubtr",cat,"Data"); hData.SetTitle("Data")
    hMCPred = yp.makeSampHisto(yds,"background_QCDsubtr",cat,"MC_expectation"); hMCPred.SetTitle("MC (Exp)")

    hSignal = yp.makeSampHisto(signalYds,"T5qqqqWW_Scan_mGo1500_mLSP1000",cat,"Signal_expectation"); hMCPred.SetTitle("T5qqqqWW (1.5, 1.0)")
    hSignal2 = yp.makeSampHisto(signalYds,"T5qqqqWW_Scan_mGo1900_mLSP100",cat,"Signal2_expectation"); hMCPred.SetTitle("T5qqqqWW (1.9, 0.1)")
    #hMCPred = yp.makeSampHisto(yds,"background",cat,"MC_expecation"); hMCPred.SetTitle("MC (Exp.)")

    #hSignal  = yp.makeSampHisto(yds,"background_QCDsubtr",cat,"Signal_prediction"); hMCPred.SetTitle("Signal")

    # Ratio
    #ratio = yp.getRatio(hTotal,hDataPred)
    ratio = yp.getRatio(hData,hMCPred)

    #ratio.GetYaxis().SetRangeUser(0,5)

    doPoisErr = True
    if doPoisErr:
        from CMGTools.TTHAnalysis.plotter.mcPlots import getDataPoissonErrors
        hDataPois = getDataPoissonErrors(hDataPred,True,True)
        hDataPois.SetName("DataPois")
        hDataPois.SetTitle("Data")

        hMCPois = getDataPoissonErrors(hDataPred,True,True)
        hMCPois.SetName("DataPois")
        hMCPois.SetTitle("Data")

        #ratioPois = yp.getRatio(hMCPois,hMCPred)
        ratioPois = yp.getRatio(hMCPois,hMCPred)

        hPredUnc = yp.getRatio(hMCPred,hMCPred)
        col = yp.kGray
        hPredUnc.SetName("PredictionUncertainty")
        hPredUnc.SetLineColor(1)
        hPredUnc.SetFillColor(col)
        hPredUnc.SetFillStyle(3244)
        hPredUnc.SetMarkerColor(col)
        hPredUnc.SetMarkerStyle(0)
        hPredUnc.GetYaxis().SetTitle(ratio.GetYaxis().GetTitle())
        hPredUnc.GetYaxis().SetRangeUser(0,3.9)

        # set error
        for i in xrange(1,hPredUnc.GetNbinsX()+1):
            try:
                hPredUnc.SetBinError(i,hMCPred.GetBinError(i)/hMCPred.GetBinContent(i))
            except ZeroDivisionError:
                hPredUnc.SetBinError(i, 0.)

    # MC samps
    samps = [(samp,cat) for samp in mcSamps]
    mcHists = yp.makeSampHists(yds,samps)
    signalSamps = [(samp,cat) for samp in signalSamples]
    signalHists = yp.makeSampHists(signalYds,signalSamps)
    signalStack = yp.getStack(signalHists)
    #signalLabel = ["T5qqqqWW (1.5, 1.0)", "T5qqqqWW (1.5, 1.0)"]
    #for hist, sample in zip(signalHists, signalSamples):
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

    doPoisErr = True
    if doPoisErr:
        if "SR" in cat:
            histsToPlot = [mcStack] + signalHists + [hUncert]
            ratio = None
        else:
            histsToPlot = [mcStack]  + signalHists + [hUncert,hDataPois]
            ratio = [hPredUnc,ratioPois]
        print(histsToPlot)
        canv = yp.plotHists(cat + "_Expectation_",histsToPlot,ratio,legPos, width, height, logY = True, nCols = len(mcSamps) + 4)
    else:
        if "SR" in cat:
            histsToPlot = [mcStack] + signalHists
            ratio = None
        else:
            histsToPlot = [mcStack] + signalHists + [hData]
            ratio = [ratio]
        canv = yp.plotHists(cat + "_Expectation_",histsToPlot,ratio,legPos, width, height, logY = True, nCols = len(mcSamps) + 2)
        #canv = yp.plotHists(cat + "_Prediction",[mcStack,hData],ratio,legPos, width, height, logY = True, nCols = len(mcSamps) + 1)
        #canv = yp.plotHists(cat,[mcStack],None,legPos, width, height, logY = True, nCols = len(mcSamps))

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
    if len(sys.argv) > 4:
        odir = sys.argv[4]
        if odir[-1] != "/": odir+="/"
    else:
        odir = "BinPlots/"

    if not os.path.isdir(odir): os.makedirs(odir)

    #for canv in canvs:
    for ext in exts:
        canv.SaveAs(odir+canv.GetName()+pattern.replace('/','_')+ext)

