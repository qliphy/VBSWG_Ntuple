from WMCore.Configuration import Configuration
config = Configuration()
config.section_("General")
config.General.requestName   = 'full_run2_2016_version5_seleB_v2'
config.General.transferLogs = True

config.section_("JobType")
config.JobType.maxMemoryMB = 3000
config.JobType.pluginName  = 'Analysis'
config.JobType.inputFiles =['Summer16_07Aug2017BCD_V11_DATA_L1FastJet_AK4PFchs.txt','Summer16_07Aug2017BCD_V11_DATA_L2Relative_AK4PFchs.txt','Summer16_07Aug2017BCD_V11_DATA_L3Absolute_AK4PFchs.txt','Summer16_07Aug2017BCD_V11_DATA_L2L3Residual_AK4PFchs.txt','Summer16_07Aug2017BCD_V11_DATA_L1FastJet_AK4PFPuppi.txt','Summer16_07Aug2017BCD_V11_DATA_L2Relative_AK4PFPuppi.txt','Summer16_07Aug2017BCD_V11_DATA_L3Absolute_AK4PFPuppi.txt','Summer16_07Aug2017BCD_V11_DATA_L2L3Residual_AK4PFPuppi.txt']

config.JobType.psetName    = 'analysis_data_BCD.py'
config.JobType.allowUndistributedCMSSW = True

config.section_("Data")
#config.Data.outputPrimaryDataset = 'VBS_WGAMMA_94X'
config.Data.inputDataset = '/SingleElectron/Run2016B-17Jul2018_ver2-v1/MINIAOD'
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 40
config.Data.lumiMask = 'Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'
config.Data.publication = False
config.Data.outputDatasetTag = 'full_run2_2016_version5_seleB_v2'

config.section_("Site")
config.Site.storageSite = 'T3_CH_CERNBOX'