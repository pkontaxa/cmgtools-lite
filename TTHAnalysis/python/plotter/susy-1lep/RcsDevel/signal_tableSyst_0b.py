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
    #year = pattern.split("_")[-1]
    if "run2" in pattern:
        year = "run2"
    elif "2016" in pattern:
        year = "2016"
    elif "2017" in pattern:
        year = "2017"
    elif "2018" in pattern:
        year = "2018"

    dirName = "signal_syst_tables_{}".format(year)
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory " , dirName ,  " Created ")
    else:
        print("Directory " , dirName ,  " already exists")

    # Define storage
    yds5 = YieldStore("lepYields")
    yds67 = YieldStore("lepYields")
    yds8 = YieldStore("lepYields")
    ydsMu5 = YieldStore("muYields")
    ydsMu67 = YieldStore("muYields")
    ydsMu8 = YieldStore("muYields")

    yds5.addFromFiles("yield_0b_premerge_" + year + "_prepSyst/signal_*/merged/LT*NJ5*", ("lep","sele"))
    yds67.addFromFiles("yield_0b_premerge_" + year + "_prepSyst/signal_*/merged/LT*NJ67*", ("lep","sele"))
    yds8.addFromFiles("yield_0b_premerge_" + year + "_prepSyst/signal_*/merged/LT*NJ8i*", ("lep","sele"))
    ydsMu5.addFromFiles("yield_0b_premerge_" + year + "_prepSyst/signal_*/merged/LT*NJ5*", ("mu","sele"))
    ydsMu67.addFromFiles("yield_0b_premerge_" + year + "_prepSyst/signal_*/merged/LT*NJ67*", ("mu","sele"))
    ydsMu8.addFromFiles("yield_0b_premerge_" + year + "_prepSyst/signal_*/merged/LT*NJ8i*", ("mu","sele"))

    systs = glob.glob('{}/signal_*'.format(pattern))
    systs = [syst[syst.find('signal_')+7:] for syst in systs]
    systsprint = systs

    #FIXME
    var = "T5qqqqWW_Scan"
    bindirs =  ['SR_MB','CR_MB','SR_SB','CR_SB', "SR_SB_NB1i", "CR_SB_NB1i", "SR_SB_NB0", "CR_SB_NB0"]

    # kinda hacky, but if you append both times, it fails
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

    label = '5 jet bins, relative uncertainties given in \%'
    yds5.printSignalTable(samps, header_names, dirName, 'signalTablev1_{}_'.format(year), var, systs)
    ydsMu5.printSignalTable(samps, header_names, dirName, 'signalTablev1_Mu_{}_'.format(year), var, systs)

    label = '6,7 jet bins, relative uncertainties given in \%'
    yds67.printSignalTable(samps, header_names, dirName, 'signalTablev1_{}_'.format(year), var, systs)
    ydsMu67.printSignalTable(samps, header_names, dirName, 'signalTablev1_Mu_{}_'.format(year), var, systs)

    label = '8 jet bins, relative uncertainties given in \%'
    yds8.printSignalTable(samps, header_names, dirName, 'signalTablev1_{}_'.format(year), var, systs)
    ydsMu8.printSignalTable(samps, header_names, dirName, 'signalTablev1_Mu_{}_'.format(year), var, systs)

    f_dat.close()
