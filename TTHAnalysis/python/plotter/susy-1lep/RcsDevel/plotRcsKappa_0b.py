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
        print '# pattern is', pattern
    else:
        print "No pattern given!"
        exit(0)

    #BinMask LTX_HTX_NBX_NJX for canvas names
    basename = os.path.basename(pattern)
    mask = basename.replace("*","X_")

    ## Create Yield Storage
    yds = yp.YieldStore("lepYields")
    yds.addFromFiles(pattern,("lep","sele"))
    yds.showStats()

    ydsMuon = yp.YieldStore("MuonYields")
    ydsMuon.addFromFiles(pattern,("mu","sele"))
    ydsMuon.showStats()

    mcSamps = ['VV','DY','TTV','SingleT']#,'WJets','TTJets']#
    #mcSamps = ['VV','DY','TTV','SingleT','WJets','TTJets']#

    #Rcs Information:
    hRcsSB_dataTT = yp.makeSampHisto(yds,"data_QCDsubtr", "Rcs_SB_NB1i_TT", "RCS_MB_TT", useRcs = True);
    hRcsSB_NB1i_TT = yp.makeSampHisto(yds,"TTJets", "Rcs_SB_NB1i_TT", "RCS_SB_NB1i_TT_MC", useRcs = True);
    hRcsSB_NB0_TT = yp.makeSampHisto(yds,"TTJets", "Rcs_SB_NB0_TT", "RCS_SB_NB0_TT_MC", useRcs = True);
    hRcsMB_TT = yp.makeSampHisto(yds,"TTJets", "Rcs_MB_TT", "RCS_MB_TT_MC", useRcs = True);
    hKappaB = yp.makeSampHisto(yds,"TTJets", "KappaB", "kappaB", useRcs = True);
    hKappaTT = yp.makeSampHisto(yds,"TTJets", "KappaTT", "kappaTT", useRcs = True);

    hRcsSB_dataW= yp.makeSampHisto(ydsMuon,"data", "Rcs_SB_W", "RCS_MB_W", useRcs = True);
    hRcsSB_W= yp.makeSampHisto(ydsMuon,"WJets", "Rcs_SB_W", "RCS_SB_W", useRcs = True);
    hRcsMB_W= yp.makeSampHisto(ydsMuon,"WJets", "Rcs_MB_W", "RCS_MB_W_MC", useRcs = True);
    hKappaW= yp.makeSampHisto(ydsMuon,"WJets", "KappaW", "kappaW", useRcs = True);

    ymin = 0
    ymax = 3
    for hRatio in [hKappaB, hKappaTT, hKappaW]:
        hRatio.GetYaxis().SetRangeUser(ymin,ymax)
        hRatio.SetMinimum(ymin)
        hRatio.SetMaximum(ymax)

    alpha = 0.7
    hRcsSB_dataTT.SetFillColorAlpha(yp.kBlue-4, alpha)
    hRcsSB_NB1i_TT.SetFillColorAlpha(yp.kMagenta-3, alpha)
    hRcsSB_NB0_TT.SetFillColorAlpha(yp.kOrange-2, alpha)
    hRcsMB_TT.SetFillColorAlpha(yp.kBlue-4, alpha)
    hKappaB.SetFillColorAlpha(yp.kOrange-2, alpha)
    hKappaTT.SetFillColorAlpha(yp.kBlue-2, alpha)

    hRcsSB_dataTT.SetLineColor(yp.kBlue-4)
    hRcsSB_NB1i_TT.SetLineColor(yp.kMagenta-3)
    hRcsSB_NB0_TT.SetLineColor(yp.kOrange-2)
    hRcsMB_TT.SetLineColor(yp.kBlue-4)
    hKappaB.SetLineColor(yp.kOrange-2)
    hKappaTT.SetLineColor(yp.kBlue-2)

    hRcsSB_dataTT.SetMarkerColor(yp.kBlue-4)
    hRcsSB_NB1i_TT.SetMarkerColor(yp.kMagenta-3)
    hRcsSB_NB0_TT.SetMarkerColor(yp.kOrange-2)
    hRcsMB_TT.SetMarkerColor(yp.kBlue-4)
    hKappaB.SetMarkerColor(yp.kOrange-2)
    hKappaTT.SetMarkerColor(yp.kBlue-2)

    hRcsSB_dataW.SetFillColorAlpha(yp.kGreen+2, alpha)
    hRcsSB_dataW.SetMarkerColor(yp.kGreen+2)
    hRcsSB_dataW.SetLineColor(yp.kGreen+2)

    hRcsMB_W.SetFillColorAlpha(yp.kGreen+2, alpha)
    hRcsMB_W.SetMarkerColor(yp.kGreen+2)
    hRcsMB_W.SetLineColor(yp.kGreen+2)

    hRcsSB_W.SetFillColorAlpha(yp.kMagenta+2, alpha)
    hRcsSB_W.SetMarkerColor(yp.kMagenta+2)
    hRcsSB_W.SetLineColor(yp.kMagenta+2)

    hKappaW.SetFillColorAlpha(yp.kGreen+2, alpha)
    hKappaW.SetMarkerColor(yp.kGreen+2)
    hKappaW.SetLineColor(yp.kGreen+2)

    width = 4000
    height = 1200
    legPos = "Long"

    # Prepare directories for saving canvas
    exts = [".pdf",".png",".root"]
    if len(sys.argv) > 2:
        odir = sys.argv[2]
        if odir[-1] != "/": odir = odir + "/"
    else:
        odir = "BinPlots/"

    if not os.path.exists(odir):
        os.makedirs(odir)
    if not os.path.exists(odir + "/MC"):
        os.makedirs(odir + "/MC")
    #if not os.path.exists(odir + "/MC/inclusive"):
        #os.makedirs(odir + "/MC/inclusive")
    if not os.path.exists(odir + "/MC/TTJets"):
        os.makedirs(odir + "/MC/TTJets")
    if not os.path.exists(odir + "/MC/W"):
        os.makedirs(odir + "/MC/W")

    if not os.path.exists(odir + "/Data"):
        os.makedirs(odir + "/Data")

    if not os.path.exists(odir + "/log"):
        os.makedirs(odir + "/log")
    if not os.path.exists(odir + "/log" + "/MC"):
        os.makedirs(odir + "/log/MC")
    #if not os.path.exists(odir + "/log/MC/inclusive"):
        #os.makedirs(odir + "/log/MC/inclusive")
    if not os.path.exists(odir + "/log/MC/TTJets"):
        os.makedirs(odir + "/log/MC/TTJets")
    if not os.path.exists(odir + "/log/MC/W"):
        os.makedirs(odir + "/log/MC/W")
    if not os.path.exists(odir + "/log" + "/Data"):
        os.makedirs(odir + "/log/Data")


    if '--log-y' in sys.argv:
        canvKappaTTLog = yp.plotHists("RcsMC_KappaTT_log", [hRcsMB_TT, hRcsSB_NB0_TT], [hKappaTT], legPos, width, height, logY = True, nCols = 4)
        canvKappaBLog = yp.plotHists("RcsMC_KappaB_log", [hRcsSB_NB0_TT, hRcsSB_NB1i_TT], [hKappaB], legPos, width, height, logY = True, nCols = 4)
        canvKappaWLog = yp.plotHists("RcsMC_KappaW_log", [hRcsSB_W, hRcsMB_W], [hKappaW], legPos, width, height, logY = True, nCols = 4)
        for ext in exts:
                canvKappaTTLog.SaveAs(odir + "/log/MC/TTJets/" +canvKappaTTLog.GetName() + "_" + str(year) + ext)
                canvKappaBLog.SaveAs(odir + "/log/MC/TTJets/" +canvKappaBLog.GetName() + "_" + str(year) + ext)
                canvKappaWLog.SaveAs(odir + "/log/MC/W/" +canvKappaWLog.GetName() + "_" + str(year) + ext)
        canvKappaTTLog.Close()
        canvKappaBLog.Close()
        canvKappaWLog.Close()
        canvKappaWLog.Close()

        canvRcsTTDataLog = yp.plotHists("RcsData_TT_log", [hRcsSB_dataTT], None, legPos, width, height, logY = True, nCols = 4)
        canvRcsWDataLog = yp.plotHists("RcsData_W_log", [hRcsSB_dataW], None, legPos, width, height, logY = True, nCols = 4)
        for ext in exts:
                canvRcsTTDataLog.SaveAs(odir + "/log/Data/" +canvRcsTTDataLog.GetName() + "_" + str(year) + ext)
                canvRcsWDataLog.SaveAs(odir + "/log/Data/" +canvRcsWDataLog.GetName() + "_" + str(year) + ext)
        canvRcsTTDataLog.Close()
        canvRcsWDataLog.Close()

    else:
        canvKappaTT = yp.plotHists("RcsMC_KappaTT", [hRcsMB_TT, hRcsSB_NB0_TT], [hKappaTT], legPos, width, height, logY = False, nCols = 4)
        canvKappaB = yp.plotHists("RcsMC_KappaB", [hRcsSB_NB0_TT, hRcsSB_NB1i_TT], [hKappaB], legPos, width, height, logY = False, nCols = 4)
        canvKappaW = yp.plotHists("RcsMC_KappaW", [hRcsSB_W, hRcsMB_W], [hKappaW], legPos, width, height, logY = False, nCols = 4)
        for ext in exts:
            canvKappaTT.SaveAs(odir + "/MC/TTJets/" +canvKappaTT.GetName() + "_" + str(year) + ext)
            canvKappaB.SaveAs(odir + "/MC/TTJets/" +canvKappaB.GetName() + "_" + str(year) + ext)
            canvKappaW.SaveAs(odir + "/MC/W/" +canvKappaW.GetName() + "_" + str(year) + ext)
        canvKappaTT.Close()
        canvKappaB.Close()
        canvKappaW.Close()

        canvRcsTTData  = yp.plotHists("RcsData_TT", [hRcsSB_dataTT], None, legPos, width, height, logY = False, nCols = 4)
        canvRcsWData = yp.plotHists("RcsData_W", [hRcsSB_dataW], None, legPos, width, height, logY = False, nCols = 4)
        for ext in exts:
            canvRcsTTData.SaveAs(odir + "/Data/" +canvRcsTTData.GetName() + "_" + str(year) + ext)
            canvRcsWData.SaveAs(odir + "/Data/" +canvRcsWData.GetName() + "_" + str(year) + ext)
        canvRcsTTData.Close()
        canvRcsWData.Close()
