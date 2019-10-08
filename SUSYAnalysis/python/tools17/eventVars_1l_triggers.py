from CMGTools.TTHAnalysis.treeReAnalyzer import *
from ROOT import TLorentzVector, TVector2, std
import ROOT
import time
import itertools
import PhysicsTools.Heppy.loadlibs
import array
import operator

class EventVars1L_triggers:
    def __init__(self):
        self.branches = [
            'HLT_HT350', 'HLT_HT590', 'HLT_HT780', 'HLT_HT890',
            'HLT_PFJet450',
            'HLT_AK4PFJet450','HLT_AK8PFJet450','HLT_CaloJet500',
            'HLT_MET100MHT100','HLT_MET110MHT110','HLT_MET120MHT120','HLT_highMHTMET',
            'HLT_SingleMu' ,'HLT_IsoMu27','HLT_IsoMu20','HLT_IsoMu24','HLT_Mu45eta2p1','HLT_Mu50',
            'HLT_MuHT600' ,'HLT_MuHT450MET50','HLT_MuHT450','HLT_Mu50HT450','HLT_MuHTMET','HLT_MuHT450B',
            'HLT_IsoEle32','HLT_IsoEle35','HLT_IsoEle27T','HLT_Ele115','HLT_Ele50PFJet165',
            'HLT_EleHT600','HLT_EleHT450MET50','HLT_EleHT450','HLT_Ele50HT450','HLT_EleHTMET','HLT_EleHT450B',
            ## custom names
            'HLT_EleOR', 'HLT_MuOR','HLT_LepOR','HLT_MetOR','HLT_EE','HLT_MuMu',
            #'HLT_IsoMu27','HLT_IsoEle32',
            #'HLT_Mu50','HLT_Ele105'
            ## Trigger efficiencies
            'TrigEff'
            ]

    def listBranches(self):
        return self.branches[:]

    def __call__(self,event,base):

        # output dict:
        ret = {}

        ## loop over all HLT names and set them in tree
        for var in self.branches:
            #print var, getattr(event,var)
            if 'HLT_' in var and hasattr(event,var):
                ret[var] = getattr(event,var)
            else:
                ret[var] = 0

        # Trigger efficiencies:
        if hasattr(self,'sample'):
#            print self.sample
            if 'Ele' in self.sample or 'Mu' in self.sample:
                ret['TrigEff'] = 1.0
            elif base['nEl']>=1: ret['TrigEff'] = 0.963 # ele efficieny (for 2016 4/fb)
            elif base['nMu']>=1: ret['TrigEff'] = 0.926 # mu efficieny (for 2016 4/fb)
            else: ret['TrigEff'] = 1.0
#old logic
#            if 'Ele' in self.sample: ret['TrigEff'] = 0.963 # ele efficieny (for 2016 4/fb)
#            elif 'Mu' in self.sample: ret['TrigEff'] = 0.926 # mu efficieny (for 2016 4/fb)
#            else: ret['TrigEff'] = 1.0
        else:
            ret['TrigEff'] = 1.00 # to make clear that this is not the accurate value

        ## print out all HLT names
        #for line in vars(event)['_tree'].GetListOfBranches():
        #    if 'HLT_' in line.GetName():
        #        print line.GetName()

        # custom names for triggers
        ret['HLT_EleOR'] = ret['HLT_Ele115'] or ret['HLT_Ele50PFJet165'] or ret['HLT_IsoEle35'] or ret['HLT_EleHT450']
        ret['HLT_MuOR'] = ret['HLT_Mu50'] or ret['HLT_IsoMu24'] or ret['HLT_MuHT450']  
        ret['HLT_LepOR'] = ret['HLT_EleOR'] or ret['HLT_MuOR']
        ret['HLT_MetOR'] = ret["HLT_MET100MHT100"] or ret["HLT_MET110MHT110"] or ret["HLT_MET120MHT120"]

        # return branches
        return ret

if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf = EventVars1L()
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
            print self.sf(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 50)
