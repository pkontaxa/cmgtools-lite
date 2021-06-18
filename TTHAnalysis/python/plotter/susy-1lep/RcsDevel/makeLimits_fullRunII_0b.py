#!/usr/bin/env python
import os, glob, sys

SMS = "T5qqqqWW"

from ROOT import *
def combineCards(f, s ):
    try:
        os.stat('combinedCards')
    except:
        os.mkdir('combinedCards')

    cmd = 'combineCards.py ' + f + '/LT*txt > ' + f.replace(s,'combinedCards') +'/' + s + '.txt'
    print cmd
    os.system(cmd)

###########################
def combineCards_all_Years(f, s, dirname):
    try:
        os.stat('combinedCardsAllYears')
    except:
        os.mkdir('combinedCardsAllYears')

    cmd = 'combineCards.py ../' + dirname + '/combinedCards/'+ s + '.txt ' + '../' + dirname.replace("2016", "2017") + '/combinedCards/'+ s + '.txt ' + '../' + dirname.replace("2016", "2018") + '/combinedCards/'+ s + '.txt' + ' > ' + f.replace(s,'combinedCardsAllYears') +'/' + s + '.txt'
    print cmd
    os.system(cmd)


def convert_to_ShapeCards(f, s):
    try:
        os.stat('combinedCardsAllYears_Shape')
    except:
        os.mkdir('combinedCardsAllYears_Shape')

    cmd = "combineCards.py -S combinedCardsAllYears/" + s +'.txt' + ' > ' +f.replace(s,'combinedCardsAllYears_Shape')+'/' + s +'_Shape.txt'
    print cmd
    os.system(cmd)
##############################

    return 1
def runCards(f, s):
    cmd = 'combine -M Asymptotic ../' + f + ' -n ' + s
    print cmd
    os.system(cmd)
    return 1

def createJobs(f, s, jobs):
    cmd = 'combine -M AsymptoticLimits ../' + f + ' -n ' + s + '\n'
    #cmd = 'combine ../' + f + ' -n ' + s + '\n'
    print cmd
    jobs.write(cmd)
    return 1


def submitJobs(jobList, nchunks):
    print 'Reading joblist'
    jobListName = jobList
    subCmd = 'condor_qsub -t 1-%s -o logs ../../nafbatch_runner_limits.sh %s' %(nchunks,jobListName)
    print 'Going to submit', nchunks, 'jobs with', subCmd
    os.system(subCmd)

    return 1

def submitJobsHTC(jobList, nchunks):
	print 'Reading joblist'
	listtxt = open(jobList,"r")
	logdir = 'logs'
	if not os.path.exists(logdir): os.system("mkdir -p "+logdir)
	if  os.path.exists('submit_Bins.sh'):
		os.remove('submit_Bins.sh')

	for line in listtxt:
		print "line is ",line
		line = line.strip()
		if line.startswith('#') :
			print "commented line continue!"
			continue
		if len(line.strip()) == 0 :
			print "empty line continue!"
			continue
		exten = line.split("-n ")[-1]
		condsub = "./submit"+exten+".condor"
		wrapsub = "./wrapnanoPost_"+exten+".sh"
		os.system("cp ../../templates/submit.condor "+condsub)
		os.system("cp ../../templates/wrapnanoPost.sh "+wrapsub)
		temp = open(condsub).read()
		temp = temp.replace('@EXESH',str(os.getcwd())+"/"+wrapsub).replace('@LOGS',str(logdir)).replace('@time','60*60*1')
		temp_toRun =  open(condsub, 'w')
		temp_toRun.write(temp)
		tempW = open(wrapsub).read()
		# for instance point to old CMSSW_BASE for excuting the combin command but i will update it to the currtent CMSSW_BASE
		#tempW = tempW.replace('@WORKDIR',os.environ['CMSSW_BASE']+"/src").replace('@EXEDIR',str(os.getcwd())).replace('@CMDBINS',line)
		tempW = tempW.replace('@WORKDIR',os.environ['CMSSW_BASE']+"/src").replace('@EXEDIR',str(os.getcwd())).replace('@CMDBINS',line)
		tempW_roRun = open(wrapsub, 'w')
		tempW_roRun.write(tempW)
		subCmd = 'condor_submit '+condsub
		print 'Going to submit', line.split("-n ")[-1], 'jobs with', subCmd
		file = open('submit_Bins.sh','a')
		file.write("\n")
		file.write(subCmd)
	file.close()
	os.system('chmod a+x submit_Bins.sh')

	return 1

if __name__ == "__main__":

    ## remove '-b' option
    if '-b' in sys.argv:
        sys.argv.remove('-b')
        _batchMode = True

    if len(sys.argv) > 1:
        pattern = sys.argv[1]
        print '# pattern is', pattern
    else:
        print "No pattern given!"
        exit(0)

    ## Create Yield Storage

    #pattern = "datacardsABCD_2p1bins_fullscan2"
    os.chdir(pattern)
    dirList = glob.glob(SMS+'*')
    samples = [x[x.find('/')+1:] for x in dirList]

    if "--combine-cards" in sys.argv:
        for (f,s) in zip(dirList,samples):
            #for year in ["2016"]:
            for year in ["2016", "2017", "2018"]:
                print f, s, year, "\n"
                tmpPattern = pattern.replace("2016", year)
                os.chdir("../" + tmpPattern)
                combineCards(f,s)
                os.chdir("../" + pattern)
            combineCards_all_Years(f,s, pattern.split("/")[0])
            convert_to_ShapeCards(f,s)
    else:
        #fileList = glob.glob('combinedCards/*')
        #fileList = glob.glob('combinedCardsAllYears/*')
        fileList = glob.glob('combinedCardsAllYears_Shape/*')
        #print fileList
        try:
            os.stat('limitOutput')
        except:
            os.mkdir('limitOutput')

        chunks = 0
        os.chdir('limitOutput')
        jobList = 'joblist_limits.txt'
        jobs = open(jobList, 'w')
        print fileList
        for f in fileList:
            #TODO find only .card.txt is probably better to only grab the standard datacards
            s = f[f.find('/')+1:f.find('.txt')]
            createJobs(f,s,jobs)
            chunks = chunks+1
            #runCards(f,s)
        #submitJobs(jobList, chunks)
        jobs.close()
