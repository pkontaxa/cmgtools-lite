import os
import math
import ROOT
import pandas as pd

from optparse import OptionParser
from ROOT import RooFit as rf


def read_fratios(fratios_file):
    fDict = {}

    with open(fratios_file) as f:
        lines = f.readlines()

        for line in lines:
            if line[0] != '#':
                (bin, ratio, error) = line.split()
                bin = bin.replace('_NJ34', '')
                if 'LT' in bin:
                    fDict[bin] = (float(ratio), float(error))
    return fDict

def calculate_fraction_uncertainty(numerator, numerator_err, denominator, denominator_err):
    if (numerator <= 0) or (denominator <= 0):
        return 0
    fraction = numerator/denominator
    a = (numerator_err/numerator)**2 + (denominator_err/denominator)**2
    return fraction*math.sqrt(a)

def template_fit(inclusive_file, positive_file, negative_file, antisel_file, fratios_file, out_path, out_filename, verbose=False):

    template_df = pd.DataFrame(columns = ['bin', 'DataPos_yield', 'DataPos_yield_err', 'DataNeg_yield', 'DataNeg_yield_err', 'TTJets_yield', 'TTJets_yield_err',
                                          'WJetsPos_yield', 'WJetsPos_yield_err', 'WJetsNeg_yield', 'WJetsNeg_yield_err', 'QCD_yield', 'QCD_yield_err',
                                          'OtherPos_yield', 'OtherPos_yield_err', 'OtherNeg_yield', 'OtherNeg_yield_err', 'TotalPos_yield', 'TotalPos_yield_err',
                                          'TotalNeg_yield', 'TotalNeg_yield_err', 'TTJetsIncl_fraction', 'TTJetsIncl_fraction_err', 'TTJetsPos_fraction',
                                          'TTJetsPos_fraction_err', 'TTJetsNeg_fraction', 'TTJetsNeg_fraction_err', 'WJetsIncl_fraction', 'WJetsIncl_fraction_err',
                                          'WJetsPos_fraction', 'WJetsPos_fraction_err', 'WJetsNeg_fraction', 'WJetsNeg_fraction_err'])

    inclusive = ROOT.TFile(inclusive_file)
    positive = ROOT.TFile(positive_file)
    negative = ROOT.TFile(negative_file)
    antisel = ROOT.TFile(antisel_file)

    fratios = read_fratios(fratios_file)

    # Extract the bins
    bin_list = set()

    keylist = inclusive.GetListOfKeys()
    keylist_iterator = keylist.MakeIterator()

    for i in range(len(keylist)):
        object_name = keylist_iterator.Next().ReadObj().GetName()
        split_name = object_name.split("_") 
        bin_name = "%s_%s_%s_%s_%s" % (split_name[1], split_name[2], split_name[3], split_name[4], split_name[5])
        bin_list.add(bin_name) 
    
    counter = 0
    # Loop over the bins
    for bin_name in bin_list:
        
        template_QCD = inclusive.Get('nBJet_'+bin_name+'_QCD')
        template_TTJets = inclusive.Get('nBJet_'+bin_name+'_TTJets')
        template_WJets_PosPdg = positive.Get('nBJet_'+bin_name+'_WJets')
        template_WJets_NegPdg = negative.Get('nBJet_'+bin_name+'_WJets')
        template_Rest_PosPdg = positive.Get('nBJet_'+bin_name+'_Other')
        template_Rest_NegPdg = negative.Get('nBJet_'+bin_name+'_Other')

        hData_PosPdg = positive.Get('nBJet_'+bin_name+'_data')
        hData_NegPdg = negative.Get('nBJet_'+bin_name+'_data')
        hData_antisel = antisel.Get('nBJet_'+bin_name+'_data')
        
        template_QCD.GetXaxis().SetRangeUser(0., 4.)
        template_TTJets.GetXaxis().SetRangeUser(0., 4.)
        template_WJets_PosPdg.GetXaxis().SetRangeUser(0., 4.)
        template_WJets_NegPdg.GetXaxis().SetRangeUser(0., 4.)
        template_Rest_PosPdg.GetXaxis().SetRangeUser(0., 4.)
        template_Rest_NegPdg.GetXaxis().SetRangeUser(0., 4.)
        hData_PosPdg.GetXaxis().SetRangeUser(0., 4.)
        hData_NegPdg.GetXaxis().SetRangeUser(0., 4.)
        hData_antisel.GetXaxis().SetRangeUser(0., 4.)
        
        LT_bin = bin_name.split("_")[0]
        fratio = fratios[LT_bin][0]
        fratio_err = fratios[LT_bin][1]
        hQCD_pred = hData_antisel.Clone()
        hQCD_pred.Scale(fratio)
        hQCD_pred.Scale(0.5) # Split to pos/neg lep charges
        
        #print "Nominal yields data Pos:", hData_PosPdg.Integral()
        #print "Nominal yields data Neg:", hData_NegPdg.Integral()
        
        #print 'Error in the 0b bin of the data hist, neg PDG:',hData_NegPdg.GetBinError(1)
        #print 'Error in the 0b bin of the data hist, pos PDG:',hData_PosPdg.GetBinError(1)
        
        #print 'Resetting the errors!'
        #for i in range(1,4):
        #  print 'Yield and error before scaling',hData_NegPdg.GetBinContent(i), hData_NegPdg.GetBinError(i)
        #  hData_NegPdg.SetBinError(i, 10*hData_NegPdg.GetBinError(i))
        #  print 'Yield and error after scaling',hData_NegPdg.GetBinContent(i), hData_NegPdg.GetBinError(i)
        #  hData_PosPdg.SetBinError(i, 11*hData_PosPdg.GetBinError(i))
          
        ##print "BEFORE FIT YIELDS Templates before scaling:"
        ##print "template_WJets_NegPdg:" , template_WJets_NegPdg.Integral() 
        ##print "template_WJets_PosPdg:" , template_WJets_PosPdg.Integral()
        ##print "template_TTJets:" ,       template_TTJets.Integral()
        ##print "template_QCD:" ,       template_QCD.Integral()
        ##print "template_Rest_PosPdg:" ,  template_Rest_PosPdg.Integral()
        ##print "template_Rest_NegPdg:" ,  template_Rest_NegPdg.Integral()
        ###print "QCD yield", hQCD.Integral()
        
        # Normalize histograms
        bootstrap=False
        if bootstrap:
          template_TTJets = getRandomHistOfTemplate(template_TTJets)
          template_WJets_PosPdg = getRandomHistOfTemplate(template_WJets_PosPdg)
          template_WJets_NegPdg = getRandomHistOfTemplate(template_WJets_NegPdg)
          template_Rest_PosPdg = getRandomHistOfTemplate(template_Rest_PosPdg)
          template_Rest_NegPdg = getRandomHistOfTemplate(template_Rest_NegPdg)


        if template_TTJets.Integral()>0: template_TTJets.Scale(1./template_TTJets.Integral())
        template_WJets_PosPdg.Scale(1./template_WJets_PosPdg.Integral())
        template_WJets_NegPdg.Scale(1./template_WJets_NegPdg.Integral())
        y_Rest_PosPdg = template_Rest_PosPdg.Integral()
        y_Rest_NegPdg = template_Rest_NegPdg.Integral()
        if y_Rest_PosPdg>0: template_Rest_PosPdg.Scale(1./template_Rest_PosPdg.Integral())
        if y_Rest_NegPdg>0: template_Rest_NegPdg.Scale(1./template_Rest_NegPdg.Integral())
         

        y_QCD = hQCD_pred.Integral()
        if y_QCD > 0: hQCD_pred.Scale(1./hQCD_pred.Integral()) 
        #y_QCD = template_QCD.Integral()
        #if y_QCD > 0: template_QCD.Scale(1./template_QCD.Integral()) 

        #hData_PosPdg.Scale(1./hData_PosPdg.Integral())
        #hData_NegPdg.Scale(1./hData_NegPdg.Integral())
        #Observable
        nBTagVar = "nBJets"
        x=ROOT.RooRealVar(nBTagVar,nBTagVar,0.,4.)
        
        # import the contents of the histograms into RooDataHist objects
        data_PosPdg = ROOT.RooDataHist("data", "data", ROOT.RooArgList(x), hData_PosPdg)
        data_NegPdg = ROOT.RooDataHist("data", "data", ROOT.RooArgList(x), hData_NegPdg)

        dh_QCDpred = ROOT.RooDataHist("predQCD", "predQCD", ROOT.RooArgList(x), hQCD_pred)
        #dh_QCD = ROOT.RooDataHist("mcQCD", "mcQCD", ROOT.RooArgList(x), template_QCD)

        dh_WJets_PosPdg = ROOT.RooDataHist("mcWJets", "mcWJets", ROOT.RooArgList(x), template_WJets_PosPdg)
        dh_WJets_NegPdg = ROOT.RooDataHist("mcWJets", "mcWJets", ROOT.RooArgList(x), template_WJets_NegPdg)
        dh_TTJets = ROOT.RooDataHist("mcTTJets", "mcTTJets", ROOT.RooArgList(x), template_TTJets)
        dh_Rest_PosPdg = ROOT.RooDataHist("mcRest", "mcRest", ROOT.RooArgList(x), template_Rest_PosPdg)
        dh_Rest_NegPdg = ROOT.RooDataHist("mcRest", "mcRest", ROOT.RooArgList(x), template_Rest_NegPdg)
        
        #if y_QCD > 0:
        #  dh_QCD=ROOT.RooDataHist("predQCD","predQCD",ROOT.RooArgList(x),hQCD)
        #  rooDataHist_arr = [data_NegPdg , data_PosPdg , dh_WJets_PosPdg , dh_WJets_NegPdg , dh_TTJets , dh_Rest_PosPdg , dh_Rest_NegPdg, dh_QCD]
        #else:
        #  rooDataHist_arr = [data_NegPdg , data_PosPdg , dh_WJets_PosPdg , dh_WJets_NegPdg , dh_TTJets , dh_Rest_PosPdg , dh_Rest_NegPdg]
        
        rooDataHist_arr = [data_NegPdg, data_PosPdg, dh_WJets_PosPdg, dh_WJets_NegPdg, dh_TTJets, dh_QCDpred, dh_Rest_PosPdg, dh_Rest_NegPdg]
        #rooDataHist_arr = [data_NegPdg, data_PosPdg, dh_WJets_PosPdg, dh_WJets_NegPdg, dh_TTJets, dh_QCD, dh_Rest_PosPdg, dh_Rest_NegPdg]
        
        print "write RooDataHist values bin by bin"
        for hist in rooDataHist_arr:
          print "roo data hist: " , hist.Print()
          for i in range(hist.numEntries()): 
            hist.get(i)
            print "weight :" , hist.weight()
        
        #Define yields as variable
        yield_TTJets=ROOT.RooRealVar("ttJets_yield","yieldTTJets",0.1,0,10**5)
        yield_WJets_PosPdg = ROOT.RooRealVar("yield_WJets_PosPdg","yield_WJets_PosPdg",0.1,0,10**5)
        yield_WJets_NegPdg = ROOT.RooRealVar("yield_WJets_NegPdg","yield_WJets_NegPdg",0.1,0,10**5)
        yield_Rest_PosPdg = ROOT.RooRealVar("yield_Rest_PosPdg","yield_Rest_PosPdg",y_Rest_PosPdg,y_Rest_PosPdg,y_Rest_PosPdg)
        yield_Rest_NegPdg = ROOT.RooRealVar("yield_Rest_NegPdg","yield_Rest_NegPdg",y_Rest_NegPdg,y_Rest_NegPdg,y_Rest_NegPdg)
        yield_Rest_PosPdg.setConstant()
        yield_Rest_NegPdg.setConstant()
        if y_QCD > 0:
          yield_QCD = ROOT.RooRealVar("yield_QCD","yield_QCD",y_QCD,y_QCD,y_QCD)
          yield_QCD.setConstant()
        
        # print "BEFORE FIT YIELDS:"
        # print "yield_WJets_NegPdg:" , yield_WJets_NegPdg.getVal()
        # print "yield_WJets_PosPdg:" , yield_WJets_PosPdg.getVal()
        # print "yield_TTJets:" , yield_TTJets.getVal()
        # print "yield_QCD:" , yield_QCD.getVal()
        # print "yield_Rest_PosPdg:" , yield_Rest_PosPdg.getVal()
        # print "yield_Rest_NegPdg:" , yield_Rest_NegPdg.getVal()

        #Make PDF from MC histograms
        model_WJets_PosPdg=ROOT.RooHistPdf("model_WJets_PosPdg","model_WJets_PosPdg",ROOT.RooArgSet(x),dh_WJets_PosPdg)
        model_WJets_NegPdg=ROOT.RooHistPdf("model_WJets_NegPdg","model_WJets_NegPdg",ROOT.RooArgSet(x),dh_WJets_NegPdg)
        model_TTJets=ROOT.RooHistPdf("model_TTJets","model_TTJets",ROOT.RooArgSet(x),dh_TTJets)
        model_Rest_PosPdg=ROOT.RooHistPdf("model_Rest_PosPdg","model_Rest_PosPdg",ROOT.RooArgSet(x),dh_Rest_PosPdg)
        model_Rest_NegPdg=ROOT.RooHistPdf("model_Rest_NegPdg","model_Rest_NegPdg",ROOT.RooArgSet(x),dh_Rest_NegPdg)
        if y_QCD > 0: model_QCD=ROOT.RooHistPdf("model_QCD","model_QCD",ROOT.RooArgSet(x),dh_QCDpred)
        #if y_QCD > 0: model_QCD=ROOT.RooHistPdf("model_QCD","model_QCD",ROOT.RooArgSet(x),dh_QCD)
        
        #Make combined PDF of all MC Backgrounds
        if y_QCD > 0:
            model_PosPdg=ROOT.RooAddPdf("model_PosPdg","model_PosPdg",ROOT.RooArgList(model_WJets_PosPdg, model_TTJets, model_Rest_PosPdg, model_QCD),ROOT.RooArgList(yield_WJets_PosPdg, yield_TTJets, yield_Rest_PosPdg, yield_QCD))
            model_NegPdg=ROOT.RooAddPdf("model_NegPdg","model_NegPdg",ROOT.RooArgList(model_WJets_NegPdg, model_TTJets, model_Rest_NegPdg, model_QCD),ROOT.RooArgList(yield_WJets_NegPdg, yield_TTJets, yield_Rest_NegPdg, yield_QCD))
        else:
            model_PosPdg=ROOT.RooAddPdf("model_PosPdg","model_PosPdg",ROOT.RooArgList(model_WJets_PosPdg, model_TTJets, model_Rest_PosPdg),ROOT.RooArgList(yield_WJets_PosPdg, yield_TTJets, yield_Rest_PosPdg))
            model_NegPdg=ROOT.RooAddPdf("model_NegPdg","model_NegPdg",ROOT.RooArgList(model_WJets_NegPdg, model_TTJets, model_Rest_NegPdg),ROOT.RooArgList(yield_WJets_NegPdg, yield_TTJets, yield_Rest_NegPdg))
        #model_PosPdg=ROOT.RooAddPdf("model_PosPdg","model_PosPdg",ROOT.RooArgList(model_WJets_PosPdg, model_TTJets, model_Rest_PosPdg),ROOT.RooArgList(yield_WJets_PosPdg, yield_TTJets, yield_Rest_PosPdg))
        #model_NegPdg=ROOT.RooAddPdf("model_NegPdg","model_NegPdg",ROOT.RooArgList(model_WJets_NegPdg, model_TTJets, model_Rest_NegPdg),ROOT.RooArgList(yield_WJets_NegPdg, yield_TTJets, yield_Rest_NegPdg))

        #Plot the imported histogram(s)
        dframe=x.frame(rf.Title("Data"))
        data_PosPdg.plotOn(dframe)
        data_NegPdg.plotOn(dframe)
        
        frame_WJets_PosPdg=x.frame(rf.Title("WJets PosPdg"))
        model_WJets_PosPdg.plotOn(frame_WJets_PosPdg)
        frame_WJets_NegPdg=x.frame(rf.Title("WJets NegPdg"))
        model_WJets_NegPdg.plotOn(frame_WJets_NegPdg)
        
        frame_TTJets=x.frame(rf.Title("TTJets"))
        model_TTJets.plotOn(frame_TTJets)
        
        if y_QCD > 0:
            frame_QCD=x.frame(rf.Title("QCD"))
            model_QCD.plotOn(frame_QCD)
        
        frame_Rest_PosPdg=x.frame(rf.Title("Rest PosPdg"))
        model_Rest_PosPdg.plotOn(frame_Rest_PosPdg)
        frame_Rest_NegPdg=x.frame(rf.Title("Rest NegPdg"))
        model_Rest_NegPdg.plotOn(frame_Rest_NegPdg)
        
        #if y_QCD > 0:
        #  frame_QCD=x.frame(rf.Title("QCD"))
        #  model_QCD.plotOn(frame_QCD)
        
        #  c=ROOT.TCanvas("roofit_example","RooFitFractionFitExample",800,1200)
        #  c.Divide(1,3)
        #  ROOT.gROOT.SetStyle("Plain")#Removes gray background from plots
        #  c.cd(1)
        #  ROOT.gPad.SetLeftMargin(0.15)
        #  dframe.GetYaxis().SetTitleOffset(1.4)
        #  dframe.Draw()
        #  c.cd(2)
        #  ROOT.gPad.SetLeftMargin(0.15)
        #  frame_WJets_PosPdg.GetYaxis().SetTitleOffset(1.4)
        #  frame_WJets_PosPdg.Draw()
        #  frame_WJets_NegPdg.Draw('same')
        #  c.cd(3)
        #  ROOT.gPad.SetLeftMargin(0.15)
        #  frame_TTJets.GetYaxis().SetTitleOffset(1.4)
        #  frame_TTJets.Draw()
        
        
        #nll=model.createNLL(data,rf.NumCPU(1)) #From other example, looks like
        ##pll_phi=nll.createProfile(ROOT.RooArgSet(mc1_yield))#another way of doing the fitTo
        #
        #ROOT.RooMinuit(nll).migrad()
        #ROOT.RooMinuit(nll).hesse()
        #ROOT.RooMinuit(nll).minos()#optional
        
        #model.fitTo(data)#It is this fitTo command that gives the statistical output
        nllComponents = ROOT.RooArgList("nllComponents")
        nll_PosPdg=model_PosPdg.createNLL(data_PosPdg,rf.NumCPU(1))
        nll_NegPdg=model_NegPdg.createNLL(data_NegPdg,rf.NumCPU(1))
        nllComponents.add(nll_PosPdg)
        nllComponents.add(nll_NegPdg)
        
        #pll_phi=nll.createProfile(r.RooArgSet(mc1_yield))#anotherwayofdoingthefitTo
        sumNLL = ROOT.RooAddition("sumNLL","sumNLL", nllComponents)
        
        ROOT.RooMinuit(sumNLL).migrad()
        ROOT.RooMinuit(sumNLL).hesse()
        ROOT.RooMinuit(sumNLL).minos()#optional
        
        #myPdf->paramOn(frame,Layout(xmin,ymin,ymax))
        fitFrame_PosPdg=x.frame(rf.Bins(50),rf.Title("FitModel"))
        
        model_PosPdg.paramOn(fitFrame_PosPdg,rf.Layout(0.42,0.9,0.9))
        data_PosPdg.plotOn(fitFrame_PosPdg,rf.LineColor(ROOT.kRed))
        model_PosPdg.plotOn(fitFrame_PosPdg,rf.LineStyle(ROOT.kDashed))
        model_PosPdg.plotOn(fitFrame_PosPdg,rf.Components("model_WJets_PosPdg"),rf.LineColor(ROOT.kGreen))
        model_PosPdg.plotOn(fitFrame_PosPdg,rf.Components("model_TTJets"),rf.LineColor(ROOT.kBlue))
        model_PosPdg.plotOn(fitFrame_PosPdg,rf.Components("model_Rest_PosPdg"),rf.LineColor(ROOT.kOrange+7))
        if y_QCD > 0: model_PosPdg.plotOn(fitFrame_PosPdg,rf.Components("model_QCD"),rf.LineColor(ROOT.kCyan+1))
        #if y_QCD > 0: dh_QCDpred.plotOn(fitFrame_PosPdg,rf.LineColor(ROOT.kCyan+1))
        
        fitFrame_NegPdg=x.frame(rf.Bins(50),rf.Title("FitModel"))
        model_NegPdg.paramOn(fitFrame_NegPdg,rf.Layout(0.42,0.9,0.9))
        data_NegPdg.plotOn(fitFrame_NegPdg,rf.LineColor(ROOT.kRed))
        model_NegPdg.plotOn(fitFrame_NegPdg,rf.LineStyle(ROOT.kDashed))
        model_NegPdg.plotOn(fitFrame_NegPdg,rf.Components("model_WJets_NegPdg"),rf.LineColor(ROOT.kGreen))
        model_NegPdg.plotOn(fitFrame_NegPdg,rf.Components("model_TTJets"),rf.LineColor(ROOT.kBlue))
        model_NegPdg.plotOn(fitFrame_NegPdg,rf.Components("model_Rest_NegPdg"),rf.LineColor(ROOT.kOrange+7))
        #if y_QCD > 0: dh_QCDpred.plotOn(fitFrame_NegPdg,rf.LineColor(ROOT.kCyan+1))
        if y_QCD > 0: model_NegPdg.plotOn(fitFrame_NegPdg,rf.Components("model_QCD"),rf.LineColor(ROOT.kCyan+1))
        

        ##print "AFTER FIT YIELDS:"
        ##print "yield_WJets_NegPdg:" , yield_WJets_NegPdg.getVal()
        ##print "yield_WJets_PosPdg:" , yield_WJets_PosPdg.getVal()
        ##print "yield_TTJets:" , yield_TTJets.getVal()
        ##print "yield_Rest_PosPdg:" , yield_Rest_PosPdg.getVal()
        ##print "yield_Rest_NegPdg:" , yield_Rest_NegPdg.getVal()
        ##if y_QCD > 0: print "yield_QCD:", yield_QCD.getVal()
        
        c1=ROOT.TCanvas("c1","FitModel",650,1000)
        ROOT.gROOT.SetStyle("Plain")
        c1.Divide(1,2)
        c1.cd(1)
        ROOT.gROOT.SetStyle("Plain")
        ROOT.gPad.SetLeftMargin(0.15)
        fitFrame_PosPdg.GetYaxis().SetTitleOffset(1.4)
        fitFrame_PosPdg.GetXaxis().SetTitle(nBTagVar)
        fitFrame_PosPdg.Draw()
        
        c1.cd(2)
        ROOT.gROOT.SetStyle("Plain")
        ROOT.gPad.SetLeftMargin(0.15)
        fitFrame_NegPdg.GetYaxis().SetTitleOffset(1.4)
        fitFrame_NegPdg.GetXaxis().SetTitle(nBTagVar)
        fitFrame_NegPdg.Draw()


        # Get and save all the yields from the 0b bin 
        data_PosPdg.get(0)
        data_NegPdg.get(0)
        dh_TTJets.get(0)
        dh_WJets_PosPdg.get(0)
        dh_WJets_NegPdg.get(0)
        dh_Rest_PosPdg.get(0)
        dh_Rest_NegPdg.get(0)
        if y_QCD > 0:
            dh_QCDpred.get(0)

        dataPos_0b_yield = data_PosPdg.weight() 
        dataNeg_0b_yield = data_NegPdg.weight() 
        TTJets_0b_yield = 2*dh_TTJets.weight()*yield_TTJets.getVal()
        WJetsPos_0b_yield = dh_WJets_PosPdg.weight()*yield_WJets_PosPdg.getVal()
        WJetsNeg_0b_yield = dh_WJets_NegPdg.weight()*yield_WJets_NegPdg.getVal()
        OtherPos_0b_yield = dh_Rest_PosPdg.weight()*yield_Rest_PosPdg.getVal()
        OtherNeg_0b_yield = dh_Rest_NegPdg.weight()*yield_Rest_NegPdg.getVal()
        if y_QCD > 0:
            QCD_0b_yield = dh_QCDpred.weight()*yield_QCD.getVal()
        else:
            QCD_0b_yield = 0

        mcPos_0b_yield = 0.5*TTJets_0b_yield + WJetsPos_0b_yield + OtherPos_0b_yield + QCD_0b_yield
        mcNeg_0b_yield = 0.5*TTJets_0b_yield + WJetsNeg_0b_yield + OtherNeg_0b_yield + QCD_0b_yield
        
        #print '-- 0b Yields --'
        #print 'TTJets Inclusive:', TTJets_0b_yield
        #print 'TTJets Pos/Neg:', 0.5*TTJets_0b_yield
        #print 'WJets Positive:', WJetsPos_0b_yield
        #print 'WJets Negative:', WJetsNeg_0b_yield
        #print 'Other Positive:', OtherPos_0b_yield
        #print 'Other Negative:', OtherNeg_0b_yield
        #print 'QCD:', QCD_0b_yield
        #print 'Data Positive:', dataPos_0b_yield
        #print 'Data Negative:', dataNeg_0b_yield
        #print 'Total MC+QCD Positive:', mcPos_0b_yield
        #print 'Total MC+QCD Negative:', mcNeg_0b_yield

        TTJets_0b_err = 2*math.sqrt(dh_TTJets.weight())*yield_TTJets.getError()
        WJetsPos_0b_err = math.sqrt(dh_WJets_PosPdg.weight())*yield_WJets_PosPdg.getError()
        WJetsNeg_0b_err = math.sqrt(dh_WJets_NegPdg.weight())*yield_WJets_NegPdg.getError()
        OtherPos_0b_err = math.sqrt(dh_Rest_PosPdg.weight())*yield_Rest_PosPdg.getError()
        OtherNeg_0b_err = math.sqrt(dh_Rest_NegPdg.weight())*yield_Rest_NegPdg.getError()
        if y_QCD > 0:
            QCD_0b_err = math.sqrt((math.sqrt(QCD_0b_yield))**2 + fratio_err**2)
        else:
            QCD_0b_err = 0
        mcPos_0b_err = math.sqrt((0.5*TTJets_0b_err)**2 + WJetsPos_0b_err**2 + OtherPos_0b_err**2 + QCD_0b_err**2)
        mcNeg_0b_err = math.sqrt((0.5*TTJets_0b_err)**2 + WJetsNeg_0b_err**2 + OtherNeg_0b_err**2 + QCD_0b_err**2)

        #print '-- 0b Yield Uncertainties --'
        #print 'TTJets Inclusive:', TTJets_0b_err
        #print 'TTJets Pos/Neg:', 0.5*TTJets_0b_err
        #print 'WJets Positive:', WJetsPos_0b_err
        #print 'WJets Negative:', WJetsNeg_0b_err
        #print 'Other Positive:', OtherPos_0b_err
        #print 'Other Negative:', OtherNeg_0b_err
        #print 'QCD:', QCD_0b_err
        #print 'Data Positive:', math.sqrt(dataPos_0b_yield)
        #print 'Data Negative:', math.sqrt(dataNeg_0b_yield)
        #print 'Total MC+QCD Positive:', mcPos_0b_err
        #print 'Total MC+QCD Negative:', mcNeg_0b_err

        TTJetsIncl_0b_fraction = TTJets_0b_yield / (mcPos_0b_yield + mcNeg_0b_yield)
        TTJetsPos_0b_fraction = 0.5*TTJets_0b_yield / mcPos_0b_yield
        TTJetsNeg_0b_fraction = 0.5*TTJets_0b_yield / mcNeg_0b_yield
        WJetsIncl_0b_fraction = (WJetsPos_0b_yield + WJetsNeg_0b_yield) / (mcPos_0b_yield + mcNeg_0b_yield)
        WJetsPos_0b_fraction = WJetsPos_0b_yield / mcPos_0b_yield
        WJetsNeg_0b_fraction = WJetsNeg_0b_yield / mcNeg_0b_yield

        #print '-- 0b Fractions --'
        #print 'TTJets Inclusive:', TTJetsIncl_0b_fraction
        #print 'TTJets Postive:', TTJetsPos_0b_fraction
        #print 'TTJets Negative:', TTJetsNeg_0b_fraction
        #print 'WJets Inclusive:', WJetsIncl_0b_fraction
        #print 'WJets Positive:', WJetsPos_0b_fraction
        #print 'WJets Negative:', WJetsNeg_0b_fraction

        TTJetsIncl_0b_fraction_err = calculate_fraction_uncertainty(TTJets_0b_yield, TTJets_0b_err, mcPos_0b_yield+mcNeg_0b_yield, math.sqrt(mcPos_0b_err**2 + mcNeg_0b_err**2))
        TTJetsPos_0b_fraction_err = calculate_fraction_uncertainty(0.5*TTJets_0b_yield, 0.5*TTJets_0b_err, mcPos_0b_yield, mcPos_0b_err)
        TTJetsNeg_0b_fraction_err = calculate_fraction_uncertainty(0.5*TTJets_0b_yield, 0.5*TTJets_0b_err, mcNeg_0b_yield, mcNeg_0b_err)
        WJetsIncl_0b_fraction_err = calculate_fraction_uncertainty(WJetsPos_0b_yield+WJetsNeg_0b_yield, math.sqrt(WJetsPos_0b_err**2 + WJetsNeg_0b_err**2), mcPos_0b_yield+mcNeg_0b_yield, math.sqrt(mcPos_0b_err**2 + mcNeg_0b_err**2))
        WJetsPos_0b_fraction_err = calculate_fraction_uncertainty(WJetsPos_0b_yield, WJetsPos_0b_err, mcPos_0b_yield, mcPos_0b_err)
        WJetsNeg_0b_fraction_err = calculate_fraction_uncertainty(WJetsNeg_0b_yield, WJetsNeg_0b_err, mcNeg_0b_yield, mcNeg_0b_err)

        #print '-- 0b Fraction Uncertainties --'
        #print 'TTJets Inclusive:', TTJetsIncl_0b_fraction_err
        #print 'TTJets Postive:', TTJetsPos_0b_fraction_err
        #print 'TTJets Negative:', TTJetsNeg_0b_fraction_err
        #print 'WJets Inclusive:', WJetsIncl_0b_fraction_err
        #print 'WJets Positive:', WJetsPos_0b_fraction_err
        #print 'WJets Negative:', WJetsNeg_0b_fraction_err

        template_dict = {'bin' : bin_name,
                'DataPos_yield' : dataPos_0b_yield, 'DataPos_yield_err' : math.sqrt(dataPos_0b_yield),
                'DataNeg_yield' : dataNeg_0b_yield, 'DataNeg_yield_err' : math.sqrt(dataNeg_0b_yield),
                'TTJets_yield' : TTJets_0b_yield, 'TTJets_yield_err' : TTJets_0b_err,
                'WJetsPos_yield' : WJetsPos_0b_yield, 'WJetsPos_yield_err' : WJetsPos_0b_err,
                'WJetsNeg_yield' : WJetsNeg_0b_yield, 'WJetsNeg_yield_err' : WJetsNeg_0b_err,
                'QCD_yield' : QCD_0b_yield, 'QCD_yield_err' : QCD_0b_err,
                'OtherPos_yield' : OtherPos_0b_yield, 'OtherPos_yield_err' : OtherPos_0b_err,
                'OtherNeg_yield' : OtherNeg_0b_yield, 'OtherNeg_yield_err' : OtherNeg_0b_err,
                'TotalPos_yield' : mcPos_0b_yield, 'TotalPos_yield_err' : mcPos_0b_err,
                'TotalNeg_yield' : mcNeg_0b_yield, 'TotalNeg_yield_err' : mcNeg_0b_err,
                'TTJetsIncl_fraction' : TTJetsIncl_0b_fraction, 'TTJetsIncl_fraction_err' : TTJetsIncl_0b_fraction_err, 
                'TTJetsPos_fraction' : TTJetsPos_0b_fraction, 'TTJetsPos_fraction_err' : TTJetsPos_0b_fraction_err,
                'TTJetsNeg_fraction' : TTJetsNeg_0b_fraction, 'TTJetsNeg_fraction_err' : TTJetsNeg_0b_fraction_err, 
                'WJetsIncl_fraction' : WJetsIncl_0b_fraction, 'WJetsIncl_fraction_err' : WJetsIncl_0b_fraction_err, 
                'WJetsPos_fraction' : WJetsPos_0b_fraction, 'WJetsPos_fraction_err' : WJetsPos_0b_fraction_err,
                'WJetsNeg_fraction' : WJetsNeg_0b_fraction, 'WJetsNeg_fraction_err' : WJetsNeg_0b_fraction_err}

        template_df = template_df.append(template_dict, ignore_index=True)

        c1.Print(out_path+'/nBJetsTemplateFit_'+bin_name+'.png')
        c1.Print(out_path+'/nBJetsTemplateFit_'+bin_name+'.pdf')
        c1.Print(out_path+'/nBJetsTemplateFit_'+bin_name+'.root')


        #print 'Total Pos MC yield: ', mcPos_0b_yield
        #print 'Total Neg MC yield: ', mcNeg_0b_yield
        #print 'QCD yield: ', QCD_0b_yield
        #print 'Pos MC + QCD yield: ', mcPos_0b_yield + QCD_0b_yield
        #print 'Neg MC + QCD yield: ', mcNeg_0b_yield + QCD_0b_yield
        #print 'Data Pos yield: ', dataPos_0b_yield
        #print 'Data Neg yield: ', dataNeg_0b_yield

        ## used to print the matrices
        #print yield_TTJets.getVal()
        #
        #fit_res = model_PosPdg.fitTo(data_PosPdg, rf.Save())
        #cov_m = fit_res.covarianceMatrix()
        #cor_m = fit_res.correlationMatrix()
        #
        #cov_m.Print()
        #cor_m.Print()
        #
        #print yield_TTJets.getVal()

    template_df = template_df.sort_values(by=['bin'])
    template_df = template_df.reset_index(drop=True)
    template_df.to_csv(out_path+'/'+out_filename, sep=',')

if __name__ == "__main__":
    opt_parser = OptionParser()
    opt_parser.add_option("-v", "--verbose", dest="verbose", default=False)
    opt_parser.add_option("--year", dest="year")
    opt_parser.add_option("--syst", dest="systematic")
    opt_parser.add_option("--inclusive", dest="inclusive_file")
    opt_parser.add_option("--positive", dest="positive_file")
    opt_parser.add_option("--negative", dest="negative_file")
    opt_parser.add_option("--antisel", dest="antisel_file")
    opt_parser.add_option("--f-ratios", dest="fratios")
    opt_parser.add_option("--out", dest="out")
    (options, args) = opt_parser.parse_args()

    year = options.year
    systematic = options.systematic
    inc_hists = options.inclusive_file
    pos_hists = options.positive_file
    neg_hists = options.negative_file
    antisel_hists = options.antisel_file
    fratios = options.fratios
    out_path = options.out
    verbose = options.verbose

    if not os.path.exists(out_path):
        os.makedirs(out_path)

    out_filename = 'templateFits_0b_'+year+'_'+systematic+'.csv'

    template_fit(inc_hists, pos_hists, neg_hists, antisel_hists, fratios, out_path, out_filename, verbose)
