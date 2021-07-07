blinded = True

# LT bins
binsLT = {}
binsLT['LT1'] = ('250 < LT && LT < 350','[250, 350]')
binsLT['LT2'] = ('350 < LT && LT < 450','[350, 450]')
binsLT['LT3'] = ('450 < LT && LT < 650','[450, 650]')
binsLT['LT4i'] = ('650 <= LT','$\geq$ 650')
binsLT['LT12']  = ('250 < LT && LT < 450','[250, 350]')
binsLT['LT3i'] = ('450 <= LT','$\geq$ 450')

# HT bins
binsHT = {}
binsHT['HT0'] = ('500 < HT && HT < 750','[500, 750]')
binsHT['HT1i'] = ('750 < HT','$\geq$ 750')
binsHT['HT1'] = ('750 < HT && HT < 1250','[750, 1250]')
binsHT['HT3i'] = ('1250 < HT','$\geq$ 1250')

binsHT['HT02'] = ('500 < HT && HT < 1000','[500, 1000]')
binsHT['HT2i'] = ('1000 < HT','$\geq$ 1000')
binsHT['HT03'] = ('500 < HT && HT < 1250','[500, 1250]')

# NB bins
binsNB = {}
binsNB['NB0'] = ('nBJet == 0','$=$ 0')
binsNB['NB1i'] = ('nBJet >= 1','$\geq$ 1')

# NW Bins
binsNW = {}
binsNW['NW0'] = ('nWTight == 0','$=$ 0')
binsNW['NW0i'] = ('nWTight >= 0','$\geq$ 0')
binsNW['NW1i'] = ('nWTight >= 1','$\geq$ 1')

# NJ Bins
binsNJ = {}
binsNJ['NJ34'] = ('3 <= nJets30Clean && nJets30Clean <= 4','[3, 4]')
binsNJ['NJ45'] = ('4 <= nJets30Clean && nJets30Clean <= 5','[4, 5]')
binsNJ['NJ5'] = ('nJets30Clean == 5','[5]')
binsNJ['NJ67'] = ('6 <= nJets30Clean && nJets30Clean <= 7','[6, 7]')
binsNJ['NJ8i'] = ('8 <= nJets30Clean','$\geq$ 8')

# List of missing bins to only reprocces remove all bins which do not match any substring given in missingBins
# e.g. missingBins = ["LT3", "NJ34"] would include all bins that use LT3 or NJ34
# if list is empty, all bins will be produced

missingBins = [
]

doMissingBinsOnly = False
#doMissingBinsOnly = True
filename = "missingBins/missingBins_syst_btagHF_2017.md"
#filename = "missingBins/missingBins_signal_btagHF_2018.md"
if doMissingBinsOnly:
    with open(filename) as missingBinsFile:
        missingBins = missingBinsFile.read().splitlines()

def getSRcut(nj_bin, lt_bin, sr_bin, blinded):

    dPhiCut = "dPhi "
    cutLbl = "$\delta \phi "

    if "SR" in sr_bin:
        dPhiCut += " > "
        cutLbl += " > $ "
    elif "CR" in sr_bin:
        dPhiCut += " < "
        cutLbl += " < $ "

    ## DPhi Cuts for LT bins
    cuts = { "LT1": 1.0, "LT1i": 1.0, "LT2": 1.0,"LT2i": 0.75, "LT3": 0.75, "LT3i": 0.75, "LT4": 0.5, "LT4i": 0.5 , "LT5i":0.5}
    #cuts = { "LT1": 1.0, "LT1i": 1.0, "LT2": 0.75,"LT2i": 0.75, "LT3": 0.75, "LT3i": 0.75, "LT4": 0.5, "LT4i": 0.2 , "LT5i":0.5} #for VeryTight W tagging

    for bin in cuts:
        if bin in lt_bin:
            cut = cuts[bin]; break
    else:
        print "No cut found for", nj_bin, lt_bin
        cut = 0

    if blinded and ('68' in nj_bin or '9i' in nj_bin) and "SR" in sr_bin:
        cut = 99.0

    dPhiCut += str(cut)
    cutLbl += str(cut)

    #print nj_bin, lt_bin, sr_bin, dPhiCut, cutLbl

    return (dPhiCut,cutLbl)


### REAL SEARCH BINS (also for RCS)
cutDictf34 = {}
cutDictf45 = {}
cutDictf5 = {}
cutDictf67 = {}
cutDictf8 = {}

cutDictSR34 = {}
cutDictCR34 = {}

cutDictSR45 = {}
cutDictCR45 = {}

cutDictSR5 = {}
cutDictCR5 = {}

cutDictSR67 = {}
cutDictCR67 = {}

cutDictSR8 = {}
cutDictCR8 = {}

njbins = ["NJ34", "NJ45", "NJ5", "NJ67", "NJ8i"]
cutDicts = [cutDictf34, cutDictf45, cutDictf5, cutDictf67, cutDictf8]
cutDictsCR = [cutDictCR34, cutDictCR45, cutDictCR5, cutDictCR67, cutDictCR8]
cutDictsSR = [cutDictSR34, cutDictSR45, cutDictSR5, cutDictSR67, cutDictSR8]
#Definition of the search bins
# WJets  SB: NJ34
# TTJets SB: NJ45, NB0, NB1i
# MainBand:  NJ5, NJ67, NJ8i
for nj_bin, cutDict, cutDictSR, cutDictCR in zip(njbins, cutDicts, cutDictsCR, cutDictsSR):
    nj_cut = binsNJ[nj_bin][0]

    nbbins = ["NB0"]
    if nj_bin == "NJ45":
        nbbins = ["NB0", "NB1i"]

    for nb_bin in nbbins:
        nb_cut = binsNB[nb_bin][0]

        for lt_bin in ['LT1','LT2','LT3', 'LT4i']:
            lt_cut = binsLT[lt_bin][0]

            htbins = []

            if nj_bin in ["NJ34", "NJ45"]:#WJets and TTJets SB, has to match MB bins
                if lt_bin in ['LT1', 'LT2']:
                    htbins = ['HT0', 'HT1i', 'HT02', 'HT2i']
                elif lt_bin in ['LT3']:
                    htbins = ['HT0', 'HT1', 'HT03', 'HT3i']
                elif lt_bin in ['LT4i']:
                    htbins = ['HT03', 'HT3i']

            elif nj_bin == "NJ5":#MB
                if lt_bin in ['LT1', 'LT2']:
                    htbins = ['HT0', 'HT1i']
                elif lt_bin in ['LT3']:
                    htbins = ['HT0', 'HT1', 'HT3i']
                elif lt_bin in ['LT4i']:
                    htbins = ['HT03', 'HT3i']

            elif nj_bin == "NJ67":#MB
                if lt_bin in ['LT1', 'LT2']:
                    htbins = ['HT02','HT2i']
                elif lt_bin in ['LT3']:
                    htbins = ['HT0', 'HT1','HT3i']
                elif lt_bin in ['LT4i']:
                    htbins = ['HT03', 'HT3i']

            elif nj_bin == "NJ8i":#MB
                if lt_bin in ['LT1', 'LT2']:
                    htbins = ['HT02','HT2i']
                elif lt_bin in ['LT3', 'LT4i']:
                    htbins = ['HT03','HT3i']

            for ht_bin in htbins:
                ht_cut =binsHT[ht_bin][0]

                nwbins = ['NW0','NW1i']
                #Expections in the NJ34 SB
                if nj_bin in ["NJ34", "NJ45"]:
                    nwbins = ["NW0", "NW0i", "NW1i"]

                for nw_bin in nwbins:
                    nw_cut = binsNW[nw_bin][0]

                    #All bins without SR, CR cut
                    binname = "%s_%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin,nw_bin)
                    cutDict[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut),("base",nw_bin,nw_cut)]

                    # Applying the SR cut: dPhi > dPhi_min
                    sr_bin = "SR"
                    sr_cut = getSRcut(nj_bin, lt_bin, sr_bin, blinded)[0]

                    binname = "%s_%s_%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin,nw_bin,sr_bin)
                    cutDictSR[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut),("base",nw_bin,nw_cut),("base",sr_bin,sr_cut)]

                    # Applying the CR cut: dPhi < dPhi_min
                    cr_bin = "CR"
                    cr_cut = getSRcut(nj_bin, lt_bin, cr_bin, blinded)[0]
                    binname = "%s_%s_%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin,nw_bin,cr_bin)
                    cutDictCR[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut),("base",nw_bin,nw_cut),("base",cr_bin,cr_cut)]

if missingBins != []:
    for cutDictf, cutDictSR, cutDictCR in [(cutDictf34, cutDictSR34, cutDictCR34), (cutDictf45, cutDictSR45, cutDictCR45), (cutDictf5, cutDictSR5, cutDictCR5), (cutDictf67, cutDictSR67, cutDictCR67), (cutDictf8, cutDictSR8, cutDictCR8)]:
        for bin in cutDictf.keys():
            keepBin = False
            for mBin in missingBins:
                if mBin in bin:
                    keepBin = True
                    break
            if not keepBin:
                del cutDictf[bin]

        for bin in cutDictSR.keys():
            keepBin = False
            for mBin in missingBins:
                if mBin in bin:
                    keepBin = True
                    break
            if not keepBin:
                del cutDictSR[bin]

        for bin in cutDictCR.keys():
            keepBin = False
            for mBin in missingBins:
                if mBin in bin:
                    keepBin = True
                    break
            if not keepBin:
                del cutDictCR[bin]

if __name__=="__main__":
    """
    Executing the searchbins file prints out all bins inside the cutDicts for debugging
    python searchBins_0b_with_NW.py | sort | uniq > searchBin.md
    ls outputDir/grid/ | grep root | sort | uniq | sed "s@.yields.root@@g" > binList.md
    diff searchBin.md binList.md
    or
    diff binList.md searchBin.md  | grep ">" | awk '{printf $2 "\n"}' > missingBins.md
    This might also list already produced bins but will definitely include missing bins!
    """

    #print "NJ34 WJets"
    for bin in cutDictSR34.keys():
        print(bin)
    for bin in cutDictCR34.keys():
        print(bin)

    #print "NJ45 TTJets"
    for bin in cutDictSR45.keys():
        print(bin)
    for bin in cutDictCR45.keys():
        print(bin)

    #print "Main Band Bins!"
    for bin in cutDictSR5.keys():
        print(bin)
    for bin in cutDictSR67.keys():
        print(bin)
    for bin in cutDictSR8.keys():
        print(bin)

    for bin in cutDictCR5.keys():
        print(bin)
    for bin in cutDictCR67.keys():
        print(bin)
    for bin in cutDictCR8.keys():
        print(bin)
