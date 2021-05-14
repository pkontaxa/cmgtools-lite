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

    # Define storage
    yds5 = YieldStore("Sele")
    yds6 = YieldStore("Sele")
    yds8 = YieldStore("Sele")
    ydsFew5 = YieldStore("lepYields")
    ydsFew6 = YieldStore("lepYields")
    ydsFew8 = YieldStore("lepYields")
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
    paths = glob.glob('{}/syst_*/merged/'.format(pattern))

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

    systs = glob.glob('{}/syst_*'.format(pattern))
    systs = [syst[syst.find('syst_')+5:] for syst in systs]
    systsprint = systs

    # Sample and variable
    samp = "WJets"
    var = "KappaW"
    sv_list = [("WJets", "KappaW"), ("TTJets", "KappaBTT")]

    # canvs and hists
    hists = []
    canvs = []

    yds5.showStats()
    for samp, var in sv_list:

        # kinda hacky, but if you append both times, it fails
        if var == "KappaW":
            f_tex =  open('sysTable_{}.tex'.format(year),'w')
        else:
            f_tex =  open('sysTable_{}.tex'.format(year),'a')

        caption = 'Multi-b analysis: Systematic uncertainties on $\kappa$ for different sources (2016)'
        samps = [(samp+'_'+syst+'_syst',var)  for syst in systs]
        printSamps = [syst  for syst in systsprint]
        #samps = [('TTJets_'+syst+'_syst','KappaTT')  for syst in systs]
        printLatexHeader(len(samps), f_tex, caption, 1)

        label = '5 jet bins, relative uncertainties given in \%'
        yds5.printLatexTable(samps, printSamps, label,f_tex, True)

        label = '6,7 jet bins, relative uncertainties given in \%'
        yds6.printLatexTable(samps, printSamps, label,f_tex, True)

        label = '8 jet bins, relative uncertainties given in \%'
        yds8.printLatexTable(samps, printSamps, label,f_tex,True)

        printLatexFooter(f_tex, 1)
        f_tex.close()

        if var == "KappaW":
            f_dat =  open('sysTable_W_{}.dat'.format(year),'w')
        else:
            f_dat =  open('sysTable_BTT_{}.dat'.format(year),'w')


        f_dat.write(samp + "|" + var + "\n")
        yds5.printTable(samps, systs, label,f_dat)
        yds6.printTable(samps, systs, label,f_dat)
        yds8.printTable(samps, systs, label,f_dat)

        f_dat.close()


    #from IPython import embed;embed()

    '''Pantelis
    f =  open('sysTable_fewbins.dat','w')
    ydsFew6.printTable(samps, systs, label,f)
    ydsFew9.printTable(samps, systs, label,f)
    f.close()
    Pantelis'''
