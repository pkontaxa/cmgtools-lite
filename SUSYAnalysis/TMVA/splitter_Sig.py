#!/usr/bin/env python
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
import sys
import os
path = sys.argv[-1]
TreeName="sf/t"
filelist=['evVarFriend_SMS_T1tttt_TuneCUETP8M1_1.root','evVarFriend_SMS_T1tttt_TuneCUETP8M1_2.root','evVarFriend_SMS_T1tttt_TuneCUETP8M1_3.root',
          'evVarFriend_SMS_T1tttt_TuneCUETP8M1_4.root','evVarFriend_SMS_T1tttt_TuneCUETP8M1_5.root','evVarFriend_SMS_T1tttt_TuneCUETP8M1_6.root']

for f in filelist : 
	file0 = ROOT.TFile.Open(path+"/"+f)
	#FEval = ROOT.TFile( 'Friends_for_MVA/evaluation/'+f, 'RECREATE' )
	#FTrain = ROOT.TFile('Friends_for_MVA/training/'+f, 'RECREATE' )
	#FEval = ROOT.TFile( 'Friends_for_MVA/evaluation_uncomp/'+f, 'RECREATE' )
	#FTrain = ROOT.TFile('Friends_for_MVA/training_uncomp/'+f, 'RECREATE' )
	FEval = ROOT.TFile( 'Friends_for_MVA/evaluation_both/'+f, 'RECREATE' )
	FTrain = ROOT.TFile('Friends_for_MVA/training_both/'+f, 'RECREATE' )
	t = file0.Get(TreeName)
	t.SetBranchStatus("*", 1)
	sfdirT = FTrain.mkdir('sf')
	sfdirT.cd()
	outTreeT = t.CloneTree(0)
	sfdirE = FEval.mkdir('sf')
	sfdirE.cd()
	outTreeE = t.CloneTree(0)
	print 'going to crop 1000 point from this file : ', f 
	XCount = 0
	for i in range(t.GetEntries()):
		t.GetEntry(i)
		# for comp signal scan points
		#if (((t.mGo == 1750 and t.mLSP == 950) or (t.mGo == 1750 and t.mLSP == 1000) or (t.mGo == 1750 and t.mLSP == 1100) or (t.mGo == 1750 and t.mLSP == 1150) or (t.mGo == 1700 and t.mLSP == 1050) or (t.mGo == 1700 and t.mLSP == 1100) or (t.mGo == 1850 and t.mLSP == 1000) or (t.mGo == 1850 and t.mLSP == 1050) or (t.mGo == 1800 and t.mLSP == 1050) or (t.mGo == 1650 and t.mLSP == 1050) or (t.mGo == 1900 and t.mLSP == 1000)) and t.nLep == 1 and t.Lep_pt > 25 and t.Selected == 1 and t.nVeto == 0 and t.nJets30Clean >= 3 and t.Jet2_pt > 80 and t.HT > 500 and t.LT > 250 ):
		# for uncomp signal scan points
		#if ((t.mGo == 1950 and t.mLSP == 100) or (t.mGo == 1950 and t.mLSP == 200) or (t.mGo == 1900 and t.mLSP == 100) or (t.mGo == 1900 and t.mLSP == 200) or (t.mGo == 1850 and t.mLSP == 100)or (t.mGo == 1850 and t.mLSP == 200)) and t.nLep == 1 and t.Lep_pt > 25 and t.Selected == 1 and t.nVeto == 0 and t.nJets30Clean >= 3 and t.Jet2_pt > 80 and t.HT > 500 and t.LT > 250 :
		if (t.nLep == 1 and t.Lep_pt > 25 and t.Selected == 1 and t.nVeto == 0 and t.nJets30Clean >= 3 and t.Jet2_pt > 80 and t.HT > 500 and t.LT > 250 and (t.mGo in range(600, 2000, 25) and t.mLSP in range(0,1200))):
			XCount+=1
			if XCount <= 700 : 
				outTreeT.Fill()
			else :
				outTreeE.Fill()
		else :
			outTreeE.Fill()
	print ' now writting the output for File ' , f
	outTreeE.AutoSave()
	FEval.Write()
	FEval.Close()
	outTreeT.AutoSave()
	FTrain.Write()
	FTrain.Close()
