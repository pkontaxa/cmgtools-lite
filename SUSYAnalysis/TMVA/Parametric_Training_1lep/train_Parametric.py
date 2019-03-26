#!/usr/bin/env python

# 
# This example is basically the same as $ROOTSYS/tmva/test/TMVAClassification.C
# 

import ROOT

# in order to start TMVA
ROOT.TMVA.Tools.Instance()

# note that it seems to be mandatory to have an
# output file, just passing None to TMVA::Factory(..)
# does not work. Make sure you don't overwrite an
# existing file.

# open input file, get trees, create output file
file1 = ROOT.TFile("/nfs/dust/cms/group/susy-desy/Run2/MC/CMGtuples/Pantelis/SIGNAL_FRIENDS_PRIVATE_MC_MULTIPLE_MASS_POINTS_V2/OUTPUT2/FRIEND_TOTAL_SIGNAL.root")
tree_s = file1.Get("sf/t")

file2 = ROOT.TFile("/nfs/dust/cms/group/susy-desy/Run2/MC/CMGtuples/Pantelis/NEW_NTUPLES_REPOSITORY/Friends_for_TMVA_BKG_Flat_mGo_mLSP_2/OUTPUT2/OUTPUT3/TOTAL_BKG_8M_w_Weights.root")
tree_b = file2.Get("sf/t")

fout = ROOT.TFile("Check_HT500_LT250_nj5_dphi075_nb2_Parametrized_Top_Properties_mass_difference_8M_Test26March.root","RECREATE")

# define factory with options
factory = ROOT.TMVA.Factory("TMVAClassification", fout,
                            ":".join([    "!V",
                                          "!Silent",
                                          "Color",
                                          "DrawProgressBar",
                                          "Transformations=I;D;P;G,D",
                                          "AnalysisType=Classification"]
                                     ))
#ROOT.TRandom my_random_generator

dataloader=ROOT.TMVA.DataLoader("dataset")


# add discriminating variables for training
dataloader.AddVariable("dM_Go_LSP","F")
#dataloader.AddVariable("mLSP","F")

dataloader.AddVariable("LT","F")
dataloader.AddVariable("HT","F")
#dataloader.AddVariable("nBJet","I")
dataloader.AddVariable("nBCleaned_TOTAL","I")
dataloader.AddVariable("nTop_Total_Combined","I")

#dataloader.AddVariable("nDeepTop_loose","I")
#dataloader.AddVariable("nResolvedTop","I")
dataloader.AddVariable("nJets30Clean","F")
dataloader.AddVariable("dPhi","F")


dataloader.AddVariable("Alt$(DeepAK8Top_Loose_pt_Array[0],400)","F")
dataloader.AddVariable("Alt$(DeepAK8Top_Loose_pt_Array[1],400)","F")

#dataloader.AddVariable("Alt$(BTag_pt_Array[0],0)","F")
#dataloader.AddVariable("Alt$(BTag_pt_Array[1],0)","F")

dataloader.AddVariable("Alt$(BTag_pt_Cleaned[0],0)","F")
dataloader.AddVariable("Alt$(BTag_pt_Cleaned[1],0)","F")


dataloader.AddVariable("Alt$(DeepAK8Top_Loose_eta_Array[0],-2.4)","F")
dataloader.AddVariable("Alt$(DeepAK8Top_Loose_eta_Array[1],-2.4)","F")

dataloader.AddVariable("Alt$(BTag_eta_Cleaned[0],-2.4)","F")
dataloader.AddVariable("Alt$(BTag_eta_Cleaned[1],-2.4)","F")

#dataloader.AddVariable("Alt$(BTag_eta_Array[0],-2.4)","F")
#dataloader.AddVariable("Alt$(BTag_eta_Array[1],-2.4)","F")

dataloader.AddVariable("Alt$(DeepAK8Top_Loose_phi_Array[0],-3.2)","F")
dataloader.AddVariable("Alt$(DeepAK8Top_Loose_phi_Array[1],-3.2)","F")

#dataloader.AddVariable("Alt$(BTag_phi_Array[0],-3.2)","F")
#dataloader.AddVariable("Alt$(BTag_phi_Array[1],-3.2)","F")

dataloader.AddVariable("Alt$(BTag_phi_Cleaned[0],-3.2)","F")
dataloader.AddVariable("Alt$(BTag_phi_Cleaned[1],-3.2)","F")

dataloader.AddVariable("Resolved_Top_pt_Cleaned[0]","F")
dataloader.AddVariable("Resolved_Top_eta_Cleaned[0]","F")
dataloader.AddVariable("Resolved_Top_phi_Cleaned[0]","F")

dataloader.AddVariable("Resolved_Top_pt_Cleaned[1]","F")
dataloader.AddVariable("Resolved_Top_eta_Cleaned[1]","F")
dataloader.AddVariable("Resolved_Top_phi_Cleaned[1]","F")


#factory.AddVariable("MT","F")


# define signal and background trees
dataloader.AddSignalTree(tree_s)
dataloader.AddBackgroundTree(tree_b)

# define additional cuts 
sigCut = ROOT.TCut("LT>=250. && HT>=500. && nJets30Clean>=5. && nBJet>=2. && dPhi>=0.75")
bgCut = ROOT.TCut("LT>=250. && HT>=500. && nJets30Clean>=5. && nBJet>=2. && dPhi>=0.75")

#sigCut = ROOT.TCut("LT>=250. && HT>=500. && nJets30Clean>=5. && nBJet>=0.")
#bgCut = ROOT.TCut("LT>=250. && HT>=500. && nJets30Clean>=5. && nBJet>=0.")

dataloader.SetSignalWeightExpression("35.9*(susyXsec*19578919./susyNgen*lepSF*btagSF)*(1000./19578919.)")
dataloader.SetBackgroundWeightExpression("weight_for_scale_35p9")

# set options for trainings
dataloader.PrepareTrainingAndTestTree(sigCut,
                                   bgCut,
                                   ":".join(["nTrain_Signal=0",
                                             "nTrain_Background=0",
                                             "SplitMode=Random",
                                             "NormMode=NumEvents",
                                             "!V"
                                             ]))

# book and define methods that should be trained
method = factory.BookMethod(dataloader,ROOT.TMVA.Types.kBDT, "BDT",
                            ":".join([ "!H",
                                       "!V",
                                       "NTrees=850",
                                       "nEventsMin=150",
                                       "MaxDepth=3",
                                       "BoostType=AdaBoost",
                                       "AdaBoostBeta=0.5",
                                       "SeparationType=GiniIndex",
                                       "nCuts=20",
                                       "PruneMethod=NoPruning",
                                       ]))


#method = factory.BookMethod(ROOT.TMVA.Types.kLD, "LD")


'''
method = factory.BookMethod(ROOT.TMVA.Types.kBDT, "BDT2",
                            ":".join([ "!H",
                                       "!V",
                                       "NTrees=5",
                                       # "nEventsMin=0",
                                       "MaxDepth=3",
                                       "BoostType=AdaBoost",
                                       "AdaBoostBeta=0.5",
                                       "SeparationType=GiniIndex",
                                       "nCuts=20",
                                       "PruneMethod=NoPruning",
                                       ]))

method = factory.BookMethod(ROOT.TMVA.Types.kBDT, "BDT3",
                            ":".join([ "!H",
                                       "!V",
                                       "NTrees=2500",
                                       # "nEventsMin=2",
                                       "MaxDepth=3",
                                       "BoostType=AdaBoost",
                                       "AdaBoostBeta=0.5",
                                       "SeparationType=GiniIndex",
                                       "nCuts=20",
                                       "PruneMethod=NoPruning",
                                       ]))

'''
# self-explaining
factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()
                                                                                                                                                                                                                                                                                                                                                                         
