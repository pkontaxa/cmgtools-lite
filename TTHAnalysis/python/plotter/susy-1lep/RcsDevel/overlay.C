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


void overlay(){


      TFile *f2=TFile::Open("datacards_BaseLine_Cards/limit_scan.root");
      Gr_Exp_NTOP0 =(TGraph*)f2->Get("T1ttttExpectedLimit");
      Xsec_hist=(TH2D*)f2->Get("T1ttttObservedExcludedXsec");

      Gr_Exp_NTOP0->GetHistogram()->GetXaxis()->SetTitle("m_{#tilde g} [GeV]");
      Gr_Exp_NTOP0->GetHistogram()->GetYaxis()->SetTitle("m_{#{chi}_{1}^{0}}");
      Gr_Exp_NTOP0->GetHistogram()->GetYaxis()->SetTitleOffset(1.5);


      TFile *f3=TFile::Open("datacards_BaseLine_BDTCu_Cards/limit_scan.root");
      Gr_Exp_NTOP1 =(TGraph*)f3->Get("T1ttttExpectedLimit");

 
      Gr_Exp_NTOP1->GetHistogram()->GetXaxis()->SetTitle("m_{g} [GeV]");
      Gr_Exp_NTOP1->GetHistogram()->GetYaxis()->SetTitle("m_{#{chi}_{1}^{0}}");
      Gr_Exp_NTOP1->GetHistogram()->GetYaxis()->SetTitleOffset(1.5);


      Gr_Exp_NTOP1->SetLineColor(37);

      TFile *f4=TFile::Open("datacards_NJ_BinnedOnly_BDTCut_Cards/limit_scan.root");
      Gr_Exp_NTOP1_v2 =(TGraph*)f4->Get("T1ttttExpectedLimit");
      Gr_Exp_NTOP1_v2->SetLineColor(8);


      TFile *f5=TFile::Open("datacards_BDT_onlyonebin_Cards/limit_scan.root");
      Gr_Exp_NTOP1_v3 =(TGraph*)f5->Get("T1ttttExpectedLimit");
      Gr_Exp_NTOP1_v3->SetLineColor(28);
      
      
      
      TFile *f6=TFile::Open("datacards_BaseLine_BDTCut_Full_Cards/limit_scan.root");
      Gr_Exp_NTOP1_v4 =(TGraph*)f6->Get("T1ttttExpectedLimit");
      Gr_Exp_NTOP1_v4->SetLineColor(40);

      TFile *f7=TFile::Open("datacards_BDT_newBins_Cards/limit_scan.root");
      Gr_Exp_NTOP1_v5 =(TGraph*)f7->Get("T1ttttExpectedLimit");
      Gr_Exp_NTOP1_v5->SetLineColor(44);

      TFile *f8=TFile::Open("datacards_BDT_newBins_2_Cards/limit_scan.root");
      Gr_Exp_NTOP1_v6 =(TGraph*)f8->Get("T1ttttExpectedLimit");
      Gr_Exp_NTOP1_v6->SetLineColor(50);


      TCanvas *c11=new TCanvas("c11","c11",10,10,1000,900);

  

      TMultiGraph *mg= new TMultiGraph();



      mg->Add(Gr_Exp_NTOP0,"l");
      //mg->Add(Gr_Exp_NTOP1,"l");     
      mg->Add(Gr_Exp_NTOP1,"l");
      mg->Add(Gr_Exp_NTOP1_v2,"l");
      mg->Add(Gr_Exp_NTOP1_v3,"l");
      mg->Add(Gr_Exp_NTOP1_v4,"l");
      mg->Add(Gr_Exp_NTOP1_v5,"l");
      mg->Add(Gr_Exp_NTOP1_v6,"l");

  


      mg->SetTitle("; m_{#tildeg} [GeV]; m_{#tilde#chi_{1}^{0}} [GeV]");
      //mg->GetYaxis()->SetTitleOffset(1.5);    

//      Xsec_hist->Draw("colz sames");
//      c11->Update();
      mg->Draw("ap sames");

///////      mg->GetXaxis()->SetRangeUser(1000,2500);
      //mg->GetXaxis()->SetLimits(1000,2000);
      //mg->GetYaxis()->SetRangeUser(0,1270);
      //mg->Draw("ap sames");

      c11->Update();

 
      leg = new TLegend(0.15,0.25,0.55,0.4);
      leg->SetHeader("T1tttt NLO+NLL exclusion"); 
      leg->AddEntry(Gr_Exp_NTOP0,"Baseline","l");
      leg->AddEntry(Gr_Exp_NTOP1,"Baseline + BDT(-0.17) ","l");
      leg->AddEntry(Gr_Exp_NTOP1_v2,"Baseline + BDT(-0.17) NJ binned","l");
      leg->AddEntry(Gr_Exp_NTOP1_v3,"Baseline + BDT(-0.17) one Bin","l");
      leg->AddEntry(Gr_Exp_NTOP1_v4,"Baseline + FS BDT(-0.07)","l");
      leg->AddEntry(Gr_Exp_NTOP1_v5,"Baseline + FS BDT(-0.07) no Dphi","l");
      leg->AddEntry(Gr_Exp_NTOP1_v6,"Baseline + FS variavle BDT no Dphi","l");


       
      leg->Draw();
      c11->SaveAs("Limit_Plot.pdf");
 
}
