#!/usr/bin/env python

import sys, glob, os
from ROOT import *

# Get lepton SF histograms

# Electrons
# Full-Sim to data
f1_full_ele = TFile.Open('ElectronScaleFactors_Run2018.root', 'read')

h1_full_ele = f1_full_ele.Get('Run2018_CutBasedTightNoIso94XV2')
h2_full_ele = f1_full_ele.Get('Run2018_Mini')

h12_full_ele = h1_full_ele.Clone()
h12_full_ele.Multiply(h2_full_ele)
h12_full_ele.SetName('El_CBtight_miniIso0p1_Moriond')
h12_full_ele.SetTitle('El_CBtight_miniIso0p1_Moriond')
h12_full_ele.SaveAs('El_CBtight_miniIso0p1_Moriond.root')

# Fast-Sim to Full-Sim
f1_fast_ele = TFile.Open('detailed_ele_full_fast_sf_18.root', 'read')
f2_fast_ele = TFile.Open('detailed_ele_full_fast_sf_18.root', 'read')

h1_fast_ele = f1_fast_ele.Get('MVAVLooseTightIP2DMini_sf')
h2_fast_ele = f2_fast_ele.Get('CutBasedTightNoIso94XV2_sf')

h12_fast_ele = h1_fast_ele.Clone()
h12_fast_ele.Multiply(h2_fast_ele)

h12_fast_ele.SetName('CBtight_miniIso0p1_FastSim_Moriond')
h12_fast_ele.SetTitle('CBtight_miniIso0p1_FastSim_Moriond')
h12_fast_ele.SaveAs('CBtight_miniIso0p1_FastSim_Moriond.root')

# Muons
f1_full_mu = TFile.Open('RunBCDEF_SF_ID.root', 'read')
f2_full_mu = TFile.Open('detailed_mu_full_fast_sf_18.root', 'read')
#f3_full_mu = TFile.Open('TnP_NUM_TightIP3D_DENOM_MediumID_VAR_map_pt_eta.root', 'read')

h1_full_mu = f1_full_mu.Get('NUM_MediumID_DEN_genTracks_pt_abseta')
h2_full_mu = f2_full_mu.Get('miniIso02_MediumId_sf')
#h3_full_mu = f3_full_mu.Get('SF')

h123_full_mu = h1_full_mu.Clone()
h123_full_mu.Multiply(h2_full_mu)
#h123_full_mu.Multiply(h3_full_mu)
h123_full_mu.SetName("Mu_Medium_miniIso0p2_SIP3D_Moriond")
h123_full_mu.SetTitle("Mu_Medium_miniIso0p2_SIP3D_Moriond")
h123_full_mu.SaveAs("Mu_Medium_miniIso0p2_SIP3D_Moriond.root")

# Fast-Sim to Full-Sim
f1_fast_mu = TFile.Open('detailed_mu_full_fast_sf_18.root', 'read')
f2_fast_mu = TFile.Open('detailed_mu_full_fast_sf_18.root', 'read')
#f3_fast_mu = TFile.Open('sf_mu_mediumID_tightIP3D.root', 'read')

h1_fast_mu = f1_fast_mu.Get('miniIso02_MediumId_sf')
h2_fast_mu = f2_fast_mu.Get('miniIso04_MediumId_sf')
#h3_fast_mu = f3_fast_mu.Get('histo2D')

h123_fast_mu = h1_fast_mu.Clone()
h123_fast_mu.Multiply(h2_fast_mu)
#h123_fast_mu.Multiply(h3_fast_mu)
h123_fast_mu.SetName("MediumMuon_miniIso0p2_SIP3D_FastSim_Moriond")
h123_fast_mu.SetTitle("MediumMuon_miniIso0p2_SIP3D_FastSim_Moriond")
h123_fast_mu.SaveAs("MediumMuon_miniIso0p2_SIP3D_FastSim_Moriond.root")
