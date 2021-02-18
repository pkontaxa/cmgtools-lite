blinded = True

# LT bins
binsLT = {}
binsLT['LT1'] = ('250 < LT && LT < 350','[250, 350]')
binsLT['LT2'] = ('350 < LT && LT < 450','[350, 450]')
binsLT['LT3'] = ('450 < LT && LT < 650','[450, 650]')
binsLT['LT4i'] = ('650 <= LT','$\geq$ 650')

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
binsNJ['NJ34_forWJets'] = ('3 <= nJets30Clean && nJets30Clean <= 4','[3, 4]')
binsNJ['NJ5_forWJets'] = ('nJets30Clean == 5','[5]')
binsNJ['NJ67_forWJets'] = ('6 <= nJets30Clean && nJets30Clean <= 7','[6, 7]')
binsNJ['NJ8i_forWJets'] = ('8 <= nJets30Clean','$\geq$ 8')

binsNJ['NJ45_forTTJets'] = ('4 <= nJets30Clean && nJets30Clean <= 5','[4, 5]')
binsNJ['NJ5_forTTJets'] = ('nJets30Clean == 5','[5]')
binsNJ['NJ67_forTTJets'] = ('6 <= nJets30Clean && nJets30Clean <= 7','[6, 7]')
binsNJ['NJ8i_forTTJets'] = ('8 <= nJets30Clean','$\geq$ 8')

# Positive/negative lepton charges
binsLepCharge = {}
binsLepCharge['pos'] = ('Lep_pdgId > 0', '+1')
binsLepCharge['neg'] = ('Lep_pdgId < 0', '-1')


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

# W+Jets sideband with nJet = [3,4]
for nj_bin in ['NJ34_forWJets']:
    nj_cut = binsNJ[nj_bin][0]

    nb_bin = 'NB0'
    nb_cut = binsNB[nb_bin][0]

    for lep_charge in ['neg', 'pos']:
        charge_sel = binsLepCharge[lep_charge][0]
	
	for nw_bin in ['NW0','NW0i','NW1i']:
    	    nw_cut = binsNW[nw_bin][0]

	    for lt_bin in ['LT1','LT2','LT3','LT4i']:
		lt_cut = binsLT[lt_bin][0]
		htbins = []

		if lt_bin in ['LT1', 'LT2']:
		    htbins+= ['HT0', 'HT1i', 'HT02', 'HT2i']

		elif lt_bin in ['LT3', 'LT4i']:
		    htbins+= ['HT0', 'HT1', 'HT03', 'HT3i']

		for ht_bin in htbins:
		    ht_cut =binsHT[ht_bin][0]

		    binname = "%s_%s_%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin,nw_bin,lep_charge)
		    cutDictf34[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut),("base",nw_bin,nw_cut),("base",lep_charge,charge_sel)]

		    # split to SR/CR
		    for sr_bin in ['SR']:
			sr_cut = getSRcut(nj_bin, lt_bin, sr_bin, blinded)[0]

			binname = "%s_%s_%s_%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin,nw_bin,lep_charge,sr_bin)
			cutDictSR34[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut),("base",nw_bin,nw_cut),("base",lep_charge,charge_sel),("base",sr_bin,sr_cut)]

		    for cr_bin in ['CR']:
			cr_cut = getSRcut(nj_bin, lt_bin, cr_bin, blinded)[0]
			binname = "%s_%s_%s_%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin,nw_bin,lep_charge,cr_bin)
			cutDictCR34[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut),("base",nw_bin,nw_cut),("base",lep_charge,charge_sel),("base",cr_bin,cr_cut)]

# TTbar sideband with nJet = [4,5]
for nj_bin in ['NJ45_forTTJets']:
    nj_cut = binsNJ[nj_bin][0]

    for nb_bin in ['NB0', 'NB1i']:
        nb_cut = binsNB[nb_bin][0]
	
	for nw_bin in ['NW0','NW0i','NW1i']:
    	    nw_cut = binsNW[nw_bin][0]

	    for lt_bin in ['LT1','LT2','LT3','LT4i']:
		lt_cut = binsLT[lt_bin][0]
		htbins = []

		if lt_bin in ['LT1', 'LT2']:
		   htbins+= ['HT0', 'HT1i', 'HT02', 'HT2i']

		elif lt_bin in ['LT3', 'LT4i']:
		     htbins+= ['HT0', 'HT1', 'HT03', 'HT3i']

		for ht_bin in htbins:
		    ht_cut =binsHT[ht_bin][0]

		    binname = "%s_%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin,nw_bin)
		    cutDictf45[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut),("base",nw_bin,nw_cut)]

		    # split to SR/CR
		    for sr_bin in ['SR']:
			sr_cut = getSRcut(nj_bin, lt_bin, sr_bin, blinded)[0]

			binname = "%s_%s_%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin,nw_bin,sr_bin)
			cutDictSR45[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut),("base",nw_bin,nw_cut),("base",sr_bin,sr_cut)]

		    for cr_bin in ['CR']:
			cr_cut = getSRcut(nj_bin, lt_bin, cr_bin, blinded)[0]
			binname = "%s_%s_%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin,nw_bin,cr_bin)
			cutDictCR45[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut),("base",nw_bin,nw_cut),("base",cr_bin,cr_cut)]

# Main bands
for nj_bin in ['NJ5_forWJets']:
    nj_cut = binsNJ[nj_bin][0]

    nb_bin = 'NB0'
    nb_cut = binsNB[nb_bin][0]

    for lep_charge in ['neg', 'pos']:
        charge_sel = binsLepCharge[lep_charge][0]
	
	for nw_bin in ['NW0','NW1i']:
	    nw_cut = binsNW[nw_bin][0]
	    
	    for lt_bin in ['LT1','LT2','LT3','LT4i']:
	        lt_cut = binsLT[lt_bin][0]
		
		htbins = []
		if lt_bin in ['LT1', 'LT2']:
		    htbins+= ['HT0', 'HT1i']
		
		elif lt_bin in ['LT3', 'LT4i']:
		    htbins+= ['HT0', 'HT1', 'HT3i']
		
		for ht_bin in htbins:
		    ht_cut =binsHT[ht_bin][0]
		    
		    binname = "%s_%s_%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin,nw_bin,lep_charge)
		    cutDictf5[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut),("base",nw_bin,nw_cut),("base",lep_charge,charge_sel)]
		    
		    # split to SR/CR
		    for sr_bin in ['SR']:
		        sr_cut = getSRcut(nj_bin, lt_bin, sr_bin, blinded)[0]

		        binname = "%s_%s_%s_%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin,nw_bin,lep_charge,sr_bin)
			cutDictSR5[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut),("base",nw_bin,nw_cut),("base",lep_charge,charge_sel),("base",sr_bin,sr_cut)]
			
		    for cr_bin in ['CR']:
		        cr_cut = getSRcut(nj_bin, lt_bin, cr_bin, blinded)[0]
			
		        binname = "%s_%s_%s_%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin,nw_bin,lep_charge,cr_bin)
			cutDictCR5[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut),("base",nw_bin,nw_cut),("base",lep_charge,charge_sel),("base",cr_bin,cr_cut)]


for nj_bin in ['NJ5_forTTJets']:
    nj_cut = binsNJ[nj_bin][0]
    
    nb_bin = 'NB0'
    nb_cut = binsNB[nb_bin][0]
    
    for nw_bin in ['NW0','NW1i']:
        nw_cut = binsNW[nw_bin][0]
	
	for lt_bin in ['LT1','LT2','LT3','LT4i']:
	    lt_cut = binsLT[lt_bin][0]
	    
	    htbins = []
	    if lt_bin in ['LT1', 'LT2']:
	        htbins+= ['HT0', 'HT1i']
	    
	    elif lt_bin in ['LT3', 'LT4i']:
	        htbins+= ['HT0', 'HT1', 'HT3i']
	    
	    for ht_bin in htbins:
	        ht_cut =binsHT[ht_bin][0]
		
		binname = "%s_%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin,nw_bin)
		cutDictf5[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut),("base",nw_bin,nw_cut)]
		
		# split to SR/CR
		for sr_bin in ['SR']:
		    sr_cut = getSRcut(nj_bin, lt_bin, sr_bin, blinded)[0]

		    binname = "%s_%s_%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin,nw_bin,sr_bin)
		    cutDictSR5[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut),("base",nw_bin,nw_cut),("base",sr_bin,sr_cut)]
		
		for cr_bin in ['CR']:
		    cr_cut = getSRcut(nj_bin, lt_bin, cr_bin, blinded)[0]
		    
		    binname = "%s_%s_%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin,nw_bin,cr_bin)
		    cutDictCR5[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut),("base",nw_bin,nw_cut),("base",cr_bin,cr_cut)]


for nj_bin in ['NJ67_forWJets']:
    nj_cut = binsNJ[nj_bin][0]
    
    nb_bin = 'NB0'
    nb_cut = binsNB[nb_bin][0]

    for lep_charge in ['neg', 'pos']:
        charge_sel = binsLepCharge[lep_charge][0]
	
	for nw_bin in ['NW0','NW1i']:
	    nw_cut = binsNW[nw_bin][0]
	    
	    for lt_bin in ['LT1','LT2','LT3','LT4i']:
	        lt_cut = binsLT[lt_bin][0]
		
		htbins = []
	        if lt_bin in ['LT1', 'LT2']:
	            htbins+= ['HT02','HT2i']
	        elif lt_bin in ['LT3', 'LT4i']:
	            htbins+= ['HT0', 'HT1','HT3i']
	
        	for ht_bin in htbins:
        	    ht_cut =binsHT[ht_bin][0]
		    
		    binname = "%s_%s_%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin,nw_bin,lep_charge)
		    cutDictf67[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut),("base",nw_bin,nw_cut),("base",lep_charge,charge_sel)]
		    
		    # split to SR/CR
		    for sr_bin in ['SR']:
		        sr_cut = getSRcut(nj_bin, lt_bin, sr_bin, blinded)[0]
			
			binname = "%s_%s_%s_%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin,nw_bin,lep_charge,sr_bin)
			cutDictSR67[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut),("base",nw_bin,nw_cut),("base",lep_charge,charge_sel),("base",sr_bin,sr_cut)]

	            for cr_bin in ['CR']:
        		cr_cut = getSRcut(nj_bin, lt_bin, cr_bin, blinded)[0]
        		    
        		binname = "%s_%s_%s_%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin,nw_bin,lep_charge,cr_bin)
        		cutDictCR67[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut),("base",nw_bin,nw_cut),("base",lep_charge,charge_sel),("base",cr_bin,cr_cut)]


for nj_bin in ['NJ67_forTTJets']:
    nj_cut = binsNJ[nj_bin][0]
    
    nb_bin = 'NB0'
    nb_cut = binsNB[nb_bin][0]
    
    for nw_bin in ['NW0','NW1i']:
        nw_cut = binsNW[nw_bin][0]
	
	for lt_bin in ['LT1','LT2','LT3','LT4i']:
	    lt_cut = binsLT[lt_bin][0]
	    
	    htbins = []
	    if lt_bin in ['LT1', 'LT2']:
	        htbins+= ['HT02','HT2i']
	    elif lt_bin in ['LT3', 'LT4i']:
	        htbins+= ['HT0', 'HT1','HT3i']
	
	    for ht_bin in htbins:
	        ht_cut =binsHT[ht_bin][0]
		
		binname = "%s_%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin,nw_bin)
		cutDictf67[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut),("base",nw_bin,nw_cut)]
		
		# split to SR/CR
		for sr_bin in ['SR']:
		    sr_cut = getSRcut(nj_bin, lt_bin, sr_bin, blinded)[0]
		    
		    binname = "%s_%s_%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin,nw_bin,sr_bin)
		    cutDictSR67[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut),("base",nw_bin,nw_cut),("base",sr_bin,sr_cut)]
		
		for cr_bin in ['CR']:
		    cr_cut = getSRcut(nj_bin, lt_bin, cr_bin, blinded)[0]
		    
		    binname = "%s_%s_%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin,nw_bin,cr_bin)
		    cutDictCR67[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut),("base",nw_bin,nw_cut),("base",cr_bin,cr_cut)]


for nj_bin in ['NJ8i_forWJets']:
    nj_cut = binsNJ[nj_bin][0]
    
    nb_bin = 'NB0'
    nb_cut = binsNB[nb_bin][0]
    
    for lep_charge in ['neg', 'pos']:
        charge_sel = binsLepCharge[lep_charge][0]
	
	for lt_bin in ['LT1','LT2','LT3','LT4i']:
	    lt_cut = binsLT[lt_bin][0]
	    
	    htbins = []
	    if lt_bin in ['LT1', 'LT2']:
	        htbins+= ['HT02','HT2i']
	    elif lt_bin in ['LT3', 'LT4i']:
	        htbins+= ['HT03','HT3i']
	    
	    for ht_bin in htbins:
	        ht_cut =binsHT[ht_bin][0]
		
		nwbins = []
		#if lt_bin in ['LT1', 'LT2', 'LT3']:
		
		if lt_bin in ['LT4i'] and ht_bin == 'HT03':
		    nwbins = ['NW0i']
	        else:
	            nwbins = ['NW0','NW1i']
		
		for nw_bin in nwbins:
		    nw_cut = binsNW[nw_bin][0]
		
		binname = "%s_%s_%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin,nw_bin,lep_charge)
		cutDictf8[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut),("base",nw_bin,nw_cut),("base",lep_charge,charge_sel)]
		
		# split to SR/CR
		for sr_bin in ['SR']:
		    sr_cut = getSRcut(nj_bin, lt_bin, sr_bin, blinded)[0]
		    
		    binname = "%s_%s_%s_%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin,nw_bin,lep_charge,sr_bin)
		    cutDictSR8[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut),("base",nw_bin,nw_cut),("base",lep_charge,charge_sel),("base",sr_bin,sr_cut)]
		
		for cr_bin in ['CR']:
		    cr_cut = getSRcut(nj_bin, lt_bin, cr_bin, blinded)[0]
		    
		    binname = "%s_%s_%s_%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin,nw_bin,lep_charge,cr_bin)
		    cutDictCR8[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut),("base",nw_bin,nw_cut),("base",lep_charge,charge_sel),("base",cr_bin,cr_cut)]


for nj_bin in ['NJ8i_forTTJets']:
    nj_cut = binsNJ[nj_bin][0]
    
    nb_bin = 'NB0'
    nb_cut = binsNB[nb_bin][0]
    
    for lt_bin in ['LT1','LT2','LT3','LT4i']:
        lt_cut = binsLT[lt_bin][0]
	
	htbins = []
	if lt_bin in ['LT1', 'LT2']:
	    htbins+= ['HT02','HT2i']
	elif lt_bin in ['LT3', 'LT4i']:
	    htbins+= ['HT03','HT3i']
	
	for ht_bin in htbins:
	    ht_cut =binsHT[ht_bin][0]
	    
	    nwbins = []
	    #if lt_bin in ['LT1', 'LT2', 'LT3']:
	    if lt_bin in ['LT4i'] and ht_bin == 'HT03':
	        nwbins = ['NW0i']
	    else:
	        nwbins = ['NW0','NW1i']
		
	    for nw_bin in nwbins:
	        nw_cut = binsNW[nw_bin][0]
		
		binname = "%s_%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin,nw_bin)
		cutDictf8[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut),("base",nw_bin,nw_cut)]
		
		# split to SR/CR
		for sr_bin in ['SR']:
		    sr_cut = getSRcut(nj_bin, lt_bin, sr_bin, blinded)[0]
		    
		    binname = "%s_%s_%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin,nw_bin,sr_bin)
		    cutDictSR8[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut),("base",nw_bin,nw_cut),("base",sr_bin,sr_cut)]
		
		for cr_bin in ['CR']:
		    cr_cut = getSRcut(nj_bin, lt_bin, cr_bin, blinded)[0]
		    
		    binname = "%s_%s_%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin,nw_bin,cr_bin)
		    cutDictCR8[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut),("base",nw_bin,nw_cut),("base",cr_bin,cr_cut)]

