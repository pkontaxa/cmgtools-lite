#!/usr/bin/env python
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
import sys
import os
path = sys.argv[-1]
TreeName="sf/t"
filelist=['evVarFriend_DYJetsToLL_M50_HT1200to2500.root','evVarFriend_DYJetsToLL_M50_HT2500toInf.root','evVarFriend_DYJetsToLL_M50_HT400to600.root',
          'evVarFriend_DYJetsToLL_M50_HT600to800.root','evVarFriend_DYJetsToLL_M50_HT800to1200.root',
          'evVarFriend_QCD_HT1000to1500.root','evVarFriend_QCD_HT1500to2000.root','evVarFriend_QCD_HT2000toInf.root',
          'evVarFriend_QCD_HT500to700.root','evVarFriend_QCD_HT700to1000.root','evVarFriend_TBar_tWch_ext1.root',
          'evVarFriend_TBar_tch_powheg.root','evVarFriend_TTJets_DiLepton.root','evVarFriend_TTJets_LO_HT1200to2500_ext.root',
          'evVarFriend_TTJets_LO_HT2500toInf_ext.root','evVarFriend_TTJets_LO_HT600to800.root',
          'evVarFriend_TTJets_LO_HT800to1200_ext.root','evVarFriend_TTJets_SingleLeptonFromT.root',
          'evVarFriend_TTJets_SingleLeptonFromTbar.root','evVarFriend_TTWToLNu.root','evVarFriend_TTWToQQ.root',
          'evVarFriend_TTZToLLNuNu.root','evVarFriend_TTZToQQ.root','evVarFriend_TToLeptons_sch.root',
          'evVarFriend_T_tWch_ext1.root','evVarFriend_T_tch_powheg.root','evVarFriend_WJetsToLNu_HT1200to2500.root',
          'evVarFriend_WJetsToLNu_HT2500toInf.root','evVarFriend_WJetsToLNu_HT400to600.root','evVarFriend_WJetsToLNu_HT600to800.root',
          'evVarFriend_WJetsToLNu_HT800to1200_ext.root','evVarFriend_WWTo2L2Nu.root','evVarFriend_WWToLNuQQ.root',
          'evVarFriend_WZTo1L1Nu2Q.root','evVarFriend_WZTo1L3Nu.root','evVarFriend_WZTo2L2Q.root','evVarFriend_ZZTo2L2Nu.root',
          'evVarFriend_ZZTo2L2Q.root']
for f in filelist : 
	FTrain = ROOT.TFile('Friends_for_MVA/traning/'+f, 'RECREATE' )
	FEval = ROOT.TFile( 'Friends_for_MVA/evaluation/'+f, 'RECREATE' )
	file0 = ROOT.TFile.Open(path+"/"+f)
	t = file0.Get(TreeName)
	t.SetBranchStatus("*", 1)
	sfdirT = FTrain.mkdir('sf')
	sfdirT.cd()
	outTreeT = t.CloneTree(0)
	sfdirE = FEval.mkdir('sf')
	sfdirE.cd()
	outTreeE = t.CloneTree(0)
	print 'going to crop 30% = ', t.GetEntries() * 30 / 100,' out of : ' , t.GetEntries() , ' from this file : ', f 
	for i in range(t.GetEntries()):
		t.GetEntry(i)
		if i <= t.GetEntries() * 30 /100 : 
			outTreeT.Fill()
		elif i > t.GetEntries() * 30 /100 : 
			outTreeE.Fill()
	print ' now writting the output for' , f
	outTreeT.AutoSave()
	outTreeE.AutoSave()
	FTrain.Write()
	FEval.Write()
	FTrain.Close()
	FEval.Close()

