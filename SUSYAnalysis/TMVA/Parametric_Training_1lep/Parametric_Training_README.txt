########### author : Pantelis Kontaxakis ##########
########### institute : National and Kapodistrian University of Athens #######################
########### Email : pantelis.kontaxakis@cern.ch #########
########### Date : March 2019 #######################

------Parametric Training for SUSY 1lep-ML analysis---------

Using the current development, the parametric training consists of three steps:

1st Step: Preparing for Parametric Training - Produce the appropriate Friend Trees (used only for training)
           
          -For this version of Parametric Training we use as parameter the difference between the masses of gluinos and neutralinos (dM_Go_LSP). In the training, components of this parameter are not meaningful for the bkg training samples. Thus, we can randomly assign values to those components of parameter according to the same distribution used for the signal class. It will be distributed as signal so it will not provide any discriminination.
          - "prepareEventVariablesFriendTree_Bkg_ONLY_Flat_dM_Go_LSP.py" module does this work: It produces Friend trees for Bkg ONLY where stores the "dM_Go_LSP" variable derived using the shape of the weighted signal events entering the training as probability density function. This module also stores the weights for Bkg ("weight_for_scale_35p9") so they can be used for the training as a single variable.
            
          IMPORTANT NOTE: For flattening the "dM_Go_LSP" variable we take into account that the following SUSY mass points are used for parametric training: 1.9/0.1, 1.9/1.0, 1.9/0.8, 1.5/1.0, 2.2/0.8, 2.2/0.1. Also, we consider weighted events for SIGNAL (see cfg file for parametric training: train_Parametric.py) and the following cuts are used for both BKG and SIGNAL:LT>=250. && HT>=500. && nJets30Clean>=5. && nBJet>=2. && dPhi>=0.75.
Currently, the flattening is "hard coded" but it will potentially improved in the near future.

2nd Step: Perform Parametric Training

          - After the Friend Tree production for Bkg with flat dM_Go_LSP (you can find the relevent Friend Trees for SIGNAL here:/nfs/dust/cms/group/susy-desy/Run2/MC/CMGtuples/Pantelis/SIGNAL_FRIENDS_PRIVATE_MC_MULTIPLE_MASS_POINTS_V2/OUTPUT2/FRIEND_TOTAL_SIGNAL.root) one can perform Parametric Training for BDT (AdaBoost) using the cfg file: "train_Parametric.py". The default training uses both Top Information and Kinematic Properties as input values, but this can be easily configured.

3rd Step: Produce Friend trees with the score of parametric BDT training stored

          - After the parametric training one can produce the Final Friend Trees for the analysis using the "prepareEventVariablesFriendTree_Parametric_Bkg.py" and "prepareEventVariablesFriendTree_Parametric_Signal.py" for BKG and SIGNAL respectively (separate production for BKG and SIGNAL from now but this will be merged into one general production... working on it).
