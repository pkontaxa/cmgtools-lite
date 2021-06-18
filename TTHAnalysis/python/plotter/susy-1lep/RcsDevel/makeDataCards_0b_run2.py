#!/usr/bin/env python
import sys
import numpy as np
import random as rd
out = 'test'
SMS = 'T5qqqqWW'

from yieldClass_0b import *
from ROOT import *

from pandas import read_csv

#import utilities as u
from utility import binDict


def shortenName(name, shorten = False):
    if shorten:
        #return name.replace("_", "").replace("N", "").replace("LT", "L").replace("HT", "H").replace("Muon", "Mu").replace("20", "")
        return binDict[name]
    else:
        return name

def printABCDCard(yds, ydsMuon, ydsObs, ydsMuObs, ydsPred, ydsKappaTT, ydsKappaW, year, yieldFractionDf, sysTableBttDf , sysTableWDf, sysTableSignalDf, sysTableMuSignalDf, sysTableOtherDf):
    folder = 'datacardsABCD_' + out + '/'
    if not os.path.exists(folder): os.makedirs(folder)
    bins = sorted(yds.keys())

    sampNames = []
    catNames = []
    for x in yds[bins[0]]:
        if "Scan" in x.name or "TTJets" == x.name or "WJets" == x.name:
            catNames .append(x.cat)
            sampNames.append(x.name)
        else:
            if sampNames[-1] != "Other":
                catNames .append(x.cat)
                sampNames.append("Other")
            else:
                pass

    sampUniqueNames = list(set(sampNames))
    for x in sampNames:
        if "Scan_m" in x: signalName = x

    mGlu = signalName[signalName.find('_mGo') + 4:signalName.find('_mLSP')]
    factor = 1.0
    if float(mGlu) < 1400:
        factor = 100.0
    catUniqueNames = [x.cat for x in ydsObs[bins[0]] ]
    nSamps = len(sampNames)
    nUniqueSamps = len(sampUniqueNames)

    precision = 4

    try:
        os.stat(folder + signalName )
    except:
        os.mkdir(folder + signalName )

    iproc = { key: i+1 for (i,key) in enumerate(sorted(reversed(sampUniqueNames)))}
    iproc.update({signalName: 0})
    rd.seed(5)

    for i,bin in enumerate(bins):
        obs0 = False
        #This assumes 6 different samples
        numberOfCategories = len(catUniqueNames)
        datacard = open(folder+ signalName+ '/' +bin + '.card.txt', 'w');
        datacard.write("## Datacard for bin %s (signal %s)\n"%(bin,signalName))
        datacard.write("imax %i  number of channels \n" % numberOfCategories)
        datacard.write("jmax %i  number of processes -1 \n" % (nUniqueSamps - 1))
        datacard.write("kmax *  number of nuisance parameters (sources of systematical uncertainties) \n")

        klen = max(len(samp) for samp in sampNames)
        kpatt = " %%%ds "  % klen
        fpatt = " %%%d.%df " % (klen,5)
        datacard.write('##---\n')
        #catDict = {"SR_MB" : "S", "CR_MB" : "C", "SR_SB" : "S2", "CR_SB" : "C2", "SR_SB_NB1i" : "S3", "CR_SB_NB1i" : "C3"}

        spaceBuffer = len("TTVxsec_2018 lnN")
        #datacard.write('bin'+ (' ' * (spaceBuffer - len("bin"))) +(" ".join([kpatt % catDict[cat]     for cat in catUniqueNames]))+"\n")
        datacard.write('bin'+ (' ' * (spaceBuffer - len("bin"))) +(" ".join([kpatt % cat     for cat in catUniqueNames]))+"\n")
        np.random.seed(42546)

        dataCardObservation = "observation" + ' ' * (spaceBuffer - len("observation") - 1)
        ##print bin
        for yd, ydMuon in zip(ydsObs[bin], ydsMuObs[bin]):
            if yd.cat == "SR_SB" or yd.cat == "CR_SB":
                dataCardObservation += " " + fpatt % ydMuon.val
            elif yd.cat == "SR_MB":
                #put prediction here
                #print "EWK = ", yd.val
                backgroundPrediction = 0
                for ydBkg in yds[bin]:
                    if ydBkg.cat == "SR_MB" and (ydBkg.name != "TTJets" and ydBkg.name != "WJets" and "T5qqqqWW" not in ydBkg.name):
                        #dataCardObservation += " " + fpatt % ydBkg.val#ydMuon.val
                        backgroundPrediction += ydBkg.val
                        ##print ydBkg.name, "=", ydBkg.val

                backgroundPrediction += ydsPred[bin][0].val
                backgroundPrediction += ydsPred[bin][1].val

                ##print   ydsPred[bin][0].name, "=", ydsPred[bin][0].val
                ##print   ydsPred[bin][1].name, "=", ydsPred[bin][1].val
                dataCardObservation += " " + fpatt % backgroundPrediction
            else:
                dataCardObservation += " " + fpatt % yd.val
        ##print "Summe = ", backgroundPrediction
        ##print ""

        datacard.write(dataCardObservation + "\n")
        datacard.write('##---\n')
        #Longer names
        datacard.write('bin'        + ' ' * (spaceBuffer - len("bin"))         + " ".join([kpatt % cat      for cat in catNames])+"\n")
        datacard.write('process'    + ' ' * (spaceBuffer - len("process"))     + " ".join([kpatt % p        for p in sampNames])+"\n")
        #shorter names
        #datacard.write('bin'        + ' ' * (spaceBuffer - len("bin"))         + " ".join([kpatt % catDict[cat]      for cat in catNames])+"\n")
        #datacard.write('process'    + ' ' * (spaceBuffer - len("process"))     + " ".join([kpatt % p        if SMS not in p else "signal" for p in sampNames])+"\n")
        datacard.write('process'    + ' ' * (spaceBuffer - len("process"))     + " ".join([kpatt % iproc[p] for p in sampNames])+"\n")

        # MC rates
        valueStringArray = []
        otherBackground = 0
        #print "yds", yds
        #print "ydsMuon", ydsMuon
        for yd, ydMu in zip(yds[bin], ydsMuon[bin]):
            tmpYd = yd
            if yd.cat == "SR_SB" or yd.cat == "CR_SB":
                tmpYd = ydMu
            #print "\n", tmpYd
            if type(tmpYd) != int and 'Scan' in tmpYd.name:
                #This is for writing the other bkg in the correct position, at this point it is converted to float.
                if otherBackground != 0:
                    valueStringArray.append(fpatt % otherBackground)
                    otherBackground = 0
                #Signal Value
                valueStringArray.append(fpatt % float(tmpYd.val / factor))
            elif "TTJets" == tmpYd.name or "WJets" == tmpYd.name:
                #This is for writing the other bkg in the correct position
                if otherBackground != 0:
                    valueStringArray.append(fpatt % otherBackground)
                    otherBackground = 0
                #TTJets or WJets written as 1.0 in the SR_MB, as it will be determined by the rateParam
                if tmpYd.cat == "SR_MB":
                    valueStringArray.append(fpatt % 1.0)
                    #valueStringArray.append(fpatt % tmpYd.val)
                else:
                    valueStringArray.append(fpatt % tmpYd.val)
            else:
                #Summing up other backgrounds
                otherBackground += tmpYd.val
        datacard.write('rate'       + ' ' * (spaceBuffer - len("rate"))        + " ".join(valueStringArray)+"\n")

        #Background systematics as lnN (This assumes SR_MB to be first cat
        systSpaceBuffer = len("DLConst_2016")
        doSystematics = True
        if doSystematics:
            for syst in sysTableBttDf.columns:
                if syst == "SBin":
                    continue
                #For testing
                #systName = syst + "_" + year + " " * (systSpaceBuffer - len(syst + "_" + year)) + " lnN"
                systName = syst + " " * (systSpaceBuffer - len(syst)) + " lnN"
                systLine = systName
                #Assume 20% flat unc. for now, do something decent later
                for cat, samp in zip(catNames, sampNames):
                    if samp == "TTJets":
                        if cat == "SR_MB":
                            systVal = "1.000"
                            if bin in sysTableBttDf.index:
                                systVal = sysTableBttDf.loc[bin, syst]
                            if float(systVal) == 1.0:
                                systLine += " " + kpatt % "-"
                            else:
                                systLine += " " + kpatt % systVal

                        else:
                            systLine += " " + kpatt % "-"
                    elif samp == "WJets":
                        if cat == "SR_MB":
                            systVal = "1.000"
                            if bin in sysTableWDf.index:
                                systVal = sysTableWDf.loc[bin, syst]
                            if float(systVal) == 1.0:
                                systLine += " " + kpatt % "-"
                            else:
                                systLine += " " + kpatt % systVal
                        else:
                            systLine += " " + kpatt % "-"
                    elif SMS in samp:
                        systVal = "1.000"
                        if bin in sysTableSignalDf.index and cat + "_" + syst in sysTableSignalDf.columns:
                            if cat not in ["CR_SB", "SR_SB"]:
                                systVal = sysTableMuSignalDf.loc[bin, cat + "_" + syst]
                            else:
                                systVal = sysTableSignalDf.loc[bin, cat + "_" + syst]

                        if systVal == None:
                            systLine += " " + kpatt % "-"
                        elif float(systVal) == 1.0:
                            systLine += " " + kpatt % "-"
                        else:
                            systLine += " " + kpatt % systVal
                    else:
                        systVal = "1.000"
                        if bin in sysTableOtherDf.index and cat + "_syst_" + syst in sysTableOtherDf.columns:
                            systVal = sysTableOtherDf.loc[bin, cat + "_syst_" + syst]
                        if float(systVal) == 1.0:
                            systLine += " " + kpatt % "-"
                        else:
                            systLine += " " + kpatt % systVal
                        #Just to have some number for now
                        #systLine += " " + fpatt % 1.15

                datacard.write(systLine + "\n")
        else: # This is just for quick tests where you do not care about systematics, do not use for real
            #For testing
            systName = "Sigsys" + " " * (systSpaceBuffer - len("Sigsys")) + " lnN"
            #systName = "Sigsys" + "_" + year + " " * (systSpaceBuffer - len("Sigsys" + "_" + year)) + " lnN"
            systLine = systName
            #Assume 20% flat unc. for now, do something decent later
            for cat, samp in zip(catNames, sampNames):
                if samp == "TTJets":
                    systLine += " " + kpatt % "-"
                elif samp == "WJets":
                    systLine += " " + kpatt % "-"
                elif SMS in samp:
                    if cat == "SR_MB":
                        systLine += " " + fpatt % 1.2
                    else:
                        systLine += " " + kpatt % "-"
                else:
                    systLine += " " + kpatt % "-"

            datacard.write(systLine + "\n")

        #Write out paramters for ABCD method based on rate params in the higgs tool
        kappaB_Name = ""
        kappaTT_Name = ""
        kappaW_Name = ""

        data_SR_SB_NB1i_Name = ""
        data_CR_SB_NB1i_Name = ""
        data_CR_MB_Name = ""

        dataMuon_SR_SB_Name = ""
        dataMuon_CR_SB_Name = ""
        dataMuon_CR_MB_Name = ""

        binNameSB = ""

        #For better formattign
        spatt = " %%%ds "  % len("rateParam")
        fpatt2 = " %%%d.%df " % (10,5)
        spaceBuffer2 = len(ydsKappaW[bin][-1].label + bin.split("_")[3] + "_Muon_" + year)
        for yd in ydsKappaTT[bin]:
            Val = yd.val
            Err = yd.err
            Cat = yd.cat
            Name = yd.name
            Label = yd.label

            #This is a bit messy but allows for arbitrary order in ydsKappa
            if "KappaB" in Cat:
                kappaB_LongName = bin + "_kB_" + year
                kappaB_Name = shortenName(bin + "_kB_" + year)
                datacard.write(kappaB_Name + " " * (spaceBuffer2 - len(kappaB_Name)) + spatt % 'param' + fpatt2 % Val +' ' + fpatt2 % Err + '\n')
            elif "KappaTT" in Cat:
                kappaTT_LongName = bin + "_kTT_" + year
                kappaTT_Name = shortenName(bin + "_kTT_" + year)
                datacard.write(kappaTT_Name + " " * (spaceBuffer2 - len(kappaTT_Name)) + spatt % 'param' + fpatt2 % Val +' ' + fpatt2 % Err + '\n')
            elif "SR_SB_NB1i" == Cat:
                data_SR_SB_NB1i_LongName = Label + bin.split("_")[3] + "_" + year
                data_SR_SB_NB1i_Name = shortenName(Label + bin.split("_")[3] + "_" + year)
                datacard.write(data_SR_SB_NB1i_Name + " " * (spaceBuffer2 - len(data_SR_SB_NB1i_Name)) + spatt % "param" + fpatt2 % Val +' ' + fpatt2 % Err + '\n')
            elif "CR_SB_NB1i" == Cat:
                data_CR_SB_NB1i_LongName = Label + bin.split("_")[3] + "_" + year
                data_CR_SB_NB1i_Name = shortenName(Label + bin.split("_")[3] + "_" + year)
                datacard.write(data_CR_SB_NB1i_Name + " " * (spaceBuffer2 - len(data_CR_SB_NB1i_Name)) + spatt % "param" + fpatt2 % Val +' ' + fpatt2 % Err + '\n')
            elif "CR_MB" == Cat:
                data_CR_MB_LongName = Label + "_" + year
                data_CR_MB_Name = shortenName(Label + "_" + year)
                datacard.write(data_CR_MB_Name + " " * (spaceBuffer2 - len(data_CR_MB_Name)) + spatt % "param" + fpatt2 % Val +' ' + fpatt2 % Err + '\n')

        for yd in ydsKappaW[bin]:
            Val = yd.val
            Err = yd.err
            Cat = yd.cat
            Name = yd.name
            Label = yd.label

            #This is a bit messy but allows for arbitrary order in ydsKappa
            if "KappaW" in Cat:
                kappaW_LongName = bin + "_kW_" + year
                kappaW_Name = shortenName(bin + "_kW_" + year)
                datacard.write(kappaW_Name + " " * (spaceBuffer2 - len(kappaW_Name)) + spatt % 'param' + fpatt2 % Val +' ' + fpatt2 % Err + '\n')
            elif "SR_SB" == Cat:
                #dataMuon_SR_SB_Name = shortenName(Label + "_Muon_" + year)
                dataMuon_SR_SB_LongName = Label + bin.split("_")[3] + "_Muon_" + year
                dataMuon_SR_SB_Name = shortenName(Label + bin.split("_")[3] + "_Muon_" + year)
                datacard.write(dataMuon_SR_SB_Name + " " * (spaceBuffer2 - len(dataMuon_SR_SB_Name)) + spatt % "param" + fpatt2 % Val +' ' + fpatt2 % Err + '\n')
            elif "CR_SB" == Cat:
                #dataMuon_CR_SB_Name = shortenName(Label + "_Muon_" + year)
                dataMuon_CR_SB_LongName = Label + bin.split("_")[3] + "_Muon_" + year
                dataMuon_CR_SB_Name = shortenName(Label + bin.split("_")[3] + "_Muon_" + year)
                datacard.write(dataMuon_CR_SB_Name + " " * (spaceBuffer2 - len(dataMuon_CR_SB_Name)) + spatt % "param" + fpatt2 % Val +' ' + fpatt2 % Err + '\n')
                binNameSB = Label.replace("_CR", "").replace("_SR", "")
            elif "CR_MB" == Cat:
                dataMuon_CR_MB_LongName = Label + "_Muon_" + year
                dataMuon_CR_MB_Name = shortenName(Label + "_Muon_" + year)
                datacard.write(dataMuon_CR_MB_Name + " " * (spaceBuffer2 - len(dataMuon_CR_MB_Name)) + spatt % "param" + fpatt2 % Val +' ' + fpatt2 % Err + '\n')

        #Prepare naming of the rateParam
        tt_SR_SB_Name = shortenName(data_SR_SB_NB1i_LongName.replace(year, "TT_" + year))
        tt_CR_SB_Name = shortenName(data_CR_SB_NB1i_LongName.replace(year, "TT_" + year))
        tt_CR_MB_Name = shortenName(data_CR_MB_LongName.replace(year, "TT_" + year))
        tt_SR_MB_Name = shortenName(data_CR_MB_LongName.replace("CR","SR").replace(year, "TT_" + year))

        w_SR_SB_Name = shortenName(dataMuon_SR_SB_LongName.replace("Muon", "W"))
        w_CR_SB_Name = shortenName(dataMuon_CR_SB_LongName.replace("Muon", "W"))
        w_SR_MB_Name  = shortenName(dataMuon_CR_MB_LongName.replace("CR", "SR").replace("Muon", "W"))

        tt_SR_MB_LongName = data_CR_MB_LongName.replace("CR","SR").replace(year, "TT_" + year)
        w_SR_SB_LongName = dataMuon_SR_SB_LongName.replace("Muon", "W")
        w_SR_MB_LongName  = dataMuon_CR_MB_LongName.replace("CR", "SR").replace("Muon", "W")

        fTT_SR_MB_Name = shortenName(tt_SR_MB_LongName.replace("TT", "fTT"))
        fTT_SR_SB_Name = shortenName(w_SR_SB_LongName.replace("_W_", "_fTT_"))
        fW_SR_MB_Name = shortenName(w_SR_MB_LongName.replace("_W_", "_fW_"))

        #TTbar in MB fraction used for TTJets prediction
        ttbarMBFraction = yieldFractionDf.loc[bin, "TTJetsIncl_fraction"]
        ttbarMBFractionErr = yieldFractionDf.loc[bin, "TTJetsIncl_fraction_err"]
        datacard.write(fTT_SR_MB_Name + " " * (spaceBuffer2 - len(fTT_SR_MB_Name)) + spatt % "param" + fpatt2 % ttbarMBFraction + " " + fpatt2 % ttbarMBFractionErr + "\n")

        #TTbar in SB fraction used for WJets prediction
        ttbarSBFraction = yieldFractionDf.loc[binNameSB, "TTJetsIncl_fraction"]
        ttbarSBFractionErr = yieldFractionDf.loc[binNameSB, "TTJetsIncl_fraction_err"]
        datacard.write(fTT_SR_SB_Name + " " * (spaceBuffer2 - len(fTT_SR_SB_Name)) + spatt % "param" + fpatt2 % ttbarSBFraction + " " + fpatt2 % ttbarSBFractionErr + "\n")

        #WJets in MB fraction used for WJets prediction
        wjetsMBFraction = yieldFractionDf.loc[bin, "WJetsIncl_fraction"]
        wjetsMBFractionErr = yieldFractionDf.loc[bin, "WJetsIncl_fraction_err"]
        datacard.write(fW_SR_MB_Name + " " * (spaceBuffer2 - len(fW_SR_MB_Name)) + spatt % "param"  + fpatt2 % wjetsMBFraction + " " + fpatt2 % wjetsMBFractionErr + "\n")

        tt_SR_MB_Formula = "(@0*@1*@2*@3/@4*@5)"
        tt_SR_MB_Parameters = fTT_SR_MB_Name       + "," + \
                              kappaB_Name          + "," + \
                              kappaTT_Name         + "," + \
                              data_SR_SB_NB1i_Name + "," + \
                              data_CR_SB_NB1i_Name + "," + \
                              data_CR_MB_Name

        w_SR_MB_Formula    = "(@0*@1*(@2-@3*@4*@5/@6*@7)/((1-@3)*@7)*@8)"

        w_SR_MB_Parameters = fW_SR_MB_Name           + "," + \
                                kappaW_Name          + "," + \
                                dataMuon_SR_SB_Name  + "," + \
                                fTT_SR_SB_Name       + "," + \
                                kappaB_Name          + "," + \
                                data_SR_SB_NB1i_Name + "," + \
                                data_CR_SB_NB1i_Name + "," + \
                                dataMuon_CR_SB_Name  + "," + \
                                data_CR_MB_Name

        #correct formula
        spatt2 = " %%%ds "  % len(w_SR_MB_Formula)
        datacard.write(tt_SR_MB_Name + " " * (spaceBuffer2 - len(tt_SR_MB_Name)) + " " + "rateParam" + " " + "SR_MB" + " " + "TTJets" + spatt2 % tt_SR_MB_Formula + " " + tt_SR_MB_Parameters + "\n")
        datacard.write(w_SR_MB_Name  + " " * (spaceBuffer2 - len(w_SR_MB_Name))  + " " + "rateParam" + " " + "SR_MB" + " " + " WJets" + spatt2 % w_SR_MB_Formula  + " " + w_SR_MB_Parameters  + "\n")

        #correct but short name
        #datacard.write(tt_SR_MB_Name + " " * (spaceBuffer2 - len(tt_SR_MB_Name)) + " " + "rateParam" + " " + catDict["SR_MB"] + " " + "TTJets"  + spatt2 % tt_SR_MB_Formula + " " + tt_SR_MB_Parameters + "\n")
        #datacard.write(w_SR_MB_Name  + " " * (spaceBuffer2 - len(w_SR_MB_Name))  + " " + "rateParam" + " " + catDict["SR_MB"] + " " + "WJets "  + spatt2 % w_SR_MB_Formula  + " " + w_SR_MB_Parameters  + "\n")

    return 1

if __name__ == "__main__":

    ## remove '-b' option
    if '-b' in sys.argv:
        sys.argv.remove('-b')
        _batchMode = True

    if len(sys.argv) > 2:
        out = sys.argv[1]
        print '# out is', out

        year = str(sys.argv[2])
        print '# year is', year
    else:
        print "Give output dir and year as argument!"
        exit(0)

    ## Create Yield Storage
    ydsSys = YieldStore("lepYields")
    storeDict = True

    #Define Signal pickle file
    pckname = "pickles/"+SMS+"_sigSysts_" + year + "all.pckz"
    if storeDict == True and os.path.exists(pckname):

        print "#Loading saved yields from pickle!"

        import cPickle as pickle
        import gzip

        ydsSys = pickle.load( gzip.open( pckname, "rb" ) )
        #print [name for name in ydsSys.samples if ("syst" in name and "mGo1500_mLSP1000" in name)]

    yds5 = YieldStore("lepYields")
    yds67 = YieldStore("lepYields")
    yds8 = YieldStore("lepYields")
    ydsMu5 = YieldStore("muYields")
    ydsMu67 = YieldStore("muYields")
    ydsMu8 = YieldStore("muYields")

    #yds5.addFromFiles("yield_0b_postmerge_" + year + "/*/merged/LT*NJ5*", ("lep","sele"))
    #yds67.addFromFiles("yield_0b_postmerge_" + year + "/*/merged/LT*NJ67*", ("lep","sele"))
    #yds8.addFromFiles("yield_0b_postmerge_" + year + "/*/merged/LT*NJ8i*", ("lep","sele"))
    #ydsMu5.addFromFiles("yield_0b_postmerge_" + year + "/*/merged/LT*NJ5*", ("mu","sele"))
    #ydsMu67.addFromFiles("yield_0b_postmerge_" + year + "/*/merged/LT*NJ67*", ("mu","sele"))
    #ydsMu8.addFromFiles("yield_0b_postmerge_" + year + "/*/merged/LT*NJ8i*", ("mu","sele"))

    yds5.addFromFiles("yield_0b_postmerge_" + year + "/*/merged/LT1_HT0_NB0_NJ5_NW0*", ("lep","sele"))
    yds67.addFromFiles("yield_0b_postmerge_" + year + "/*/merged/LT4i_HT3i_NB0_NJ67_NW0*", ("lep","sele"))
    yds8.addFromFiles("yield_0b_postmerge_" + year + "/*/merged/LT1_HT02_NB0_NJ8i_NW0*", ("lep","sele"))
    ydsMu5.addFromFiles("yield_0b_postmerge_" + year + "/*/merged/LT1_HT0_NB0_NJ5_NW0*", ("mu","sele"))
    ydsMu67.addFromFiles("yield_0b_postmerge_" + year + "/*/merged/LT4i_HT3i_NB0_NJ67_NW0*", ("mu","sele"))
    ydsMu8.addFromFiles("yield_0b_postmerge_" + year + "/*/merged/LT1_HT02_NB0_NJ8i_NW0*", ("mu","sele"))

    #Read the yield fractions from csv
    yearString = "2016_EXT"
    if year == "2016":
        yearString = "2016_EXT"
    elif year == "2017":
        yearString = "2017"
    elif year == "2018":
        yearString = "2018"
    elif year == "run2":
        yearString = "run2"

    yieldCsvFile =  "TemplateFit/templateFits_0b_" + yearString + "_nominal.csv"
    #if "grid-dilep" in pattern:
        #yieldCsvFile =  "TemplateFit/templateFits_0b_" + yearString + "_dilep-corr.csv"
    yieldFractionDf = read_csv(yieldCsvFile, index_col = "bin")

    sysTableBttFile = "SystTables/sysTable_BTT_" + year + ".dat"
    sysTableBttDf = read_csv(sysTableBttFile, index_col = "bin", sep = "\s*\|\s*", skiprows = 1, engine='python')

    sysTableWFile = "SystTables/sysTable_W_" + year + ".dat"
    sysTableWDf = read_csv(sysTableWFile, index_col = "bin", sep = "\s*\|\s*", skiprows = 1, engine='python')

    #sysTableSignalFile = "SystTables/signalTablev1_" + year + ".dat"

    sysTableOtherFile = "sysTable_combinedBKG_run2.dat"
    sysTableOtherDf = read_csv(sysTableOtherFile, index_col = "bin", sep = "\s*\|\s*", engine='python')

    ####SELECT DATA OR MC###
    prefix = 'EWK'
    #prefix = 'data'

    for mGo in [1500, 1900]:
        for mLSP in [0, 100]:
            for ydIn, ydMuIn in ((yds5, ydsMu5), (yds67, ydsMu67) , (yds8, ydsMu8)):
                print "making datacards for "+str(mGo)+ ' '+str(mLSP)
                signal = SMS+'_Scan_mGo'+str(mGo)+'_mLSP'+str(mLSP)
                cat = 'SR_MB'
                sampsObs = [('EWK',cat),]
                ydsObs = ydIn.getMixDict(sampsObs)
                sampsBkg = [('TTJets',cat), ('WJets',cat), ('TTV',cat), ('SingleT',cat), ('DY',cat), ('QCD',cat)]
                sampsSig = [(signal ,cat),]
                samps = sampsBkg + sampsSig
                ydsSig = ydIn.getMixDict(sampsSig)
                ydsMuonSig = ydMuIn.getMixDict(sampsSig)
                #print ydsSig
                if type(ydsSig.values()[0][0]) == int or type(ydsMuonSig.values()[0][0]) == int:
                    print "signal not available will skip"
                    continue

                sysTableSignalFile = "signal_syst_tables_run2merged/signalTablev1_run2merged" + "_mGo" + str(mGo)+ "_mLSP" + str(mLSP) + ".dat"
                sysTableSignalDf = read_csv(sysTableSignalFile, index_col = "bin", sep = "\s*\|\s*", engine='python')

		sysTableMuSignalFile = "signal_syst_tables_run2merged/signalTablev1_Mu_run2merged" + "_mGo" + str(mGo)+ "_mLSP" + str(mLSP) + ".dat"
                sysTableMuSignalDf = read_csv(sysTableSignalFile, index_col = "bin", sep = "\s*\|\s*", engine='python')

                yds = ydIn.getMixDict(samps)

                cats = ('SR_MB', 'CR_MB', 'SR_SB','CR_SB', 'SR_SB_NB1i', 'CR_SB_NB1i')
                catsNoSR = ('CR_MB', 'SR_SB','CR_SB', 'SR_SB_NB1i', 'CR_SB_NB1i')

                sampsABCDbkg = []
                sampsABCDObs = []
                for cat in cats:
                    sampsABCDObs.append((prefix, cat))
                    sampsABCDbkg.append(("TTJets", cat))
                    sampsABCDbkg.append(("WJets", cat))
                    sampsABCDbkg.append(("TTV", cat))
                    sampsABCDbkg.append(("SingleT", cat))
                    sampsABCDbkg.append(("DY", cat))
                    sampsABCDbkg.append(("VV", cat))

                sampsABCDsig = [(SMS+'_Scan_mGo'+str(mGo)+'_mLSP'+str(mLSP),cat) for cat in cats]

                cat = 'SR_MB'
                sampsABCD = sampsABCDbkg + sampsABCDsig

                ydsABCD = ydIn.getMixDict(sampsABCD)
                ydsMuonABCD = ydMuIn.getMixDict(sampsABCD)
                ydsObsABCD = ydIn.getMixDict(sampsABCDObs)
                ydsMuonObsABCD = ydMuIn.getMixDict(sampsABCDObs)
                ydsPredABCD = ydIn.getMixDict([("TTJets_pred", "SR_MB"), ("WJets_pred", "SR_MB")])

                ydsKappaTT = ydIn.getMixDict([("TTJets", "KappaB"), ("TTJets", "KappaTT"), ("data_QCDsubtr", "CR_MB"), ("data_QCDsubtr", "CR_SB_NB1i"), ("data_QCDsubtr", "SR_SB_NB1i")])
                ydsKappaW = ydMuIn.getMixDict([("WJets", "KappaW"), ("data", "CR_MB"), ("data", "CR_SB"), ("data", "SR_SB")])

		printABCDCard(ydsABCD, ydsMuonABCD, ydsObsABCD, ydsMuonObsABCD, ydsPredABCD, ydsKappaTT, ydsKappaW, year = year, yieldFractionDf = yieldFractionDf, sysTableBttDf = sysTableBttDf, sysTableWDf = sysTableWDf, sysTableSignalDf = sysTableSignalDf, sysTableMuSignalDf = sysTableMuSignalDf, sysTableOtherDf = sysTableOtherDf)
