from CMGTools.TTHAnalysis.treeReAnalyzer import *
from ROOT import TLorentzVector, TVector2, std

import os, math
import pickle

######## !!!!!!!!!! IMPORTANT: Use this module ONLY for BKG (It stores the variable "weight_for_scale_35p9" used for weighting the BDT training)!!!!!!!!!!!!!!!!!!!

class Weight_for_Scale:
      def __init__(self):

            self.branches = [
                     "weight_for_scale_35p9",
            ]

      def listBranches(self):
            return self.branches[:]

      def __call__(self,event,base={}):
           out = {}

           res = -999
 
           total_w = 0.
           ################ PICKLE ####################################
           pckfile ="/nfs/dust/cms/group/susy-desy/Run2/MC/CMGtuples/Pantelis/trees_NEW/"+self.sample+"/skimAnalyzerCount/SkimReport.pck" 
           pckobj = pickle.load(open(pckfile,'r'))
           counters = dict(pckobj)
           total_w += counters['All Events']
           #print("TOTAL WEIGHT FROM MODULE PANTELIS:", total_w)
           ############################################################

           if "Xsec" in base : Xsec = base["Xsec"]
           if "btagSF" in base: btagSF = base["btagSF"]
           if "puRatio" in base: puRatio = base["puRatio"]
           if "lepSF" in base: lepSF = base["lepSF"]
           if "nISRttweight" in base: nISRttweight = base["nISRttweight"]

           res = 35.9*(Xsec*1.*lepSF*btagSF*puRatio)*(1000./total_w)


           out["%s"%self.branches[0]]=res

           return out

if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    tree.vectorTree = True
    tree.AddFriend("sf/t",argv[2]) # recleaner

    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf = BDT_resolvedTopTagger('../../data/kinMVA/tth/BDT_Limits_w_DeepAK8.weights.xml')
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
            print self.sf(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 500)


           
           
           
          

