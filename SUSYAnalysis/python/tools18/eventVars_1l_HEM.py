import ROOT
import time
import itertools
import PhysicsTools.Heppy.loadlibs
import array
import operator

from CMGTools.TTHAnalysis.treeReAnalyzer import *
from ROOT import TLorentzVector, TVector2, std

from math import sqrt, pi, acos, cos


class EventVars1L_HEM:
    def __init__(self):

        self.branches = [
            "nHEMJetVeto","nHEMEleVeto","etaHEMJetVeto","etaHEMEleVeto","phiHEMJetVeto","phiHEMEleVeto","ptHEMJetVeto","ptHEMEleVeto","HEM_MC_SF"
            ]

    def listBranches(self):
        return self.branches[:]

    def __call__(self,event,keyvals):

        # prepare output
        #ret = dict([(name,-999.0) for name in self.branches])
        ret = {}
        for name in self.branches:
            if type(name) == 'tuple':
                ret[name] = []
            elif type(name) == 'str':
                ret[name] = -999
        leps = [l for l in Collection(event,"LepGood","nLepGood")]
        otherleps = [l for l in Collection(event,"LepOther","nLepOther")]
    
        jets = [j for j in Collection(event,"Jet","nJet")]
        HEMEleVeto = []
        HEMJetVeto = []
        if ((not event.isData) or (event.isData and event.run >= 319077)): 
            for idx,lep in enumerate(leps) : 
                if abs(lep.pdgId) == 11 and lep.pt > 30 and  lep.eta > -3.0  and  lep.eta < -1.4 and lep.phi > -1.57 and lep.phi < -0.87 :
                    HEMEleVeto.append(lep)
                    ret["etaHEMEleVeto"] = lep.eta
                    ret["phiHEMEleVeto"] = lep.phi
                    ret["ptHEMEleVeto"] = lep.pt

            for idx,lep in enumerate(otherleps) : 
                if abs(lep.pdgId) == 11 and lep.pt > 30 and  lep.eta > -3.0  and  lep.eta < -1.4 and lep.phi > -1.57 and lep.phi < -0.87 :
                    HEMEleVeto.append(lep)
                    ret["etaHEMEleVeto"] = lep.eta
                    ret["phiHEMEleVeto"] = lep.phi
                    ret["ptHEMEleVeto"] = lep.pt

            for idx,jet in enumerate(jets): 
                if (jet.pt > 30 and (jet.eta > -3.2) and (jet.eta < -1.2) and (jet.phi > -1.77) and (jet.phi < -0.67) ) : 
                    HEMJetVeto.append(jet)
                    ret["etaHEMJetVeto"] = jet.eta
                    ret["phiHEMJetVeto"] = jet.phi
                    ret["ptHEMJetVeto"] = jet.pt

            ret['nHEMJetVeto'] = len(HEMJetVeto)
            ret['nHEMEleVeto'] = len(HEMEleVeto)

        else : 
            ret['nHEMEleVeto'] = 0 
            ret['nHEMJetVeto'] = 0 
        if (len(HEMJetVeto)+len(HEMEleVeto)) != 0 :
            ret["HEM_MC_SF"] = 1.0 - 0.655
        else : 
            ret["HEM_MC_SF"] = 1.0
        return ret

# Main function for test
if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf = EventVars1L_HEM()
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
            print self.sf(ev,{})
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 50)
