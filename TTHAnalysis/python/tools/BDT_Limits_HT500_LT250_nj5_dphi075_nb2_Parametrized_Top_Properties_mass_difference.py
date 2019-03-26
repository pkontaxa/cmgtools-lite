from CMGTools.TTHAnalysis.treeReAnalyzer import *
import os, math

class BDT_Limits_Parametrized:
     def __init__(self, weightfile):

         if "/BDT_limits_C.so" not in ROOT.gSystem.GetLibraries():
               ROOT.gSystem.CompileMacro("%s/src/CMGTools/TTHAnalysis/macros/finalMVA/SUSY_1lep/BDT_Limits_HT500_LT250_nj5_dphi075_nb2_Parametrized_Top_Properties_mass_difference.C" % os.environ['CMSSW_BASE'],"kO");

         self.run = ROOT.BDT_limits_19_01_dPhi075_BTag2(weightfile)

         self.branches = [
              "BDT_Limits_HT500_LT250_nj5_dphi075_nb2_Parametrized_Top_Properties_mass_difference_8M",
         ] 

     def listBranches(self):
         return["%s"%k for k in self.branches] 

     def __call__(self,event,base={}):
          out = {} 

          res = -100           

          if "dM_Go_LSP" in base: dM_Go_LSP = base["dM_Go_LSP"]
          if "LT" in base: LT = base["LT"]
          if "HT" in base: HT = base["HT"] 
          if "nBCleaned_TOTAL" in base: nBCleaned_TOTAL = base["nBCleaned_TOTAL"]
          if "nTop_Total_Combined" in base: nTop_Total_Combined = base["nTop_Total_Combined"]
          if "nJets30Clean" in base: nJets30Clean = base["nJets30Clean"]
          if "dPhi" in base: dPhi = base["dPhi"]

          if "DeepAK8Top_Loose_pt_Array" in base: DeepAK8Top_Loose_pt_Array = base["DeepAK8Top_Loose_pt_Array"]
          if "BTag_pt_Cleaned" in base: BTag_pt_Cleaned = base["BTag_pt_Cleaned"]
          if "DeepAK8Top_Loose_eta_Array" in base: DeepAK8Top_Loose_eta_Array = base["DeepAK8Top_Loose_eta_Array"]
          if "BTag_eta_Cleaned" in base: BTag_eta_Cleaned = base["BTag_eta_Cleaned"]
          if "DeepAK8Top_Loose_phi_Array" in base: DeepAK8Top_Loose_phi_Array = base["DeepAK8Top_Loose_phi_Array"]
          if "BTag_phi_Cleaned" in base: BTag_phi_Cleaned = base["BTag_phi_Cleaned"]
          if "Resolved_Top_pt_Cleaned" in base: Resolved_Top_pt_Cleaned = base["Resolved_Top_pt_Cleaned"]
          if "Resolved_Top_eta_Cleaned" in base: Resolved_Top_eta_Cleaned = base["Resolved_Top_eta_Cleaned"]
          if "Resolved_Top_phi_Cleaned" in base: Resolved_Top_phi_Cleaned = base["Resolved_Top_phi_Cleaned"]

          #print("len of DeepAK8Top_Loose_pt_Array: ",len(DeepAK8Top_Loose_pt_Array))
          #print HT

          ######################### Variables manipulation ##############################################   
          if(len(DeepAK8Top_Loose_pt_Array)==0):
                     DeepAK8Top_Loose_pt_1=400
                     DeepAK8Top_Loose_pt_2=400    
          elif(len(DeepAK8Top_Loose_pt_Array)==1):
                     DeepAK8Top_Loose_pt_1=DeepAK8Top_Loose_pt_Array[0]
                     DeepAK8Top_Loose_pt_2=400
          elif(len(DeepAK8Top_Loose_pt_Array)>=2):
                     DeepAK8Top_Loose_pt_1=DeepAK8Top_Loose_pt_Array[0]
                     DeepAK8Top_Loose_pt_2=DeepAK8Top_Loose_pt_Array[1]
          ##
          if(len(BTag_pt_Cleaned)==0):
                     BTag_pt_1=0
                     BTag_pt_2=0
          elif(len(BTag_pt_Cleaned)==1):             
                     BTag_pt_1=BTag_pt_Cleaned[0]  
                     BTag_pt_2=0
          elif(len(BTag_pt_Cleaned)>=2):
                     BTag_pt_1=BTag_pt_Cleaned[0] 
                     BTag_pt_2=BTag_pt_Cleaned[1] 
          ##
          if(len(DeepAK8Top_Loose_eta_Array)==0):
                     DeepAK8Top_Loose_eta_1=-2.4
                     DeepAK8Top_Loose_eta_2=-2.4
          elif(len(DeepAK8Top_Loose_eta_Array)==1):
                     DeepAK8Top_Loose_eta_1=DeepAK8Top_Loose_eta_Array[0]
                     DeepAK8Top_Loose_eta_2=-2.4
          elif(len(DeepAK8Top_Loose_eta_Array)>=2):
                     DeepAK8Top_Loose_eta_1=DeepAK8Top_Loose_eta_Array[0]
                     DeepAK8Top_Loose_eta_2=DeepAK8Top_Loose_eta_Array[1]
          ##
          if(len(BTag_eta_Cleaned)==0):
                     BTag_eta_1=-2.4
                     BTag_eta_2=-2.4
          elif(len(BTag_eta_Cleaned)==1):
                     BTag_eta_1=BTag_eta_Cleaned[0]
                     BTag_eta_2=-2.4
          elif(len(BTag_eta_Cleaned)>=2):     
                     BTag_eta_1=BTag_eta_Cleaned[0] 
                     BTag_eta_2=BTag_eta_Cleaned[1] 
          ##
          if(len(DeepAK8Top_Loose_phi_Array)==0): 
                     DeepAK8Top_Loose_phi_1=-3.2
                     DeepAK8Top_Loose_phi_2=-3.2
          elif(len(DeepAK8Top_Loose_phi_Array)==1):
                     DeepAK8Top_Loose_phi_1=DeepAK8Top_Loose_phi_Array[0]
                     DeepAK8Top_Loose_phi_2=-3.2
          elif(len(DeepAK8Top_Loose_phi_Array)>=2):
                     DeepAK8Top_Loose_phi_1=DeepAK8Top_Loose_phi_Array[0]
                     DeepAK8Top_Loose_phi_2=DeepAK8Top_Loose_phi_Array[1]
          ##
          if(len(BTag_phi_Cleaned)==0):
                     BTag_phi_1=-3.2
                     BTag_phi_2=-3.2
          elif(len(BTag_phi_Cleaned)==1):
                     BTag_phi_1=BTag_phi_Cleaned[0]
                     BTag_phi_2=-3.2
          elif(len(BTag_phi_Cleaned)>=2):
                     BTag_phi_1=BTag_phi_Cleaned[0]
                     BTag_phi_2=BTag_phi_Cleaned[1]
          #######################################################################################################
          HadTop_pt=Resolved_Top_pt_Cleaned[0]
          HadTop_pt_2=Resolved_Top_pt_Cleaned[1]    
 
          HadTop_eta=Resolved_Top_eta_Cleaned[0] 
          HadTop_eta_2=Resolved_Top_eta_Cleaned[1]

          HadTop_phi=Resolved_Top_phi_Cleaned[0]
          HadTop_phi_2=Resolved_Top_phi_Cleaned[1]                    
          ######################################################################################################## 

          self.run.clear()
          self.run.addVariables(dM_Go_LSP, LT, HT, nBCleaned_TOTAL, nTop_Total_Combined, nJets30Clean, dPhi, DeepAK8Top_Loose_pt_1,DeepAK8Top_Loose_pt_2, BTag_pt_1, BTag_pt_2, DeepAK8Top_Loose_eta_1, DeepAK8Top_Loose_eta_2, BTag_eta_1, BTag_eta_2, DeepAK8Top_Loose_phi_1, DeepAK8Top_Loose_phi_2, BTag_phi_1, BTag_phi_2, HadTop_pt, HadTop_eta, HadTop_phi, HadTop_pt_2, HadTop_eta_2, HadTop_phi_2)   
          res = self.run.EvalMVA(dM_Go_LSP, LT, HT, nBCleaned_TOTAL, nTop_Total_Combined, nJets30Clean, dPhi, DeepAK8Top_Loose_pt_1,DeepAK8Top_Loose_pt_2, BTag_pt_1, BTag_pt_2, DeepAK8Top_Loose_eta_1, DeepAK8Top_Loose_eta_2, BTag_eta_1, BTag_eta_2, DeepAK8Top_Loose_phi_1, DeepAK8Top_Loose_phi_2, BTag_phi_1, BTag_phi_2, HadTop_pt, HadTop_eta, HadTop_phi, HadTop_pt_2, HadTop_eta_2, HadTop_phi_2)

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

