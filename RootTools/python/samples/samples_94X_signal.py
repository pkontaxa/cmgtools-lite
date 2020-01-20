import PhysicsTools.HeppyCore.framework.config as cfg
import os

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

### SUSY2016B
SMS_T1tttt_TuneCUETP8M1 = kreator.makeMCComponent("SMS_T1tttt_TuneCUETP8M1"	,"/SMS-T1tttt_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUSummer16v3Fast_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM","CMS",".*root")
SMS_T1tttt_TuneCP2      = kreator.makeMCComponent("SMS_T1tttt_TuneCP2"      ,"/SMS-T1tttt_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PUFall17Fast_pilot_94X_mc2017_realistic_v15-v3/MINIAODSIM","CMS",".*root")
SMS_T1tttt_TuneCP2_102  = kreator.makeMCComponent("SMS_T1tttt_TuneCP2"      ,"/SMS-T1tttt_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-PUFall18Fast_102X_upgrade2018_realistic_v15-v2/MINIAODSIM","CMS",".*root")
mcSamplesT1tttt = [SMS_T1tttt_TuneCUETP8M1,SMS_T1tttt_TuneCP2,SMS_T1tttt_TuneCP2_102]
mcSamplesT1tttt16 = [SMS_T1tttt_TuneCUETP8M1]
mcSamplesT1tttt17 = [SMS_T1tttt_TuneCP2]

SMS_T5qqqqVV_TuneCUETP8M1 = kreator.makeMCComponent("SMS_T5qqqqVV_TuneCUETP8M1","/SMS-T5qqqqVV_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUSummer16v3Fast_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM","CMS",".*root")
SMS_T5qqqqVV_TuneCP2 = kreator.makeMCComponent("SMS_T5qqqqVV_TuneCP2","/SMS-T5qqqqVV_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PUFall17Fast_94X_mc2017_realistic_v15-v1/MINIAODSIM","CMS",".*root")
SMS_T5qqqqVV_TuneCP2_ext = kreator.makeMCComponent("SMS_T5qqqqVV_TuneCP2_ext","/SMS-T5qqqqVV_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PUFall17Fast_94X_mc2017_realistic_v15_ext1-v1/MINIAODSIM","CMS",".*root")
SMS_T5qqqqVV_TuneCP2_102 = kreator.makeMCComponent("SMS_T5qqqqVV_TuneCP2","/SMS-T5qqqqVV_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-PUFall18Fast_102X_upgrade2018_realistic_v15-v2/MINIAODSIM","CMS",".*root")

mcSamplesT5qqqqVV = [SMS_T5qqqqVV_TuneCUETP8M1,SMS_T5qqqqVV_TuneCP2,SMS_T5qqqqVV_TuneCP2_ext,SMS_T5qqqqVV_TuneCP2_102]

SMS_T1ttttCP5_MVA = kreator.makeMCComponentFromLocal("SMS_T1ttttCP5_MVA","LOCAL","/pnfs/desy.de/cms/tier2/store/user/amohamed/SMS-T1tttt_1512-1611-1712-1813_MiniAOD/T1tttt_1512-1611-1712-1813_AOD/SMS-T1tttt_1512-1611-1712-1813_MiniAOD/190916_214932/",".*root")
SMS_T5qqqqCP5_MVA = kreator.makeMCComponentFromLocal("SMS_T5qqqqCP5_MVA","LOCAL","/pnfs/desy.de/cms/tier2/store/user/amohamed/T5qqqqWW_MVA_MiniAOD/T5qqqqWW_MVA_AOD/T5qqqqWW_MVA_MiniAOD/200120_100458/",".*root")
#SMS_T5qqqqVV_0p4 = kreator.makeMCComponentFromLocal("SMS_T5qqqqVV_0p4","LOCAL","/pnfs/desy.de/cms/tier2/store/user/amohamed/T5qqqqWW_19_22_0p4_MiniAOD/T5qqqqWW_19_22_0p4_AOD/T5qqqqWW_19_22_0p4_MiniAOD/191018_131144/",".*root")
#SMS_T5qqqqVV_0p5 = kreator.makeMCComponentFromLocal("SMS_T5qqqqVV_0p5","LOCAL","/pnfs/desy.de/cms/tier2/store/user/amohamed/T5qqqqWW_19_22_0p5_MiniAOD/T5qqqqWW_19_22_0p5_AOD/T5qqqqWW_19_22_0p5_MiniAOD/191018_131214/",".*root")
#SMS_T5qqqqVV_0p6 = kreator.makeMCComponentFromLocal("SMS_T5qqqqVV_0p6","LOCAL","/pnfs/desy.de/cms/tier2/store/user/amohamed/T5qqqqWW_19_22_0p6_MiniAOD/T5qqqqWW_19_22_0p6_AOD/T5qqqqWW_19_22_0p6_MiniAOD/191018_131239/",".*root")

#SMS_T5qqqqVV_paper = [SMS_T5qqqqVV_0p4 , SMS_T5qqqqVV_0p5 , SMS_T5qqqqVV_0p6]

mcSamples = mcSamplesT1tttt + mcSamplesT5qqqqVV

samples = mcSamples

dataSamples = []

### ---------------------------------------------------------------------

from CMGTools.TTHAnalysis.setup.Efficiencies import *
dataDir = "$CMSSW_BASE/src/CMGTools/TTHAnalysis/data"

#Define splitting
for comp in mcSamples:
    comp.isMC = True
    comp.isData = False
    comp.splitFactor = 250 #  if comp.name in [ "WJets", "DY3JetsM50", "DY4JetsM50","W1Jets","W2Jets","W3Jets","W4Jets","TTJetsHad" ] else 100
    comp.puFileMC=dataDir+"/puProfile_Summer12_53X.root"
    comp.puFileData=dataDir+"/puProfile_Data12.root"
    comp.efficiency = eff2012

for comp in dataSamples:
    comp.splitFactor = 1000
    comp.isMC = False
    comp.isData = True

if __name__ == "__main__":
   import sys
   if "test" in sys.argv:
       from CMGTools.RootTools.samples.ComponentCreator import testSamples
       testSamples(samples)
