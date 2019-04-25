# COMPONENT CREATOR
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

# ----------------------------- 2018 pp run  ----------------------------------------
dataDir = "$CMSSW_BASE/src/CMGTools/TTHAnalysis/data"  # use environmental variable, useful for instance to run on CRAB
json=dataDir+'/json/Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt'

#json = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions17/13TeV/Final/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt'

run_range = (315252, 325175)
label = "_runs%s_%s" % (run_range[0], run_range[1])

# ----------------------------- Run2018A 17Sep2018 ----------------------------------------

JetHT_Run2018A_17Sep2018 = kreator.makeDataComponent("JetHT_Run2018A_17Sep2018", "/JetHT/Run2018A-17Sep2018-v1/MINIAOD", "CMS", ".*root", json)
MET_Run2018A_17Sep2018 = kreator.makeDataComponent("MET_Run2018A_17Sep2018", "/MET/Run2018A-17Sep2018-v1/MINIAOD", "CMS", ".*root", json)
SingleElectron_Run2018A_17Sep2018 = kreator.makeDataComponent("SingleElectron_Run2018A_17Sep2018", "/EGamma/Run2018A-17Sep2018-v2/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2018A_17Sep2018 = kreator.makeDataComponent("SingleMuon_Run2018A_17Sep2018", "/SingleMuon/Run2018A-17Sep2018-v2/MINIAOD", "CMS", ".*root", json)

dataSamples_Run2018A_17Sep2018 = [MET_Run2018A_17Sep2018, SingleElectron_Run2018A_17Sep2018, SingleMuon_Run2018A_17Sep2018,JetHT_Run2018A_17Sep2018]
dataSamples_Run2018A_17Sep2018_1l = [MET_Run2018A_17Sep2018, SingleElectron_Run2018A_17Sep2018, SingleMuon_Run2018A_17Sep2018]

# ----------------------------- Run2018B 17Sep2018 ----------------------------------------

JetHT_Run2018B_17Sep2018 = kreator.makeDataComponent("JetHT_Run2018B_17Sep2018", "/JetHT/Run2018B-17Sep2018-v1/MINIAOD", "CMS", ".*root", json)
MET_Run2018B_17Sep2018 = kreator.makeDataComponent("MET_Run2018B_17Sep2018", "/MET/Run2018B-17Sep2018-v1/MINIAOD", "CMS", ".*root", json)
SingleElectron_Run2018B_17Sep2018 = kreator.makeDataComponent("SingleElectron_Run2018B_17Sep2018", "/EGamma/Run2018B-17Sep2018-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2018B_17Sep2018 = kreator.makeDataComponent("SingleMuon_Run2018B_17Sep2018", "/SingleMuon/Run2018B-17Sep2018-v1/MINIAOD", "CMS", ".*root", json)


dataSamples_Run2018B_17Sep2018 = [JetHT_Run2018B_17Sep2018, MET_Run2018B_17Sep2018, SingleElectron_Run2018B_17Sep2018, SingleMuon_Run2018B_17Sep2018]
dataSamples_Run2018B_17Sep2018_1l = [MET_Run2018B_17Sep2018, SingleElectron_Run2018B_17Sep2018, SingleMuon_Run2018B_17Sep2018]


# ----------------------------- Run2018C 17Sep2018----------------------------------------

JetHT_Run2018C_17Sep2018 = kreator.makeDataComponent("JetHT_Run2018C_17Sep2018", "/JetHT/Run2018C-17Sep2018-v1/MINIAOD", "CMS", ".*root", json)
MET_Run2018C_17Sep2018 = kreator.makeDataComponent("MET_Run2018C_17Sep2018", "/MET/Run2018C-17Sep2018-v1/MINIAOD", "CMS", ".*root", json)
SingleElectron_Run2018C_17Sep2018 = kreator.makeDataComponent("SingleElectron_Run2018C_17Sep2018", "/EGamma/Run2018C-17Sep2018-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2018C_17Sep2018 = kreator.makeDataComponent("SingleMuon_Run2018C_17Sep2018", "/SingleMuon/Run2018C-17Sep2018-v1/MINIAOD", "CMS", ".*root", json)


dataSamples_Run2018C_17Sep2018 = [JetHT_Run2018C_17Sep2018, MET_Run2018C_17Sep2018, SingleElectron_Run2018C_17Sep2018, SingleMuon_Run2018C_17Sep2018]
dataSamples_Run2018C_17Sep2018_1l = [MET_Run2018C_17Sep2018, SingleElectron_Run2018C_17Sep2018, SingleMuon_Run2018C_17Sep2018]

# -----------------------------  Run2018D 17Sep2018 ----------------------------------------

JetHT_Run2018D_17Sep2018 = kreator.makeDataComponent("JetHT_Run2018D_17Sep2018", "/JetHT/Run2018D-PromptReco-v2/MINIAOD", "CMS", ".*root", json)
MET_Run2018D_17Sep2018 = kreator.makeDataComponent("MET_Run2018D_17Sep2018", "/MET/Run2018D-PromptReco-v2/MINIAOD", "CMS", ".*root", json)
SingleElectron_Run2018D_17Sep2018 = kreator.makeDataComponent("SingleElectron_Run2018D_17Sep2018", "/EGamma/Run2018D-PromptReco-v2/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2018D_17Sep2018 = kreator.makeDataComponent("SingleMuon_Run2018D_17Sep2018", "/SingleMuon/Run2018D-PromptReco-v2/MINIAOD", "CMS", ".*root", json)

dataSamples_Run2018D_17Sep2018 = [JetHT_Run2018D_17Sep2018, MET_Run2018D_17Sep2018, SingleElectron_Run2018D_17Sep2018, SingleMuon_Run2018D_17Sep2018]
dataSamples_Run2018D_17Sep2018_1l = [MET_Run2018D_17Sep2018, SingleElectron_Run2018D_17Sep2018, SingleMuon_Run2018D_17Sep2018]

# Summary of 17Sep2018
dataSamples_17Sep2018 = dataSamples_Run2018B_17Sep2018 + dataSamples_Run2018C_17Sep2018 + dataSamples_Run2018D_17Sep2018 + dataSamples_Run2018A_17Sep2018
dataSamples_17Sep2018_1l = dataSamples_Run2018B_17Sep2018_1l + dataSamples_Run2018C_17Sep2018_1l + dataSamples_Run2018D_17Sep2018_1l + dataSamples_Run2018A_17Sep2018_1l

dataSamples = dataSamples_17Sep2018
dataSamples_1l = dataSamples_17Sep2018_1l

samples = dataSamples

# ---------------------------------------------------------------------

if __name__ == "__main__":
    from CMGTools.RootTools.samples.tools import runMain
    runMain(samples)
