from CMGTools.TTHAnalysis.treeReAnalyzer import *
from ROOT import TLorentzVector, TVector2, std

import os, math
import pickle

######## !!!!!!!!!! IMPORTANT: Use this module ONLY for BKG (It stores the variable "weight_for_scale_35p9" used for weighting the BDT training)!!!!!!!!!!!!!!!!!!!

class Weight_for_Scale:
    def __init__(self):

        self.branches = [
                    "sumOfWeights","sumOfWeights2",
        ]

    def listBranches(self):
        return self.branches[:]

    def __call__(self,event,base={}):
        if event.isData: return {}
        ret = {}
        for name in self.branches:
            if type(name) == 'tuple':
                ret[name] = []
            elif type(name) == 'str':
                ret[name] = -999


        total_w = 0.
        total_w2 = 0.
        ################ PICKLE ####################################
        pckfile =self.path+"/"+self.sample+"/skimAnalyzerCount/SkimReport.pck" 
        pckobj = pickle.load(open(pckfile,'r'))
        counters = dict(pckobj)
        
        othersamples = [x for x in os.listdir(self.path) if x != self.sample]

        if ('Sum Weights' in counters):
            total_w += counters['Sum Weights']
        else:
            total_w += counters['All Events']

        ret["sumOfWeights"] = total_w
        total_w2 = total_w
        smaller_list = []
        if "_ext" in self.sample : 
            nom = self.sample.replace(self.sample[self.sample.find("_ext"):],'')
            for sam in othersamples : 
                if nom in sam : smaller_list.append(sam)
        else : 
            nom = self.sample
            for sam in othersamples : 
                if nom+"_ex" in sam : smaller_list.append(sam)
        
        for samp in smaller_list : 
            pckfile =self.path+"/"+samp+"/skimAnalyzerCount/SkimReport.pck" 
            pckobj = pickle.load(open(pckfile,'r'))
            counters = dict(pckobj)
            if ('Sum Weights' in counters):
                total_w2 += counters['Sum Weights']
            else:
                total_w2 += counters['All Events']

        ret["sumOfWeights2"] = total_w2
            
        return ret

if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf = Weight_for_Scale()
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
            print self.sf(ev,{})
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 50)
