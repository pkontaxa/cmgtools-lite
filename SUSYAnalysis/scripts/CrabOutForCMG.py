#!/usr/bin/env python
import sys,os, re, pprint
import re
from os import listdir
from os.path import isfile, join
import argparse
import commands
import subprocess
import shutil
from ROOT import TFile
if  os.path.exists('submit_all_to_batch_HTC.sh'):
   os.remove('submit_all_to_batch_HTC.sh')
cmssw_release = os.environ['CMSSW_BASE']
user = os.environ['USER']

def find_all_matching(substring, path):
	result = []
	for root, dirs, files in os.walk(path):
		for thisfile in files:
			if substring in thisfile:
				result.append(os.path.join(root, thisfile ))
	return result

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Runs a NAF batch system for nanoAOD', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('--indir', help='List of datasets to process', metavar='indir')
	parser.add_argument('--outdir', help='output directory',default=None, metavar='outdir')
	#parser.add_argument('--pattern', help='output directory',default=None, metavar='outdir')
	parser.add_argument('--batchMode', '-b', help="Batch mode.", action='store_true')

	args = parser.parse_args()
	batch = args.batchMode
	indire = args.indir
	outdire = args.outdir

	JDir = os.path.join(outdire,"jobs")
	if  not os.path.exists(JDir):
		os.makedirs(str(JDir))
	logdir = os.path.join(outdire,"logs")
	if  not os.path.exists(logdir):
		os.makedirs(str(logdir))

	if  os.path.exists(outdire):
		des = raw_input(" this dir is already exist : "+str(outdire)+" do you want to remove it [y/n]: ")
		if ( "y" in des or "Y" in des or "Yes" in des) :
			shutil.rmtree(str(outdire))
			os.makedirs(str(outdire))
		elif ( "N" in des or  "n" in des or  "No" in des ): print str(outdire) , "will be ovewritten by the job output -- take care"
		else :
			raise ValueError( "do not understand your potion")
	else : os.makedirs(str(outdire))
	pattern = os.listdir(indire)
	for i,pat in enumerate(pattern) :
		#if not ('SingleElectron_Run2018D' in pat or 'SingleMuon_Run2018D' in pat): continue
		#if not ('MET_Run2017C' in pat or 'SingleMuon_Run2017E' in pat):
		#   continue
		#if not 'MET_Run2017F_31Mar2018' in pat : continue
		print pat
		patout = outdire+'/'+pat
		os.makedirs(str(patout))
		tarfiles = find_all_matching('heppyOutput_',indire+'/'+pat)
		cmd_list = ['source /cvmfs/cms.cern.ch/cmsset_default.sh','cd '+os.path.abspath(patout) , 'cd '+cmssw_release+'/src','eval `scramv1 ru -sh`','cd -','echo running','export X509_USER_PROXY=/nfs/dust/cms/user/'+user+'/k5-ca-proxy.pem']
		#cmd_list.append('export GFAL_CONFIG_DIR=/cvmfs/grid.cern.ch/emi-ui-3.17.1-1.el6umd4v5/etc/gfal2.d')
		#cmd_list.append('export GFAL_PLUGIN_DIR=/cvmfs/grid.cern.ch/emi-ui-3.17.1-1.el6umd4v5/usr/lib64/gfal2-plugins/')
		for tar in tarfiles:
			chunkname = patout+'/'+pat+'_Chunk'+tar.split('heppyOutput_')[-1].replace('.tgz','')
			os.makedirs(str(chunkname))
			if not batch :
				cmd = 'tar -zxvf '+tar+' -C '+chunkname+' ; mv '+ chunkname+'/Output/* '+chunkname+'; rm -rf '+ chunkname+'/Output/ ; rm -rf '+chunkname+'/heppyOutput_*'
				os.system(cmd)
			else :
				#os.system('cp '+tar+' '+chunkname)
				newChunk = chunkname.split("/")[-1]
				#cmd = 'tar -zxvf '+newChunk+'/heppyOutput_* -C '+newChunk+' ; mv '+ newChunk+'/Output/* '+newChunk+'; rm -rf '+ newChunk+'/Output/ ; rm -rf '+newChunk+'/heppyOutput_*'
				cmd = cmd = 'tar -zxvf '+tar+' -C '+newChunk+' ; mv '+ newChunk+'/Output/* '+newChunk+'; rm -rf '+ newChunk+'/Output/ ; rm -rf '+newChunk+'/heppyOutput_*'
				cmd_list.append(cmd)
		if batch :
			#cmd_list.append('heppy_hadd.py .')
			#cmd_list.append('rm -rf '+pat+'*_Chunk*')
			#cmd_list.append('gfal-copy '+pat+' srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/amohamed/heppy_final_trees/'+pat)
			#cmd_list.append('rm -rf '+pat)
			cmd_list.append('echo `DONE DONE DONE`')
			confDir = os.path.join(JDir,"job_"+str(i))
			if os.path.exists(confDir):
				shutil.rmtree(str(confDir))
			else : os.makedirs(confDir)
			exec_ = open(confDir+"/exec.sh","w+")
			exec_.write("echo 'running job' >> "+os.path.abspath(confDir)+"/processing"+"\n")
			exec_.writelines("%s\n" % item for item in cmd_list )
			exec_.write("\n")
			exec_.write("rm -rf "+os.path.abspath(confDir))		
			exec_.close()
			os.system('chmod +x '+confDir+"/exec.sh")
		else :
			pwd = os.getcwd()
			os.chdir(patout)
			os.system('heppy_hadd.py .')
			os.chdir(pwd)
	if batch:
		subFilename = os.path.join(JDir,"submitAllhadds.conf")
		subFile = open(subFilename,"w+")
		subFile.write("executable = $(DIR)/exec.sh"+"\n")
		subFile.write("universe =  vanilla")
		subFile.write("\n")
		subFile.write("should_transfer_files = YES")
		subFile.write("\n")
		subFile.write("log = "+"{}/job_$(Cluster)_$(Process).log".format(os.path.abspath(logdir)))
		subFile.write("\n")
		subFile.write("output = "+"{}/job_$(Cluster)_$(Process).out".format(os.path.abspath(logdir)))
		subFile.write("\n")
		subFile.write("error = "+"{}/job_$(Cluster)_$(Process).err".format(os.path.abspath(logdir)))
		subFile.write("\n")
		subFile.write("when_to_transfer_output   = ON_EXIT")
		subFile.write("\n")
		subFile.write('Requirements  = (OpSysAndVer == "SL6")')
		subFile.write("\n")
		subFile.write("queue DIR matching dirs "+JDir+"/job_*/")
		subFile.close()
		#os.system("condor_submit "+subFilename)


