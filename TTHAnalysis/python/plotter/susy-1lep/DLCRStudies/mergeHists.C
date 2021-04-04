#include "TH1.h"
#include "TH2.h"
#include "TF1.h"
#include "TStyle.h"
#include "TCanvas.h"
#include "TGraph.h"
#include "TLine.h"
#include "TPolyLine.h"
#include "TGraphErrors.h"
#include "TROOT.h"
#include "TApplication.h"
#include "TString.h"
#include "TProfile.h"
#include "TMath.h"
#include "Riostream.h"
#include <iostream>
#include <iomanip>
#include <stdlib.h>
#include <stdio.h>
#include <vector>
#include <sstream>
#include <string>
#include <TString.h>
#include "time.h"
#include <ctime>
#include <cstdlib>
#include "TLegend.h"
#include "TTree.h"
#include "TFile.h"
#include "TCut.h"
#include "TString.h"
#include "TLatex.h"
#include <cstring>
#include <math.h>

void mergeHists(){

    TFile *f2016 = TFile::Open("/nfs/dust/cms/user/pakontax/CMSSW/Full_Run_II_Analysis_FINAL_FINAL_FINAL_17July2020/CMSSW_10_4_0/src/CMGTools/TTHAnalysis/python/plotter/susy-1lep/DLCRStudies/Output/2016/2L_ForDL_plots.root");
    TFile *f2017 = TFile::Open("/nfs/dust/cms/user/pakontax/CMSSW/Full_Run_II_Analysis_FINAL_FINAL_FINAL_17July2020/CMSSW_10_4_0/src/CMGTools/TTHAnalysis/python/plotter/susy-1lep/DLCRStudies/Output/2017/2L_ForDL_plots.root");
    TFile *f2018 = TFile::Open("/nfs/dust/cms/user/pakontax/CMSSW/Full_Run_II_Analysis_FINAL_FINAL_FINAL_17July2020/CMSSW_10_4_0/src/CMGTools/TTHAnalysis/python/plotter/susy-1lep/DLCRStudies/Output/2018/2L_ForDL_plots.root");


    vector<TString> bkg_list={"background","TTsemiLep","TTdiLep","TTV","SingleT","WJets","VV","DY","QCD","data"};
    
    vector<TString> LT_list={"LTInc","LT12","LT3","LT4i"};

    const int dir_check=system("stat ./MergedPlots_ROOTFile");

    if(dir_check==256){
                const int dir_create = system("mkdir -p ./MergedPlots_ROOTFile");
    }

    TFile f_merged("./MergedPlots_ROOTFile/merged_histos_2L.root","new");

    for(unsigned iLT=0; iLT<LT_list.size();++iLT){

    for(unsigned iBkg=0;iBkg<bkg_list.size();++iBkg){

        TH1D *hist_2016;
        TH1D *hist_2017;
        TH1D *hist_2018;
    
        hist_2016 = (TH1D*)f2016->Get("nJ_DL"+LT_list[iLT]+"_"+bkg_list[iBkg]);
        hist_2017 = (TH1D*)f2017->Get("nJ_DL"+LT_list[iLT]+"_"+bkg_list[iBkg]);
        hist_2018 = (TH1D*)f2018->Get("nJ_DL"+LT_list[iLT]+"_"+bkg_list[iBkg]);

        TH1D *hist_merged;
        hist_merged = (TH1D*)hist_2016->Clone();
        hist_merged -> Sumw2();
        hist_merged->Add(hist_2017);
        hist_merged->Add(hist_2018);

        hist_merged->Write();    

        /* 
        float yields_OLD=0;
        yields_OLD = hist_OLD->Integral();
        string yields_OLD_str=to_string(yields_OLD);

        float yields_NEW=0;
        yields_NEW = hist_NEW->Integral();
        string yields_NEW_str=to_string(yields_NEW);
 

        hist_NEW->SetStats(0);
        hist_NEW->SetTitle("");
        hist_NEW->SetFillStyle(0);
        hist_NEW->SetLineWidth(3);
        hist_NEW->SetLineColor(2);

        hist_OLD->SetStats(0);
        hist_OLD->SetTitle("");
        hist_OLD->SetFillStyle(0);
        hist_OLD->SetLineWidth(3);
        hist_OLD->SetLineColor(1);

        hist_NEW->Scale(1/hist_NEW->Integral());
        hist_OLD->Scale(1/hist_OLD->Integral());

        TString canvas_name = "c_"+to_string(iLT)+"_"+to_string(iBkg);
        TCanvas *ci= new TCanvas(canvas_name,canvas_name,800,800);

        hist_OLD->Draw("hist sames");
        hist_NEW->Draw("hist sames"); 
 
        TLegend *leg= new TLegend(0.6,0.5,0.9,0.9);
        leg->SetHeader("#splitline{"+bkg_list[iBkg]+"}{Antiselected |"+LT_list[iLT]+"}");
        leg->AddEntry(hist_OLD,"Previous e CBID","l");
        leg->AddEntry(hist_NEW,"New e CBID","l");
        leg->Draw();
 
        TLatex y_fakes;
        string longstring= "Yields_Previous: "+yields_OLD_str; 
        const char *longstring2 = longstring.c_str();
        y_fakes.SetTextSize(0.05);
        y_fakes.SetTextFont(41); 
        y_fakes.DrawLatexNDC(0.2,0.96,longstring2); 

        TLatex y_non_fakes;
        string longstring_non= "Yields_NEW: "+yields_NEW_str;
        const char *longstring2_non = longstring_non.c_str();
        y_non_fakes.SetTextSize(0.05);
        y_non_fakes.SetTextFont(42);
        y_non_fakes.DrawLatexNDC(0.2,0.91,longstring2_non);

        //ci->SaveAs("Plots_Antiselected_"+LT_list[iLT]+"/electronCBID_comparison_"+LT_list[iLT]+"_"+bkg_list[iBkg]+".png","png");  
        ci->SaveAs("Plots_Antiselected_"+LT_list[iLT]+"/electronCBID_comparison_"+LT_list[iLT]+"_"+bkg_list[iBkg]+".pdf","pdf"); 
        */
    }
    }
    f_merged.Close();
  
}
