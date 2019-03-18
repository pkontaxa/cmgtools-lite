########### author : Pantelis Kontaxakis ##########
########### institute : National and Kapodistrian University of Athens #######################
########### Email : pantelis.kontaxakis@cern.ch #########
########### Date : February 2019 #######################

from CMGTools.TTHAnalysis.treeReAnalyzer import *
import os, math
import ROOT

class BDT_resolvedTopTagger: # has to run on a recleaner with label _Recl
    def __init__(self, weightfile, recllabel='Recl', selection = []):

        self.inputlabel = '_'+recllabel
        self.systsJEC = {0:"", 1:"_jecUp", -1:"_jecDown"}
        self.selection = selection

        if "/BDT_resolvedTopTagger_v7_C.so" not in ROOT.gSystem.GetLibraries():
            ROOT.gSystem.CompileMacro("%s/src/CMGTools/TTHAnalysis/macros/finalMVA/BDT_resolvedTopTagger_v7_1lep_dPhi.C" % os.environ['CMSSW_BASE'],"kO");

        self.run = ROOT.BDT_resolvedTopTagger(weightfile)


        self.branches = [
             "mvaValue",
             "HadTop_pt", 
             "HadTop_eta",
             "HadTop_phi",
             "HadTop_mass",
             "j1_eta",
             "j1_phi",
             "j2_eta",
             "j2_phi",
             "j3_eta",
             "j3_phi",
             "W_fromHadTop_dRb",
             "b_fromHadTop_CSV",
             "j1",
             "j2",
             "j3",
             "mvaValue_2",
             "HadTop_pt_2",  
             "HadTop_eta_2",
             "HadTop_phi_2",
             "HadTop_mass_2",
             "j1_eta_2",
             "j1_phi_2",
             "j2_eta_2",
             "j2_phi_2",
             "j3_eta_2",
             "j3_phi_2",
             "W_fromHadTop_dRb_2",
             "b_fromHadTop_CSV_2",
             "j1_2",
             "j2_2",
             "j3_2",             
             "mvaValue_3",
             "HadTop_pt_3",
             "HadTop_eta_3",
             "HadTop_phi_3",
             "HadTop_mass_3",
             "j1_eta_3",
             "j1_phi_3",
             "j2_eta_3",
             "j2_phi_3",
             "j3_eta_3",
             "j3_phi_3",
             "W_fromHadTop_dRb_3",
             "b_fromHadTop_CSV_3",
             "j1_3",
             "j2_3",
             "j3_3",
             "mvaValue_4",
             "HadTop_pt_4",
             "HadTop_eta_4",
             "HadTop_phi_4",
             "HadTop_mass_4",
             "j1_eta_4",
             "j1_phi_4",
             "j2_eta_4",
             "j2_phi_4",
             "j3_eta_4",
             "j3_phi_4",
             "W_fromHadTop_dRb_4",
             "b_fromHadTop_CSV_4",
             "j1_4",
             "j2_4",
             "j3_4",
             "nResolvedTop",
             "nTop_Total_Combined",
             ("Resolved_Had_Top_mvaValue","F",4,"4"),
             ("Resolved_Had_Top_pt","F",4,"4"), 
             ("Resolved_Had_Top_eta","F",4,"4"),
             ("Resolved_Had_Top_phi","F",4,"4"),
             ("Resolved_Had_Top_mass","F",4,"4"),
             ("nBCleaned_TOTAL","I"),
             ("Resolved_Top_pt_Cleaned","F",4,"4"),
             ("Resolved_Top_eta_Cleaned","F",4,"4"),
             ("Resolved_Top_phi_Cleaned","F",4,"4"),
             ("BTag_pt_Cleaned","F",15,"nBCleaned_TOTAL"),
             ("BTag_eta_Cleaned","F",15,"nBCleaned_TOTAL"),
             ("BTag_phi_Cleaned","F",15,"nBCleaned_TOTAL"),
            ]   
                   

    def listBranches(self):
           #return ["BDT_resolvedTopTagger_%s"%k for k in self.branches ]
           # commented out for v4 return ["%s"%k for k in self.branches]
           return self.branches[:]

    def __call__(self,event,base):
            out = {}
            scores=[]

####################### DeepAK8 nDeepLooseTop ########################################
            FatJets =[l for l in Collection(event,"FatJet","nFatJet")]
            nTop_Total = 0
            for i,j in enumerate(FatJets):
                  if(j.raw_score_deep_Top_PUPPI > 0.18 and j.pt>=400.):
                         nTop_Total +=1
###############################################################################################

            jets = [j for j in Collection(event,"Jet","nJet")]

            jetptcut = 25

            jets = filter(lambda x : x.pt>jetptcut,jets) 

            res = [-100]*(len(self.branches)-14)

            good = True
            for sel in self.selection:
                if not sel(leps,jets,event):
                    good = False
                    break           
            if good:
                self.run.clear()
             
                for i,j in enumerate(jets): self.run.addJet(j.pt,j.eta,j.phi,j.mass,j.btagCSV,j.ctagCsvL,j.ptd,j.axis1,j.mult)
                res = self.run.EvalMVA()

                Resolved_Top_mvaValue = []
                Resolved_Top_mvaValue.append(res[0])
                Resolved_Top_mvaValue.append(res[16])
                Resolved_Top_mvaValue.append(res[32])
                Resolved_Top_mvaValue.append(res[48])

                Resolved_Top_pt = []

                if (res[1]<-2):                    
                       Resolved_Top_pt.append(0.)
                else:
                     Resolved_Top_pt.append(res[1])
                
                if (res[17]<-2):                         
                       Resolved_Top_pt.append(0.)                     
                else:
                     Resolved_Top_pt.append(res[17])

                if (res[33]<-2):                        
                       Resolved_Top_pt.append(0.)
                else:
                       Resolved_Top_pt.append(res[33])

                if (res[49]<-2):                    
                       Resolved_Top_pt.append(0.)
                else:
                       Resolved_Top_pt.append(res[49])


                Resolved_Top_eta = []

                if (res[2]<-60):                       
                       Resolved_Top_eta.append(-6.)
                else:                   
                       Resolved_Top_eta.append(res[2])
                if (res[18]<-60):                       
                       Resolved_Top_eta.append(-6.)
                else:
                       Resolved_Top_eta.append(res[18])
                if (res[34]<-60):                       
                       Resolved_Top_eta.append(-6.)
                else:
                       Resolved_Top_eta.append(res[34])

                if (res[50]<-60):                       
                       Resolved_Top_eta.append(-6.)
                else:
                       Resolved_Top_eta.append(res[50])

                Resolved_Top_phi = []

                if (res[3]<-60):                       
                       Resolved_Top_phi.append(-3.2)
                else:   
                       Resolved_Top_phi.append(res[3])
                if (res[19]<-60):                       
                       Resolved_Top_phi.append(-3.2)
                else:
                       Resolved_Top_phi.append(res[19])
                if (res[35]<-60):                       
                       Resolved_Top_phi.append(-3.2)
                else:
                       Resolved_Top_phi.append(res[35])
                if (res[51]<-60):                       
                       Resolved_Top_phi.append(-3.2)
                else:
                       Resolved_Top_phi.append(res[51])

                Resolved_Top_mass = []
                Resolved_Top_mass.append(res[4])
                Resolved_Top_mass.append(res[20])
                Resolved_Top_mass.append(res[36])
                Resolved_Top_mass.append(res[52])

################################### Combination of DeepAK8 and Resolved Top Taggers #####################################
                j1_eta = res[5]
                j1_phi = res[6]
                j2_eta = res[7]
                j2_phi = res[8]
                j3_eta = res[9]
                j3_phi = res[10]

                j1_eta_2 = res[21]
                j1_phi_2 = res[22]
                j2_eta_2 = res[23]
                j2_phi_2 = res[24]
                j3_eta_2 = res[25]
                j3_phi_2 = res[26]

                j1_eta_3 = res[37]
                j1_phi_3 = res[38]
                j2_eta_3 = res[39]
                j2_phi_3 = res[40]
                j3_eta_3 = res[41]
                j3_phi_3 = res[42]

                j1_eta_4 = res[53]
                j1_phi_4 = res[54]
                j2_eta_4 = res[55]
                j2_phi_4 = res[56]
                j3_eta_4 = res[57]
                j3_phi_4 = res[58]


                for i,x in enumerate(res): out["%s"%self.branches[i]]=res[i]
 
                NResolved = 0

                Resolved_Cleaned_pt = []
                Resolved_Cleaned_eta = []
                Resolved_Cleaned_phi = []
                          
                if(res[0]<=0. and res[16]<=0. and res[32]<=0. and res[48]<=0.):
                      NResolved = 0
                      for i_for_clean in range(4):
                             Resolved_Cleaned_pt.append(0.)
                             Resolved_Cleaned_eta.append(-6.)
                             Resolved_Cleaned_phi.append(-3.2)                                             

                elif(res[0]>=0. and res[16]<=0. and res[32]<=0. and res[48]<=0.):   
                      NResolved = 1
                      flag_leq_08_loose_first_resolved_Top=0
                      nDeepAK8Loose=0
                      for i,j in enumerate(FatJets):
                             if(j.raw_score_deep_Top_PUPPI > 0.18 and j.pt>=400.):
                                  nDeepAK8Loose+=1
                                  _DeepAK8_Loose_Top_phi=j.phi
                                  _DeepAK8_Loose_Top_eta=j.eta

                                  _delta_phi_Loose_j1=fabs(acos(cos(_DeepAK8_Loose_Top_phi-j1_phi))) 
                                  _delta_phi_Loose_j2=fabs(acos(cos(_DeepAK8_Loose_Top_phi-j2_phi)))
                                  _delta_phi_Loose_j3=fabs(acos(cos(_DeepAK8_Loose_Top_phi-j3_phi)))

                                  _delta_eta_Loose_j1=fabs(_DeepAK8_Loose_Top_eta-j1_eta)
                                  _delta_eta_Loose_j2=fabs(_DeepAK8_Loose_Top_eta-j2_eta)
                                  _delta_eta_Loose_j3=fabs(_DeepAK8_Loose_Top_eta-j3_eta)

                                  _delta_R_Loose_j1=sqrt(pow(_delta_eta_Loose_j1,2)+pow(_delta_phi_Loose_j1,2))
                                  _delta_R_Loose_j2=sqrt(pow(_delta_eta_Loose_j2,2)+pow(_delta_phi_Loose_j2,2))
                                  _delta_R_Loose_j3=sqrt(pow(_delta_eta_Loose_j3,2)+pow(_delta_phi_Loose_j3,2))

                                  if(_delta_R_Loose_j1<0.8 or _delta_R_Loose_j2<0.8 or _delta_R_Loose_j3<0.8):
                                           flag_leq_08_loose_first_resolved_Top+=1
                      if(nDeepAK8Loose>0):
                             if(flag_leq_08_loose_first_resolved_Top==0):
                                   nTop_Total+=1  

                                   Resolved_Cleaned_pt.append(res[1])
                                   Resolved_Cleaned_eta.append(res[2])
                                   Resolved_Cleaned_phi.append(res[3])
                                   for i_for_clean in range (3):
                                         Resolved_Cleaned_pt.append(0.)
                                         Resolved_Cleaned_eta.append(-6.)
                                         Resolved_Cleaned_phi.append(-3.2)
                             else:
                                   for i_for_clean in range(4):
                                         Resolved_Cleaned_pt.append(0.)
                                         Resolved_Cleaned_eta.append(-6.)
                                         Resolved_Cleaned_phi.append(-3.2)
                                   
                                        
                      elif(nDeepAK8Loose==0):
                                   nTop_Total+=1
                                   Resolved_Cleaned_pt.append(res[1])
                                   Resolved_Cleaned_eta.append(res[2])
                                   Resolved_Cleaned_phi.append(res[3])
                                   for i_for_clean in range (3):
                                         Resolved_Cleaned_pt.append(0.)
                                         Resolved_Cleaned_eta.append(-6.)
                                         Resolved_Cleaned_phi.append(-3.2)


                elif(res[0]>=0. and res[16]>=0. and res[32]<=0. and res[48]<=0.):
                      NResolved = 2

                      flag_leq_08_loose_first_resolved_Top=0
                      flag_leq_08_loose_second_resolved_Top=0
                      nDeepAK8Loose=0

                      for i,j in enumerate(FatJets):
                             if(j.raw_score_deep_Top_PUPPI > 0.18 and j.pt>=400.):
                                  nDeepAK8Loose+=1
                                  _DeepAK8_Loose_Top_phi=j.phi
                                  _DeepAK8_Loose_Top_eta=j.eta

                                  _delta_phi_Loose_j1=fabs(acos(cos(_DeepAK8_Loose_Top_phi-j1_phi)))
                                  _delta_phi_Loose_j2=fabs(acos(cos(_DeepAK8_Loose_Top_phi-j2_phi)))
                                  _delta_phi_Loose_j3=fabs(acos(cos(_DeepAK8_Loose_Top_phi-j3_phi)))

                                  _delta_eta_Loose_j1=fabs(_DeepAK8_Loose_Top_eta-j1_eta)
                                  _delta_eta_Loose_j2=fabs(_DeepAK8_Loose_Top_eta-j2_eta)
                                  _delta_eta_Loose_j3=fabs(_DeepAK8_Loose_Top_eta-j3_eta)

                                  _delta_R_Loose_j1=sqrt(pow(_delta_eta_Loose_j1,2)+pow(_delta_phi_Loose_j1,2))
                                  _delta_R_Loose_j2=sqrt(pow(_delta_eta_Loose_j2,2)+pow(_delta_phi_Loose_j2,2))
                                  _delta_R_Loose_j3=sqrt(pow(_delta_eta_Loose_j3,2)+pow(_delta_phi_Loose_j3,2))

                                    #### second resolved Top ###########
                                  _delta_phi_Loose_j1_2=fabs(acos(cos(_DeepAK8_Loose_Top_phi-j1_phi_2)))
                                  _delta_phi_Loose_j2_2=fabs(acos(cos(_DeepAK8_Loose_Top_phi-j2_phi_2)))
                                  _delta_phi_Loose_j3_2=fabs(acos(cos(_DeepAK8_Loose_Top_phi-j3_phi_2)))

                                  _delta_eta_Loose_j1_2=fabs(_DeepAK8_Loose_Top_eta-j1_eta_2)
                                  _delta_eta_Loose_j2_2=fabs(_DeepAK8_Loose_Top_eta-j2_eta_2)
                                  _delta_eta_Loose_j3_2=fabs(_DeepAK8_Loose_Top_eta-j3_eta_2)

                                  _delta_R_Loose_j1_2=sqrt(pow(_delta_eta_Loose_j1_2,2)+pow(_delta_phi_Loose_j1_2,2))
                                  _delta_R_Loose_j2_2=sqrt(pow(_delta_eta_Loose_j2_2,2)+pow(_delta_phi_Loose_j2_2,2))
                                  _delta_R_Loose_j3_2=sqrt(pow(_delta_eta_Loose_j3_2,2)+pow(_delta_phi_Loose_j3_2,2))

                                  if(_delta_R_Loose_j1<0.8 or _delta_R_Loose_j2<0.8 or _delta_R_Loose_j3<0.8):
                                           flag_leq_08_loose_first_resolved_Top+=1

                                  if(_delta_R_Loose_j1_2<0.8 or _delta_R_Loose_j2_2<0.8 or _delta_R_Loose_j3_2<0.8):
                                           flag_leq_08_loose_second_resolved_Top+=1

                      if(nDeepAK8Loose>0):
                             if(flag_leq_08_loose_first_resolved_Top==0):
                                   nTop_Total+=1

                                   Resolved_Cleaned_pt.append(res[1])
                                   Resolved_Cleaned_eta.append(res[2])
                                   Resolved_Cleaned_phi.append(res[3])

                             if(flag_leq_08_loose_second_resolved_Top==0):
                                   nTop_Total+=1

                                   Resolved_Cleaned_pt.append(res[17])
                                   Resolved_Cleaned_eta.append(res[18])
                                   Resolved_Cleaned_phi.append(res[19])

                             if(flag_leq_08_loose_first_resolved_Top==0 and flag_leq_08_loose_second_resolved_Top==0):
                                   for i_for_clean in range(2):
                                         Resolved_Cleaned_pt.append(0.)
                                         Resolved_Cleaned_eta.append(-6.)
                                         Resolved_Cleaned_phi.append(-3.2)
                             elif((flag_leq_08_loose_first_resolved_Top!=0 and flag_leq_08_loose_second_resolved_Top==0) or (flag_leq_08_loose_first_resolved_Top==0 and flag_leq_08_loose_second_resolved_Top!=0)):
                                   for i_for_clean in range(3):
                                         Resolved_Cleaned_pt.append(0.)
                                         Resolved_Cleaned_eta.append(-6.)
                                         Resolved_Cleaned_phi.append(-3.2)
                             elif(flag_leq_08_loose_first_resolved_Top!=0 and flag_leq_08_loose_second_resolved_Top!=0):
                                   for i_for_clean in range(4):
                                         Resolved_Cleaned_pt.append(0.)
                                         Resolved_Cleaned_eta.append(-6.)
                                         Resolved_Cleaned_phi.append(-3.2)
                                                                        

                      elif(nDeepAK8Loose==0):
                             nTop_Total+=2

                             Resolved_Cleaned_pt.append(res[1])
                             Resolved_Cleaned_pt.append(res[17])

                             Resolved_Cleaned_eta.append(res[2])
                             Resolved_Cleaned_eta.append(res[18])

                             Resolved_Cleaned_phi.append(res[3])
                             Resolved_Cleaned_phi.append(res[19])

                             for i_for_clean in range (2):
                                   Resolved_Cleaned_pt.append(0.)
                                   Resolved_Cleaned_eta.append(-6.)
                                   Resolved_Cleaned_phi.append(-3.2)



                elif(res[0]>=0. and res[16]>=0. and res[32]>=0. and res[48]<=0.):
                      NResolved = 3

                      flag_leq_08_loose_first_resolved_Top=0
                      flag_leq_08_loose_second_resolved_Top=0
                      flag_leq_08_loose_third_resolved_Top=0
                      nDeepAK8Loose=0


                      for i,j in enumerate(FatJets):
                             if(j.raw_score_deep_Top_PUPPI > 0.18 and j.pt>=400.):
                                  nDeepAK8Loose+=1
                                  _DeepAK8_Loose_Top_phi=j.phi
                                  _DeepAK8_Loose_Top_eta=j.eta

                                  _delta_phi_Loose_j1=fabs(acos(cos(_DeepAK8_Loose_Top_phi-j1_phi)))
                                  _delta_phi_Loose_j2=fabs(acos(cos(_DeepAK8_Loose_Top_phi-j2_phi)))
                                  _delta_phi_Loose_j3=fabs(acos(cos(_DeepAK8_Loose_Top_phi-j3_phi)))

                                  _delta_eta_Loose_j1=fabs(_DeepAK8_Loose_Top_eta-j1_eta)
                                  _delta_eta_Loose_j2=fabs(_DeepAK8_Loose_Top_eta-j2_eta)
                                  _delta_eta_Loose_j3=fabs(_DeepAK8_Loose_Top_eta-j3_eta)

                                  _delta_R_Loose_j1=sqrt(pow(_delta_eta_Loose_j1,2)+pow(_delta_phi_Loose_j1,2))
                                  _delta_R_Loose_j2=sqrt(pow(_delta_eta_Loose_j2,2)+pow(_delta_phi_Loose_j2,2))
                                  _delta_R_Loose_j3=sqrt(pow(_delta_eta_Loose_j3,2)+pow(_delta_phi_Loose_j3,2))

                                    #### second resolved Top ###########
                                  _delta_phi_Loose_j1_2=fabs(acos(cos(_DeepAK8_Loose_Top_phi-j1_phi_2)))
                                  _delta_phi_Loose_j2_2=fabs(acos(cos(_DeepAK8_Loose_Top_phi-j2_phi_2)))
                                  _delta_phi_Loose_j3_2=fabs(acos(cos(_DeepAK8_Loose_Top_phi-j3_phi_2)))

                                  _delta_eta_Loose_j1_2=fabs(_DeepAK8_Loose_Top_eta-j1_eta_2)
                                  _delta_eta_Loose_j2_2=fabs(_DeepAK8_Loose_Top_eta-j2_eta_2)
                                  _delta_eta_Loose_j3_2=fabs(_DeepAK8_Loose_Top_eta-j3_eta_2)

                                  _delta_R_Loose_j1_2=sqrt(pow(_delta_eta_Loose_j1_2,2)+pow(_delta_phi_Loose_j1_2,2))
                                  _delta_R_Loose_j2_2=sqrt(pow(_delta_eta_Loose_j2_2,2)+pow(_delta_phi_Loose_j2_2,2))
                                  _delta_R_Loose_j3_2=sqrt(pow(_delta_eta_Loose_j3_2,2)+pow(_delta_phi_Loose_j3_2,2))

                                    #### third resolved Top ###########
                                  _delta_phi_Loose_j1_3=fabs(acos(cos(_DeepAK8_Loose_Top_phi-j1_phi_3)))
                                  _delta_phi_Loose_j2_3=fabs(acos(cos(_DeepAK8_Loose_Top_phi-j2_phi_3)))
                                  _delta_phi_Loose_j3_3=fabs(acos(cos(_DeepAK8_Loose_Top_phi-j3_phi_3)))

                                  _delta_eta_Loose_j1_3=fabs(_DeepAK8_Loose_Top_eta-j1_eta_3)
                                  _delta_eta_Loose_j2_3=fabs(_DeepAK8_Loose_Top_eta-j2_eta_3)
                                  _delta_eta_Loose_j3_3=fabs(_DeepAK8_Loose_Top_eta-j3_eta_3)

                                  _delta_R_Loose_j1_3=sqrt(pow(_delta_eta_Loose_j1_3,2)+pow(_delta_phi_Loose_j1_3,2))
                                  _delta_R_Loose_j2_3=sqrt(pow(_delta_eta_Loose_j2_3,2)+pow(_delta_phi_Loose_j2_3,2))
                                  _delta_R_Loose_j3_3=sqrt(pow(_delta_eta_Loose_j3_3,2)+pow(_delta_phi_Loose_j3_3,2))


                                  if(_delta_R_Loose_j1<0.8 or _delta_R_Loose_j2<0.8 or _delta_R_Loose_j3<0.8):
                                           flag_leq_08_loose_first_resolved_Top+=1

                                  if(_delta_R_Loose_j1_2<0.8 or _delta_R_Loose_j2_2<0.8 or _delta_R_Loose_j3_2<0.8):
                                           flag_leq_08_loose_second_resolved_Top+=1

                                  if(_delta_R_Loose_j1_3<0.8 or _delta_R_Loose_j2_3<0.8 or _delta_R_Loose_j3_3<0.8):
                                           flag_leq_08_loose_third_resolved_Top+=1


                      if(nDeepAK8Loose>0):
                             if(flag_leq_08_loose_first_resolved_Top==0):
                                  nTop_Total+=1
 
                                  Resolved_Cleaned_pt.append(res[1])
                                  Resolved_Cleaned_eta.append(res[2])
                                  Resolved_Cleaned_phi.append(res[3])


                             if(flag_leq_08_loose_second_resolved_Top==0):
                                  nTop_Total+=1

                                  Resolved_Cleaned_pt.append(res[17])
                                  Resolved_Cleaned_eta.append(res[18])
                                  Resolved_Cleaned_phi.append(res[19])

                             if(flag_leq_08_loose_third_resolved_Top==0):
                                  nTop_Total+=1

                                  Resolved_Cleaned_pt.append(res[33])
                                  Resolved_Cleaned_eta.append(res[34])
                                  Resolved_Cleaned_phi.append(res[35])

                             if(flag_leq_08_loose_first_resolved_Top==0 and flag_leq_08_loose_second_resolved_Top==0 and flag_leq_08_loose_third_resolved_Top==0):
                                  Resolved_Cleaned_pt.append(0.)
                                  Resolved_Cleaned_eta.append(-6.)
                                  Resolved_Cleaned_phi.append(-3.2)
                                 
                             elif((flag_leq_08_loose_first_resolved_Top!=0 and flag_leq_08_loose_second_resolved_Top==0 and flag_leq_08_loose_third_resolved_Top==0) or (flag_leq_08_loose_first_resolved_Top==0 and flag_leq_08_loose_second_resolved_Top!=0 and flag_leq_08_loose_third_resolved_Top==0) or (flag_leq_08_loose_first_resolved_Top==0 and flag_leq_08_loose_second_resolved_Top==0 and flag_leq_08_loose_third_resolved_Top!=0)): 
                                  for i_for_clean in range (2):
                                         Resolved_Cleaned_pt.append(0.)
                                         Resolved_Cleaned_eta.append(-6.)
                                         Resolved_Cleaned_phi.append(-3.2)

                             elif((flag_leq_08_loose_first_resolved_Top!=0 and flag_leq_08_loose_second_resolved_Top!=0 and flag_leq_08_loose_third_resolved_Top==0) or (flag_leq_08_loose_first_resolved_Top==0 and flag_leq_08_loose_second_resolved_Top!=0 and flag_leq_08_loose_third_resolved_Top!=0) or (flag_leq_08_loose_first_resolved_Top!=0 and flag_leq_08_loose_second_resolved_Top==0 and flag_leq_08_loose_third_resolved_Top!=0)):
                                  for i_for_clean in range (3):
                                         Resolved_Cleaned_pt.append(0.)
                                         Resolved_Cleaned_eta.append(-6.)
                                         Resolved_Cleaned_phi.append(-3.2)

                             elif(flag_leq_08_loose_first_resolved_Top!=0 and flag_leq_08_loose_second_resolved_Top!=0 and flag_leq_08_loose_third_resolved_Top!=0):                                                  
                                  for i_for_clean in range (4):
                                         Resolved_Cleaned_pt.append(0.)
                                         Resolved_Cleaned_eta.append(-6.)
                                         Resolved_Cleaned_phi.append(-3.2)
                                    


                      elif(nDeepAK8Loose==0):
                             nTop_Total+=3

                             Resolved_Cleaned_pt.append(res[1])
                             Resolved_Cleaned_pt.append(res[17])
                             Resolved_Cleaned_pt.append(res[33])


                             Resolved_Cleaned_eta.append(res[2])
                             Resolved_Cleaned_eta.append(res[18])
                             Resolved_Cleaned_eta.append(res[34])


                             Resolved_Cleaned_phi.append(res[3])
                             Resolved_Cleaned_phi.append(res[19])
                             Resolved_Cleaned_phi.append(res[35])

                             for i_for_clean in range (1):
                                   Resolved_Cleaned_pt.append(0.)
                                   Resolved_Cleaned_eta.append(-6.)
                                   Resolved_Cleaned_phi.append(-3.2)



                elif(res[0]>=0. and res[16]>=0. and res[32]>=0. and res[48]>=0.):
                      NResolved = 4

                      flag_leq_08_loose_first_resolved_Top=0
                      flag_leq_08_loose_second_resolved_Top=0
                      flag_leq_08_loose_third_resolved_Top=0
                      flag_leq_08_loose_fourth_resolved_Top=0
                      nDeepAK8Loose=0


                      for i,j in enumerate(FatJets):
                             if(j.raw_score_deep_Top_PUPPI > 0.18 and j.pt>=400.):
                                  nDeepAK8Loose+=1
                                  _DeepAK8_Loose_Top_phi=j.phi
                                  _DeepAK8_Loose_Top_eta=j.eta

                                  _delta_phi_Loose_j1=fabs(acos(cos(_DeepAK8_Loose_Top_phi-j1_phi)))
                                  _delta_phi_Loose_j2=fabs(acos(cos(_DeepAK8_Loose_Top_phi-j2_phi)))
                                  _delta_phi_Loose_j3=fabs(acos(cos(_DeepAK8_Loose_Top_phi-j3_phi)))

                                  _delta_eta_Loose_j1=fabs(_DeepAK8_Loose_Top_eta-j1_eta)
                                  _delta_eta_Loose_j2=fabs(_DeepAK8_Loose_Top_eta-j2_eta)
                                  _delta_eta_Loose_j3=fabs(_DeepAK8_Loose_Top_eta-j3_eta)

                                  _delta_R_Loose_j1=sqrt(pow(_delta_eta_Loose_j1,2)+pow(_delta_phi_Loose_j1,2))
                                  _delta_R_Loose_j2=sqrt(pow(_delta_eta_Loose_j2,2)+pow(_delta_phi_Loose_j2,2))
                                  _delta_R_Loose_j3=sqrt(pow(_delta_eta_Loose_j3,2)+pow(_delta_phi_Loose_j3,2))

                                    #### second resolved Top ###########
                                  _delta_phi_Loose_j1_2=fabs(acos(cos(_DeepAK8_Loose_Top_phi-j1_phi_2)))
                                  _delta_phi_Loose_j2_2=fabs(acos(cos(_DeepAK8_Loose_Top_phi-j2_phi_2)))
                                  _delta_phi_Loose_j3_2=fabs(acos(cos(_DeepAK8_Loose_Top_phi-j3_phi_2)))

                                  _delta_eta_Loose_j1_2=fabs(_DeepAK8_Loose_Top_eta-j1_eta_2)
                                  _delta_eta_Loose_j2_2=fabs(_DeepAK8_Loose_Top_eta-j2_eta_2)
                                  _delta_eta_Loose_j3_2=fabs(_DeepAK8_Loose_Top_eta-j3_eta_2)

                                  _delta_R_Loose_j1_2=sqrt(pow(_delta_eta_Loose_j1_2,2)+pow(_delta_phi_Loose_j1_2,2))
                                  _delta_R_Loose_j2_2=sqrt(pow(_delta_eta_Loose_j2_2,2)+pow(_delta_phi_Loose_j2_2,2))
                                  _delta_R_Loose_j3_2=sqrt(pow(_delta_eta_Loose_j3_2,2)+pow(_delta_phi_Loose_j3_2,2))

                                    #### third resolved Top ###########
                                  _delta_phi_Loose_j1_3=fabs(acos(cos(_DeepAK8_Loose_Top_phi-j1_phi_3)))
                                  _delta_phi_Loose_j2_3=fabs(acos(cos(_DeepAK8_Loose_Top_phi-j2_phi_3)))
                                  _delta_phi_Loose_j3_3=fabs(acos(cos(_DeepAK8_Loose_Top_phi-j3_phi_3)))

                                  _delta_eta_Loose_j1_3=fabs(_DeepAK8_Loose_Top_eta-j1_eta_3)
                                  _delta_eta_Loose_j2_3=fabs(_DeepAK8_Loose_Top_eta-j2_eta_3)
                                  _delta_eta_Loose_j3_3=fabs(_DeepAK8_Loose_Top_eta-j3_eta_3)

                                  _delta_R_Loose_j1_3=sqrt(pow(_delta_eta_Loose_j1_3,2)+pow(_delta_phi_Loose_j1_3,2))
                                  _delta_R_Loose_j2_3=sqrt(pow(_delta_eta_Loose_j2_3,2)+pow(_delta_phi_Loose_j2_3,2))
                                  _delta_R_Loose_j3_3=sqrt(pow(_delta_eta_Loose_j3_3,2)+pow(_delta_phi_Loose_j3_3,2))

                                    #### fourth resolved Top ###########
                                  _delta_phi_Loose_j1_4=fabs(acos(cos(_DeepAK8_Loose_Top_phi-j1_phi_4)))
                                  _delta_phi_Loose_j2_4=fabs(acos(cos(_DeepAK8_Loose_Top_phi-j2_phi_4)))
                                  _delta_phi_Loose_j3_4=fabs(acos(cos(_DeepAK8_Loose_Top_phi-j3_phi_4)))

                                  _delta_eta_Loose_j1_4=fabs(_DeepAK8_Loose_Top_eta-j1_eta_4)
                                  _delta_eta_Loose_j2_4=fabs(_DeepAK8_Loose_Top_eta-j2_eta_4)
                                  _delta_eta_Loose_j3_4=fabs(_DeepAK8_Loose_Top_eta-j3_eta_4)

                                  _delta_R_Loose_j1_4=sqrt(pow(_delta_eta_Loose_j1_4,2)+pow(_delta_phi_Loose_j1_4,2))
                                  _delta_R_Loose_j2_4=sqrt(pow(_delta_eta_Loose_j2_4,2)+pow(_delta_phi_Loose_j2_4,2))
                                  _delta_R_Loose_j3_4=sqrt(pow(_delta_eta_Loose_j3_4,2)+pow(_delta_phi_Loose_j3_4,2))



                                  if(_delta_R_Loose_j1<0.8 or _delta_R_Loose_j2<0.8 or _delta_R_Loose_j3<0.8):
                                           flag_leq_08_loose_first_resolved_Top+=1

                                  if(_delta_R_Loose_j1_2<0.8 or _delta_R_Loose_j2_2<0.8 or _delta_R_Loose_j3_2<0.8):
                                           flag_leq_08_loose_second_resolved_Top+=1

                                  if(_delta_R_Loose_j1_3<0.8 or _delta_R_Loose_j2_3<0.8 or _delta_R_Loose_j3_3<0.8):
                                           flag_leq_08_loose_third_resolved_Top+=1

                                  if(_delta_R_Loose_j1_4<0.8 or _delta_R_Loose_j2_4<0.8 or _delta_R_Loose_j3_4<0.8):
                                           flag_leq_08_loose_fourth_resolved_Top+=1


                      if(nDeepAK8Loose>0):
                             if(flag_leq_08_loose_first_resolved_Top==0):
                                   nTop_Total+=1

                                   Resolved_Cleaned_pt.append(res[1])
                                   Resolved_Cleaned_eta.append(res[2])
                                   Resolved_Cleaned_phi.append(res[3])


                             if(flag_leq_08_loose_second_resolved_Top==0):
                                   nTop_Total+=1

                                   Resolved_Cleaned_pt.append(res[17])
                                   Resolved_Cleaned_eta.append(res[18])
                                   Resolved_Cleaned_phi.append(res[19])

                             if(flag_leq_08_loose_third_resolved_Top==0):
                                   nTop_Total+=1

                                   Resolved_Cleaned_pt.append(res[33])
                                   Resolved_Cleaned_eta.append(res[34])
                                   Resolved_Cleaned_phi.append(res[35])


                             if(flag_leq_08_loose_fourth_resolved_Top==0):
                                   nTop_Total+=1

                                   Resolved_Cleaned_pt.append(res[49])
                                   Resolved_Cleaned_eta.append(res[50])
                                   Resolved_Cleaned_phi.append(res[51])

                             
                             if((flag_leq_08_loose_first_resolved_Top!=0 and flag_leq_08_loose_second_resolved_Top==0 and flag_leq_08_loose_third_resolved_Top==0 and flag_leq_08_loose_fourth_resolved_Top==0) or (flag_leq_08_loose_first_resolved_Top==0 and flag_leq_08_loose_second_resolved_Top!=0 and flag_leq_08_loose_third_resolved_Top==0 and flag_leq_08_loose_fourth_resolved_Top==0) or (flag_leq_08_loose_first_resolved_Top==0 and flag_leq_08_loose_second_resolved_Top==0 and flag_leq_08_loose_third_resolved_Top!=0 and flag_leq_08_loose_fourth_resolved_Top==0) or (flag_leq_08_loose_first_resolved_Top==0 and flag_leq_08_loose_second_resolved_Top==0 and flag_leq_08_loose_third_resolved_Top==0 and flag_leq_08_loose_fourth_resolved_Top!=0)):

                                  for i_for_clean in range (1):
                                         Resolved_Cleaned_pt.append(0.)
                                         Resolved_Cleaned_eta.append(-6.)
                                         Resolved_Cleaned_phi.append(-3.2)
                              

                             elif((flag_leq_08_loose_first_resolved_Top!=0 and flag_leq_08_loose_second_resolved_Top!=0 and flag_leq_08_loose_third_resolved_Top==0 and flag_leq_08_loose_fourth_resolved_Top==0) or (flag_leq_08_loose_first_resolved_Top==0 and flag_leq_08_loose_second_resolved_Top!=0 and flag_leq_08_loose_third_resolved_Top!=0 and flag_leq_08_loose_fourth_resolved_Top==0) or (flag_leq_08_loose_first_resolved_Top==0 and flag_leq_08_loose_second_resolved_Top==0 and flag_leq_08_loose_third_resolved_Top!=0 and flag_leq_08_loose_fourth_resolved_Top!=0) or (flag_leq_08_loose_first_resolved_Top!=0 and flag_leq_08_loose_second_resolved_Top==0 and flag_leq_08_loose_third_resolved_Top==0 and flag_leq_08_loose_fourth_resolved_Top!=0) or (flag_leq_08_loose_first_resolved_Top!=0 and flag_leq_08_loose_second_resolved_Top==0 and flag_leq_08_loose_third_resolved_Top!=0 and flag_leq_08_loose_fourth_resolved_Top==0) or (flag_leq_08_loose_first_resolved_Top==0 and flag_leq_08_loose_second_resolved_Top!=0 and flag_leq_08_loose_third_resolved_Top==0 and flag_leq_08_loose_fourth_resolved_Top!=0) ):

                                  for i_for_clean in range (2):
                                         Resolved_Cleaned_pt.append(0.)
                                         Resolved_Cleaned_eta.append(-6.)
                                         Resolved_Cleaned_phi.append(-3.2)

                             elif((flag_leq_08_loose_first_resolved_Top!=0 and flag_leq_08_loose_second_resolved_Top!=0 and flag_leq_08_loose_third_resolved_Top!=0 and flag_leq_08_loose_fourth_resolved_Top==0) or (flag_leq_08_loose_first_resolved_Top==0 and flag_leq_08_loose_second_resolved_Top!=0 and flag_leq_08_loose_third_resolved_Top!=0 and flag_leq_08_loose_fourth_resolved_Top!=0) or (flag_leq_08_loose_first_resolved_Top!=0 and flag_leq_08_loose_second_resolved_Top==0 and flag_leq_08_loose_third_resolved_Top!=0 and flag_leq_08_loose_fourth_resolved_Top!=0) or (flag_leq_08_loose_first_resolved_Top!=0 and flag_leq_08_loose_second_resolved_Top!=0 and flag_leq_08_loose_third_resolved_Top==0 and flag_leq_08_loose_fourth_resolved_Top!=0)):

                                  for i_for_clean in range (3):
                                         Resolved_Cleaned_pt.append(0.)
                                         Resolved_Cleaned_eta.append(-6.)
                                         Resolved_Cleaned_phi.append(-3.2)

                             elif(flag_leq_08_loose_first_resolved_Top!=0 and flag_leq_08_loose_second_resolved_Top!=0 and flag_leq_08_loose_third_resolved_Top!=0 and flag_leq_08_loose_fourth_resolved_Top!=0):

                                  for i_for_clean in range (4):
                                         Resolved_Cleaned_pt.append(0.)
                                         Resolved_Cleaned_eta.append(-6.)
                                         Resolved_Cleaned_phi.append(-3.2)
                                          



                      elif(nDeepAK8Loose==0):
                             nTop_Total+=4

                             Resolved_Cleaned_pt.append(res[1])
                             Resolved_Cleaned_pt.append(res[17])
                             Resolved_Cleaned_pt.append(res[33])
                             Resolved_Cleaned_pt.append(res[49])


                             Resolved_Cleaned_eta.append(res[2])
                             Resolved_Cleaned_eta.append(res[18])
                             Resolved_Cleaned_eta.append(res[34])
                             Resolved_Cleaned_eta.append(res[50])


                             Resolved_Cleaned_phi.append(res[3])
                             Resolved_Cleaned_phi.append(res[19])
                             Resolved_Cleaned_phi.append(res[35])
                             Resolved_Cleaned_phi.append(res[51])


 
                out["nResolvedTop"] = NResolved
                out["nTop_Total_Combined"] = nTop_Total

                out["Resolved_Had_Top_mvaValue"] = Resolved_Top_mvaValue
                out["Resolved_Had_Top_pt"] = Resolved_Top_pt
                out["Resolved_Had_Top_eta"] = Resolved_Top_eta
                out["Resolved_Had_Top_phi"] = Resolved_Top_phi
                out["Resolved_Had_Top_mass"] = Resolved_Top_mass

                out["Resolved_Top_pt_Cleaned"] = Resolved_Cleaned_pt
                out["Resolved_Top_eta_Cleaned"] = Resolved_Cleaned_eta
                out["Resolved_Top_phi_Cleaned"] = Resolved_Cleaned_phi



########################################## Total b-tag cleaning ######################################################################################
                if "Flag_Btag_leq_08_from_Loose_DeepAK8" in base: Flag_Btag_leq_08_from_Loose_DeepAK8 = base["Flag_Btag_leq_08_from_Loose_DeepAK8"] 
                if "BTag_pt_Array" in base : BTag_pt_Array = base["BTag_pt_Array"]
                if "BTag_phi_Array" in base: BTag_phi_Array = base["BTag_phi_Array"]
                if "BTag_eta_Array" in base: BTag_eta_Array = base["BTag_eta_Array"]
 
                nBtag_cleaned_from_all_tops = 0

                _BTag_pt_Cleaned = []
                _BTag_eta_Cleaned = []
                _BTag_phi_Cleaned = []


                for i,j in enumerate(BTag_phi_Array):
                      flag_Btag_leq_04_from_B_of_resolved1 = 0
                      flag_Btag_leq_04_from_B_of_resolved2 = 0
                      flag_Btag_leq_04_from_B_of_resolved3 = 0
                      flag_Btag_leq_04_from_B_of_resolved4 = 0

                      if(res[0]>=0.):
                           delta_phi_1= fabs(acos(cos(j1_phi-BTag_phi_Array[i])))
                           delta_eta_1= fabs(acos(cos(j1_eta-BTag_eta_Array[i])))
                           delta_R_1=sqrt(pow(delta_eta_1,2)+pow(delta_phi_1,2))
                         
                           if(delta_R_1<0.4):
                                 flag_Btag_leq_04_from_B_of_resolved1+=1

                      if(res[16]>=0.):
                           delta_phi_2= fabs(acos(cos(j1_phi_2-BTag_phi_Array[i])))
                           delta_eta_2= fabs(acos(cos(j1_eta_2-BTag_eta_Array[i])))
                           delta_R_2=sqrt(pow(delta_eta_2,2)+pow(delta_phi_2,2))

                           if(delta_R_2<0.4):
                                 flag_Btag_leq_04_from_B_of_resolved2+=1

                      if(res[32]>=0.):
                           delta_phi_3= fabs(acos(cos(j1_phi_3-BTag_phi_Array[i])))
                           delta_eta_3= fabs(acos(cos(j1_eta_3-BTag_eta_Array[i])))
                           delta_R_3=sqrt(pow(delta_eta_3,2)+pow(delta_phi_3,2))

                           if(delta_R_3<0.4):
                                 flag_Btag_leq_04_from_B_of_resolved3+=1

                      if(res[48]>=0.):
                           delta_phi_4= fabs(acos(cos(j1_phi_4-BTag_phi_Array[i])))
                           delta_eta_4= fabs(acos(cos(j1_eta_4-BTag_eta_Array[i])))
                           delta_R_4=sqrt(pow(delta_eta_4,2)+pow(delta_phi_4,2))

                           if(delta_R_4<0.4):
                                 flag_Btag_leq_04_from_B_of_resolved4+=1

                     
                      ##### 0 resolved top case ########################################################################
                      if(res[0]<=0. and res[16]<=0. and res[32]<=0. and res[48]<=0.):
                               if(Flag_Btag_leq_08_from_Loose_DeepAK8[i]==0):
                                    nBtag_cleaned_from_all_tops+=1
                                    
                                    _BTag_pt_Cleaned.append(BTag_pt_Array[i])
                                    _BTag_eta_Cleaned.append(BTag_eta_Array[i])
                                    _BTag_phi_Cleaned.append(BTag_phi_Array[i])

                      ##### 1 resolved top case ########################################################################               
                      elif(res[0]>=0. and res[16]<=0. and res[32]<=0. and res[48]<=0.):
                               if(flag_leq_08_loose_first_resolved_Top==0):
                                     if(Flag_Btag_leq_08_from_Loose_DeepAK8[i]==0 and flag_Btag_leq_04_from_B_of_resolved1==0):
                                          nBtag_cleaned_from_all_tops+=1

                                          _BTag_pt_Cleaned.append(BTag_pt_Array[i])
                                          _BTag_eta_Cleaned.append(BTag_eta_Array[i])
                                          _BTag_phi_Cleaned.append(BTag_phi_Array[i])

                               else:
                                     if(Flag_Btag_leq_08_from_Loose_DeepAK8[i]==0 and flag_Btag_leq_04_from_B_of_resolved1==1):
                                          nBtag_cleaned_from_all_tops+=1

                                          _BTag_pt_Cleaned.append(BTag_pt_Array[i])
                                          _BTag_eta_Cleaned.append(BTag_eta_Array[i])
                                          _BTag_phi_Cleaned.append(BTag_phi_Array[i])

                      ##### 2 resolved top case ########################################################################               
                      elif(res[0]>=0. and res[16]>=0. and res[32]<=0. and res[48]<=0.):
                               if(flag_leq_08_loose_first_resolved_Top==0 and flag_leq_08_loose_second_resolved_Top==0):
                                      if(Flag_Btag_leq_08_from_Loose_DeepAK8[i]==0 and flag_Btag_leq_04_from_B_of_resolved1==0 and flag_Btag_leq_04_from_B_of_resolved2==0):
                                            nBtag_cleaned_from_all_tops+=1

                                            _BTag_pt_Cleaned.append(BTag_pt_Array[i])
                                            _BTag_eta_Cleaned.append(BTag_eta_Array[i])
                                            _BTag_phi_Cleaned.append(BTag_phi_Array[i])

                               elif(flag_leq_08_loose_first_resolved_Top!=0):
                                      if(Flag_Btag_leq_08_from_Loose_DeepAK8[i]==0 and flag_Btag_leq_04_from_B_of_resolved1==1):
                                            nBtag_cleaned_from_all_tops+=1

                                            _BTag_pt_Cleaned.append(BTag_pt_Array[i])
                                            _BTag_eta_Cleaned.append(BTag_eta_Array[i])
                                            _BTag_phi_Cleaned.append(BTag_phi_Array[i])


                               elif(flag_leq_08_loose_second_resolved_Top!=0):
                                      if(Flag_Btag_leq_08_from_Loose_DeepAK8[i]==0 and flag_Btag_leq_04_from_B_of_resolved2==1):
                                            nBtag_cleaned_from_all_tops+=1

                                            _BTag_pt_Cleaned.append(BTag_pt_Array[i])
                                            _BTag_eta_Cleaned.append(BTag_eta_Array[i])
                                            _BTag_phi_Cleaned.append(BTag_phi_Array[i])

                      ##### 3 resolved top case ########################################################################               
                      elif(res[0]>=0. and res[16]>=0. and res[32]>=0. and res[48]<=0.):
                               if(flag_leq_08_loose_first_resolved_Top==0 and flag_leq_08_loose_second_resolved_Top==0 and flag_leq_08_loose_third_resolved_Top==0):
                                      if(Flag_Btag_leq_08_from_Loose_DeepAK8[i]==0 and flag_Btag_leq_04_from_B_of_resolved1==0 and flag_Btag_leq_04_from_B_of_resolved2==0 and flag_Btag_leq_04_from_B_of_resolved3==0):
                                            nBtag_cleaned_from_all_tops+=1

                                            _BTag_pt_Cleaned.append(BTag_pt_Array[i])
                                            _BTag_eta_Cleaned.append(BTag_eta_Array[i])
                                            _BTag_phi_Cleaned.append(BTag_phi_Array[i])

                               elif(flag_leq_08_loose_first_resolved_Top!=0):
                                      if(Flag_Btag_leq_08_from_Loose_DeepAK8[i]==0 and flag_Btag_leq_04_from_B_of_resolved1==1):
                                            nBtag_cleaned_from_all_tops+=1

                                            _BTag_pt_Cleaned.append(BTag_pt_Array[i])
                                            _BTag_eta_Cleaned.append(BTag_eta_Array[i])
                                            _BTag_phi_Cleaned.append(BTag_phi_Array[i])

                               elif(flag_leq_08_loose_second_resolved_Top!=0):
                                      if(Flag_Btag_leq_08_from_Loose_DeepAK8[i]==0 and flag_Btag_leq_04_from_B_of_resolved2==1):
                                            nBtag_cleaned_from_all_tops+=1

                                            _BTag_pt_Cleaned.append(BTag_pt_Array[i])
                                            _BTag_eta_Cleaned.append(BTag_eta_Array[i])
                                            _BTag_phi_Cleaned.append(BTag_phi_Array[i])

                               elif(flag_leq_08_loose_third_resolved_Top!=0):
                                      if(Flag_Btag_leq_08_from_Loose_DeepAK8[i]==0 and flag_Btag_leq_04_from_B_of_resolved3==1):
                                            nBtag_cleaned_from_all_tops+=1

                                            _BTag_pt_Cleaned.append(BTag_pt_Array[i])
                                            _BTag_eta_Cleaned.append(BTag_eta_Array[i])
                                            _BTag_phi_Cleaned.append(BTag_phi_Array[i])

                      ##### 4 resolved top case ########################################################################               
                      elif(res[0]>=0. and res[16]>=0. and res[32]>=0. and res[48]>=0.):
                               if(flag_leq_08_loose_first_resolved_Top==0 and flag_leq_08_loose_second_resolved_Top==0 and flag_leq_08_loose_third_resolved_Top==0 and flag_leq_08_loose_fourth_resolved_Top==0):
                                      if(Flag_Btag_leq_08_from_Loose_DeepAK8[i]==0 and flag_Btag_leq_04_from_B_of_resolved1==0 and flag_Btag_leq_04_from_B_of_resolved2==0 and flag_Btag_leq_04_from_B_of_resolved3==0 and flag_Btag_leq_04_from_B_of_resolved4==0):
                                            nBtag_cleaned_from_all_tops+=1

                                            _BTag_pt_Cleaned.append(BTag_pt_Array[i])
                                            _BTag_eta_Cleaned.append(BTag_eta_Array[i])
                                            _BTag_phi_Cleaned.append(BTag_phi_Array[i])


                               elif(flag_leq_08_loose_first_resolved_Top!=0):
                                      if(Flag_Btag_leq_08_from_Loose_DeepAK8[i]==0 and flag_Btag_leq_04_from_B_of_resolved1==1):
                                            nBtag_cleaned_from_all_tops+=1

                                            _BTag_pt_Cleaned.append(BTag_pt_Array[i])
                                            _BTag_eta_Cleaned.append(BTag_eta_Array[i])
                                            _BTag_phi_Cleaned.append(BTag_phi_Array[i])


                               elif(flag_leq_08_loose_second_resolved_Top!=0):
                                      if(Flag_Btag_leq_08_from_Loose_DeepAK8[i]==0 and flag_Btag_leq_04_from_B_of_resolved2==1):
                                            nBtag_cleaned_from_all_tops+=1

                                            _BTag_pt_Cleaned.append(BTag_pt_Array[i])
                                            _BTag_eta_Cleaned.append(BTag_eta_Array[i])
                                            _BTag_phi_Cleaned.append(BTag_phi_Array[i])


                               elif(flag_leq_08_loose_third_resolved_Top!=0):
                                      if(Flag_Btag_leq_08_from_Loose_DeepAK8[i]==0 and flag_Btag_leq_04_from_B_of_resolved3==1):
                                            nBtag_cleaned_from_all_tops+=1

                                            _BTag_pt_Cleaned.append(BTag_pt_Array[i])
                                            _BTag_eta_Cleaned.append(BTag_eta_Array[i])
                                            _BTag_phi_Cleaned.append(BTag_phi_Array[i])


                               elif(flag_leq_08_loose_fourth_resolved_Top!=0):
                                      if(Flag_Btag_leq_08_from_Loose_DeepAK8[i]==0 and flag_Btag_leq_04_from_B_of_resolved4==1):
                                            nBtag_cleaned_from_all_tops+=1

                                            _BTag_pt_Cleaned.append(BTag_pt_Array[i])
                                            _BTag_eta_Cleaned.append(BTag_eta_Array[i])
                                            _BTag_phi_Cleaned.append(BTag_phi_Array[i])


                #print("nBtag_cleaned_from_all_tops: ",nBtag_cleaned_from_all_tops)
                out["nBCleaned_TOTAL"] = nBtag_cleaned_from_all_tops
                out["BTag_pt_Cleaned"] = _BTag_pt_Cleaned
                out["BTag_eta_Cleaned"] = _BTag_eta_Cleaned
                out["BTag_phi_Cleaned"] = _BTag_phi_Cleaned
                                                     
                #print("End of Btag array")

######################################### END of Total b-tag cleaning ############################################################################################################

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
            self.sf = BDT_resolvedTopTagger('../../data/kinMVA/tth/resTop_xGBoost_v0.weights.xml')
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
            print self.sf(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 500)

