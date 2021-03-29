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
    yp.colorDict["RCS_SB_NB1i_TT_MC"] = yp.kRed
    #yp.colorDict["kappaB"] = yp.kBlue+3
    #yp.colorDict["kappaTT"] = yp.kBlue+4

    hRcsSB_dataWneg = yp.makeSampHisto(ydsMuon,"data", "Rcs_SB_Wneg", "RCS_MB_Wneg", useRcs = True);
    hRcsSB_Wneg = yp.makeSampHisto(ydsMuon,"WJets", "Rcs_SB_Wneg", "RCS_SB_Wneg_MC", useRcs = True);
    hRcsMB_Wneg = yp.makeSampHisto(ydsMuon,"WJets", "Rcs_MB_Wneg", "RCS_MB_Wneg_MC", useRcs = True);
    hKappaWneg = yp.makeSampHisto(ydsMuon,"WJets", "KappaW_neg", "kappaW_neg", useRcs = True);
    #yp.colorDict["Rcs_MB_Wneg"] = yp.kGreen-1
    #yp.colorDict["kappaWneg"] = yp.kGreen+3

    hRcsSB_dataWpos = yp.makeSampHisto(ydsMuon,"data", "Rcs_SB_Wpos", "RCS_MB_Wpos", useRcs = True);
    hRcsSB_Wpos = yp.makeSampHisto(ydsMuon,"WJets", "Rcs_SB_Wpos", "RCS_SB_Wpos_MC", useRcs = True);
    hRcsMB_Wpos = yp.makeSampHisto(ydsMuon,"WJets", "Rcs_MB_Wpos", "RCS_MB_Wpos_MC", useRcs = True);
    hKappaWpos = yp.makeSampHisto(ydsMuon,"WJets", "KappaW_pos", "kappaW_pos", useRcs = True);

    alpha = 0.7
    hRcsSB_dataTT.SetFillColorAlpha(yp.kBlue-4, alpha)
    hRcsSB_NB1i_TT.SetFillColorAlpha(yp.kMagenta-3, alpha)
    hRcsSB_NB0_TT.SetFillColorAlpha(yp.kOrange-2, alpha)
    hRcsMB_TT.SetFillColorAlpha(yp.kBlue-4, alpha)
    hKappaB.SetFillColorAlpha(yp.kOrange-2, alpha)
    hKappaTT.SetFillColorAlpha(yp.kBlue-2, alpha)

    hRcsSB_dataWneg.SetFillColorAlpha(yp.kGreen+2, alpha)
    hRcsSB_Wneg.SetFillColorAlpha(yp.kMagenta-3, alpha)
    hRcsMB_Wneg.SetFillColorAlpha(yp.kGreen+2, alpha)
    hKappaWneg.SetFillColorAlpha(yp.kGreen+2, alpha)

    hRcsSB_dataWpos.SetFillColorAlpha(yp.kGreen+2, alpha)
    hRcsSB_Wpos.SetFillColorAlpha(yp.kMagenta-3, alpha)
    hRcsMB_Wpos.SetFillColorAlpha(yp.kGreen+2, alpha)
    hKappaWpos.SetFillColorAlpha(yp.kGreen+2, alpha)

    hRcsSB_dataTT.SetLineColor(yp.kBlue-4)
    hRcsSB_NB1i_TT.SetLineColor(yp.kMagenta-3)
    hRcsSB_NB0_TT.SetLineColor(yp.kOrange-2)
    hRcsMB_TT.SetLineColor(yp.kBlue-4)
    hKappaB.SetLineColor(yp.kOrange-2)
    hKappaTT.SetLineColor(yp.kBlue-2)

    hRcsSB_dataWneg.SetLineColor(yp.kGreen+2)
    hRcsSB_Wneg.SetLineColor(yp.kMagenta-3)
    hRcsMB_Wneg.SetLineColor(yp.kGreen+2)
    hKappaWneg.SetLineColor(yp.kGreen+2)

    hRcsSB_dataWpos.SetLineColor(yp.kGreen+2)
    hRcsSB_Wpos.SetLineColor(yp.kMagenta-3)
    hRcsMB_Wpos.SetLineColor(yp.kGreen+2)
    hKappaWpos.SetLineColor(yp.kGreen+2)

    hRcsSB_dataTT.SetMarkerColor(yp.kBlue-4)
    hRcsSB_NB1i_TT.SetMarkerColor(yp.kMagenta-3)
    hRcsSB_NB0_TT.SetMarkerColor(yp.kOrange-2)
    hRcsMB_TT.SetMarkerColor(yp.kBlue-4)
    hKappaB.SetMarkerColor(yp.kOrange-2)
    hKappaTT.SetMarkerColor(yp.kBlue-2)

    hRcsSB_dataWneg.SetMarkerColor(yp.kGreen+2)
    hRcsSB_Wneg.SetMarkerColor(yp.kMagenta-3)
    hRcsMB_Wneg.SetMarkerColor(yp.kGreen+2)
    hKappaWneg.SetMarkerColor(yp.kGreen+2)

    hRcsSB_dataWpos.SetMarkerColor(yp.kGreen+2)
    hRcsSB_Wpos.SetMarkerColor(yp.kMagenta-3)
    hRcsMB_Wpos.SetMarkerColor(yp.kGreen+2)
    hKappaWpos.SetMarkerColor(yp.kGreen+2)


    width = 4000 #Previous 1200 Pantelis
    height = 1200
    legPos = "Long"

    if '--log-y' in sys.argv:
        canv4 = yp.plotHists("Rcs_KappaTT_log", [hRcsMB_TT, hRcsSB_NB0_TT, hRcsSB_NB1i_TT, hRcsSB_dataTT], [hKappaB, hKappaTT], legPos, width, height, logY = True, nCols = 4)
        canv5 = yp.plotHists("Rcs_KappaWneg_log", [hRcsSB_Wneg, hRcsMB_Wneg, hRcsSB_dataWneg], [hKappaWneg], legPos, width, height, logY = True, nCols = 4)
        canv6 = yp.plotHists("Rcs_KappaWpos_log", [hRcsSB_Wpos, hRcsMB_Wpos, hRcsSB_dataWpos], [hKappaWpos], legPos, width, height, logY = True, nCols = 4)

        canv4_1 = yp.plotHists("RcsMC_KappaTT_log", [hRcsMB_TT, hRcsSB_NB0_TT], [hKappaTT], legPos, width, height, logY = True, nCols = 4)
        canv4_2 = yp.plotHists("RcsMC_KappaB_log", [hRcsSB_NB0_TT, hRcsSB_NB1i_TT], [hKappaB], legPos, width, height, logY = True, nCols = 4)
        #canv4_3MC = yp.plotHists("RcsMC_Kappa_log", [hRcsMB_TT, hRcsSB_NB0_TT, hRcsSB_NB1i_TT], [hKappaB, hKappaTT], legPos, width, height, logY = True, nCols = 4)
        canv5_2 = yp.plotHists("RcsMC_KappaWneg_log", [hRcsSB_dataWneg, hRcsSB_Wneg, hRcsMB_Wneg], [hKappaWneg], legPos, width, height, logY = True, nCols = 4)
        canv6_2 = yp.plotHists("RcsMC_KappaWpos_log", [hRcsSB_dataWpos, hRcsSB_Wpos, hRcsMB_Wpos], [hKappaWpos], legPos, width, height, logY = True, nCols = 4)

        canv4_3 = yp.plotHists("RcsData_TT_log", [hRcsSB_dataTT], None, legPos, width, height, logY = True, nCols = 4)
        canv5_3 = yp.plotHists("RcsData_Wneg_log", [hRcsSB_dataWneg], None, legPos, width, height, logY = True, nCols = 4)
        canv6_3 = yp.plotHists("RcsData_Wpos_log", [hRcsSB_dataWpos], None, legPos, width, height, logY = True, nCols = 4)
    else:
        canv  = yp.plotHists("Rcs_KappaTT", [hRcsMB_TT, hRcsSB_NB0_TT, hRcsSB_NB1i_TT, hRcsSB_dataTT], [hKappaB, hKappaTT], legPos, width, height, logY = False, nCols = 4)
        canv2 = yp.plotHists("Rcs_KappaWneg", [hRcsSB_Wneg, hRcsMB_Wneg, hRcsSB_dataWneg], [hKappaWneg], legPos, width, height, logY = False, nCols = 4)
        canv3 = yp.plotHists("Rcs_KappaWpos", [hRcsSB_Wpos, hRcsMB_Wpos, hRcsSB_dataWpos], [hKappaWpos], legPos, width, height, logY = False, nCols = 4)

        canv_1 = yp.plotHists("RcsMC_KappaTT", [hRcsMB_TT, hRcsSB_NB0_TT], [hKappaTT], legPos, width, height, logY = False, nCols = 4)
        canv_2 = yp.plotHists("RcsMC_KappaB", [hRcsSB_NB0_TT, hRcsSB_NB1i_TT], [hKappaB], legPos, width, height, logY = False, nCols = 4)
        #canv_3MC  = yp.plotHists("RcsMC_Kappa", [hRcsMB_TT, hRcsSB_NB0_TT, hRcsSB_NB1i_TT], [hKappaB, hKappaTT], legPos, width, height, logY = False, nCols = 4)
        canv2_2 = yp.plotHists("RcsMC_KappaWneg", [hRcsSB_Wneg, hRcsMB_Wneg], [hKappaWneg], legPos, width, height, logY = False, nCols = 4)
        canv3_2 = yp.plotHists("RcsMC_KappaWpos", [hRcsSB_Wpos, hRcsMB_Wpos], [hKappaWpos], legPos, width, height, logY = False, nCols = 4)

        canv_3  = yp.plotHists("RcsData_TT", [hRcsSB_dataTT], None, legPos, width, height, logY = False, nCols = 4)
        canv2_3 = yp.plotHists("RcsData_Wneg", [hRcsSB_dataWneg], None, legPos, width, height, logY = False, nCols = 4)
        canv3_3 = yp.plotHists("RcsData_WPos", [hRcsSB_dataWpos], None, legPos, width, height, logY = False, nCols = 4)

    # Save canvases
    exts = [".pdf",".png",".root"]
    if len(sys.argv) > 2:
        odir = sys.argv[2]
        if odir[-1] != "/": odir = odir + "/"
    else:
        odir = "BinPlots/"

    if not os.path.exists(odir):
        os.makedirs(odir)
    if not os.path.exists(odir + "/log"):
        os.makedirs(odir + "/log")

    # Save canvases
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
    if not os.path.exists(odir + "/MC/inclusive"):
        os.makedirs(odir + "/MC/inclusive")
    if not os.path.exists(odir + "/MC/TTJets"):
        os.makedirs(odir + "/MC/TTJets")
    if not os.path.exists(odir + "/MC/Wneg"):
        os.makedirs(odir + "/MC/Wneg")
    if not os.path.exists(odir + "/MC/Wpos"):
        os.makedirs(odir + "/MC/Wpos")

    if not os.path.exists(odir + "/Data"):
        os.makedirs(odir + "/Data")
    if not os.path.exists(odir + "/log"):
        os.makedirs(odir + "/log")
    if not os.path.exists(odir + "/log" + "/MC"):
        os.makedirs(odir + "/log/MC")
    if not os.path.exists(odir + "/log/MC/inclusive"):
        os.makedirs(odir + "/log/MC/inclusive")
    if not os.path.exists(odir + "/log/MC/TTJets"):
        os.makedirs(odir + "/log/MC/TTJets")
    if not os.path.exists(odir + "/log/MC/Wneg"):
        os.makedirs(odir + "/log/MC/Wneg")
    if not os.path.exists(odir + "/log/MC/Wpos"):
        os.makedirs(odir + "/log/MC/Wpos")

    if not os.path.exists(odir + "/log" + "/Data"):
        os.makedirs(odir + "/log/Data")

    ###if not os.path.isdir(odir): os.makedirs(odir)

    #for canv in canvs:
    for ext in exts:
        if '--log-y' in sys.argv:
            canv4.SaveAs(odir + "/log/MC/inclusive/" +canv4.GetName() + "_" + str(year) + ext)
            canv5.SaveAs(odir + "/log/MC/inclusive/" +canv5.GetName() + "_" + str(year) + ext)
            canv6.SaveAs(odir + "/log/MC/inclusive/" +canv6.GetName() + "_" + str(year) + ext)

            canv4_1.SaveAs(odir + "/log/MC/TTJets/" +canv4_1.GetName() + "_" + str(year) + ext)
            canv4_2.SaveAs(odir + "/log/MC/TTJets/" +canv4_2.GetName() + "_" + str(year) + ext)
            #canv4_3MC.SaveAs(odir + "/log/MC/inclusive/" +canv4_3MC.GetName() + "_" + str(year) + ext)
            canv5_2.SaveAs(odir + "/log/MC/Wneg/" +canv5_2.GetName() + "_" + str(year) + ext)
            canv6_2.SaveAs(odir + "/log/MC/Wpos/" +canv6_2.GetName() + "_" + str(year) + ext)

            canv4_3.SaveAs(odir + "/log/Data/" +canv4_3.GetName() + "_" + str(year) + ext)
            canv5_3.SaveAs(odir + "/log/Data/" +canv5_3.GetName() + "_" + str(year) + ext)
            canv6_3.SaveAs(odir + "/log/Data/" +canv6_3.GetName() + "_" + str(year) + ext)
        else:
            canv.SaveAs(odir + "/MC/inclusive/" +canv.GetName() + "_" + str(year) + ext)
            canv2.SaveAs(odir + "/MC/inclusive/" +canv2.GetName() + "_" + str(year) + ext)
            canv3.SaveAs(odir + "/MC/inclusive/" +canv3.GetName() + "_" + str(year) + ext)

            canv_1.SaveAs(odir + "/MC/TTJets/" +canv_1.GetName() + "_" + str(year) + ext)
            canv_2.SaveAs(odir + "/MC/TTJets/" +canv_2.GetName() + "_" + str(year) + ext)
            #canv_3MC.SaveAs(odir + "/MC/" +canv.GetName() + "_" + str(year) + ext)
            canv2_2.SaveAs(odir + "/MC/Wneg/" +canv2_2.GetName() + "_" + str(year) + ext)
            canv3_2.SaveAs(odir + "/MC/Wpos/" +canv3_2.GetName() + "_" + str(year) + ext)

            canv_3.SaveAs(odir + "/Data/" +canv_3.GetName() + "_" + str(year) + ext)
            canv2_3.SaveAs(odir + "/Data/" +canv2_3.GetName() + "_" + str(year) + ext)
            canv3_3.SaveAs(odir + "/Data/" +canv3_3.GetName() + "_" + str(year) + ext)
