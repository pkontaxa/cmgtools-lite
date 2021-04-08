import os

if not os.path.exists('batch_logs'):
        os.makedirs('batch_logs')
        if not os.path.exists('batch_logs/log'):
            os.makedirs('batch_logs/log')
        if not os.path.exists('batch_logs/err'):
            os.makedirs('batch_logs/err')
        if not os.path.exists('batch_logs/out'):
            os.makedirs('batch_logs/out')

systs = ['nominal', 'dilep-corr']
#systs = ['nominal', 'dilep-corr', 'DLConst', 'DLSlope', 'JEC', 'PU', 'TTVsec', 'TTVxsec', 'Wpol', 'Wxsec', 'btagHF', 'btagLF', 'lepSF', 'nISR']
selections = ['inclusive', 'positive', 'negative', 'antiselected']
year = '2016_EXT'

mca_file = ''
lumi = ''

for syst in systs:

    if year == '2016_EXT':
        mca_file = 'mca-Summer16_'+syst+'.txt'
        lumi = '35.9'
    elif year == '2017':
        mca_file = 'mca-Fall17_'+syst+'.txt'
        lumi = '41.5'
    elif year == '2018':
        mca_file = 'mca-Autumn18_'+syst+'.txt'
        lumi = '59.7'

    job_tag = year+'_'+syst

    file_name = 'nBJet_job_' + job_tag + '.submit'
    with open(file_name, 'w') as f:
        f.write('executable = make_nBJet_plots\n')
        f.write('arguments = -s '+syst+' -c $(selection) -y '+year+' -m '+mca_file+' -l '+lumi+' \n')
        f.write('should_transfer_files = YES\n')
        f.write('log = batch_logs/log/nBJet_job_' + job_tag + '_$(selection)_$(ClusterId).log\n')
        f.write('output = batch_logs/out/nBJet_job_' + job_tag + '_$(selection)_$(ClusterId).out\n')
        f.write('error = batch_logs/err/nBJet_job_' + job_tag + '_$(selection)_$(ClusterId).Err\n')
        f.write('getenv = True\n')
        f.write('request_cpus = 4\n')
        f.write('request_memory = 1GB\n')
        f.write('request_disk = 300MB\n')
        f.write('+RequestRuntime = 60*60*11\n')
        f.write('queue selection in (inclusive negative positive antiselected)\n')
        
    os.system('condor_submit '+file_name)
    os.system('rm '+file_name)
