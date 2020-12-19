from WMCore.Configuration import Configuration
config = Configuration()
config.section_("General")
config.General.requestName   = 'full_run2_2017_for_analysis_version5_TTGJ_v2'
config.General.transferLogs = True

config.section_("JobType")
config.JobType.maxMemoryMB = 3000
config.JobType.pluginName  = 'Analysis'
config.JobType.inputFiles = ['Fall17_17Nov2017_V32_MC_L1FastJet_AK4PFchs.txt','Fall17_17Nov2017_V32_MC_L1FastJet_AK4PFPuppi.txt','Fall17_17Nov2017_V32_MC_L2L3Residual_AK4PFchs.txt','Fall17_17Nov2017_V32_MC_L2L3Residual_AK4PFPuppi.txt','Fall17_17Nov2017_V32_MC_L2Relative_AK4PFchs.txt','Fall17_17Nov2017_V32_MC_L2Relative_AK4PFPuppi.txt','Fall17_17Nov2017_V32_MC_L3Absolute_AK4PFchs.txt','Fall17_17Nov2017_V32_MC_L3Absolute_AK4PFPuppi.txt']
config.JobType.psetName    = 'analysis_mc.py'
config.JobType.allowUndistributedCMSSW = True

config.section_("Data")
##config.Data.outputPrimaryDataset = 'VBS_WGAMMA_94X'
config.Data.inputDataset = '/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v2/MINIAODSIM'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 2
config.Data.totalUnits = -1
config.Data.publication = False
config.Data.outputDatasetTag = 'full_run2_2017_for_analysis_version5_TTGJ_v2'

config.section_("Site")
config.Site.storageSite = 'T3_CH_CERNBOX'
