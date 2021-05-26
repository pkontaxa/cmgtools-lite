#!/usr/bin/env python

import sys,os
import glob

#from makeYieldPlots import *
from makeYieldTables_0b import *
#from yieldClass import *

if __name__ == "__main__":

    ## remove '-b' option

    if len(sys.argv) > 1:
        pattern = sys.argv[1]
        print '# pattern is', pattern
    else:
        print "No pattern given!"
        exit(0)

    #BinMask LTX_HTX_NBX_NJX for canvas names
    basename = os.path.basename('Syst')
    mask = basename.replace("*","X_")
    year = pattern.split("_")[-1]

    dirName = "signal_syst_tables_{}".format(year)
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory " , dirName ,  " Created ")
    else:
        print("Directory " , dirName ,  " already exists")

    # Define storage
    yds5 = YieldStore("Sele")
    yds6 = YieldStore("Sele")
    yds8 = YieldStore("Sele")
    # ydsFew5 = YieldStore("lepYields")
    # ydsFew6 = YieldStore("lepYields")
    # ydsFew8 = YieldStore("lepYields")
    paths = []

    # Add files
    #old ntuples
#    btagPath = "Yields/systs/btag/test/merged/"; paths.append(btagPath)
#    puPath = "Yields/systs/PU/test/merged/"; paths.append(puPath)
#    wxsecPath = "Yields/systs/wXsec/test/merged/"; paths.append(wxsecPath)
#    tptPath = "Yields/systs/topPt/test/merged"; paths.append(tptPath)
#    dlConstPath = "Yields/systs/dilepConst/test/merged"; paths.append(dlConstPath)
#    dlSlopePath = "Yields/systs/dilepSlope/test/merged"; paths.append(dlSlopePath)


    #tptPath = "YieldsJan15/systs/topPt/MC/allSF_noPU/meth1A/merged/"; paths.append(tptPath)
    #puPath = "YieldsJan15/systs/PU/MC/allSF/meth1A/merged/"; paths.append(puPath)
    #wxsecPath = "YieldsJan15/systs/wXsec/MC/allSF_noPU/meth1A/merged/"; paths.append(wxsecPath)
    #dlConstPath = "YieldsJan15/systs/DLConst/merged"; paths.append(dlConstPath)
    #dlSlopePath = "YieldsJan15/systs/DLSlope/merged"; paths.append(dlSlopePath)
    ##jerPath = "Yields/systs/JER/merged"; paths.append(jerPath)                                                               #jerNoPath = "YieldsJan15/systs/JER_YesNo/merged"; paths.append(jerNoPath)
    #btagPath = "YieldsJan15/systs/btag/hadFlavour/fixXsec/allSF_noPU/meth1A/merged/"; paths.append(btagPath)
    #jecPath = "YieldsJan15/systs/JEC/MC/allSF_noPU/meth1A/merged/"; paths.append(jecPath)
    #wpolPath = "YieldsJan15/systs/Wpol/MC/allSF_noPU/meth1A/merged/"; paths.append(wpolPath)
    #ttvxsecPath = "YieldsJan15/systs/TTVxsec/MC/allSF_noPU/meth1A/merged/"; paths.append(ttvxsecPath)

    #jecPath = "Yields/systs/JEC/EWK/full/merged/"; paths.append(jecPath)

    # Add all systematics
    paths = glob.glob('{}/signal_*/merged/'.format(pattern))

    for path in paths:
        yds5.addFromFiles(path+'*NJ5*',("lep","sele"))
        yds6.addFromFiles(path+'*NJ67*',("lep","sele"))
        yds8.addFromFiles(path+'*NJ8i*',("lep","sele"))

    '''Pantelis
    paths = glob.glob('{}/syst_*/mergedFew/'.format(pattern))

    for path in paths:
        ydsFew6.addFromFiles(path+'/*NJ6i*', ('lep', 'sele'))
        ydsFew9.addFromFiles(path+'/*NJ9*', ('lep', 'sele'))
    Pantelis'''

    del paths

    #systs = ["btagHF","btagLF","Wxsec","Wpol","TTVxsec","topPt","PU","JEC","DLSlope","DLConst"]#,"JEC"]
    #systsprint = ["b-tag HF","b-tag LF","W xsec","W polar","TTV xsec","Top pT","PU","JES","dilep slope","dilep const"]#,"JEC"]

    systs = glob.glob('{}/signal_*'.format(pattern))
    systs = [syst[syst.find('signal_')+7:] for syst in systs]
    systsprint = systs

    # canvs and hists
    hists = []
    canvs = []

    #yds5.showStats()
    #FIXME
    var = "T5qqqqWW_Scan"
    bindirs =  ['SR_MB','CR_MB','SR_SB','CR_SB', "SR_SB_NB1i", "CR_SB_NB1i", "SR_SB_NB0", "CR_SB_NB0"]
    #b = "SR_MB"
    #from IPython import embed; embed()

    # kinda hacky, but if you append both times, it fails
    #f_tex =  open(dirName+'/signalTable_{}.tex'.format(year),'w')
    f_dat =  open(dirName+'/signalTablev1_{}.dat'.format(year),'w')

    caption = 'Zero-b analysis: Systematic uncertainties on Signal for different sources {}'.format(year)

    #for mGo in range(600, 2800, 25):
    #   for mLSP in range(0,1800,25):

    mLSP_list = [   0,  100,  200,  300,  400,  450,  475,  500,  525,  550,  575,
            600,  625,  650,  675,  700,  725,  750,  775,  800,  825,  850,
            875,  900,  950,  975, 1000, 1050, 1075, 1100, 1125, 1150, 1175,
           1200, 1250, 1300, 1350, 1400, 1425, 1450, 1500, 1550, 1600, 1650,
           1700, 1750, 1800, 1850, 1900]

    samps = [("T5qqqqWW_Scan_{}_syst_mGo{}_mLSP{}".format(syst,mGo,mLSP),b)
            for syst in systs
            for b in bindirs
            for mGo in range(600, 2600, 50) # previously ,2800, 25, but not found for 0b
            for mLSP in mLSP_list #range(0,1800,25)
            if mGo >= mLSP
            ]
    header_names = [b+"_"+syst
                   for syst in systsprint
                   for b in bindirs]

    #samps = [('TTJets_'+syst+'_syst','KappaTT')  for syst in systs]
    #printLatexHeader(len(samps), f_tex, caption, 1)
    label = '5 jet bins, relative uncertainties given in \%'
    #yds5.printLatexTable(samps, printSamps, label,f_tex, True)
    #from IPython import embed; embed()
    yds5.printSignalTable(samps, header_names, dirName, 'signalTablev1_{}_'.format(year), var, systs)

    #yds5.printTable(samps, header_names, label,f_dat)

    label = '6,7 jet bins, relative uncertainties given in \%'
    yds6.printSignalTable(samps, header_names, dirName, 'signalTablev1_{}_'.format(year), var, systs)

    #yds6.printLatexTable(samps, printSamps, label,f_tex, True)
    #yds6.printTable(samps, header_names, label,f_dat)

    label = '8 jet bins, relative uncertainties given in \%'
    yds8.printSignalTable(samps, header_names, dirName, 'signalTablev1_{}_'.format(year), var, systs)
    #yds8.printLatexTable(samps, printSamps, label,f_tex,True)
    #yds8.printTable(samps, header_names, label,f_dat)

    #printLatexFooter(f_tex, 1)
    #f_tex.close()

    f_dat.close()



    #######################
    # signal systematics



    #from IPython import embed;embed()

    '''Pantelis
    f =  open('sysTable_fewbins.dat','w')
    ydsFew6.printTable(samps, systs, label,f)
    ydsFew9.printTable(samps, systs, label,f)
    f.close()
    Pantelis'''
