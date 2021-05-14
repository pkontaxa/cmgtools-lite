#!/usr/bin/env python

import sys,os
from glob import glob

#from makeYieldPlots import *
import makeYieldPlots_0b as yp
#import makeYieldPlots_Pantelis as yp
#import makeYieldPlots_Frederic as yp
import ROOT as ROOT
import numpy as np


yp._batchMode = False
yp._alpha = 0.8

if __name__ == "__main__":
    ROOT.TH1.AddDirectory(False)

    ## remove '-b' option
    if '-b' in sys.argv:
        sys.argv.remove('-b')
        yp._batchMode = True


    if len(sys.argv) > 1:
        pattern = sys.argv[1]
        print '# pattern is', pattern
    else:
        print "No pattern given!"
        pattern = ""
        #exit(0)

    basename = os.path.basename(pattern)
    mask = basename.replace("*","X_")
    year = pattern.split("_")[-1]
    print basename, mask

    lumi_dict={
        "2016":"35.9 fb^{-1}",
        "2017":"41.9 fb^{-1}",
        "2018":"59.74 fb^{-1}",
    }


    yp.CMS_lumi.lumi_13TeV = lumi_dict[year]
    yp.CMS_lumi.extraText = " Simulation"

    ## Store dict in pickle file
    storeDict = True
    pckname = "pickles/bkgSysts_fixSR_"+mask+".pck"
    print 'pickle name is {}'.format(pckname)
    if storeDict == True and os.path.exists(pckname):

        print "#Loading saved yields from pickle!"

        import cPickle as pickle
        yds = pickle.load( open( pckname, "rb" ) )
        yds.showStats()

    else:

        print "#Reading yields from files!"

        # Define storage
        yds = yp.YieldStore("Sele")
        #paths = []

        ## Add files
        #tptPath = "Yields2015Uncert/systs/topPt/MC/allSF_noPU/meth1A/merged/"; paths.append(tptPath)
        #puPath = "Yields2015Uncert/systs/PU/MC/allSF/meth1A/merged/"; paths.append(puPath)
        #wxsecPath = "Yields2015Uncert/systs/wXsec/MC/allSF_noPU/meth1A/merged/"; paths.append(wxsecPath)
        #ttvxsecPath = "Yields2015Uncert/systs/TTVxsec/MC/allSF_noPU/meth1A/merged/"; paths.append(ttvxsecPath)
        #wpolPath = "Yields2015Uncert/systs/Wpol/MC/allSF_noPU/meth1A/merged/"; paths.append(wpolPath)
        #dlConstPath = "Yields2015Uncert/systs/DLConst/merged/"; paths.append(dlConstPath)
        #dlSlopePath = "Yields2015Uncert/systs/DLSlope/merged/"; paths.append(dlSlopePath)
        #jerPath = "Yields2015Uncert/systs/JER/merged/"; paths.append(jerPath)
        #jerNoPath = "Yields2015Uncert/systs/JER_YesNo/merged/"; paths.append(jerNoPath)
        ##jecPath = "Yields/systs/JEC/MC/allSF_noPU/meth1A/merged/"; paths.append(jecPath)
        #jecPath = "Yields2015Uncert/systs/JEC/MC/allSF_noPU_fixLT/meth1A/merged/"; paths.append(jecPath)
        #btagPath = "Yields2015Uncert/systs/btag/hadFlavour/fixXsec/allSF_noPU/meth1A/merged/"; paths.append(btagPath)
#       # dlScaleMatchVarPath = "lumi22fb_DlMakeBinYields/ScaleMatchVar/merged"; paths.append(dlScaleMatchVarPath)
#       # dlPDFUncPath = "lumi22fb_DlMakeBinYields/PDFUnc-RMS/merged"; paths.append(dlPDFUncPath)
        ## lep SF unct < 1%
        ##paths = ["Yields/systs/lepSF/test/allSF_noPU/merged_main/"]
        ## central value
#       # centrPath = "Yields/wData/jecv7_fixSR/lumi2p3fb/allbins/allSF_noPU/merged"; paths.append(centrPath)
        #centrPath = "YieldsJune29/lumi3p99/grid/merged/"; paths.append(centrPath)

        # Add all systematics
        paths = glob('{}/syst_*/merged/'.format(pattern))

        # Add central value
        paths.append('{}/grid-dilep/merged/'.format(pattern))

        print 'paths', paths
        for path in paths:
            yds.addFromFiles(path+"LT",("lep","sele"))

        yds.showStats()

        print "#Saving yields to pickle"
        #from IPython import embed; embed()
        # save to pickle
        import cPickle as pickle
        pickle.dump( yds, open( pckname, "wb" ) )

    #print [name for name in yds.samples if ("syst" in name and "EWK" in name)]
    #exit(0)

    # Sys types
#    systs = ["btagHF","btagLF","Wxsec","PU"]#,"topPt"]#,"JEC"]
#    systs = ["btagHF","btagLF","Wxsec","PU","topPt"]#,"JEC"]
#    systs = ["btagHF","Wxsec","topPt","PU","DLSlope","DLConst"]#,"JEC"]
#    systs = ["JEC"]
#    systs = ["btagHF","btagLF"]
#    systs = ["btagLF","btagHF"]
#    systs = ["DLConst","DLSlope"]

#    systs = ["TTVxsec","Wxsec"]
#    systs = ["Wpol","Wxsec"]
#    systs = ["ScaleMatchVar-Env","PDFUnc-RMS"]
#    systs = ["Wpol","Wxsec","PU","JEC","btagHF","btagLF","topPt","DLConst","DLSlope","JER","JERYesNo"]
    #systs = ["TTVxsec","Wpol","Wxsec","PU","JEC","btagHF","btagLF","topPt","DLConst","DLSlope"]
#    systs = ["lepSF"]
    systs = glob('{}/syst_*'.format(pattern))
    systs = [syst[syst.find('syst_')+5:] for syst in systs]

    systNames = {
        "btagLF" : "b-mistag (light)",
        "btagHF" : "b-tag (b/c)",
        "JEC" : "JEC",
        "topPt" : "Top p_{T}",
        "PU" : "PU",
        "ISR": "ISR",
        "Scale-Env": "Scale",
        #"Wxsec" : "#sigma_{W}",
        "Wxsec" : "W x-sec",
        "TTVxsec" : "t#bar{t}V x-sec",
        "TTxsec" : "t#bar{t} x-sec",
        "Wpol" : "W polar.",
        "JER" : "JER",
        "JERYesNo" : "JER Yes/No",
        #"DLSlope" : "DiLep (N_{j} Slope)",
        "DLSlope" : "N_{j} Slope",
        #"DLConst" : "DiLep (N_{j} Const)",
        "DLConst" : "N_{j} Offset",
        "lumi" : "Lumi.",
        "trig" : "Trigger",
        "lepSF": "Lepton SF",
        "stat": "Stat.",
        "nISR" : "nISR rew.",
        "iso" : "Iso. track veto",
        "scale" : "Q2 scale",
        }



    #sysCols = [2,4,7,8,3,9,6] + range(40,50)#[1,2,3] + range(4,10)
    #sysCols = [50] + range(49,0,-2)#range(30,50,2)
    #sysCols = range(40,100,1)#range(30,50,2)
    sysCols = range(35,100,3)
    #sysCols = range(28,100,2)
    #sysCols = range(49,1,-2)
    #sysCols = range(30,40,4) + range(40,100,3)
    #sysCols = range(49,40,-2) + range(40,30,-3) + range(50,100,5)
    #Pantelis sysCols = [40, 20, 30, 45, 36, 24, 29, 38, 28, 39, 32, 47, 49, 43]


    # Sample and variable
    #samp = "EWK"
    #samps = ["EWK","TTJets","WJets","SingleTop","DY","TTV"]
    #samps = ['T_tWch','TToLeptons_tch','TBar_tWch', 'TToLeptons_sch',"EWK"]
    #samp = samps[4]

    #var = "KappaTT"
    #var = "KappaB"
    #var = "KappaW"
    #var = "SR_SB"

    # create the empty file to append later
    the_file=open('syst_0b_{}.txt'.format(year), 'w')
    the_file.close()

    for var, samp in ("KappaTT", "TTJets"), ("KappaB", "TTJets"), ("KappaW", "WJets"), ("KappaBTT", "TTJets"):

        #var, samp =("KappaW", "WJets")

        # canvs and hists
        hists = []
        canvs = []

        #from IPython import embed;embed()
        # read in central value
        hCentral = yp.makeSampHisto(yds,samp,var)
        print "hCentral done for {0} in {1}".format(var, samp)
        yp.prepRatio(hCentral)

        # FIXME
        #systs = ['JEC']

        for i,syst in enumerate(systs):
            try:
                # Get the color from a list
                yp.colorDict[syst+"_syst"] = sysCols[i]
            except IndexError:
                # If list is out of bounds, use black
                yp.colorDict[syst+"_syst"] = 1

            sname = samp+"_"+syst+"_syst"
            #from IPython import embed;embed()
            print "Making hist for", sname
            #hist = yp.makeSampHisto(yds,sname,var,syst+"_syst")
            hist = yp.makeSampHisto(yds,sname,var,syst+"_syst", useRcs = True)
            #from IPython import embed;embed()
            if hist!=0:
                if syst in systNames: hist.SetTitle(systNames[syst])
                else: hist.SetTitle(syst)

                hist.GetYaxis().SetTitle("Relative uncertainty")
                hist.GetYaxis().SetTitleSize(0.04)
                hist.GetYaxis().SetTitleOffset(0.8)

                #yp.prepKappaHist(hist)
                #yp.prepRatio(hist)10
                # normalize to central value
                #hist.Divide(hCentral)

                hists.append(hist)

        # make stack/total syst hists
        #total = yp.getTotal(hists)
        stack = yp.getStack(hists)
        sqHist = yp.getSquaredSum(hists)

        hCentral.GetYaxis().SetTitle("#kappa_{%s}" % var.split("Kappa")[1])
        hCentral.GetYaxis().SetTitleSize(0.15)
        hCentral.GetYaxis().SetTitleOffset(0.17)

        hCentralUncert = yp.getHistWithError(hCentral, sqHist, True)

        '''
        for bin in range(1,hCentral.GetNbinsX()+1):
            print bin
            print hCentral.GetBinContent(bin), hCentralUncert.GetBinContent(bin)
            print hCentral.GetBinError(bin), hCentralUncert.GetBinError(bin)
        '''
        #from IPython import embed;embed()

        #canv = yp.plotHists(var+"_"+samp+"_Syst",[stack,sqHist],[hCentral,hCentralUncert],"TM", 1200, 600, nCols = 5)
        canv = yp.plotHists(var+"_"+samp+"_Syst",[stack,sqHist],[hCentral,hCentralUncert],"TLC", 2000, 600, nCols = 2)
        #    canv = yp.plotHists(var+"_"+samp+"_Syst",[sqHist]+hists,[hCentral,hCentralUncert],"TM", 1200, 600)
        #    canv = yp.plotHists(var+"_"+samp+"_Stat",[stack,sqHist],hCentral,"TM", 1200, 600)

        #from IPython import embed; embed()
        #canv.Divide(1,2)
        #canv.cd(1)
        #canv.SetLogy()
        #ROOT.gPad.SetLogy()

        canvs.append(canv)
        #if not yp._batchMode: raw_input("Enter any key to exit")

        # Save canvases
        exts = [".pdf",".png",".root"]
        #exts = [".pdf"]

        #odir = "BinPlots/Syst/Combine/test/allSF_noPU_Wpol/Method1A/"
        #odir = "BinPlots/Syst/Combine/allSF_noPU_LTfix/Method1A/"
        odir = "BinPlots/Syst/Combine_{}/".format(year)
        if not os.path.isdir(odir): os.makedirs(odir)

        ## Save hists
        #pattern = "Syst"
        #mask = pattern

        for canv in canvs:
            for ext in exts:
                canv.SaveAs(odir+mask+canv.GetName()+ext)

        # write systs binwise into file to have a crosscheck
        with open('syst_0b_{}.txt'.format(year), 'a') as the_file:
            the_file.write(var + "|"+ samp +pattern+ "\n")
            the_file.write(str(systs)+ " Sqared sum," + " Kap-value")
            the_file.write("\n")
            for i in range(1, int(hists[0].GetEntries())+1):
                for h in hists:
                    the_file.write(str(np.round(h.GetBinContent(i),6)) + ",")
                the_file.write("]"+str(np.round(sqHist.GetBinContent(i),6))+",")
                the_file.write(str(np.round(hCentralUncert.GetBinContent(i),6)))
                #print(hCentralUncert.GetBinContent(i))
                the_file.write("\n")

        """
        without this shell
        pure virtual method called
        terminate called without an active exception
        occurs and kills the loop
        if you just type exit() into the shell, the loop works fine.
        Or use strg+D  then ->  y
        """
        print("type exit() to escape this shell")
        #from IPython import embed;embed()
