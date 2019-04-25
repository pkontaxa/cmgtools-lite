/// \file
/// \ingroup tutorial_tmva
/// \notebook -nodraw
/// This example shows the training of signal with three different backgrounds
/// Then in the application a tree is created with all signal and background
/// events where the true class ID and the three classifier outputs are added
/// finally with the application tree, the significance is maximized with the
/// help of the TMVA genetic algrorithm.
/// - Project   : TMVA - a Root-integrated toolkit for multivariate data analysis
/// - Package   : TMVA
/// - Exectuable: TMVAGAexample
///
/// \macro_output
/// \macro_code
/// \author Andreas Hoecker


#include <iostream> // Stream declarations
#include <vector>
#include <limits>

#include "TChain.h"
#include "TCut.h"
#include "TDirectory.h"
#include "TH1F.h"
#include "TH1.h"
#include "TMath.h"
#include "TFile.h"
#include "TStopwatch.h"
#include "TROOT.h"
#include "TSystem.h"

#include "TMVA/GeneticAlgorithm.h"
#include "TMVA/GeneticFitter.h"
#include "TMVA/IFitterTarget.h"
#include "TMVA/Factory.h"
#include "TMVA/DataLoader.h"//required to load dataset
#include "TMVA/Reader.h"

using namespace std;

using namespace TMVA;

// ----------------------------------------------------------------------------------------------
// Training
// ----------------------------------------------------------------------------------------------
//
int TMVA_1lep_CMG_v6_1(TString myMethodList = "" ){
	
	
	
	   // The explicit loading of the shared libTMVA is done in TMVAlogon.C, defined in .rootrc
   // if you use your private .rootrc, or run from a different directory, please copy the
   // corresponding lines from .rootrc

   // Methods to be processed can be given as an argument; use format:
   //
   //     mylinux~> root -l TMVAClassification.C\(\"myMethod1,myMethod2,myMethod3\"\)

   //---------------------------------------------------------------
   // This loads the library
   TMVA::Tools::Instance();
   //ROOT::R::TRInterface &r = ROOT::R::TRInterface::Instance();

   // Default MVA methods to be trained + tested
   std::map<std::string,int> Use;
   //
   // Boosted Decision Trees
   Use["BDT"]             = 1; // uses Adaptive Boost
   Use["BDTG"]            = 0; // uses Gradient Boost
   Use["BDTB"]            = 0; // uses Bagging
   Use["BDTD"]            = 0; // decorrelation + Adaptive Boost
   Use["BDTF"]            = 0; // allow usage of fisher discriminant for node splitting
   //
   // Friedman's RuleFit method, ie, an optimised series of cuts ("rules")
   Use["RuleFit"]         = 1;
   // ---------------------------------------------------------------

   std::cout << std::endl;
   std::cout << "==> Start TMVAClassification" << std::endl;

   // Select methods (don't look at this code - not of interest)
   if (myMethodList != "") {
      for (std::map<std::string,int>::iterator it = Use.begin(); it != Use.end(); it++) it->second = 0;

      std::vector<TString> mlist = TMVA::gTools().SplitString( myMethodList, ',' );
      for (UInt_t i=0; i<mlist.size(); i++) {
         std::string regMethod(mlist[i]);

         if (Use.find(regMethod) == Use.end()) {
            std::cout << "Method \"" << regMethod << "\" not known in TMVA under this name. Choose among the following:" << std::endl;
            for (std::map<std::string,int>::iterator it = Use.begin(); it != Use.end(); it++) std::cout << it->first << " ";
            std::cout << std::endl;
            return 1;
         }
         Use[regMethod] = 1;
      }
   }

	std::string factoryOptions( "!V:!Silent:Transformations=I;D;P;G,D:AnalysisType=Classification" );
	//string inputFolder = "/nfs/dust/cms/user/amohamed/susy-desy/CMGSamples/Friends_for_Limits/";
   string inputFolder = "./FR_forMVA_nosplit_resTop/";

   Double_t signalWeight      = 1.0;
   Double_t backgroundWeight = 1.0;
   Double_t lumi=35.9 ;
   // Create a new root output file.
   TString outfileName("TMVA_OUT_SMS_T1tttt_combined_topkin_dphiMTout.root");
   TFile* outputFile = TFile::Open( outfileName, "RECREATE" );
   // ____________
   TMVA::Factory *factory = new TMVA::Factory( "TMVAClassification", outputFile, factoryOptions );
   TMVA::DataLoader *dataloader = new TMVA::DataLoader("TMVA_OUT_SMS_T1tttt_combined_topkin_dphiMTout");

   TString T1tttt_MiniAOD_19_10 = inputFolder + "evVarFriend_T1tttt_MiniAOD_19_10.root";
   TFile *input_T1tttt_MiniAOD_19_10;
   input_T1tttt_MiniAOD_19_10 = TFile::Open(T1tttt_MiniAOD_19_10);
   TTree *tree_T1tttt_MiniAOD_19_10 = (TTree *)input_T1tttt_MiniAOD_19_10->Get("sf/t");
   dataloader->AddSignalTree(tree_T1tttt_MiniAOD_19_10, 1);
   TString QCD_HT2000toInf_ext = inputFolder + "evVarFriend_QCD_HT2000toInf_ext.root";
   TFile *input_QCD_HT2000toInf_ext;
   input_QCD_HT2000toInf_ext = TFile::Open(QCD_HT2000toInf_ext);
   TTree *tree_QCD_HT2000toInf_ext = (TTree *)input_QCD_HT2000toInf_ext->Get("sf/t");
   dataloader->AddBackgroundTree(tree_QCD_HT2000toInf_ext, 1);
   TString QCD_HT1500to2000_ext = inputFolder + "evVarFriend_QCD_HT1500to2000_ext.root";
   TFile *input_QCD_HT1500to2000_ext;
   input_QCD_HT1500to2000_ext = TFile::Open(QCD_HT1500to2000_ext);
   TTree *tree_QCD_HT1500to2000_ext = (TTree *)input_QCD_HT1500to2000_ext->Get("sf/t");
   dataloader->AddBackgroundTree(tree_QCD_HT1500to2000_ext, 1);
   TString WJetsToLNu_HT400to600_ext = inputFolder + "evVarFriend_WJetsToLNu_HT400to600_ext.root";
   TFile *input_WJetsToLNu_HT400to600_ext;
   input_WJetsToLNu_HT400to600_ext = TFile::Open(WJetsToLNu_HT400to600_ext);
   TTree *tree_WJetsToLNu_HT400to600_ext = (TTree *)input_WJetsToLNu_HT400to600_ext->Get("sf/t");
   dataloader->AddBackgroundTree(tree_WJetsToLNu_HT400to600_ext, 1);
   TString QCD_HT300to500_ext = inputFolder + "evVarFriend_QCD_HT300to500_ext.root";
   TFile *input_QCD_HT300to500_ext;
   input_QCD_HT300to500_ext = TFile::Open(QCD_HT300to500_ext);
   TTree *tree_QCD_HT300to500_ext = (TTree *)input_QCD_HT300to500_ext->Get("sf/t");
   dataloader->AddBackgroundTree(tree_QCD_HT300to500_ext, 1);
   TString TTJets_SingleLeptonFromTbar_genMET = inputFolder + "evVarFriend_TTJets_SingleLeptonFromTbar_genMET.root";
   TFile *input_TTJets_SingleLeptonFromTbar_genMET;
   input_TTJets_SingleLeptonFromTbar_genMET = TFile::Open(TTJets_SingleLeptonFromTbar_genMET);
   TTree *tree_TTJets_SingleLeptonFromTbar_genMET = (TTree *)input_TTJets_SingleLeptonFromTbar_genMET->Get("sf/t");
   dataloader->AddBackgroundTree(tree_TTJets_SingleLeptonFromTbar_genMET, 1);
   TString WJetsToLNu_HT1200to2500_ext = inputFolder + "evVarFriend_WJetsToLNu_HT1200to2500_ext.root";
   TFile *input_WJetsToLNu_HT1200to2500_ext;
   input_WJetsToLNu_HT1200to2500_ext = TFile::Open(WJetsToLNu_HT1200to2500_ext);
   TTree *tree_WJetsToLNu_HT1200to2500_ext = (TTree *)input_WJetsToLNu_HT1200to2500_ext->Get("sf/t");
   dataloader->AddBackgroundTree(tree_WJetsToLNu_HT1200to2500_ext, 1);
   TString TTJets_SingleLeptonFromT_ext = inputFolder + "evVarFriend_TTJets_SingleLeptonFromT_ext.root";
   TFile *input_TTJets_SingleLeptonFromT_ext;
   input_TTJets_SingleLeptonFromT_ext = TFile::Open(TTJets_SingleLeptonFromT_ext);
   TTree *tree_TTJets_SingleLeptonFromT_ext = (TTree *)input_TTJets_SingleLeptonFromT_ext->Get("sf/t");
   dataloader->AddBackgroundTree(tree_TTJets_SingleLeptonFromT_ext, 1);
   TString TTJets_DiLepton_ext = inputFolder + "evVarFriend_TTJets_DiLepton_ext.root";
   TFile *input_TTJets_DiLepton_ext;
   input_TTJets_DiLepton_ext = TFile::Open(TTJets_DiLepton_ext);
   TTree *tree_TTJets_DiLepton_ext = (TTree *)input_TTJets_DiLepton_ext->Get("sf/t");
   dataloader->AddBackgroundTree(tree_TTJets_DiLepton_ext, 1);
   TString TTJets_SingleLeptonFromT_genMET = inputFolder + "evVarFriend_TTJets_SingleLeptonFromT_genMET.root";
   TFile *input_TTJets_SingleLeptonFromT_genMET;
   input_TTJets_SingleLeptonFromT_genMET = TFile::Open(TTJets_SingleLeptonFromT_genMET);
   TTree *tree_TTJets_SingleLeptonFromT_genMET = (TTree *)input_TTJets_SingleLeptonFromT_genMET->Get("sf/t");
   dataloader->AddBackgroundTree(tree_TTJets_SingleLeptonFromT_genMET, 1);
   TString WJetsToLNu_HT600to800_ext = inputFolder + "evVarFriend_WJetsToLNu_HT600to800_ext.root";
   TFile *input_WJetsToLNu_HT600to800_ext;
   input_WJetsToLNu_HT600to800_ext = TFile::Open(WJetsToLNu_HT600to800_ext);
   TTree *tree_WJetsToLNu_HT600to800_ext = (TTree *)input_WJetsToLNu_HT600to800_ext->Get("sf/t");
   dataloader->AddBackgroundTree(tree_WJetsToLNu_HT600to800_ext, 1);
   TString QCD_HT200to300_ext = inputFolder + "evVarFriend_QCD_HT200to300_ext.root";
   TFile *input_QCD_HT200to300_ext;
   input_QCD_HT200to300_ext = TFile::Open(QCD_HT200to300_ext);
   TTree *tree_QCD_HT200to300_ext = (TTree *)input_QCD_HT200to300_ext->Get("sf/t");
   dataloader->AddBackgroundTree(tree_QCD_HT200to300_ext, 1);
   TString DYJetsToLL_M50_HT200to400_ext = inputFolder + "evVarFriend_DYJetsToLL_M50_HT200to400_ext.root";
   TFile *input_DYJetsToLL_M50_HT200to400_ext;
   input_DYJetsToLL_M50_HT200to400_ext = TFile::Open(DYJetsToLL_M50_HT200to400_ext);
   TTree *tree_DYJetsToLL_M50_HT200to400_ext = (TTree *)input_DYJetsToLL_M50_HT200to400_ext->Get("sf/t");
   dataloader->AddBackgroundTree(tree_DYJetsToLL_M50_HT200to400_ext, 1);
   TString QCD_HT500to700_ext = inputFolder + "evVarFriend_QCD_HT500to700_ext.root";
   TFile *input_QCD_HT500to700_ext;
   input_QCD_HT500to700_ext = TFile::Open(QCD_HT500to700_ext);
   TTree *tree_QCD_HT500to700_ext = (TTree *)input_QCD_HT500to700_ext->Get("sf/t");
   dataloader->AddBackgroundTree(tree_QCD_HT500to700_ext, 1);
   TString WJetsToLNu_HT200to400_ext = inputFolder + "evVarFriend_WJetsToLNu_HT200to400_ext.root";
   TFile *input_WJetsToLNu_HT200to400_ext;
   input_WJetsToLNu_HT200to400_ext = TFile::Open(WJetsToLNu_HT200to400_ext);
   TTree *tree_WJetsToLNu_HT200to400_ext = (TTree *)input_WJetsToLNu_HT200to400_ext->Get("sf/t");
   dataloader->AddBackgroundTree(tree_WJetsToLNu_HT200to400_ext, 1);
   TString T1tttt_MiniAOD_22_01 = inputFolder + "evVarFriend_T1tttt_MiniAOD_22_01.root";
   TFile *input_T1tttt_MiniAOD_22_01;
   input_T1tttt_MiniAOD_22_01 = TFile::Open(T1tttt_MiniAOD_22_01);
   TTree *tree_T1tttt_MiniAOD_22_01 = (TTree *)input_T1tttt_MiniAOD_22_01->Get("sf/t");
   dataloader->AddSignalTree(tree_T1tttt_MiniAOD_22_01, 1);
   TString WJetsToLNu_HT2500toInf_ext = inputFolder + "evVarFriend_WJetsToLNu_HT2500toInf_ext.root";
   TFile *input_WJetsToLNu_HT2500toInf_ext;
   input_WJetsToLNu_HT2500toInf_ext = TFile::Open(WJetsToLNu_HT2500toInf_ext);
   TTree *tree_WJetsToLNu_HT2500toInf_ext = (TTree *)input_WJetsToLNu_HT2500toInf_ext->Get("sf/t");
   dataloader->AddBackgroundTree(tree_WJetsToLNu_HT2500toInf_ext, 1);
   TString TTJets_SingleLeptonFromTbar_ext = inputFolder + "evVarFriend_TTJets_SingleLeptonFromTbar_ext.root";
   TFile *input_TTJets_SingleLeptonFromTbar_ext;
   input_TTJets_SingleLeptonFromTbar_ext = TFile::Open(TTJets_SingleLeptonFromTbar_ext);
   TTree *tree_TTJets_SingleLeptonFromTbar_ext = (TTree *)input_TTJets_SingleLeptonFromTbar_ext->Get("sf/t");
   dataloader->AddBackgroundTree(tree_TTJets_SingleLeptonFromTbar_ext, 1);
   TString T1tttt_MiniAOD_22_08 = inputFolder + "evVarFriend_T1tttt_MiniAOD_22_08.root";
   TFile *input_T1tttt_MiniAOD_22_08;
   input_T1tttt_MiniAOD_22_08 = TFile::Open(T1tttt_MiniAOD_22_08);
   TTree *tree_T1tttt_MiniAOD_22_08 = (TTree *)input_T1tttt_MiniAOD_22_08->Get("sf/t");
   dataloader->AddSignalTree(tree_T1tttt_MiniAOD_22_08, 1);
   TString T1tttt_MiniAOD_19_08 = inputFolder + "evVarFriend_T1tttt_MiniAOD_19_08.root";
   TFile *input_T1tttt_MiniAOD_19_08;
   input_T1tttt_MiniAOD_19_08 = TFile::Open(T1tttt_MiniAOD_19_08);
   TTree *tree_T1tttt_MiniAOD_19_08 = (TTree *)input_T1tttt_MiniAOD_19_08->Get("sf/t");
   dataloader->AddSignalTree(tree_T1tttt_MiniAOD_19_08, 1);
   TString TTJets_DiLepton_genMET = inputFolder + "evVarFriend_TTJets_DiLepton_genMET.root";
   TFile *input_TTJets_DiLepton_genMET;
   input_TTJets_DiLepton_genMET = TFile::Open(TTJets_DiLepton_genMET);
   TTree *tree_TTJets_DiLepton_genMET = (TTree *)input_TTJets_DiLepton_genMET->Get("sf/t");
   dataloader->AddBackgroundTree(tree_TTJets_DiLepton_genMET, 1);
   TString T1tttt_MiniAOD_19_01_v2 = inputFolder + "evVarFriend_T1tttt_MiniAOD_19_01_v2.root";
   TFile *input_T1tttt_MiniAOD_19_01_v2;
   input_T1tttt_MiniAOD_19_01_v2 = TFile::Open(T1tttt_MiniAOD_19_01_v2);
   TTree *tree_T1tttt_MiniAOD_19_01_v2 = (TTree *)input_T1tttt_MiniAOD_19_01_v2->Get("sf/t");
   dataloader->AddSignalTree(tree_T1tttt_MiniAOD_19_01_v2, 1);
   TString DYJetsToLL_M50_HT400to600_ext = inputFolder + "evVarFriend_DYJetsToLL_M50_HT400to600_ext.root";
   TFile *input_DYJetsToLL_M50_HT400to600_ext;
   input_DYJetsToLL_M50_HT400to600_ext = TFile::Open(DYJetsToLL_M50_HT400to600_ext);
   TTree *tree_DYJetsToLL_M50_HT400to600_ext = (TTree *)input_DYJetsToLL_M50_HT400to600_ext->Get("sf/t");
   dataloader->AddBackgroundTree(tree_DYJetsToLL_M50_HT400to600_ext, 1);
   TString WJetsToLNu_HT200to400_ext2 = inputFolder + "evVarFriend_WJetsToLNu_HT200to400_ext2.root";
   TFile *input_WJetsToLNu_HT200to400_ext2;
   input_WJetsToLNu_HT200to400_ext2 = TFile::Open(WJetsToLNu_HT200to400_ext2);
   TTree *tree_WJetsToLNu_HT200to400_ext2 = (TTree *)input_WJetsToLNu_HT200to400_ext2->Get("sf/t");
   dataloader->AddBackgroundTree(tree_WJetsToLNu_HT200to400_ext2, 1);
   TString QCD_HT1000to1500_ext = inputFolder + "evVarFriend_QCD_HT1000to1500_ext.root";
   TFile *input_QCD_HT1000to1500_ext;
   input_QCD_HT1000to1500_ext = TFile::Open(QCD_HT1000to1500_ext);
   TTree *tree_QCD_HT1000to1500_ext = (TTree *)input_QCD_HT1000to1500_ext->Get("sf/t");
   dataloader->AddBackgroundTree(tree_QCD_HT1000to1500_ext, 1);
   TString T1tttt_MiniAOD_15_10 = inputFolder + "evVarFriend_T1tttt_MiniAOD_15_10.root";
   TFile *input_T1tttt_MiniAOD_15_10;
   input_T1tttt_MiniAOD_15_10 = TFile::Open(T1tttt_MiniAOD_15_10);
   TTree *tree_T1tttt_MiniAOD_15_10 = (TTree *)input_T1tttt_MiniAOD_15_10->Get("sf/t");
   dataloader->AddSignalTree(tree_T1tttt_MiniAOD_15_10, 1);
   TString WJetsToLNu_HT800to1200_ext = inputFolder + "evVarFriend_WJetsToLNu_HT800to1200_ext.root";
   TFile *input_WJetsToLNu_HT800to1200_ext;
   input_WJetsToLNu_HT800to1200_ext = TFile::Open(WJetsToLNu_HT800to1200_ext);
   TTree *tree_WJetsToLNu_HT800to1200_ext = (TTree *)input_WJetsToLNu_HT800to1200_ext->Get("sf/t");
   dataloader->AddBackgroundTree(tree_WJetsToLNu_HT800to1200_ext, 1);

   
   //dataloader->AddVariable("FatJet1_pt"      ,"FatJet1_pt"      ,"",'F');
   //dataloader->AddVariable("FatJet2_pt"      ,"FatJet2_pt"      ,"",'F');
   //dataloader->AddVariable("FatJet1_eta"     ,"FatJet1_eta"     ,"",'F');
   //dataloader->AddVariable("FatJet2_eta"     ,"FatJet2_eta"     ,"",'F');
   //dataloader->AddVariable("FatJet1_phi"     ,"FatJet1_phi"     ,"",'F');
   //dataloader->AddVariable("FatJet2_phi"     ,"FatJet2_phi"     ,"",'F');
   //dataloader->AddVariable("FatJet1_mass"    ,"FatJet1_mass"    ,"",'F');
   //dataloader->AddVariable("FatJet2_mass"    ,"FatJet2_mass"    ,"",'F');
   //dataloader->AddVariable("nDeepTop_medium" ,"nDeepTop_medium" ,"",'F');
   //dataloader->AddVariable("nDeepTop_tight"  ,"nDeepTop_tight"  ,"",'F');
   //dataloader->AddVariable("nDeepTop_loose"  ,"nDeepTop_loose"  ,"",'F');
   //dataloader->AddVariable("MT"              ,"MT"              ,"",'F');

   dataloader->AddVariable("Lep_pt"                                  ,"Lep_pt"                                  ,""  ,'F');
   dataloader->AddVariable("Jet1_pt"                                 ,"Jet1_pt"                                 ,""  ,'F');
   dataloader->AddVariable("Jet2_pt"                                 ,"Jet2_pt"                                 ,""  ,'F');
   dataloader->AddVariable("MET"                                     ,"MET"                                     ,""  ,'F');
      
   dataloader->AddVariable("LT"                                      ,"LT"                                      ,""  ,'F');
   dataloader->AddVariable("HT"                                      ,"HT"                                      ,""  ,'F');
   dataloader->AddVariable("nJets30Clean"                            ,"nJets30Clean"                            ,""  ,'F');
   dataloader->AddVariable("nBCleaned_TOTAL"                         ,"nBCleaned_TOTAL"                        , ""  ,'I');
	
   dataloader->AddVariable("nTop_Total_Combined"                     ,"nTop_Total_Combined"                     ,""  ,'I');
   dataloader->AddVariable("nResolvedTop"                            ,"nResolvedTop"                            ,""  ,'F');
     
   dataloader->AddSpectator("dPhi"                                   , "dPhi"                                   , "", 'F');

   //0.00359842 1750
   //0.00212345 1850
   //0.01419030 1500
   //0.00163547 1900

   dataloader->SetBackgroundWeightExpression("Xsec*lepSF*btagSF*nISRttweight*puRatio");
   dataloader->SetSignalWeightExpression( "susyXsec*lepSF*btagSF*nISRweight" );
   //     factory->SetBackgroundWeightExpression("weight");
   TCut mycuts = "nLep == 1 && Lep_pt > 25 && Selected == 1 &&  nVeto == 0 && nJets30Clean >= 5 && Jet2_pt > 80 &&  HT > 500 && LT > 250"; //&& FatJet1_mass > 40 && FatJet1_mass > 40 "; // for example: TCut mycuts = "abs(var1)<0.5 && abs(var2-0.5)<1";
   TCut mycutb = "nLep == 1 && Lep_pt > 25 && Selected == 1 &&  nVeto == 0 && nJets30Clean >= 5 && Jet2_pt > 80 &&  HT > 500 && LT > 250";//&& FatJet1_mass > 40 && FatJet1_mass > 40 "; // for example: TCut mycutb = "abs(var1)<0.5";

   // tell the factory to use all remaining events in the trees after training for testing:
   // dataloader->PrepareTrainingAndTestTree( mycuts, mycutb,
   //                                     "nTrain_Signal=0:nTrain_Background=0:SplitMode=Random:NormMode=NumEvents:!V" );
   dataloader->PrepareTrainingAndTestTree( mycuts, mycutb,
                                        "nTrain_Signal=0:nTrain_Background=0:SplitMode=Random:NormMode=NumEvents:!V" );
   

   // Boosted Decision Trees
   if (Use["BDTG"]) // Gradient Boost
      factory->BookMethod( dataloader, TMVA::Types::kBDT, "BDTG",
                           "!H:!V:NTrees=1000:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.10:UseBaggedBoost:BaggedSampleFraction=0.5:nCuts=20:MaxDepth=2" );

   if (Use["BDT"])  // Adaptive Boost
      factory->BookMethod( dataloader, TMVA::Types::kBDT, "BDT",
                           "!H:!V:NTrees=850:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" );

   if (Use["BDTB"]) // Bagging
      factory->BookMethod( dataloader, TMVA::Types::kBDT, "BDTB",
                           "!H:!V:NTrees=400:BoostType=Bagging:SeparationType=GiniIndex:nCuts=20" );

   if (Use["BDTD"]) // Decorrelation + Adaptive Boost
      factory->BookMethod( dataloader, TMVA::Types::kBDT, "BDTD",
                           "!H:!V:NTrees=400:MinNodeSize=5%:MaxDepth=3:BoostType=AdaBoost:SeparationType=GiniIndex:nCuts=20:VarTransform=Decorrelate" );

   if (Use["BDTF"])  // Allow Using Fisher discriminant in node splitting for (strong) linearly correlated variables
      factory->BookMethod( dataloader, TMVA::Types::kBDT, "BDTF",
                           "!H:!V:NTrees=50:MinNodeSize=2.5%:UseFisherCuts:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:SeparationType=GiniIndex:nCuts=20" );
   if (Use["RXGB"])
      factory->BookMethod( dataloader, TMVA::Types::kRXGB, "RXGB",
                           "!V:NRounds=80:MaxDepth=2:Eta=1");
   
   
   
   
      // For an example of the category classifier usage, see: TMVAClassificationCategory
   //
   // --------------------------------------------------------------------------------------------------
   //  Now you can optimize the setting (configuration) of the MVAs using the set of training events
   // STILL EXPERIMENTAL and only implemented for BDT's !
   //
   //     factory->OptimizeAllMethods("SigEffAt001","Scan");
   //     factory->OptimizeAllMethods("ROCIntegral","FitGA");
   //
   // --------------------------------------------------------------------------------------------------

   // Now you can tell the factory to train, test, and evaluate the MVAs
   //
   // Train MVAs using the set of training events
   factory->TrainAllMethods();

   // Evaluate all MVAs using the set of test events
   factory->TestAllMethods();

   // Evaluate and compare performance of all configured MVAs
   factory->EvaluateAllMethods();

   // --------------------------------------------------------------


   outputFile->Close();

   std::cout << "==> Wrote root file: " << outputFile->GetName() << std::endl;
   std::cout << "==> TMVAClassification is done!" << std::endl;

   delete factory;
   delete dataloader;
   // Launch the GUI for the root macros
   if (!gROOT->IsBatch()) TMVA::TMVAGui( outfileName );

   return 0;
}


int main( int argc, char** argv )
{
   // Select methods (don't look at this code - not of interest)
   TString methodList;
   for (int i=1; i<argc; i++) {
      TString regMethod(argv[i]);
      if(regMethod=="-b" || regMethod=="--batch") continue;
      if (!methodList.IsNull()) methodList += TString(",");
      methodList += regMethod;
   }
   return TMVA_1lep_CMG_v6_1(methodList);
}


