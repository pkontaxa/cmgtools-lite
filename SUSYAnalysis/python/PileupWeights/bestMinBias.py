#!/usr/bin/env python
import ROOT
import subprocess
import os

f = ROOT.TFile.Open("metRespBCDdata_NVtxDistribution.root")
nvtx_ntrue = f.Get('DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/nvtx_nTruePU')
data_nvtx  = f.Get('DoubleMuon/nvtx')

# For 80X:
# https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/SimGeneral/MixingModule/python/mix_2016_25ns_SpringMC_PUScenarioV1_PoissonOOTPU_cfi.py
nTruePU = [0.000829312873542, 0.00124276120498, 0.00339329181587, 0.00408224735376, 0.00383036590008, 0.00659159288946, 0.00816022734493, 0.00943640833116, 0.0137777376066, 0.017059392038, 0.0213193035468, 0.0247343174676, 0.0280848773878, 0.0323308476564, 0.0370394341409, 0.0456917721191, 0.0558762890594, 0.0576956187107, 0.0625325287017, 0.0591603758776, 0.0656650815128, 0.0678329011676, 0.0625142146389, 0.0548068448797, 0.0503893295063, 0.040209818868, 0.0374446988111, 0.0299661572042, 0.0272024759921, 0.0219328403791, 0.0179586571619, 0.0142926728247, 0.00839941654725, 0.00522366397213, 0.00224457976761, 0.000779274977993, 0.000197066585944, 7.16031761328e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] 
nPu = 50
nTrue = ROOT.TH1D("pileup", "MC Pileup", nPu, 0, nPu)
for i in range(nPu) :
   nTrue.SetBinContent(i+1, nTruePU[i])

def getNtrueReweight(xs):
    fn = 'temp%d.root' % xs
    if not os.path.exists(fn):
        cmd = "pileupCalc.py -i 2016BCD.json --inputLumiJSON /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/PileUp/pileup_latest.txt --calcMode true --minBiasXsec {xsec} --maxPileupBin {bins} --numPileupBins {bins} temp{xsec}.root".format(bins=nPu, xsec=xs)
        subprocess.call(cmd.split())
    ftmp = ROOT.TFile.Open(fn)
    data = ftmp.Get("pileup")
    data.Scale(1./data.Integral())
    data.Divide(nTrue)
    data.SetName("dataPUminBias%d" % xs)
    data.SetDirectory(0)
    return data

def doReweight(xs):
    mc_nvtx = ROOT.TH1D("mcNvtx", "MC nvtx", 70, 0, 70)
    reweight = getNtrueReweight(xs)
    for i in range(nPu):
        for j in range(70):
            x = nvtx_ntrue.GetBinContent(1+j, 1+i) * reweight.GetBinContent(1+i)
            mc_nvtx.Fill(j, x)
    print "Reweighting xs = %d ub" % xs
    print "Data int = ", data_nvtx.Integral()
    print "MC   int = ", mc_nvtx.Integral()
    mc_nvtx.Scale(data_nvtx.Integral()/mc_nvtx.Integral())
    chi2 = 0.
    for i in range(70):
        di = data_nvtx.GetBinContent(1+i)
        mi = mc_nvtx.GetBinContent(1+i)
        chi2 += (di-mi)**2 / max(di, mi)
    print "Chi2 = ", chi2
    return chi2

toCheck = [
    69200,
    71300,
]
for i in range(60000, 73000, 1000):
    toCheck.append(i)

hchi2 = ROOT.TGraph(len(toCheck))
hchi2.SetNameTitle("chi2", "chi2;minBias #sigma [mb];nvtx #chi^{2}")
for i, xs in enumerate(toCheck):
    chi2 = doReweight(xs)
    hchi2.SetPoint(i, xs/1000., chi2)
hchi2.Draw("ap")
res = hchi2.Fit("pol2", "S")
res = res.Get()
best = -res.Parameter(1)/res.Parameter(2)/2.
print "Best fit minBias xs = %f mb" % best
ROOT.gPad.Print("minBiasScan.root")
ROOT.gPad.Print("minBiasScan.pdf")
