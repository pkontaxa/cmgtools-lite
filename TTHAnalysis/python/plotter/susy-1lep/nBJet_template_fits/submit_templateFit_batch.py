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
year = '2016_EXT'

fratio_file = ''

for syst in systs:
    job_tag = year+'_'+syst
    out_dir = year+'_'+syst

    if year == '2016_EXT':
        fratio_file = 'Lp_LTbins_0b_2016_f-ratios_MC.txt'
    elif year == '2017':
        fratio_file = 'Lp_LTbins_0b_2017_f-ratios_MC.txt'
    elif year == '2018':
        fratio_file = 'Lp_LTbins_0b_2018_f-ratios_MC.txt'

    file_name = 'tempFit_job_' + job_tag + '.submit'
    with open(file_name, 'w') as f:
        f.write('executable = make_template_fits\n')
        f.write('arguments = -s '+syst+' -y '+year+' -f '+fratio_file+' -o '+out_dir+' \n')
        f.write('should_transfer_files = YES\n')
        f.write('log = batch_logs/log/tempFit_job_' + job_tag + '_$(ClusterId).log\n')
        f.write('output = batch_logs/out/tempFit_job_' + job_tag + '_$(ClusterId).out\n')
        f.write('error = batch_logs/err/tempFit_job_' + job_tag + '_$(ClusterId).Err\n')
        f.write('getenv = True\n')
        f.write('request_cpus = 4\n')
        f.write('request_memory = 1GB\n')
        f.write('request_disk = 300MB\n')
        f.write('+RequestRuntime = 60*60*11\n')
        f.write('queue 1\n')
        
    os.system('condor_submit '+file_name)
    os.system('rm '+file_name)
