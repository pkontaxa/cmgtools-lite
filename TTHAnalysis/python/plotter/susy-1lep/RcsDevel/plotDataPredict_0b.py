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
    elif "run2" in sys.argv[1]:
        lum = "137.31"
        year = "Run II"

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
    mask = basename.replace("*","X_")
    signalMask = signalBasename.replace("*","X_")

    ## Create Yield Storage
    yds = yp.YieldStore("lepYields")
    yds.addFromFiles(pattern,("lep","sele"))
    #yds.showStats()

    ydsMuon = yp.YieldStore("MuonYields")
    ydsMuon.addFromFiles(pattern,("mu","sele"))
    #ydsMuon.showStats()

    #signalYds = yp.YieldStore("Signal")
    #pathSig = pattern2
    #signalYds.addFromFiles(pathSig,("lep","sele"))
    ## Define storage
    ### Store dict in pickle file
    pckname = "pickles/lep/" + str(year) + "/allSigCentral.pckz"
    if not os.path.exists("pickles"):
        os.makedirs("pickles")
    if not os.path.exists("pickles/lep"):
        os.makedirs("pickles/lep")
    if not os.path.exists("pickles/lep/" + str(year)):
        os.makedirs("pickles/lep/" + str(year))


    loadDict = "--redo-pickle" not in sys.argv
    if loadDict and os.path.exists(pckname):
        print "#Loading saved yields from pickle:", pckname
        import cPickle as pickle
        import gzip
        signalYds = pickle.load( gzip.open( pckname, "rb" ) )
    else:
        signalYds = yp.YieldStore("Signal")
        pathSig = pattern2
        signalYds.addFromFiles(pathSig,("lep","sele"))

        print "#Saving yields to pickle:", pckname
        # save to pickle
        import cPickle as pickle
        import gzip
        pickle.dump( signalYds, gzip.open( pckname, "wb" ) )


    mcSamps = ['VV','DY','TTV','SingleT']#,'WJets','TTJets']#
    #mcSamps = ['VV','DY','TTV','SingleT','WJets','TTJets']#
    signalSamples = ['T5qqqqWW_Scan_mGo1500_mLSP1000', 'T5qqqqWW_Scan_mGo1900_mLSP100']

    # update colors

    # Category
    cat = "SR_MB"
    if len(sys.argv) > 3:
        cat = sys.argv[3]

    canvs = []

    #for cat in cats:

    # Totals
    hData = yp.makeSampHisto(yds,"data_QCDsubtr",cat,"Data"); hData.SetTitle("Data")

    hWPred = yp.makeSampHisto(yds,"WJets_pred", "SR_MB", "W+jets (Pred)", useRcs = True); hWPred.SetTitle("WJets (Pred)");
    hWPred.SetTitle("WJets (Pred)")
    #hWPred.Add(hWposPred)

    hTTJetsPred = yp.makeSampHisto(ydsMuon,"TTJets_pred", "SR_MB", "TTJets (Pred)", useRcs = True); hTTJetsPred.SetTitle("TTJets (Pred)");

    ##### MC samps
    samps = [(samp,cat) for samp in mcSamps]
    mcHists = yp.makeSampHists(yds,samps)
    #mcHists = mcHists + [hTTsemiLepPred, hTTdiLepPred, hWPred]
    mcHists = mcHists + [hTTJetsPred, hWPred]

    #signalSamps = [(samp,"SR_MB") for samp in signalSamples]
    #signalHists = yp.makeSampHists(signalYds,signalSamps)
    #signalStack = yp.getStack(signalHists)

    signalCat = cat.replace("_pos", "").replace("_neg", "")
    signalSamps = [(samp,signalCat) for samp in signalSamples]
    signalHists = yp.makeSampHists(signalYds,signalSamps)
    signalStack = yp.getStack(signalHists)

    # Scale MC hists to Prediction
    #scaleToHist(mcHists,hDataPred)

    mcStack = yp.getStack(mcHists)
    hMCPred = mcHists[0].Clone()
    if len(mcHists) > 1:
        for hist in mcHists[1:]:
            hMCPred.Add(hist)


    #hMCPred = sum(mcHists)
    hUncert = hMCPred.Clone("uncert")
    hUncert.SetTitle("Stat. Unc.")
    yp.setUnc(hUncert)

    # Ratio
    ratio = yp.getRatio(hData,hMCPred)

    doPoisErr = True
    if doPoisErr:
        from CMGTools.TTHAnalysis.plotter.mcPlots import getDataPoissonErrors
        hDataPois = getDataPoissonErrors(hData,True,True)
        hDataPois.SetName("DataPois")
        hDataPois.SetTitle("Data")

        hMCPois = getDataPoissonErrors(hData,True,True)
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
        canv = yp.plotHists(cat + "_Prediction_",histsToPlot,ratio,legPos, width, height, logY = True, nCols = len(mcSamps) + 4)
    else:
        if "SR" in cat:
            histsToPlot = [mcStack] + signalHists
            ratio = None
        else:
            histsToPlot = [mcStack] + signalHists + [hData]
            ratio = [ratio]
        canv = yp.plotHists(cat + "_Prediction_",histsToPlot,ratio,legPos, width, height, logY = True, nCols = len(mcSamps) + 2)

    cname = "MC_" + cat + "_" +lum.replace('.','p')+"_"+mask

    if doPoisErr: cname += "poisErr_"

    canv.SetName(cname + canv.GetName())

    # Save canvases
    exts = [".pdf",".png",".root"]
    #exts = [".pdf"]
    if len(sys.argv) > 4:
        odir = sys.argv[4]
        if odir[-1] != "/": odir+="/"
    else:
        odir = "BinPlots/"

    if not os.path.exists(odir):
        os.makedirs(odir)

    ###if not os.path.isdir(odir): os.makedirs(odir)

    #for canv in canvs:
    for ext in exts:
        canv.SaveAs(odir+canv.GetName()+pattern.replace('/','_')+ext)
