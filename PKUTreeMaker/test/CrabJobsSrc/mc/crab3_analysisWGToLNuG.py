from WMCore.Configuration import Configuration
config = Configuration()
config.section_("General")
config.General.requestName   = 'full_run2_2018_WGJets_version1'
config.General.transferLogs = True

config.section_("JobType")
config.JobType.maxMemoryMB = 3000
config.JobType.pluginName  = 'Analysis'
config.JobType.inputFiles = ['Autumn18_V19_MC_L1FastJet_AK4PFchs.txt','Autumn18_V19_MC_L1FastJet_AK4PFPuppi.txt','Autumn18_V19_MC_L2L3Residual_AK4PFchs.txt','Autumn18_V19_MC_L2L3Residual_AK4PFPuppi.txt','Autumn18_V19_MC_L2Relative_AK4PFchs.txt','Autumn18_V19_MC_L2Relative_AK4PFPuppi.txt','Autumn18_V19_MC_L3Absolute_AK4PFchs.txt','Autumn18_V19_MC_L3Absolute_AK4PFPuppi.txt']
config.JobType.psetName    = 'analysis_mc.py'
config.JobType.allowUndistributedCMSSW = True

config.section_("Data")
##config.Data.outputPrimaryDataset = 'VBS_WGAMMA_94X'
config.Data.inputDataset = '/WGToLNuG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v1/MINIAODSIM'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 2
config.Data.totalUnits = -1
config.Data.publication = False
config.Data.outputDatasetTag = 'full_run2_2018_WGJets_version1'

config.section_("Site")
config.Site.storageSite = 'T3_CH_CERNBOX'
