#include <memory>
#include <vector>
#include <array>
#include <string>
#include <utility>
#include "DataFormats/Math/interface/LorentzVector.h"
#include <DataFormats/Math/interface/deltaR.h>
#include "TMVA/Reader.h"
#include <iostream>

class BDT_limits_19_01_dPhi075_BTag2{
public:
     BDT_limits_19_01_dPhi075_BTag2(std::string weight_file_name){
           Init(weight_file_name);
     };
     ~BDT_limits_19_01_dPhi075_BTag2(){
         clear();
     };
     void addVariables(float dM_Go_LSP, float LT, float HT, float nBCleaned_TOTAL, float nTop_Total_Combined, float nJets30Clean, float dPhi, float DeepAK8Top_Loose_pt_1, float DeepAK8Top_Loose_pt_2, float BTag_pt_1, float BTag_pt_2, float DeepAK8Top_Loose_eta_1, float DeepAK8Top_Loose_eta_2, float BTag_eta_1, float BTag_eta_2, float DeepAK8Top_Loose_phi_1, float DeepAK8Top_Loose_phi_2, float BTag_phi_1, float BTag_phi_2, float HadTop_pt, float HadTop_eta, float HadTop_phi, float HadTop_pt_2, float HadTop_eta_2, float HadTop_phi_2){
          float _dM_Go_LSP = dM_Go_LSP;
          float _LT = LT;
          float _HT = HT;
          float _nBCleaned_TOTAL = nBCleaned_TOTAL;
          float _nTop_Total_Combined = nTop_Total_Combined;
          float _nJets30Clean = nJets30Clean;
          float _dPhi=dPhi;
          float _DeepAK8Top_Loose_pt_1 = DeepAK8Top_Loose_pt_1;
          float _DeepAK8Top_Loose_pt_2 = DeepAK8Top_Loose_pt_2;
          float _BTag_pt_1 = BTag_pt_1;
          float _BTag_pt_2 = BTag_pt_2;
          float _DeepAK8Top_Loose_eta_1 = DeepAK8Top_Loose_eta_1;
          float _DeepAK8Top_Loose_eta_2 = DeepAK8Top_Loose_eta_2;
          float _BTag_eta_1 = BTag_eta_1;
          float _BTag_eta_2 = BTag_eta_2;
          float _DeepAK8Top_Loose_phi_1 = DeepAK8Top_Loose_phi_1;
          float _DeepAK8Top_Loose_phi_2 = DeepAK8Top_Loose_phi_2;
          float _BTag_phi_1 = BTag_phi_1;
          float _BTag_phi_2 = BTag_phi_2;
          float _HadTop_pt = HadTop_pt;
          float _HadTop_eta = HadTop_eta;
          float _HadTop_phi = HadTop_phi;
          float _HadTop_pt_2 = HadTop_pt_2;
          float _HadTop_eta_2 = HadTop_eta_2;
          float _HadTop_phi_2 = HadTop_phi_2;

   
          //cout<<"_HT: "<<_HT<<endl;
     }
     void clear();
     void Init(std::string weight_file_name);
     float EvalMVA(float dM_Go_LSP, float LT, float HT, float nBCleaned_TOTAL, float nTop_Total_Combined, float nJets30Clean, float dPhi, float DeepAK8Top_Loose_pt_1, float DeepAK8Top_Loose_pt_2, float BTag_pt_1, float BTag_pt_2, float DeepAK8Top_Loose_eta_1, float DeepAK8Top_Loose_eta_2, float BTag_eta_1, float BTag_eta_2, float DeepAK8Top_Loose_phi_1, float DeepAK8Top_Loose_phi_2, float BTag_phi_1, float BTag_phi_2, float HadTop_pt, float HadTop_eta, float HadTop_phi, float HadTop_pt_2, float HadTop_eta_2, float HadTop_phi_2);

private:

     float EvalScore(float _dM_Go_LSP, float _LT, float _HT, float _nBCleaned_TOTAL, float _nTop_Total_Combined, float _nJets30Clean, float _dPhi, float _DeepAK8Top_Loose_pt_1, float _DeepAK8Top_Loose_pt_2, float _BTag_pt_1, float _BTag_pt_2, float _DeepAK8Top_Loose_eta_1, float _DeepAK8Top_Loose_eta_2, float _BTag_eta_1, float _BTag_eta_2, float _DeepAK8Top_Loose_phi_1, float _DeepAK8Top_Loose_phi_2, float _BTag_phi_1, float _BTag_phi_2, float _HadTop_pt, float _HadTop_eta, float _HadTop_phi, float _HadTop_pt_2, float _HadTop_eta_2, float _HadTop_phi_2);
 
//     float HT_Final=-99;
//     float LT_Final=-99;
//     float nBCleaned_TOTAL_Final=-99;
//     float nTop_Total_Combined_Final=-99;
//     float nJets30Clean_Final=-99;

     float _dM_Go_LSP;
     float _HT;
     float _LT;
     float _nBCleaned_TOTAL;
     float _nTop_Total_Combined;
     float _nJets30Clean;
     float _dPhi;
     float _DeepAK8Top_Loose_pt_1;
     float _DeepAK8Top_Loose_pt_2;
     float _BTag_pt_1;
     float _BTag_pt_2;
     float _DeepAK8Top_Loose_eta_1;
     float _DeepAK8Top_Loose_eta_2;
     float _BTag_eta_1;
     float _BTag_eta_2;
     float _DeepAK8Top_Loose_phi_1;
     float _DeepAK8Top_Loose_phi_2;
     float _BTag_phi_1;
     float _BTag_phi_2;
     float _HadTop_pt;
     float _HadTop_eta;
     float _HadTop_phi;
     float _HadTop_pt_2;
     float _HadTop_eta_2;
     float _HadTop_phi_2;

   
     float dM_Go_LSP_Final; 
     float LT_Final;
     float HT_Final;
     float nBCleaned_TOTAL_Final;
     float nTop_Total_Combined_Final;
     float nJets30Clean_Final;
     float dPhi_Final;
     float DeepAK8Top_Loose_pt_1_Final;
     float DeepAK8Top_Loose_pt_2_Final;
     float BTag_pt_1_Final;
     float BTag_pt_2_Final;
     float DeepAK8Top_Loose_eta_1_Final;
     float DeepAK8Top_Loose_eta_2_Final;
     float BTag_eta_1_Final;
     float BTag_eta_2_Final;
     float DeepAK8Top_Loose_phi_1_Final;
     float DeepAK8Top_Loose_phi_2_Final;
     float BTag_phi_1_Final;
     float BTag_phi_2_Final;
     float HadTop_pt_Final;
     float HadTop_eta_Final;
     float HadTop_phi_Final;
     float HadTop_pt_2_Final;
     float HadTop_eta_2_Final;
     float HadTop_phi_2_Final;


     std::shared_ptr<TMVA::Reader> TMVAReader_ = nullptr;


     
 
};

void BDT_limits_19_01_dPhi075_BTag2::Init(std::string weight_file_name){

     TMVAReader_ = std::make_shared<TMVA::Reader>( "!Color:!Silent" );

     //cout<<"DeepAK8Top_Loose_pt_1_Final: "<<DeepAK8Top_Loose_pt_1_Final<<endl;
     //cout<<"DeepAK8Top_Loose_pt_2_Final: "<<DeepAK8Top_Loose_pt_2_Final<<endl<<endl;

     //cout<<"_HT: "<<_HT<<endl;
     //cout<<endl;

     TMVAReader_->AddVariable("dM_Go_LSP",&dM_Go_LSP_Final);           
     TMVAReader_->AddVariable("LT",&LT_Final);
     TMVAReader_->AddVariable("HT",&HT_Final);
     TMVAReader_->AddVariable("nBCleaned_TOTAL",&nBCleaned_TOTAL_Final);
     TMVAReader_->AddVariable("nTop_Total_Combined",&nTop_Total_Combined_Final);
     TMVAReader_->AddVariable("nJets30Clean",&nJets30Clean_Final);
     TMVAReader_->AddVariable("dPhi",&dPhi_Final);
     TMVAReader_->AddVariable("Alt$(DeepAK8Top_Loose_pt_Array[0],400)",&DeepAK8Top_Loose_pt_1_Final);
     TMVAReader_->AddVariable("Alt$(DeepAK8Top_Loose_pt_Array[1],400)",&DeepAK8Top_Loose_pt_2_Final);
     TMVAReader_->AddVariable("Alt$(BTag_pt_Cleaned[0],0)",&BTag_pt_1_Final);
     TMVAReader_->AddVariable("Alt$(BTag_pt_Cleaned[1],0)",&BTag_pt_2_Final);
     TMVAReader_->AddVariable("Alt$(DeepAK8Top_Loose_eta_Array[0],-2.4)",&DeepAK8Top_Loose_eta_1_Final);
     TMVAReader_->AddVariable("Alt$(DeepAK8Top_Loose_eta_Array[1],-2.4)",&DeepAK8Top_Loose_eta_2_Final);
     TMVAReader_->AddVariable("Alt$(BTag_eta_Cleaned[0],-2.4)",&BTag_eta_1_Final);
     TMVAReader_->AddVariable("Alt$(BTag_eta_Cleaned[1],-2.4)",&BTag_eta_2_Final);
     TMVAReader_->AddVariable("Alt$(DeepAK8Top_Loose_phi_Array[0],-3.2)",&DeepAK8Top_Loose_phi_1_Final);
     TMVAReader_->AddVariable("Alt$(DeepAK8Top_Loose_phi_Array[1],-3.2)",&DeepAK8Top_Loose_phi_2_Final);
     TMVAReader_->AddVariable("Alt$(BTag_phi_Cleaned[0],-3.2)",&BTag_phi_1_Final);
     TMVAReader_->AddVariable("Alt$(BTag_phi_Cleaned[1],-3.2)",&BTag_phi_2_Final);
     TMVAReader_->AddVariable("Resolved_Top_pt_Cleaned[0]",&HadTop_pt_Final);
     TMVAReader_->AddVariable("Resolved_Top_eta_Cleaned[0]",&HadTop_eta_Final);
     TMVAReader_->AddVariable("Resolved_Top_phi_Cleaned[0]",&HadTop_phi_Final);
     TMVAReader_->AddVariable("Resolved_Top_pt_Cleaned[1]",&HadTop_pt_2_Final);
     TMVAReader_->AddVariable("Resolved_Top_eta_Cleaned[1]",&HadTop_eta_2_Final);
     TMVAReader_->AddVariable("Resolved_Top_phi_Cleaned[1]",&HadTop_phi_2_Final);


     TMVAReader_->BookMVA("BDT",weight_file_name);
};



void BDT_limits_19_01_dPhi075_BTag2::clear(){
     
     _dM_Go_LSP = -99;
     _HT=-99;
     _LT=-99;
     _nBCleaned_TOTAL=-99;
     _nTop_Total_Combined=-99;
     _nJets30Clean=-99;
     _dPhi=-99;
     _DeepAK8Top_Loose_pt_1=-99;
     _DeepAK8Top_Loose_pt_2=-99;
     _BTag_pt_1=-99;
     _BTag_pt_2=-99;
     _DeepAK8Top_Loose_eta_1=-99;
     _DeepAK8Top_Loose_eta_2=-99;
     _BTag_eta_1=-99;
     _BTag_eta_2=-99;
     _DeepAK8Top_Loose_phi_1=-99;
     _DeepAK8Top_Loose_phi_2=-99;
     _BTag_phi_1=-99;
     _BTag_phi_2=-99;
     _HadTop_pt=-99;
     _HadTop_eta=-99;
     _HadTop_phi=-99;
     _HadTop_pt_2=-99;
     _HadTop_eta_2=-99;
     _HadTop_phi_2=-99;

     dM_Go_LSP_Final=-99;
     HT_Final=-99;
     LT_Final=-99;
     nBCleaned_TOTAL_Final=-99;
     nTop_Total_Combined_Final=-99;
     nJets30Clean_Final=-99;
     dPhi_Final=-99;
     DeepAK8Top_Loose_pt_1_Final=-99;
     DeepAK8Top_Loose_pt_2_Final=-99;
     BTag_pt_1_Final=-99;
     BTag_pt_2_Final=-99;
     DeepAK8Top_Loose_eta_1_Final=-99;
     DeepAK8Top_Loose_eta_2_Final=-99;
     BTag_eta_1_Final=-99;
     BTag_eta_2_Final=-99;
     DeepAK8Top_Loose_phi_1_Final=-99;
     DeepAK8Top_Loose_phi_2_Final=-99;
     BTag_phi_1_Final=-99;
     BTag_phi_2_Final=-99;
     HadTop_pt_Final=-99;
     HadTop_eta_Final=-99;
     HadTop_phi_Final=-99;
     HadTop_pt_2_Final=-99;
     HadTop_eta_2_Final=-99;
     HadTop_phi_2_Final=-99;


}


float BDT_limits_19_01_dPhi075_BTag2::EvalMVA(float dM_Go_LSP, float LT, float HT, float nBCleaned_TOTAL, float nTop_Total_Combined,  float nJets30Clean, float dPhi, float DeepAK8Top_Loose_pt_1, float DeepAK8Top_Loose_pt_2, float BTag_pt_1, float BTag_pt_2, float DeepAK8Top_Loose_eta_1, float DeepAK8Top_Loose_eta_2, float BTag_eta_1, float BTag_eta_2, float DeepAK8Top_Loose_phi_1, float DeepAK8Top_Loose_phi_2, float BTag_phi_1, float BTag_phi_2, float HadTop_pt, float HadTop_eta, float HadTop_phi, float HadTop_pt_2, float HadTop_eta_2, float HadTop_phi_2){
   
       float score=-99;

       //cout<<"LT: "<<_LT<<endl;
       //cout<<"HT: "<<_HT<<endl;
       //cout<<endl;
       _dM_Go_LSP = dM_Go_LSP; 
       _LT = LT;
       _HT = HT;
       _nBCleaned_TOTAL = nBCleaned_TOTAL;
       _nTop_Total_Combined = nTop_Total_Combined;
       _nJets30Clean = nJets30Clean;
       _dPhi = dPhi;
       _DeepAK8Top_Loose_pt_1 = DeepAK8Top_Loose_pt_1;
       _DeepAK8Top_Loose_pt_2 = DeepAK8Top_Loose_pt_2;
       _BTag_pt_1 = BTag_pt_1;
       _BTag_pt_2 = BTag_pt_2;
       _DeepAK8Top_Loose_eta_1 = DeepAK8Top_Loose_eta_1;
       _DeepAK8Top_Loose_eta_2 = DeepAK8Top_Loose_eta_2;
       _BTag_eta_1 = BTag_eta_1;
       _BTag_eta_2 = BTag_eta_2;
       _DeepAK8Top_Loose_phi_1 = DeepAK8Top_Loose_phi_1;
       _DeepAK8Top_Loose_phi_2 = DeepAK8Top_Loose_phi_2;
       _BTag_phi_1 = BTag_phi_1;
       _BTag_phi_2 = BTag_phi_2;
       _HadTop_pt = HadTop_pt;
       _HadTop_eta = HadTop_eta;
       _HadTop_phi = HadTop_phi;
       _HadTop_pt_2 = HadTop_pt_2;
       _HadTop_eta_2 = HadTop_eta_2;
       _HadTop_phi_2 = HadTop_phi_2;
  
       //cout<<"HT: "<<_HT<<endl;

 
       score = EvalScore(_dM_Go_LSP,_LT, _HT, _nBCleaned_TOTAL,_nTop_Total_Combined, _nJets30Clean, _dPhi, _DeepAK8Top_Loose_pt_1, _DeepAK8Top_Loose_pt_2, _BTag_pt_1, _BTag_pt_2, _DeepAK8Top_Loose_eta_1, _DeepAK8Top_Loose_eta_2, _BTag_eta_1, _BTag_eta_2, _DeepAK8Top_Loose_phi_1, _DeepAK8Top_Loose_phi_2, _BTag_phi_1, _BTag_phi_2, _HadTop_pt, _HadTop_eta, _HadTop_phi, _HadTop_pt_2, _HadTop_eta_2, _HadTop_phi_2);

       return score;

};

float BDT_limits_19_01_dPhi075_BTag2::EvalScore(float _dM_Go_LSP, float _LT, float _HT, float _nBCleaned_TOTAL, float _nTop_Total_Combined, float _nJets30Clean, float _dPhi, float _DeepAK8Top_Loose_pt_1, float _DeepAK8Top_Loose_pt_2, float _BTag_pt_1, float _BTag_pt_2, float _DeepAK8Top_Loose_eta_1, float _DeepAK8Top_Loose_eta_2, float _BTag_eta_1, float _BTag_eta_2, float _DeepAK8Top_Loose_phi_1, float _DeepAK8Top_Loose_phi_2, float _BTag_phi_1, float _BTag_phi_2, float _HadTop_pt, float _HadTop_eta, float _HadTop_phi, float _HadTop_pt_2, float _HadTop_eta_2, float _HadTop_phi_2){

    dM_Go_LSP_Final = _dM_Go_LSP; 
    LT_Final = _LT;
    HT_Final = _HT;
    nBCleaned_TOTAL_Final = _nBCleaned_TOTAL;
    nTop_Total_Combined_Final = _nTop_Total_Combined;
    nJets30Clean_Final = _nJets30Clean;
    dPhi_Final = _dPhi;
    DeepAK8Top_Loose_pt_1_Final = _DeepAK8Top_Loose_pt_1;
    DeepAK8Top_Loose_pt_2_Final = _DeepAK8Top_Loose_pt_2;
    BTag_pt_1_Final = _BTag_pt_1;
    BTag_pt_2_Final = _BTag_pt_2;
    DeepAK8Top_Loose_eta_1_Final = _DeepAK8Top_Loose_eta_1;
    DeepAK8Top_Loose_eta_2_Final = _DeepAK8Top_Loose_eta_2;
    BTag_eta_1_Final = _BTag_eta_1;
    BTag_eta_2_Final = _BTag_eta_2;
    DeepAK8Top_Loose_phi_1_Final = _DeepAK8Top_Loose_phi_1;
    DeepAK8Top_Loose_phi_2_Final = _DeepAK8Top_Loose_phi_2;
    BTag_phi_1_Final = _BTag_phi_1;
    BTag_phi_2_Final = _BTag_phi_2;
    HadTop_pt_Final = _HadTop_pt;
    HadTop_eta_Final = _HadTop_eta;
    HadTop_phi_Final = _HadTop_phi;
    HadTop_pt_2_Final = _HadTop_pt_2;
    HadTop_eta_2_Final = _HadTop_eta_2;
    HadTop_phi_2_Final = _HadTop_phi_2;

    //cout<<"BTag_eta_1_Final: "<<BTag_eta_1_Final<<endl;
    //cout<<"BTag_eta_2_Final: "<<BTag_eta_2_Final<<endl<<endl;


    return TMVAReader_->EvaluateMVA("BDT");

};


