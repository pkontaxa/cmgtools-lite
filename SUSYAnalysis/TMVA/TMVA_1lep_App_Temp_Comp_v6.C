/// \file
/// \ingroup tutorial_tmva
/// \notebook -nodraw
/// This macro provides a simple example on how to use the trained classifiers
/// within an analysis module
/// - Project   : TMVA - a Root-integrated toolkit for multivariate data analysis
/// - Package   : TMVA
/// - Exectuable: TMVAClassificationApplication
///
/// \macro_output
/// \macro_code
/// \author Andreas Hoecker

#include <cstdlib>
#include <vector>
#include <iostream>
#include <map>
#include <string>

#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "TSystem.h"
#include "TROOT.h"
#include "TStopwatch.h"

#include "TMVA/Tools.h"
#include "TMVA/Reader.h"
#include "TMVA/MethodCuts.h"

using namespace TMVA;

void @SCRIPTNAME( TString myMethodList = ""  )
{

   //---------------------------------------------------------------
   // This loads the library
   TMVA::Tools::Instance();
   TString inFile = "@INFILE";
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
   std::cout << std::endl;
   std::cout << "==> Start TMVAClassificationApplication" << std::endl;

   // Select methods (don't look at this code - not of interest)
   if (myMethodList != "") {
      for (std::map<std::string,int>::iterator it = Use.begin(); it != Use.end(); it++) it->second = 0;

      std::vector<TString> mlist = gTools().SplitString( myMethodList, ',' );
      for (UInt_t i=0; i<mlist.size(); i++) {
         std::string regMethod(mlist[i]);

         if (Use.find(regMethod) == Use.end()) {
            std::cout << "Method \"" << regMethod
                      << "\" not known in TMVA under this name. Choose among the following:" << std::endl;
            for (std::map<std::string,int>::iterator it = Use.begin(); it != Use.end(); it++) {
               std::cout << it->first << " ";
            }
            std::cout << std::endl;
            return;
         }
         Use[regMethod] = 1;
      }
   }

   // --------------------------------------------------------------------------------------------------

   // Create the Reader object
   
   TMVA::Reader *reader = new TMVA::Reader( "!Color:!Silent" );

   // Declaration of leaf types
   Float_t         Run;
   Float_t         Lumi;
   Float_t         Xsec;
   Long64_t        Event;
   Float_t         genWeight;
   Float_t         isData;
   Float_t         nLep;
   Float_t         nVeto;
   Float_t         nEl;
   Float_t         nMu;
   Float_t         nTightEl;
   Float_t         nTightMu;
   Int_t           nTightLeps;
   Int_t           tightLepsIdx[4];   //[nTightLeps]
   Float_t         Lep_pdgId;
   Float_t         Lep_pt;
   Float_t         Lep_eta;
   Float_t         Lep_phi;
   Float_t         Lep_Idx;
   Float_t         Lep_relIso;
   Float_t         Lep_miniIso;
   Float_t         Lep_hOverE;
   Float_t         Selected;
   Float_t         Lep2_pt;
   Float_t         Selected2;
   Float_t         MET;
   Float_t         LT;
   Float_t         ST;
   Float_t         MT;
   Float_t         DeltaPhiLepW;
   Float_t         dPhi;
   Float_t         Lp;
   Float_t         GendPhi;
   Float_t         GenLT;
   Float_t         GenMET;
   Float_t         HT;
   Float_t         nJets;
   Int_t           nBJet;
   Float_t         nBJetDeep;
   Int_t           nJets30;
   Int_t           Jets30Idx[15];   //[nJets30]
   Float_t         nBJets30;
   Float_t         nJets30Clean;
   Float_t         nJets40;
   Float_t         nBJets40;
   Float_t         htJet30j;
   Float_t         htJet30ja;
   Float_t         htJet40j;
   Float_t         Jet1_pt;
   Float_t         Jet2_pt;
   Float_t         nFatJets;
   Float_t         FatJet1_pt;
   Float_t         FatJet2_pt;
   Float_t         FatJet1_eta;
   Float_t         FatJet2_eta;
   Float_t         FatJet1_phi;
   Float_t         FatJet2_phi;
   Float_t         FatJet1_mass;
   Float_t         FatJet2_mass;
   Int_t           nDeepTop_loose;
   Int_t           nDeepTop_medium;
   Int_t           nDeepTop_tight;
   Int_t           nBJet_Excl_LooseTop_08;
   Int_t           nBJet_Excl_MediumTop_08;
   Int_t           nBJet_Excl_TightTop_08;
   Int_t           nBJetDeep_Excl_LooseTop_08;
   Int_t           nBJetDeep_Excl_MediumTop_08;
   Int_t           nBJetDeep_Excl_TightTop_08;
   Float_t         DeepAK8Top_Loose_pt_Array[3];   //[nDeepTop_loose]
   Float_t         DeepAK8Top_Loose_eta_Array[3];   //[nDeepTop_loose]
   Float_t         DeepAK8Top_Loose_phi_Array[3];   //[nDeepTop_loose]
   Int_t           Flag_Btag_leq_08_from_Loose_DeepAK8[6];   //[nBJet]
   Float_t         BTag_phi_Array[6];   //[nBJet]
   Float_t         BTag_eta_Array[6];   //[nBJet]
   Float_t         BTag_pt_Array[6];   //[nBJet]
   Float_t         nHighPtTopTag;
   Float_t         nHighPtTopTagPlusTau23;
   Float_t         LSLjetptGT80;
   Float_t         isSR;
   Float_t         Mll;
   Float_t         METfilters;
   Float_t         PD_JetHT;
   Float_t         PD_SingleEle;
   Float_t         PD_SingleMu;
   Float_t         PD_MET;
   Float_t         isDPhiSignal;
   Float_t         RA2_muJetFilter;
   Float_t         Flag_fastSimCorridorJetCleaning;
   Float_t         nGenJets;
   Float_t         nGenbJets;
   Float_t         nGenJets30;
   Float_t         nGenbJets30;
   Float_t         prefireW;
   Float_t         prefireWup;
   Float_t         prefireWdwn;
   Float_t         HLT_HT350;
   Float_t         HLT_HT600;
   Float_t         HLT_HT800;
   Float_t         HLT_HT900;
   Float_t         HLT_PFJet450;
   Float_t         HLT_MET170;
   Float_t         HLT_HT350MET120;
   Float_t         HLT_HT350MET100;
   Float_t         HLT_HTMET;
   Float_t         HLT_IsoMu27;
   Float_t         HLT_IsoMu20;
   Float_t         HLT_IsoMu24;
   Float_t         HLT_Mu50;
   Float_t         HLT_MuHT400MET70;
   Float_t         HLT_MuHT350MET70;
   Float_t         HLT_MuHT350MET50;
   Float_t         HLT_MuHTMET;
   Float_t         HLT_MuHT350;
   Float_t         HLT_IsoEle32;
   Float_t         HLT_IsoEle22;
   Float_t         HLT_IsoEle23;
   Float_t         HLT_IsoEle27T;
   Float_t         HLT_Ele105;
   Float_t         HLT_Ele115;
   Float_t         HLT_Ele50PFJet165;
   Float_t         HLT_EleHT400MET70;
   Float_t         HLT_EleHT350MET70;
   Float_t         HLT_EleHT350MET50;
   Float_t         HLT_EleHTMET;
   Float_t         HLT_EleHT350;
   Float_t         HLT_EleHT400;
   Float_t         HLT_MuHT400;
   Float_t         HLT_Ele50HT400;
   Float_t         HLT_Mu50HT400;
   Float_t         HLT_highMHTMET;
   Float_t         HLT_MET100MHT100;
   Float_t         HLT_MET110MHT110;
   Float_t         HLT_MET120MHT120;
   Float_t         HLT_MET190_TypeOne_HBHE_BH;
   Float_t         HLT_EleOR;
   Float_t         HLT_MuOR;
   Float_t         HLT_LepOR;
   Float_t         HLT_MetOR;
   Float_t         TrigEff;
   Float_t         nVtx;
   Float_t         nTrueInt;
   Float_t         puRatio;
   Float_t         puRatio_up;
   Float_t         puRatio_down;
   Float_t         mGo;
   Float_t         mLSP;
   Float_t         susyXsec;
   Float_t         susyNgen;
   Float_t         totalNgen;
   Float_t         susyWgen;
   Float_t         nISR;
   Float_t         nISRweight;
   Float_t         nISRweightsyst_up;
   Float_t         nISRweightsyst_down;
   Float_t         ScaleWgt[10];
   Float_t         lepSF;
   Float_t         lepSFerr;
   Float_t         lepSFunc;
   Float_t         btagW_1p;
   Float_t         btagW_2p;
   Float_t         btagW_3p;
   Float_t         btagW_0;
   Float_t         btagW_1;
   Float_t         btagW_2;
   Float_t         btagW_1p_SF;
   Float_t         btagW_2p_SF;
   Float_t         btagW_3p_SF;
   Float_t         btagW_0_SF;
   Float_t         btagW_1_SF;
   Float_t         btagW_2_SF;
   Float_t         btagW_1p_SF_b_Up;
   Float_t         btagW_2p_SF_b_Up;
   Float_t         btagW_3p_SF_b_Up;
   Float_t         btagW_0_SF_b_Up;
   Float_t         btagW_1_SF_b_Up;
   Float_t         btagW_2_SF_b_Up;
   Float_t         btagW_1p_SF_b_Down;
   Float_t         btagW_2p_SF_b_Down;
   Float_t         btagW_3p_SF_b_Down;
   Float_t         btagW_0_SF_b_Down;
   Float_t         btagW_1_SF_b_Down;
   Float_t         btagW_2_SF_b_Down;
   Float_t         btagW_1p_SF_light_Up;
   Float_t         btagW_2p_SF_light_Up;
   Float_t         btagW_3p_SF_light_Up;
   Float_t         btagW_0_SF_light_Up;
   Float_t         btagW_1_SF_light_Up;
   Float_t         btagW_2_SF_light_Up;
   Float_t         btagW_1p_SF_light_Down;
   Float_t         btagW_2p_SF_light_Down;
   Float_t         btagW_3p_SF_light_Down;
   Float_t         btagW_0_SF_light_Down;
   Float_t         btagW_1_SF_light_Down;
   Float_t         btagW_2_SF_light_Down;
   Float_t         btagSF_l_down;
   Float_t         btagSF_l_up;
   Float_t         btagSF_b_down;
   Float_t         btagSF_b_up;
   Float_t         btagSF;
   Float_t         GenTopPt;
   Float_t         GenAntiTopPt;
   Float_t         TopPtWeight;
   Float_t         TopPtWeightII;
   Float_t         GenTTBarPt;
   Float_t         GenTTBarWeight;
   Float_t         ISRTTBarWeight;
   Float_t         GenGGPt;
   Float_t         ISRSigUp;
   Float_t         ISRSigDown;
   Float_t         DilepNJetCorr;
   Float_t         DilepNJetWeightConstUp;
   Float_t         DilepNJetWeightSlopeUp;
   Float_t         DilepNJetWeightConstDn;
   Float_t         DilepNJetWeightSlopeDn;
   Float_t         WpolWup;
   Float_t         WpolWdown;
   Float_t         nISRtt;
   Float_t         nISRttweight;
   Float_t         nISRttweightsyst_up;
   Float_t         nISRttweightsyst_down;
   Float_t         DL_LepGoodOne_pt;
   Float_t         DL_LepGoodOne_pdgId;
   Float_t         DL_l1l2ovMET;
   Float_t         DL_Vecl1l2ovMET;
   Float_t         DL_DPhil1l2;
   Int_t           nLostLepTreatments;
   Float_t         DL_ST[3];   //[nLostLepTreatments]
   Float_t         DL_HT[3];   //[nLostLepTreatments]
   Float_t         DL_dPhiLepW[3];   //[nLostLepTreatments]
   Float_t         DL_nJets30Clean[3];   //[nLostLepTreatments]
   Int_t           nMaxStat;
   Float_t         DLMS_ST[2];   //[nMaxStat]
   Float_t         DLMS_HT[2];   //[nMaxStat]
   Float_t         DLMS_dPhiLepW[2];   //[nMaxStat]
   Float_t         DLMS_nJets30Clean[2];   //[nMaxStat]
   Float_t         iso_had;
   Float_t         iso_pt;
   Float_t         iso_MT2;
   Float_t         iso_Veto;
   Float_t         mvaValue;
   Float_t         HadTop_pt;
   Float_t         HadTop_eta;
   Float_t         HadTop_phi;
   Float_t         HadTop_mass;
   Float_t         j1_eta;
   Float_t         j1_phi;
   Float_t         j2_eta;
   Float_t         j2_phi;
   Float_t         j3_eta;
   Float_t         j3_phi;
   Float_t         W_fromHadTop_dRb;
   Float_t         b_fromHadTop_CSV;
   Float_t         j1;
   Float_t         j2;
   Float_t         j3;
   Float_t         mvaValue_2;
   Float_t         HadTop_pt_2;
   Float_t         HadTop_eta_2;
   Float_t         HadTop_phi_2;
   Float_t         HadTop_mass_2;
   Float_t         j1_eta_2;
   Float_t         j1_phi_2;
   Float_t         j2_eta_2;
   Float_t         j2_phi_2;
   Float_t         j3_eta_2;
   Float_t         j3_phi_2;
   Float_t         W_fromHadTop_dRb_2;
   Float_t         b_fromHadTop_CSV_2;
   Float_t         j1_2;
   Float_t         j2_2;
   Float_t         j3_2;
   Float_t         mvaValue_3;
   Float_t         HadTop_pt_3;
   Float_t         HadTop_eta_3;
   Float_t         HadTop_phi_3;
   Float_t         HadTop_mass_3;
   Float_t         j1_eta_3;
   Float_t         j1_phi_3;
   Float_t         j2_eta_3;
   Float_t         j2_phi_3;
   Float_t         j3_eta_3;
   Float_t         j3_phi_3;
   Float_t         W_fromHadTop_dRb_3;
   Float_t         b_fromHadTop_CSV_3;
   Float_t         j1_3;
   Float_t         j2_3;
   Float_t         j3_3;
   Float_t         mvaValue_4;
   Float_t         HadTop_pt_4;
   Float_t         HadTop_eta_4;
   Float_t         HadTop_phi_4;
   Float_t         HadTop_mass_4;
   Float_t         j1_eta_4;
   Float_t         j1_phi_4;
   Float_t         j2_eta_4;
   Float_t         j2_phi_4;
   Float_t         j3_eta_4;
   Float_t         j3_phi_4;
   Float_t         W_fromHadTop_dRb_4;
   Float_t         b_fromHadTop_CSV_4;
   Float_t         j1_4;
   Float_t         j2_4;
   Float_t         j3_4;
   Float_t         nResolvedTop;
   Float_t         nTop_Total_Combined;
   Float_t         Resolved_Had_Top_mvaValue[4];
   Float_t         Resolved_Had_Top_pt[4];
   Float_t         Resolved_Had_Top_eta[4];
   Float_t         Resolved_Had_Top_phi[4];
   Float_t         Resolved_Had_Top_mass[4];
   Float_t         nBCleaned_TOTAL;
   Float_t         Resolved_Top_pt_Cleaned[4];
   Float_t         Resolved_Top_eta_Cleaned[4];
   Float_t         Resolved_Top_phi_Cleaned[4];
   Float_t         BTag_pt_Cleaned[6];   //[nBCleaned_TOTAL]
   Float_t         BTag_eta_Cleaned[6];   //[nBCleaned_TOTAL]
   Float_t         BTag_phi_Cleaned[6];   //[nBCleaned_TOTAL]

   // Create a set of variables and declare them to the reader
   // - the variable names MUST corresponds in name and type to those given in the weight file(s) used

	//reader->AddVariable( "MT"			,&MT			 );

   reader->AddVariable("Lep_pt"                                  ,&Lep_pt              );
   reader->AddVariable("Jet1_pt"                                 ,&Jet1_pt             );
   reader->AddVariable("Jet2_pt"                                 ,&Jet2_pt             );
   reader->AddVariable("MET"                                     ,&MET                 );
      
   reader->AddVariable("LT"                                      ,&LT                  );
   reader->AddVariable("HT"                                      ,&HT                  );
   reader->AddVariable("nJets30Clean"                            ,&nJets30Clean        );
   reader->AddVariable("nBCleaned_TOTAL"                         ,&nBCleaned_TOTAL     );
	
   reader->AddVariable("nTop_Total_Combined"                     ,&nTop_Total_Combined );
   reader->AddVariable("nResolvedTop"                            ,&nResolvedTop        );
     
   reader->AddSpectator("dPhi"                                   ,&dPhi                );

   // Book the MVA methods
   TString dir    = "dataset/weights/";
   TString prefix = "TMVAClassification";

   // Book method(s)
   for (std::map<std::string,int>::iterator it = Use.begin(); it != Use.end(); it++) {
      if (it->second) {
         TString methodName = TString(it->first) + TString(" method");
         TString weightfile = "/nfs/dust/cms/user/amohamed/susy-desy/deepAK8/resTop/CMSSW_9_4_11/src/CMGTools/SUSYAnalysis/TMVA/@MASSPOINT/weights/TMVAClassification_BDT.weights.xml";
         reader->BookMVA( methodName, weightfile );
      }
   }

   // Book output histograms
   UInt_t nbin = 100;
   TH1F *histBdt(0);
   TH1F *histBdtG(0);
   TH1F *histBdtB(0);
   TH1F *histBdtD(0);
   TH1F *histBdtF(0);

   if (Use["BDT"])           histBdt     = new TH1F( "MVA_BDT",           "MVA_BDT",           nbin, -0.8, 0.8 );
   if (Use["BDTG"])          histBdtG    = new TH1F( "MVA_BDTG",          "MVA_BDTG",          nbin, -1.0, 1.0 );
   if (Use["BDTB"])          histBdtB    = new TH1F( "MVA_BDTB",          "MVA_BDTB",          nbin, -1.0, 1.0 );
   if (Use["BDTD"])          histBdtD    = new TH1F( "MVA_BDTD",          "MVA_BDTD",          nbin, -0.8, 0.8 );
   if (Use["BDTF"])          histBdtF    = new TH1F( "MVA_BDTF",          "MVA_BDTF",          nbin, -1.0, 1.0 );

   // Prepare input tree (this must be replaced by your data source)
   // in this example, there is a toy tree with signal and one with background events
   // we'll later on use only the "signal" events for the test in this example.
   //
   TFile *input(0);
   //TString fname = "./tmva_class_example.root";
   if (!gSystem->AccessPathName( inFile )) {
      input = TFile::Open( inFile ); // check if file in local directory exists
   }
   if (!input) {
      std::cout << "ERROR: could not open data file" << std::endl;
      exit(1);
   }
   std::cout << "--- TMVAClassificationApp    : Using input file: " << input->GetName() << std::endl;

   // Event loop

   // Prepare the event tree
   // - Here the variable names have to corresponds to your tree
   // - You can use the same variables as above which is slightly faster,
   //   but of course you can use different ones and copy the values inside the event loop
   //
   std::cout << "--- Select signal sample" << std::endl;
   TTree* theTree = (TTree*)input->Get("sf/t");
	theTree->SetBranchAddress("Run",&Run);
	theTree->SetBranchAddress("Lumi",&Lumi);
	theTree->SetBranchAddress("Xsec",&Xsec);
	theTree->SetBranchAddress("Event",&Event);
	theTree->SetBranchAddress("genWeight",&genWeight);
	theTree->SetBranchAddress("isData",&isData);
	theTree->SetBranchAddress("nLep",&nLep);
	theTree->SetBranchAddress("nVeto",&nVeto);
	theTree->SetBranchAddress("nEl",&nEl);
	theTree->SetBranchAddress("nMu",&nMu);
	theTree->SetBranchAddress("nTightEl",&nTightEl);
	theTree->SetBranchAddress("nTightMu",&nTightMu);
	theTree->SetBranchAddress("nTightLeps",&nTightLeps);
	theTree->SetBranchAddress("tightLepsIdx",&tightLepsIdx);
	theTree->SetBranchAddress("Lep_pdgId",&Lep_pdgId);
	theTree->SetBranchAddress("Lep_pt",&Lep_pt);
	theTree->SetBranchAddress("Lep_eta",&Lep_eta);
	theTree->SetBranchAddress("Lep_phi",&Lep_phi);
	theTree->SetBranchAddress("Lep_Idx",&Lep_Idx);
	theTree->SetBranchAddress("Lep_relIso",&Lep_relIso);
	theTree->SetBranchAddress("Lep_miniIso",&Lep_miniIso);
	theTree->SetBranchAddress("Lep_hOverE",&Lep_hOverE);
	theTree->SetBranchAddress("Selected",&Selected);
	theTree->SetBranchAddress("Lep2_pt",&Lep2_pt);
	theTree->SetBranchAddress("Selected2",&Selected2);
	theTree->SetBranchAddress("MET",&MET);
	theTree->SetBranchAddress("LT",&LT);
	theTree->SetBranchAddress("ST",&ST);
	theTree->SetBranchAddress("MT",&MT);
	theTree->SetBranchAddress("DeltaPhiLepW",&DeltaPhiLepW);
	theTree->SetBranchAddress("dPhi",&dPhi);
	theTree->SetBranchAddress("Lp",&Lp);
	theTree->SetBranchAddress("GendPhi",&GendPhi);
	theTree->SetBranchAddress("GenLT",&GenLT);
	theTree->SetBranchAddress("GenMET",&GenMET);
	theTree->SetBranchAddress("HT",&HT);
	theTree->SetBranchAddress("nJets",&nJets);
	theTree->SetBranchAddress("nBJet",&nBJet);
	theTree->SetBranchAddress("nBJetDeep",&nBJetDeep);
	theTree->SetBranchAddress("nJets30",&nJets30);
	theTree->SetBranchAddress("Jets30Idx",&Jets30Idx);
	theTree->SetBranchAddress("nBJets30",&nBJets30);
	theTree->SetBranchAddress("nJets30Clean",&nJets30Clean);
	theTree->SetBranchAddress("nJets40",&nJets40);
	theTree->SetBranchAddress("nBJets40",&nBJets40);
	theTree->SetBranchAddress("htJet30j",&htJet30j);
	theTree->SetBranchAddress("htJet30ja",&htJet30ja);
	theTree->SetBranchAddress("htJet40j",&htJet40j);
	theTree->SetBranchAddress("Jet1_pt",&Jet1_pt);
	theTree->SetBranchAddress("Jet2_pt",&Jet2_pt);
	theTree->SetBranchAddress("nFatJets",&nFatJets);
	theTree->SetBranchAddress("FatJet1_pt",&FatJet1_pt);
	theTree->SetBranchAddress("FatJet2_pt",&FatJet2_pt);
	theTree->SetBranchAddress("FatJet1_eta",&FatJet1_eta);
	theTree->SetBranchAddress("FatJet2_eta",&FatJet2_eta);
	theTree->SetBranchAddress("FatJet1_phi",&FatJet1_phi);
	theTree->SetBranchAddress("FatJet2_phi",&FatJet2_phi);
	theTree->SetBranchAddress("FatJet1_mass",&FatJet1_mass);
	theTree->SetBranchAddress("FatJet2_mass",&FatJet2_mass);
	theTree->SetBranchAddress("nDeepTop_loose",&nDeepTop_loose);
	theTree->SetBranchAddress("nDeepTop_medium",&nDeepTop_medium);
	theTree->SetBranchAddress("nDeepTop_tight",&nDeepTop_tight);
	theTree->SetBranchAddress("nBJet_Excl_LooseTop_08",&nBJet_Excl_LooseTop_08);
	theTree->SetBranchAddress("nBJet_Excl_MediumTop_08",&nBJet_Excl_MediumTop_08);
	theTree->SetBranchAddress("nBJet_Excl_TightTop_08",&nBJet_Excl_TightTop_08);
	theTree->SetBranchAddress("nBJetDeep_Excl_LooseTop_08",&nBJetDeep_Excl_LooseTop_08);
	theTree->SetBranchAddress("nBJetDeep_Excl_MediumTop_08",&nBJetDeep_Excl_MediumTop_08);
	theTree->SetBranchAddress("nBJetDeep_Excl_TightTop_08",&nBJetDeep_Excl_TightTop_08);
	theTree->SetBranchAddress("DeepAK8Top_Loose_pt_Array",&DeepAK8Top_Loose_pt_Array);
	theTree->SetBranchAddress("DeepAK8Top_Loose_eta_Array",&DeepAK8Top_Loose_eta_Array);
	theTree->SetBranchAddress("DeepAK8Top_Loose_phi_Array",&DeepAK8Top_Loose_phi_Array);
	theTree->SetBranchAddress("Flag_Btag_leq_08_from_Loose_DeepAK8",&Flag_Btag_leq_08_from_Loose_DeepAK8);
	theTree->SetBranchAddress("BTag_phi_Array",&BTag_phi_Array);
	theTree->SetBranchAddress("BTag_eta_Array",&BTag_eta_Array);
	theTree->SetBranchAddress("BTag_pt_Array",&BTag_pt_Array);
	theTree->SetBranchAddress("nHighPtTopTag",&nHighPtTopTag);
	theTree->SetBranchAddress("nHighPtTopTagPlusTau23",&nHighPtTopTagPlusTau23);
	theTree->SetBranchAddress("LSLjetptGT80",&LSLjetptGT80);
	theTree->SetBranchAddress("isSR",&isSR);
	theTree->SetBranchAddress("Mll",&Mll);
	theTree->SetBranchAddress("METfilters",&METfilters);
	theTree->SetBranchAddress("PD_JetHT",&PD_JetHT);
	theTree->SetBranchAddress("PD_SingleEle",&PD_SingleEle);
	theTree->SetBranchAddress("PD_SingleMu",&PD_SingleMu);
	theTree->SetBranchAddress("PD_MET",&PD_MET);
	theTree->SetBranchAddress("isDPhiSignal",&isDPhiSignal);
	theTree->SetBranchAddress("RA2_muJetFilter",&RA2_muJetFilter);
	theTree->SetBranchAddress("Flag_fastSimCorridorJetCleaning",&Flag_fastSimCorridorJetCleaning);
	theTree->SetBranchAddress("nGenJets",&nGenJets);
	theTree->SetBranchAddress("nGenbJets",&nGenbJets);
	theTree->SetBranchAddress("nGenJets30",&nGenJets30);
	theTree->SetBranchAddress("nGenbJets30",&nGenbJets30);
	theTree->SetBranchAddress("prefireW",&prefireW);
	theTree->SetBranchAddress("prefireWup",&prefireWup);
	theTree->SetBranchAddress("prefireWdwn",&prefireWdwn);
	theTree->SetBranchAddress("HLT_HT350",&HLT_HT350);
	theTree->SetBranchAddress("HLT_HT600",&HLT_HT600);
	theTree->SetBranchAddress("HLT_HT800",&HLT_HT800);
	theTree->SetBranchAddress("HLT_HT900",&HLT_HT900);
	theTree->SetBranchAddress("HLT_PFJet450",&HLT_PFJet450);
	theTree->SetBranchAddress("HLT_MET170",&HLT_MET170);
	theTree->SetBranchAddress("HLT_HT350MET120",&HLT_HT350MET120);
	theTree->SetBranchAddress("HLT_HT350MET100",&HLT_HT350MET100);
	theTree->SetBranchAddress("HLT_HTMET",&HLT_HTMET);
	theTree->SetBranchAddress("HLT_IsoMu27",&HLT_IsoMu27);
	theTree->SetBranchAddress("HLT_IsoMu20",&HLT_IsoMu20);
	theTree->SetBranchAddress("HLT_IsoMu24",&HLT_IsoMu24);
	theTree->SetBranchAddress("HLT_Mu50",&HLT_Mu50);
	theTree->SetBranchAddress("HLT_MuHT400MET70",&HLT_MuHT400MET70);
	theTree->SetBranchAddress("HLT_MuHT350MET70",&HLT_MuHT350MET70);
	theTree->SetBranchAddress("HLT_MuHT350MET50",&HLT_MuHT350MET50);
	theTree->SetBranchAddress("HLT_MuHTMET",&HLT_MuHTMET);
	theTree->SetBranchAddress("HLT_MuHT350",&HLT_MuHT350);
	theTree->SetBranchAddress("HLT_IsoEle32",&HLT_IsoEle32);
	theTree->SetBranchAddress("HLT_IsoEle22",&HLT_IsoEle22);
	theTree->SetBranchAddress("HLT_IsoEle23",&HLT_IsoEle23);
	theTree->SetBranchAddress("HLT_IsoEle27T",&HLT_IsoEle27T);
	theTree->SetBranchAddress("HLT_Ele105",&HLT_Ele105);
	theTree->SetBranchAddress("HLT_Ele115",&HLT_Ele115);
	theTree->SetBranchAddress("HLT_Ele50PFJet165",&HLT_Ele50PFJet165);
	theTree->SetBranchAddress("HLT_EleHT400MET70",&HLT_EleHT400MET70);
	theTree->SetBranchAddress("HLT_EleHT350MET70",&HLT_EleHT350MET70);
	theTree->SetBranchAddress("HLT_EleHT350MET50",&HLT_EleHT350MET50);
	theTree->SetBranchAddress("HLT_EleHTMET",&HLT_EleHTMET);
	theTree->SetBranchAddress("HLT_EleHT350",&HLT_EleHT350);
	theTree->SetBranchAddress("HLT_EleHT400",&HLT_EleHT400);
	theTree->SetBranchAddress("HLT_MuHT400",&HLT_MuHT400);
	theTree->SetBranchAddress("HLT_Ele50HT400",&HLT_Ele50HT400);
	theTree->SetBranchAddress("HLT_Mu50HT400",&HLT_Mu50HT400);
	theTree->SetBranchAddress("HLT_highMHTMET",&HLT_highMHTMET);
	theTree->SetBranchAddress("HLT_MET100MHT100",&HLT_MET100MHT100);
	theTree->SetBranchAddress("HLT_MET110MHT110",&HLT_MET110MHT110);
	theTree->SetBranchAddress("HLT_MET120MHT120",&HLT_MET120MHT120);
	theTree->SetBranchAddress("HLT_MET190_TypeOne_HBHE_BH",&HLT_MET190_TypeOne_HBHE_BH);
	theTree->SetBranchAddress("HLT_EleOR",&HLT_EleOR);
	theTree->SetBranchAddress("HLT_MuOR",&HLT_MuOR);
	theTree->SetBranchAddress("HLT_LepOR",&HLT_LepOR);
	theTree->SetBranchAddress("HLT_MetOR",&HLT_MetOR);
	theTree->SetBranchAddress("TrigEff",&TrigEff);
	theTree->SetBranchAddress("nVtx",&nVtx);
	theTree->SetBranchAddress("nTrueInt",&nTrueInt);
	theTree->SetBranchAddress("puRatio",&puRatio);
	theTree->SetBranchAddress("puRatio_up",&puRatio_up);
	theTree->SetBranchAddress("puRatio_down",&puRatio_down);
	theTree->SetBranchAddress("mGo",&mGo);
	theTree->SetBranchAddress("mLSP",&mLSP);
	theTree->SetBranchAddress("susyXsec",&susyXsec);
	theTree->SetBranchAddress("susyNgen",&susyNgen);
	theTree->SetBranchAddress("totalNgen",&totalNgen);
	theTree->SetBranchAddress("susyWgen",&susyWgen);
	theTree->SetBranchAddress("nISR",&nISR);
	theTree->SetBranchAddress("nISRweight",&nISRweight);
	theTree->SetBranchAddress("nISRweightsyst_up",&nISRweightsyst_up);
	theTree->SetBranchAddress("nISRweightsyst_down",&nISRweightsyst_down);
	theTree->SetBranchAddress("ScaleWgt",&ScaleWgt);
	theTree->SetBranchAddress("lepSF",&lepSF);
	theTree->SetBranchAddress("lepSFerr",&lepSFerr);
	theTree->SetBranchAddress("lepSFunc",&lepSFunc);
	theTree->SetBranchAddress("btagW_1p",&btagW_1p);
	theTree->SetBranchAddress("btagW_2p",&btagW_2p);
	theTree->SetBranchAddress("btagW_3p",&btagW_3p);
	theTree->SetBranchAddress("btagW_0",&btagW_0);
	theTree->SetBranchAddress("btagW_1",&btagW_1);
	theTree->SetBranchAddress("btagW_2",&btagW_2);
	theTree->SetBranchAddress("btagW_1p_SF",&btagW_1p_SF);
	theTree->SetBranchAddress("btagW_2p_SF",&btagW_2p_SF);
	theTree->SetBranchAddress("btagW_3p_SF",&btagW_3p_SF);
	theTree->SetBranchAddress("btagW_0_SF",&btagW_0_SF);
	theTree->SetBranchAddress("btagW_1_SF",&btagW_1_SF);
	theTree->SetBranchAddress("btagW_2_SF",&btagW_2_SF);
	theTree->SetBranchAddress("btagW_1p_SF_b_Up",&btagW_1p_SF_b_Up);
	theTree->SetBranchAddress("btagW_2p_SF_b_Up",&btagW_2p_SF_b_Up);
	theTree->SetBranchAddress("btagW_3p_SF_b_Up",&btagW_3p_SF_b_Up);
	theTree->SetBranchAddress("btagW_0_SF_b_Up",&btagW_0_SF_b_Up);
	theTree->SetBranchAddress("btagW_1_SF_b_Up",&btagW_1_SF_b_Up);
	theTree->SetBranchAddress("btagW_2_SF_b_Up",&btagW_2_SF_b_Up);
	theTree->SetBranchAddress("btagW_1p_SF_b_Down",&btagW_1p_SF_b_Down);
	theTree->SetBranchAddress("btagW_2p_SF_b_Down",&btagW_2p_SF_b_Down);
	theTree->SetBranchAddress("btagW_3p_SF_b_Down",&btagW_3p_SF_b_Down);
	theTree->SetBranchAddress("btagW_0_SF_b_Down",&btagW_0_SF_b_Down);
	theTree->SetBranchAddress("btagW_1_SF_b_Down",&btagW_1_SF_b_Down);
	theTree->SetBranchAddress("btagW_2_SF_b_Down",&btagW_2_SF_b_Down);
	theTree->SetBranchAddress("btagW_1p_SF_light_Up",&btagW_1p_SF_light_Up);
	theTree->SetBranchAddress("btagW_2p_SF_light_Up",&btagW_2p_SF_light_Up);
	theTree->SetBranchAddress("btagW_3p_SF_light_Up",&btagW_3p_SF_light_Up);
	theTree->SetBranchAddress("btagW_0_SF_light_Up",&btagW_0_SF_light_Up);
	theTree->SetBranchAddress("btagW_1_SF_light_Up",&btagW_1_SF_light_Up);
	theTree->SetBranchAddress("btagW_2_SF_light_Up",&btagW_2_SF_light_Up);
	theTree->SetBranchAddress("btagW_1p_SF_light_Down",&btagW_1p_SF_light_Down);
	theTree->SetBranchAddress("btagW_2p_SF_light_Down",&btagW_2p_SF_light_Down);
	theTree->SetBranchAddress("btagW_3p_SF_light_Down",&btagW_3p_SF_light_Down);
	theTree->SetBranchAddress("btagW_0_SF_light_Down",&btagW_0_SF_light_Down);
	theTree->SetBranchAddress("btagW_1_SF_light_Down",&btagW_1_SF_light_Down);
	theTree->SetBranchAddress("btagW_2_SF_light_Down",&btagW_2_SF_light_Down);
	theTree->SetBranchAddress("btagSF_l_down",&btagSF_l_down);
	theTree->SetBranchAddress("btagSF_l_up",&btagSF_l_up);
	theTree->SetBranchAddress("btagSF_b_down",&btagSF_b_down);
	theTree->SetBranchAddress("btagSF_b_up",&btagSF_b_up);
	theTree->SetBranchAddress("btagSF",&btagSF);
	theTree->SetBranchAddress("GenTopPt",&GenTopPt);
	theTree->SetBranchAddress("GenAntiTopPt",&GenAntiTopPt);
	theTree->SetBranchAddress("TopPtWeight",&TopPtWeight);
	theTree->SetBranchAddress("TopPtWeightII",&TopPtWeightII);
	theTree->SetBranchAddress("GenTTBarPt",&GenTTBarPt);
	theTree->SetBranchAddress("GenTTBarWeight",&GenTTBarWeight);
	theTree->SetBranchAddress("ISRTTBarWeight",&ISRTTBarWeight);
	theTree->SetBranchAddress("GenGGPt",&GenGGPt);
	theTree->SetBranchAddress("ISRSigUp",&ISRSigUp);
	theTree->SetBranchAddress("ISRSigDown",&ISRSigDown);
	theTree->SetBranchAddress("DilepNJetCorr",&DilepNJetCorr);
	theTree->SetBranchAddress("DilepNJetWeightConstUp",&DilepNJetWeightConstUp);
	theTree->SetBranchAddress("DilepNJetWeightSlopeUp",&DilepNJetWeightSlopeUp);
	theTree->SetBranchAddress("DilepNJetWeightConstDn",&DilepNJetWeightConstDn);
	theTree->SetBranchAddress("DilepNJetWeightSlopeDn",&DilepNJetWeightSlopeDn);
	theTree->SetBranchAddress("WpolWup",&WpolWup);
	theTree->SetBranchAddress("WpolWdown",&WpolWdown);
	theTree->SetBranchAddress("nISRtt",&nISRtt);
	theTree->SetBranchAddress("nISRttweight",&nISRttweight);
	theTree->SetBranchAddress("nISRttweightsyst_up",&nISRttweightsyst_up);
	theTree->SetBranchAddress("nISRttweightsyst_down",&nISRttweightsyst_down);
	theTree->SetBranchAddress("DL_LepGoodOne_pt",&DL_LepGoodOne_pt);
	theTree->SetBranchAddress("DL_LepGoodOne_pdgId",&DL_LepGoodOne_pdgId);
	theTree->SetBranchAddress("DL_l1l2ovMET",&DL_l1l2ovMET);
	theTree->SetBranchAddress("DL_Vecl1l2ovMET",&DL_Vecl1l2ovMET);
	theTree->SetBranchAddress("DL_DPhil1l2",&DL_DPhil1l2);
	theTree->SetBranchAddress("nLostLepTreatments",&nLostLepTreatments);
	theTree->SetBranchAddress("DL_ST",&DL_ST);
	theTree->SetBranchAddress("DL_HT",&DL_HT);
	theTree->SetBranchAddress("DL_dPhiLepW",&DL_dPhiLepW);
	theTree->SetBranchAddress("DL_nJets30Clean",&DL_nJets30Clean);
	theTree->SetBranchAddress("nMaxStat",&nMaxStat);
	theTree->SetBranchAddress("DLMS_ST",&DLMS_ST);
	theTree->SetBranchAddress("DLMS_HT",&DLMS_HT);
	theTree->SetBranchAddress("DLMS_dPhiLepW",&DLMS_dPhiLepW);
	theTree->SetBranchAddress("DLMS_nJets30Clean",&DLMS_nJets30Clean);
	theTree->SetBranchAddress("iso_had",&iso_had);
	theTree->SetBranchAddress("iso_pt",&iso_pt);
	theTree->SetBranchAddress("iso_MT2",&iso_MT2);
	theTree->SetBranchAddress("iso_Veto",&iso_Veto);
	theTree->SetBranchAddress("mvaValue",&mvaValue);
	theTree->SetBranchAddress("HadTop_pt",&HadTop_pt);
	theTree->SetBranchAddress("HadTop_eta",&HadTop_eta);
	theTree->SetBranchAddress("HadTop_phi",&HadTop_phi);
	theTree->SetBranchAddress("HadTop_mass",&HadTop_mass);
	theTree->SetBranchAddress("j1_eta",&j1_eta);
	theTree->SetBranchAddress("j1_phi",&j1_phi);
	theTree->SetBranchAddress("j2_eta",&j2_eta);
	theTree->SetBranchAddress("j2_phi",&j2_phi);
	theTree->SetBranchAddress("j3_eta",&j3_eta);
	theTree->SetBranchAddress("j3_phi",&j3_phi);
	theTree->SetBranchAddress("W_fromHadTop_dRb",&W_fromHadTop_dRb);
	theTree->SetBranchAddress("b_fromHadTop_CSV",&b_fromHadTop_CSV);
	theTree->SetBranchAddress("j1",&j1);
	theTree->SetBranchAddress("j2",&j2);
	theTree->SetBranchAddress("j3",&j3);
	theTree->SetBranchAddress("mvaValue_2",&mvaValue_2);
	theTree->SetBranchAddress("HadTop_pt_2",&HadTop_pt_2);
	theTree->SetBranchAddress("HadTop_eta_2",&HadTop_eta_2);
	theTree->SetBranchAddress("HadTop_phi_2",&HadTop_phi_2);
	theTree->SetBranchAddress("HadTop_mass_2",&HadTop_mass_2);
	theTree->SetBranchAddress("j1_eta_2",&j1_eta_2);
	theTree->SetBranchAddress("j1_phi_2",&j1_phi_2);
	theTree->SetBranchAddress("j2_eta_2",&j2_eta_2);
	theTree->SetBranchAddress("j2_phi_2",&j2_phi_2);
	theTree->SetBranchAddress("j3_eta_2",&j3_eta_2);
	theTree->SetBranchAddress("j3_phi_2",&j3_phi_2);
	theTree->SetBranchAddress("W_fromHadTop_dRb_2",&W_fromHadTop_dRb_2);
	theTree->SetBranchAddress("b_fromHadTop_CSV_2",&b_fromHadTop_CSV_2);
	theTree->SetBranchAddress("j1_2",&j1_2);
	theTree->SetBranchAddress("j2_2",&j2_2);
	theTree->SetBranchAddress("j3_2",&j3_2);
	theTree->SetBranchAddress("mvaValue_3",&mvaValue_3);
	theTree->SetBranchAddress("HadTop_pt_3",&HadTop_pt_3);
	theTree->SetBranchAddress("HadTop_eta_3",&HadTop_eta_3);
	theTree->SetBranchAddress("HadTop_phi_3",&HadTop_phi_3);
	theTree->SetBranchAddress("HadTop_mass_3",&HadTop_mass_3);
	theTree->SetBranchAddress("j1_eta_3",&j1_eta_3);
	theTree->SetBranchAddress("j1_phi_3",&j1_phi_3);
	theTree->SetBranchAddress("j2_eta_3",&j2_eta_3);
	theTree->SetBranchAddress("j2_phi_3",&j2_phi_3);
	theTree->SetBranchAddress("j3_eta_3",&j3_eta_3);
	theTree->SetBranchAddress("j3_phi_3",&j3_phi_3);
	theTree->SetBranchAddress("W_fromHadTop_dRb_3",&W_fromHadTop_dRb_3);
	theTree->SetBranchAddress("b_fromHadTop_CSV_3",&b_fromHadTop_CSV_3);
	theTree->SetBranchAddress("j1_3",&j1_3);
	theTree->SetBranchAddress("j2_3",&j2_3);
	theTree->SetBranchAddress("j3_3",&j3_3);
	theTree->SetBranchAddress("mvaValue_4",&mvaValue_4);
	theTree->SetBranchAddress("HadTop_pt_4",&HadTop_pt_4);
	theTree->SetBranchAddress("HadTop_eta_4",&HadTop_eta_4);
	theTree->SetBranchAddress("HadTop_phi_4",&HadTop_phi_4);
	theTree->SetBranchAddress("HadTop_mass_4",&HadTop_mass_4);
	theTree->SetBranchAddress("j1_eta_4",&j1_eta_4);
	theTree->SetBranchAddress("j1_phi_4",&j1_phi_4);
	theTree->SetBranchAddress("j2_eta_4",&j2_eta_4);
	theTree->SetBranchAddress("j2_phi_4",&j2_phi_4);
	theTree->SetBranchAddress("j3_eta_4",&j3_eta_4);
	theTree->SetBranchAddress("j3_phi_4",&j3_phi_4);
	theTree->SetBranchAddress("W_fromHadTop_dRb_4",&W_fromHadTop_dRb_4);
	theTree->SetBranchAddress("b_fromHadTop_CSV_4",&b_fromHadTop_CSV_4);
	theTree->SetBranchAddress("j1_4",&j1_4);
	theTree->SetBranchAddress("j2_4",&j2_4);
	theTree->SetBranchAddress("j3_4",&j3_4);
	theTree->SetBranchAddress("nResolvedTop",&nResolvedTop);
	theTree->SetBranchAddress("nTop_Total_Combined",&nTop_Total_Combined);
	theTree->SetBranchAddress("Resolved_Had_Top_mvaValue",&Resolved_Had_Top_mvaValue);
	theTree->SetBranchAddress("Resolved_Had_Top_pt",&Resolved_Had_Top_pt);
	theTree->SetBranchAddress("Resolved_Had_Top_eta",&Resolved_Had_Top_eta);
	theTree->SetBranchAddress("Resolved_Had_Top_phi",&Resolved_Had_Top_phi);
	theTree->SetBranchAddress("Resolved_Had_Top_mass",&Resolved_Had_Top_mass);
	theTree->SetBranchAddress("nBCleaned_TOTAL",&nBCleaned_TOTAL);
	theTree->SetBranchAddress("Resolved_Top_pt_Cleaned",&Resolved_Top_pt_Cleaned);
	theTree->SetBranchAddress("Resolved_Top_eta_Cleaned",&Resolved_Top_eta_Cleaned);
	theTree->SetBranchAddress("Resolved_Top_phi_Cleaned",&Resolved_Top_phi_Cleaned);
	theTree->SetBranchAddress("BTag_pt_Cleaned",&BTag_pt_Cleaned);
	theTree->SetBranchAddress("BTag_eta_Cleaned",&BTag_eta_Cleaned);
	theTree->SetBranchAddress("BTag_phi_Cleaned",&BTag_phi_Cleaned);

   TFile *target  = new TFile( "@OUTFILE","RECREATE" );
   Float_t b_@BDT;
   Int_t _nBCleaned_TOTAL = nBCleaned_TOTAL;
   TDirectory *sfdir;
   sfdir = target->mkdir("sf");
   sfdir->cd();
   TTree *t=new TTree("t","t");
    t->Branch("@BDT",  &b_@BDT);
	t->Branch("Run",&Run);
	t->Branch("Lumi",&Lumi);
	t->Branch("Xsec",&Xsec);
	t->Branch("Event",&Event);
	t->Branch("genWeight",&genWeight);
	t->Branch("isData",&isData);
	t->Branch("nLep",&nLep);
	t->Branch("nVeto",&nVeto);
	t->Branch("nEl",&nEl);
	t->Branch("nMu",&nMu);
	t->Branch("nTightEl",&nTightEl);
	t->Branch("nTightMu",&nTightMu);
	t->Branch("nTightLeps",&nTightLeps);
	t->Branch("tightLepsIdx",&tightLepsIdx);
	t->Branch("Lep_pdgId",&Lep_pdgId);
	t->Branch("Lep_pt",&Lep_pt);
	t->Branch("Lep_eta",&Lep_eta);
	t->Branch("Lep_phi",&Lep_phi);
	t->Branch("Lep_Idx",&Lep_Idx);
	t->Branch("Lep_relIso",&Lep_relIso);
	t->Branch("Lep_miniIso",&Lep_miniIso);
	t->Branch("Lep_hOverE",&Lep_hOverE);
	t->Branch("Selected",&Selected);
	t->Branch("Lep2_pt",&Lep2_pt);
	t->Branch("Selected2",&Selected2);
	t->Branch("MET",&MET);
	t->Branch("LT",&LT);
	t->Branch("ST",&ST);
	t->Branch("MT",&MT);
	t->Branch("DeltaPhiLepW",&DeltaPhiLepW);
	t->Branch("dPhi",&dPhi);
	t->Branch("Lp",&Lp);
	t->Branch("GendPhi",&GendPhi);
	t->Branch("GenLT",&GenLT);
	t->Branch("GenMET",&GenMET);
	t->Branch("HT",&HT);
	t->Branch("nJets",&nJets);
	t->Branch("nBJet",&nBJet);
	t->Branch("nBJetDeep",&nBJetDeep);
	t->Branch("nJets30",&nJets30);
	t->Branch("Jets30Idx",&Jets30Idx);
	t->Branch("nBJets30",&nBJets30);
	t->Branch("nJets30Clean",&nJets30Clean);
	t->Branch("nJets40",&nJets40);
	t->Branch("nBJets40",&nBJets40);
	t->Branch("htJet30j",&htJet30j);
	t->Branch("htJet30ja",&htJet30ja);
	t->Branch("htJet40j",&htJet40j);
	t->Branch("Jet1_pt",&Jet1_pt);
	t->Branch("Jet2_pt",&Jet2_pt);
	t->Branch("nFatJets",&nFatJets);
	t->Branch("FatJet1_pt",&FatJet1_pt);
	t->Branch("FatJet2_pt",&FatJet2_pt);
	t->Branch("FatJet1_eta",&FatJet1_eta);
	t->Branch("FatJet2_eta",&FatJet2_eta);
	t->Branch("FatJet1_phi",&FatJet1_phi);
	t->Branch("FatJet2_phi",&FatJet2_phi);
	t->Branch("FatJet1_mass",&FatJet1_mass);
	t->Branch("FatJet2_mass",&FatJet2_mass);
	t->Branch("nDeepTop_loose",&nDeepTop_loose);
	t->Branch("nDeepTop_medium",&nDeepTop_medium);
	t->Branch("nDeepTop_tight",&nDeepTop_tight);
	t->Branch("nBJet_Excl_LooseTop_08",&nBJet_Excl_LooseTop_08);
	t->Branch("nBJet_Excl_MediumTop_08",&nBJet_Excl_MediumTop_08);
	t->Branch("nBJet_Excl_TightTop_08",&nBJet_Excl_TightTop_08);
	t->Branch("nBJetDeep_Excl_LooseTop_08",&nBJetDeep_Excl_LooseTop_08);
	t->Branch("nBJetDeep_Excl_MediumTop_08",&nBJetDeep_Excl_MediumTop_08);
	t->Branch("nBJetDeep_Excl_TightTop_08",&nBJetDeep_Excl_TightTop_08);
	t->Branch("DeepAK8Top_Loose_pt_Array",&DeepAK8Top_Loose_pt_Array);
	t->Branch("DeepAK8Top_Loose_eta_Array",&DeepAK8Top_Loose_eta_Array);
	t->Branch("DeepAK8Top_Loose_phi_Array",&DeepAK8Top_Loose_phi_Array);
	t->Branch("Flag_Btag_leq_08_from_Loose_DeepAK8",&Flag_Btag_leq_08_from_Loose_DeepAK8);
	t->Branch("BTag_phi_Array",&BTag_phi_Array);
	t->Branch("BTag_eta_Array",&BTag_eta_Array);
	t->Branch("BTag_pt_Array",&BTag_pt_Array);
	t->Branch("nHighPtTopTag",&nHighPtTopTag);
	t->Branch("nHighPtTopTagPlusTau23",&nHighPtTopTagPlusTau23);
	t->Branch("LSLjetptGT80",&LSLjetptGT80);
	t->Branch("isSR",&isSR);
	t->Branch("Mll",&Mll);
	t->Branch("METfilters",&METfilters);
	t->Branch("PD_JetHT",&PD_JetHT);
	t->Branch("PD_SingleEle",&PD_SingleEle);
	t->Branch("PD_SingleMu",&PD_SingleMu);
	t->Branch("PD_MET",&PD_MET);
	t->Branch("isDPhiSignal",&isDPhiSignal);
	t->Branch("RA2_muJetFilter",&RA2_muJetFilter);
	t->Branch("Flag_fastSimCorridorJetCleaning",&Flag_fastSimCorridorJetCleaning);
	t->Branch("nGenJets",&nGenJets);
	t->Branch("nGenbJets",&nGenbJets);
	t->Branch("nGenJets30",&nGenJets30);
	t->Branch("nGenbJets30",&nGenbJets30);
	t->Branch("prefireW",&prefireW);
	t->Branch("prefireWup",&prefireWup);
	t->Branch("prefireWdwn",&prefireWdwn);
	t->Branch("HLT_HT350",&HLT_HT350);
	t->Branch("HLT_HT600",&HLT_HT600);
	t->Branch("HLT_HT800",&HLT_HT800);
	t->Branch("HLT_HT900",&HLT_HT900);
	t->Branch("HLT_PFJet450",&HLT_PFJet450);
	t->Branch("HLT_MET170",&HLT_MET170);
	t->Branch("HLT_HT350MET120",&HLT_HT350MET120);
	t->Branch("HLT_HT350MET100",&HLT_HT350MET100);
	t->Branch("HLT_HTMET",&HLT_HTMET);
	t->Branch("HLT_IsoMu27",&HLT_IsoMu27);
	t->Branch("HLT_IsoMu20",&HLT_IsoMu20);
	t->Branch("HLT_IsoMu24",&HLT_IsoMu24);
	t->Branch("HLT_Mu50",&HLT_Mu50);
	t->Branch("HLT_MuHT400MET70",&HLT_MuHT400MET70);
	t->Branch("HLT_MuHT350MET70",&HLT_MuHT350MET70);
	t->Branch("HLT_MuHT350MET50",&HLT_MuHT350MET50);
	t->Branch("HLT_MuHTMET",&HLT_MuHTMET);
	t->Branch("HLT_MuHT350",&HLT_MuHT350);
	t->Branch("HLT_IsoEle32",&HLT_IsoEle32);
	t->Branch("HLT_IsoEle22",&HLT_IsoEle22);
	t->Branch("HLT_IsoEle23",&HLT_IsoEle23);
	t->Branch("HLT_IsoEle27T",&HLT_IsoEle27T);
	t->Branch("HLT_Ele105",&HLT_Ele105);
	t->Branch("HLT_Ele115",&HLT_Ele115);
	t->Branch("HLT_Ele50PFJet165",&HLT_Ele50PFJet165);
	t->Branch("HLT_EleHT400MET70",&HLT_EleHT400MET70);
	t->Branch("HLT_EleHT350MET70",&HLT_EleHT350MET70);
	t->Branch("HLT_EleHT350MET50",&HLT_EleHT350MET50);
	t->Branch("HLT_EleHTMET",&HLT_EleHTMET);
	t->Branch("HLT_EleHT350",&HLT_EleHT350);
	t->Branch("HLT_EleHT400",&HLT_EleHT400);
	t->Branch("HLT_MuHT400",&HLT_MuHT400);
	t->Branch("HLT_Ele50HT400",&HLT_Ele50HT400);
	t->Branch("HLT_Mu50HT400",&HLT_Mu50HT400);
	t->Branch("HLT_highMHTMET",&HLT_highMHTMET);
	t->Branch("HLT_MET100MHT100",&HLT_MET100MHT100);
	t->Branch("HLT_MET110MHT110",&HLT_MET110MHT110);
	t->Branch("HLT_MET120MHT120",&HLT_MET120MHT120);
	t->Branch("HLT_MET190_TypeOne_HBHE_BH",&HLT_MET190_TypeOne_HBHE_BH);
	t->Branch("HLT_EleOR",&HLT_EleOR);
	t->Branch("HLT_MuOR",&HLT_MuOR);
	t->Branch("HLT_LepOR",&HLT_LepOR);
	t->Branch("HLT_MetOR",&HLT_MetOR);
	t->Branch("TrigEff",&TrigEff);
	t->Branch("nVtx",&nVtx);
	t->Branch("nTrueInt",&nTrueInt);
	t->Branch("puRatio",&puRatio);
	t->Branch("puRatio_up",&puRatio_up);
	t->Branch("puRatio_down",&puRatio_down);
	t->Branch("mGo",&mGo);
	t->Branch("mLSP",&mLSP);
	t->Branch("susyXsec",&susyXsec);
	t->Branch("susyNgen",&susyNgen);
	t->Branch("totalNgen",&totalNgen);
	t->Branch("susyWgen",&susyWgen);
	t->Branch("nISR",&nISR);
	t->Branch("nISRweight",&nISRweight);
	t->Branch("nISRweightsyst_up",&nISRweightsyst_up);
	t->Branch("nISRweightsyst_down",&nISRweightsyst_down);
	t->Branch("ScaleWgt",&ScaleWgt);
	t->Branch("lepSF",&lepSF);
	t->Branch("lepSFerr",&lepSFerr);
	t->Branch("lepSFunc",&lepSFunc);
	t->Branch("btagW_1p",&btagW_1p);
	t->Branch("btagW_2p",&btagW_2p);
	t->Branch("btagW_3p",&btagW_3p);
	t->Branch("btagW_0",&btagW_0);
	t->Branch("btagW_1",&btagW_1);
	t->Branch("btagW_2",&btagW_2);
	t->Branch("btagW_1p_SF",&btagW_1p_SF);
	t->Branch("btagW_2p_SF",&btagW_2p_SF);
	t->Branch("btagW_3p_SF",&btagW_3p_SF);
	t->Branch("btagW_0_SF",&btagW_0_SF);
	t->Branch("btagW_1_SF",&btagW_1_SF);
	t->Branch("btagW_2_SF",&btagW_2_SF);
	t->Branch("btagW_1p_SF_b_Up",&btagW_1p_SF_b_Up);
	t->Branch("btagW_2p_SF_b_Up",&btagW_2p_SF_b_Up);
	t->Branch("btagW_3p_SF_b_Up",&btagW_3p_SF_b_Up);
	t->Branch("btagW_0_SF_b_Up",&btagW_0_SF_b_Up);
	t->Branch("btagW_1_SF_b_Up",&btagW_1_SF_b_Up);
	t->Branch("btagW_2_SF_b_Up",&btagW_2_SF_b_Up);
	t->Branch("btagW_1p_SF_b_Down",&btagW_1p_SF_b_Down);
	t->Branch("btagW_2p_SF_b_Down",&btagW_2p_SF_b_Down);
	t->Branch("btagW_3p_SF_b_Down",&btagW_3p_SF_b_Down);
	t->Branch("btagW_0_SF_b_Down",&btagW_0_SF_b_Down);
	t->Branch("btagW_1_SF_b_Down",&btagW_1_SF_b_Down);
	t->Branch("btagW_2_SF_b_Down",&btagW_2_SF_b_Down);
	t->Branch("btagW_1p_SF_light_Up",&btagW_1p_SF_light_Up);
	t->Branch("btagW_2p_SF_light_Up",&btagW_2p_SF_light_Up);
	t->Branch("btagW_3p_SF_light_Up",&btagW_3p_SF_light_Up);
	t->Branch("btagW_0_SF_light_Up",&btagW_0_SF_light_Up);
	t->Branch("btagW_1_SF_light_Up",&btagW_1_SF_light_Up);
	t->Branch("btagW_2_SF_light_Up",&btagW_2_SF_light_Up);
	t->Branch("btagW_1p_SF_light_Down",&btagW_1p_SF_light_Down);
	t->Branch("btagW_2p_SF_light_Down",&btagW_2p_SF_light_Down);
	t->Branch("btagW_3p_SF_light_Down",&btagW_3p_SF_light_Down);
	t->Branch("btagW_0_SF_light_Down",&btagW_0_SF_light_Down);
	t->Branch("btagW_1_SF_light_Down",&btagW_1_SF_light_Down);
	t->Branch("btagW_2_SF_light_Down",&btagW_2_SF_light_Down);
	t->Branch("btagSF_l_down",&btagSF_l_down);
	t->Branch("btagSF_l_up",&btagSF_l_up);
	t->Branch("btagSF_b_down",&btagSF_b_down);
	t->Branch("btagSF_b_up",&btagSF_b_up);
	t->Branch("btagSF",&btagSF);
	t->Branch("GenTopPt",&GenTopPt);
	t->Branch("GenAntiTopPt",&GenAntiTopPt);
	t->Branch("TopPtWeight",&TopPtWeight);
	t->Branch("TopPtWeightII",&TopPtWeightII);
	t->Branch("GenTTBarPt",&GenTTBarPt);
	t->Branch("GenTTBarWeight",&GenTTBarWeight);
	t->Branch("ISRTTBarWeight",&ISRTTBarWeight);
	t->Branch("GenGGPt",&GenGGPt);
	t->Branch("ISRSigUp",&ISRSigUp);
	t->Branch("ISRSigDown",&ISRSigDown);
	t->Branch("DilepNJetCorr",&DilepNJetCorr);
	t->Branch("DilepNJetWeightConstUp",&DilepNJetWeightConstUp);
	t->Branch("DilepNJetWeightSlopeUp",&DilepNJetWeightSlopeUp);
	t->Branch("DilepNJetWeightConstDn",&DilepNJetWeightConstDn);
	t->Branch("DilepNJetWeightSlopeDn",&DilepNJetWeightSlopeDn);
	t->Branch("WpolWup",&WpolWup);
	t->Branch("WpolWdown",&WpolWdown);
	t->Branch("nISRtt",&nISRtt);
	t->Branch("nISRttweight",&nISRttweight);
	t->Branch("nISRttweightsyst_up",&nISRttweightsyst_up);
	t->Branch("nISRttweightsyst_down",&nISRttweightsyst_down);
	t->Branch("DL_LepGoodOne_pt",&DL_LepGoodOne_pt);
	t->Branch("DL_LepGoodOne_pdgId",&DL_LepGoodOne_pdgId);
	t->Branch("DL_l1l2ovMET",&DL_l1l2ovMET);
	t->Branch("DL_Vecl1l2ovMET",&DL_Vecl1l2ovMET);
	t->Branch("DL_DPhil1l2",&DL_DPhil1l2);
	t->Branch("nLostLepTreatments",&nLostLepTreatments);
	t->Branch("DL_ST",&DL_ST);
	t->Branch("DL_HT",&DL_HT);
	t->Branch("DL_dPhiLepW",&DL_dPhiLepW);
	t->Branch("DL_nJets30Clean",&DL_nJets30Clean);
	t->Branch("nMaxStat",&nMaxStat);
	t->Branch("DLMS_ST",&DLMS_ST);
	t->Branch("DLMS_HT",&DLMS_HT);
	t->Branch("DLMS_dPhiLepW",&DLMS_dPhiLepW);
	t->Branch("DLMS_nJets30Clean",&DLMS_nJets30Clean);
	t->Branch("iso_had",&iso_had);
	t->Branch("iso_pt",&iso_pt);
	t->Branch("iso_MT2",&iso_MT2);
	t->Branch("iso_Veto",&iso_Veto);
	t->Branch("mvaValue",&mvaValue);
	t->Branch("HadTop_pt",&HadTop_pt);
	t->Branch("HadTop_eta",&HadTop_eta);
	t->Branch("HadTop_phi",&HadTop_phi);
	t->Branch("HadTop_mass",&HadTop_mass);
	t->Branch("j1_eta",&j1_eta);
	t->Branch("j1_phi",&j1_phi);
	t->Branch("j2_eta",&j2_eta);
	t->Branch("j2_phi",&j2_phi);
	t->Branch("j3_eta",&j3_eta);
	t->Branch("j3_phi",&j3_phi);
	t->Branch("W_fromHadTop_dRb",&W_fromHadTop_dRb);
	t->Branch("b_fromHadTop_CSV",&b_fromHadTop_CSV);
	t->Branch("j1",&j1);
	t->Branch("j2",&j2);
	t->Branch("j3",&j3);
	t->Branch("mvaValue_2",&mvaValue_2);
	t->Branch("HadTop_pt_2",&HadTop_pt_2);
	t->Branch("HadTop_eta_2",&HadTop_eta_2);
	t->Branch("HadTop_phi_2",&HadTop_phi_2);
	t->Branch("HadTop_mass_2",&HadTop_mass_2);
	t->Branch("j1_eta_2",&j1_eta_2);
	t->Branch("j1_phi_2",&j1_phi_2);
	t->Branch("j2_eta_2",&j2_eta_2);
	t->Branch("j2_phi_2",&j2_phi_2);
	t->Branch("j3_eta_2",&j3_eta_2);
	t->Branch("j3_phi_2",&j3_phi_2);
	t->Branch("W_fromHadTop_dRb_2",&W_fromHadTop_dRb_2);
	t->Branch("b_fromHadTop_CSV_2",&b_fromHadTop_CSV_2);
	t->Branch("j1_2",&j1_2);
	t->Branch("j2_2",&j2_2);
	t->Branch("j3_2",&j3_2);
	t->Branch("mvaValue_3",&mvaValue_3);
	t->Branch("HadTop_pt_3",&HadTop_pt_3);
	t->Branch("HadTop_eta_3",&HadTop_eta_3);
	t->Branch("HadTop_phi_3",&HadTop_phi_3);
	t->Branch("HadTop_mass_3",&HadTop_mass_3);
	t->Branch("j1_eta_3",&j1_eta_3);
	t->Branch("j1_phi_3",&j1_phi_3);
	t->Branch("j2_eta_3",&j2_eta_3);
	t->Branch("j2_phi_3",&j2_phi_3);
	t->Branch("j3_eta_3",&j3_eta_3);
	t->Branch("j3_phi_3",&j3_phi_3);
	t->Branch("W_fromHadTop_dRb_3",&W_fromHadTop_dRb_3);
	t->Branch("b_fromHadTop_CSV_3",&b_fromHadTop_CSV_3);
	t->Branch("j1_3",&j1_3);
	t->Branch("j2_3",&j2_3);
	t->Branch("j3_3",&j3_3);
	t->Branch("mvaValue_4",&mvaValue_4);
	t->Branch("HadTop_pt_4",&HadTop_pt_4);
	t->Branch("HadTop_eta_4",&HadTop_eta_4);
	t->Branch("HadTop_phi_4",&HadTop_phi_4);
	t->Branch("HadTop_mass_4",&HadTop_mass_4);
	t->Branch("j1_eta_4",&j1_eta_4);
	t->Branch("j1_phi_4",&j1_phi_4);
	t->Branch("j2_eta_4",&j2_eta_4);
	t->Branch("j2_phi_4",&j2_phi_4);
	t->Branch("j3_eta_4",&j3_eta_4);
	t->Branch("j3_phi_4",&j3_phi_4);
	t->Branch("W_fromHadTop_dRb_4",&W_fromHadTop_dRb_4);
	t->Branch("b_fromHadTop_CSV_4",&b_fromHadTop_CSV_4);
	t->Branch("j1_4",&j1_4);
	t->Branch("j2_4",&j2_4);
	t->Branch("j3_4",&j3_4);
	t->Branch("nResolvedTop",&nResolvedTop);
	t->Branch("nTop_Total_Combined",&nTop_Total_Combined);
	t->Branch("Resolved_Had_Top_mvaValue",&Resolved_Had_Top_mvaValue);
	t->Branch("Resolved_Had_Top_pt",&Resolved_Had_Top_pt);
	t->Branch("Resolved_Had_Top_eta",&Resolved_Had_Top_eta);
	t->Branch("Resolved_Had_Top_phi",&Resolved_Had_Top_phi);
	t->Branch("Resolved_Had_Top_mass",&Resolved_Had_Top_mass);
	t->Branch("nBCleaned_TOTAL",&_nBCleaned_TOTAL);
	t->Branch("Resolved_Top_pt_Cleaned",&Resolved_Top_pt_Cleaned);
	t->Branch("Resolved_Top_eta_Cleaned",&Resolved_Top_eta_Cleaned);
	t->Branch("Resolved_Top_phi_Cleaned",&Resolved_Top_phi_Cleaned);
	t->Branch("BTag_pt_Cleaned",&BTag_pt_Cleaned);
	t->Branch("BTag_eta_Cleaned",&BTag_eta_Cleaned);
	t->Branch("BTag_phi_Cleaned",&BTag_phi_Cleaned);

   std::vector<Float_t> vecVar(4); // vector for EvaluateMVA tests

   std::cout << "--- Processing: " << theTree->GetEntries() << " events" << std::endl;
   TStopwatch sw;
   sw.Start();
   for (Long64_t ievt=0; ievt<theTree->GetEntries();ievt++) {

      if (ievt%10000 == 0) std::cout << "--- ... Processing event: " << ievt << std::endl;

      theTree->GetEntry(ievt);

      //var1 = userVar1 + userVar2;
      //var2 = userVar1 - userVar2;

      // Return the MVA outputs and fill into histograms

      if (Use["BDT"          ]) {
		    histBdt    ->Fill( reader->EvaluateMVA( "BDT method"           ) );
		    b_@BDT= reader->EvaluateMVA( "BDT method");
		    t->Fill();		}
      if (Use["BDTG"         ])   histBdtG   ->Fill( reader->EvaluateMVA( "BDTG method"          ) );
      if (Use["BDTB"         ])   histBdtB   ->Fill( reader->EvaluateMVA( "BDTB method"          ) );
      if (Use["BDTD"         ])   histBdtD   ->Fill( reader->EvaluateMVA( "BDTD method"          ) );
      if (Use["BDTF"         ])   histBdtF   ->Fill( reader->EvaluateMVA( "BDTF method"          ) );      
   }

   // Get elapsed time
   sw.Stop();
   std::cout << "--- End of event loop: "; sw.Print();

   // Write also error and significance histos

   t->Write();
   target->Close();

   std::cout << "--- Created root file: " << target<<  "containing the MVA output histograms" << std::endl;

   delete reader;

   std::cout << "==> TMVAClassificationApplication is done!" << std::endl << std::endl;
}

int main( int argc, char** argv )
{
   TString methodList;
   for (int i=1; i<argc; i++) {
      TString regMethod(argv[i]);
      if(regMethod=="-b" || regMethod=="--batch") continue;
      if (!methodList.IsNull()) methodList += TString(",");
      methodList += regMethod;
   }
   @SCRIPTNAME(methodList);
   return 0;
}
