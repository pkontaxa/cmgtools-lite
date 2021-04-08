file_path = 'nBJet_distributions/nBJet_plots_0b_templateFit.txt'

cond_LT = {}
cond_LT['LT1'] = '250 < LT && LT < 350'
cond_LT['LT2'] = '350 < LT && LT < 450'
cond_LT['LT3'] = '450 < LT && LT < 650'
cond_LT['LT3i'] = '450 <= LT'
cond_LT['LT4i'] = '650 <= LT'

cond_HT = {}
cond_HT['HT0'] = '500 < HT && HT < 750'
cond_HT['HT02'] = '500 < HT && HT < 1000'
cond_HT['HT03'] = '500 < HT && HT < 1250'
cond_HT['HT1'] = '750 < HT && HT < 1250'
cond_HT['HT1i'] = '750 < HT'
cond_HT['HT2i'] = '1000 < HT'
cond_HT['HT3i'] = '1250 < HT'

cond_NJ = {}
cond_NJ['NJ34'] = '3 <= nJets30Clean && nJets30Clean <= 4'
cond_NJ['NJ45'] = '4 <= nJets30Clean && nJets30Clean <= 5'
cond_NJ['NJ5'] = 'nJets30Clean == 5'
cond_NJ['NJ67'] = '6 <= nJets30Clean && nJets30Clean <= 7'
cond_NJ['NJ8i'] = '8 <= nJets30Clean'

dPhi_cut = {}
dPhi_cut['LT1'] = 'dPhi < 1.0'
dPhi_cut['LT2'] = 'dPhi < 1.0'
dPhi_cut['LT3'] = 'dPhi < 0.75'
dPhi_cut['LT3i'] = 'dPhi < 0.75'
dPhi_cut['LT4i'] = 'dPhi < 0.5'

cond_NW = {}
cond_NW['NW0'] = 'nWTight == 0'
cond_NW['NW0i'] = 'nWTight >= 0'
cond_NW['NW1i'] = 'nWTight >= 1'


def get_output_string(lt_bin, ht_bin, nj_bin, nw_bin):

    bin_name = (lt_bin + '_' 
              + ht_bin + '_'
              + 'NB0_'
              + nj_bin + '_'
              + nw_bin)
    
    conditions_string = (cond_LT[lt_bin] + ' && '
                       + cond_HT[ht_bin] + ' && '
                       + cond_NJ[nj_bin] + ' && '
                       + dPhi_cut[lt_bin] + ' && '
                       + cond_NW[nw_bin])

    if nj_bin == 'NJ34':
        conditions_string += ' && nMu == 1'
    
    plot_name = 'nBJet_' + bin_name
    binning = '4, 0, 4'
    x_label = '''XTitle="b-jet multiplicity (''' + bin_name.replace('NB0_','') + ''')"''' 

    output_string = (plot_name 
                   + ': if3('
                   + conditions_string
                   + ', nBJet, -99) : '
                   + binning + ' ; '
                   + x_label
                   + ', IncludeOverflows=False')

    return (output_string + '\n')


bins_34 = []
bins_45 = []
bins_5 = []
bins_67 = []
bins_8i = []

counter_nJet34 = 0
counter_nJet45 = 0
counter_nJet5 = 0
counter_nJet67 = 0
counter_nJet8i = 0

with open(file_path, "w") as f:
    for nj_bin in ['NJ34']:
        for lt_bin in ['LT1','LT2','LT3','LT4i']:
            htbins = []
            if lt_bin in ['LT1', 'LT2']:
                htbins+= ['HT0', 'HT1i', 'HT02', 'HT2i']
            elif lt_bin in ['LT3']:
                htbins+= ['HT0', 'HT1', 'HT03', 'HT3i']
            elif lt_bin in ['LT4i']:
                htbins+= ['HT03', 'HT3i']
            for ht_bin in htbins:
                if lt_bin == 'LT2' and ht_bin == 'HT2i':
                    nwbins = ['NW0', 'NW0i']
                elif lt_bin == 'LT3' and ht_bin == 'HT3i':
                    nwbins = ['NW0', 'NW0i']
                elif lt_bin == 'LT4i' and (ht_bin == 'HT03' or ht_bin == 'HT3i'):
                    nwbins = ['NW0', 'NW0i']
                else:
                    nwbins = ['NW0', 'NW1i']
                for nw_bin in nwbins:
                    f.write(get_output_string(lt_bin, ht_bin, nj_bin, nw_bin))
                    bins_34.append(lt_bin+'_'+ht_bin+'_NB0_'+nj_bin+'_forWJets_'+nw_bin+'_neg_CR')
                    counter_nJet34 += 1
    
    f.write('\n')

    for nj_bin in ['NJ45']:
        for lt_bin in ['LT1','LT2','LT3','LT4i']:
            lt_bin_temp = lt_bin
            htbins = []
            if lt_bin in ['LT1', 'LT2']:
                htbins+= ['HT0', 'HT1i', 'HT02', 'HT2i']
            elif lt_bin in ['LT3']:
                htbins+= ['HT0', 'HT1', 'HT03', 'HT3i']
            elif lt_bin in ['LT4i']:
                htbins+= ['HT03', 'HT3i']
            for ht_bin in htbins:
                nwbins = ['NW0', 'NW0i', 'NW1i']
                for nw_bin in nwbins:
                    f.write(get_output_string(lt_bin, ht_bin, nj_bin, nw_bin))
                    bins_45.append(lt_bin+'_'+ht_bin+'_NB0_'+nj_bin+'_forTTJets_'+nw_bin+'_CR')
                    lt_bin = lt_bin_temp
                    counter_nJet45 += 1
    
    f.write('\n')

    for nj_bin in ['NJ5']:
        for nw_bin in ['NW0','NW1i']:
            for lt_bin in ['LT1','LT2','LT3','LT4i']:
                htbins = []
                if lt_bin in ['LT1', 'LT2']:
                    htbins+= ['HT0', 'HT1i']
                elif lt_bin in ['LT3']:
                    htbins+= ['HT0', 'HT1', 'HT3i']
                elif lt_bin in ['LT4i']:
                    htbins+= ['HT03', 'HT3i']
                for ht_bin in htbins:
                    f.write(get_output_string(lt_bin, ht_bin, nj_bin, nw_bin))
                    bins_5.append(lt_bin+'_'+ht_bin+'_NB0_'+nj_bin+'_forTTJets_'+nw_bin+'_CR')
                    counter_nJet5 += 1

    f.write('\n')
    
    for nj_bin in ['NJ67']:
        for nw_bin in ['NW0','NW1i']:
            for lt_bin in ['LT1','LT2','LT3','LT4i']:
                htbins = []
                if lt_bin in ['LT1', 'LT2']:
                    htbins += ['HT02','HT2i']
                elif lt_bin in ['LT3']:
                    htbins += ['HT0', 'HT1','HT3i']
                elif lt_bin in ['LT4i']:
                    htbins += ['HT03', 'HT3i']
                for ht_bin in htbins:
                    f.write(get_output_string(lt_bin, ht_bin, nj_bin, nw_bin))
                    bins_67.append(lt_bin+'_'+ht_bin+'_NB0_'+nj_bin+'_forTTJets_'+nw_bin+'_CR')
                    counter_nJet67 += 1
    
    f.write('\n')

    for nj_bin in ['NJ8i']:
        for lt_bin in ['LT1','LT2','LT3','LT4i']:
            htbins = []
            if lt_bin in ['LT1', 'LT2']:
                htbins+= ['HT02','HT2i']
            elif lt_bin in ['LT3', 'LT4i']:
                htbins+= ['HT03','HT3i']
            for ht_bin in htbins:
                nwbins = []
                if lt_bin in ['LT4i'] and (ht_bin == 'HT03' or ht_bin == 'HT3i'):
                    nwbins = ['NW0i']
                else:
                    nwbins = ['NW0','NW1i']
                for nw_bin in nwbins:
                    f.write(get_output_string(lt_bin, ht_bin, nj_bin, nw_bin))
                    bins_8i.append(lt_bin+'_'+ht_bin+'_NB0_'+nj_bin+'_forTTJets_'+nw_bin+'_CR')
                    counter_nJet8i += 1
    
#for bin in sorted(bins_34):
#    print bin
#for bin in sorted(bins_45):
#    print bin
#for bin in sorted(bins_5):
#    print bin
#for bin in sorted(bins_67):
#    print bin
#for bin in sorted(bins_8i):
#    print bin

#print 'nJet_34: ', counter_nJet34
#print 'nJet_45: ', counter_nJet45
#print 'nJet_5: ', counter_nJet5
#print 'nJet_67: ', counter_nJet67
#print 'nJet_8i: ', counter_nJet8i 
#print 'Total: ', counter_nJet34 + counter_nJet45 + counter_nJet5 + counter_nJet67 + counter_nJet8i
