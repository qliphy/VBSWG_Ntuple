import FWCore.ParameterSet.Config as cms

process = cms.Process( "TEST" )
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True),
				     SkipEvent = cms.untracked.vstring('ProductNotFound'))
corrJetsOnTheFly = True
runOnMC = True
chsorpuppi = True  # AK4Chs or AK4Puppi
#****************************************************************************************************#
process.load("Configuration.StandardSequences.GeometryRecoDB_cff")
process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_condDBv2_cff')
process.load("Configuration.StandardSequences.MagneticField_38T_cff")
process.load("RecoTracker.CkfPattern.CkfTrackCandidates_cff")
process.load("TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorAlong_cfi")

from Configuration.AlCa.GlobalTag import GlobalTag
if runOnMC:
	process.GlobalTag.globaltag = '102X_mcRun2_asymptotic_v8'
elif not(runOnMC):
	process.GlobalTag.globaltag = '102X_dataRun2_v13'

##########			                                                             
hltFiltersProcessName = 'RECO'
if runOnMC:
	hltFiltersProcessName = 'PAT' #'RECO'
reducedConversionsName = 'RECO'
if runOnMC:
	reducedConversionsName= 'PAT' #'RECO'

process.load("VAJets.PKUCommon.goodMuons_cff")
process.load("VAJets.PKUCommon.goodElectrons_cff")
process.load("VAJets.PKUCommon.goodPhotons_cff")
process.load("VAJets.PKUCommon.leptonicW_cff")
process.load("VAJets.PKUCommon.goodJets_cff")

#for egamma smearing
from RecoEgamma.EgammaTools.EgammaPostRecoTools import setupEgammaPostRecoSeq
setupEgammaPostRecoSeq(process,
						runVID=True,
						runEnergyCorrections=False, #no point in re-running them, they are already fine
						era='2016-Legacy')  #era is new to select between 2016 / 2017,  it defaults to 2017
#for egamma smearing

# If Update
process.goodMuons.src = "slimmedMuons"
process.goodElectrons.src = "slimmedElectrons"
process.goodPhotons.src = "slimmedPhotons"
process.Wtoenu.MET  = "slimmedMETs"
process.Wtomunu.MET = "slimmedMETs"

# jerc uncer 2017/5/7
if chsorpuppi:
		jLabel = "slimmedJets"
		jetAlgo    = 'AK4PFchs'
else:
		jLabel = "slimmedJetsPuppi"
		jetAlgo    = 'AK4PFPuppi'

jer_era = "Summer16_07Aug2017_V11_MC"
triggerResultsLabel      = "TriggerResults"
triggerSummaryLabel      = "hltTriggerSummaryAOD"
hltProcess = "HLT"

if runOnMC:
	jecLevelsAK4chs = [
			'Summer16_07Aug2017_V11_MC_L1FastJet_AK4PFchs.txt',
			'Summer16_07Aug2017_V11_MC_L2Relative_AK4PFchs.txt',
			'Summer16_07Aug2017_V11_MC_L3Absolute_AK4PFchs.txt'
	]

	jecLevelsAK4puppi = [
			'Summer16_07Aug2017_V11_MC_L1FastJet_AK4PFPuppi.txt',
			'Summer16_07Aug2017_V11_MC_L2Relative_AK4PFPuppi.txt',
			'Summer16_07Aug2017_V11_MC_L3Absolute_AK4PFPuppi.txt'
	]
else:
	jecLevelsAK4chs = [
			'Summer16_07Aug2017BCD_V11_DATA_L1FastJet_AK4PFchs.txt',
			'Summer16_07Aug2017BCD_V11_DATA_L2Relative_AK4PFchs.txt',
			'Summer16_07Aug2017BCD_V11_DATA_L3Absolute_AK4PFchs.txt',
			'Summer16_07Aug2017BCD_V11_DATA_L2L3Residual_AK4PFchs.txt'
	]

	jecLevelsAK4puppi = [
			'Summer16_07Aug2017BCD_V11_DATA_L1FastJet_AK4PFPuppi.txt',
			'Summer16_07Aug2017BCD_V11_DATA_L2Relative_AK4PFPuppi.txt',
			'Summer16_07Aug2017BCD_V11_DATA_L3Absolute_AK4PFPuppi.txt',
			'Summer16_07Aug2017BCD_V11_DATA_L2L3Residual_AK4PFPuppi.txt'
	]


process.JetUserData = cms.EDProducer(
	'JetUserData',
	jetLabel          = cms.InputTag(jLabel),
	rho               = cms.InputTag("fixedGridRhoFastjetAll"),
	coneSize          = cms.double(0.4),
	getJERFromTxt     = cms.bool(False),
	jetCorrLabel      = cms.string(jetAlgo),
	jerLabel          = cms.string(jetAlgo),
	resolutionsFile   = cms.string(jer_era+'_PtResolution_'+jetAlgo+'.txt'),
	scaleFactorsFile  = cms.string(jer_era+'_SF_'+jetAlgo+'.txt'),
	### TTRIGGER ###
	triggerResults = cms.InputTag(triggerResultsLabel,"",hltProcess),
	triggerSummary = cms.InputTag(triggerSummaryLabel,"",hltProcess),
	hltJetFilter       = cms.InputTag("hltPFHT"),
	hltPath            = cms.string("HLT_PFHT800"),
	hlt2reco_deltaRmax = cms.double(0.2),
	candSVTagInfos         = cms.string("pfInclusiveSecondaryVertexFinder"), 
	jecAK4chsPayloadNames_jetUserdata = cms.vstring( jecLevelsAK4chs ),
	vertex_jetUserdata = cms.InputTag("offlineSlimmedPrimaryVertices"),
	)

#jerc uncer Meng
process.load("VAJets.PKUCommon.goodJets_cff") 
if chsorpuppi:
	#process.goodAK4Jets.src = "slimmedJets"
	process.goodAK4Jets.src = "JetUserData"
else:
	process.goodAK4Jets.src = "slimmedJetsPuppi"
 
#process.goodOfflinePrimaryVertex = cms.EDFilter("VertexSelector",
#                                       src = cms.InputTag("offlineSlimmedPrimaryVertices"),
#                                       cut = cms.string("chi2!=0 && ndof >= 4.0 && abs(z) <= 24.0 && abs(position.Rho) <= 2.0"),
#                                       filter = cms.bool(False)
#                                       )

WBOSONCUT = "pt > 0.0"

process.leptonicVSelector = cms.EDFilter("CandViewSelector",
										src = cms.InputTag("leptonicV"),
										cut = cms.string( WBOSONCUT ), 
										filter = cms.bool(False)
										)

process.leptonicVFilter = cms.EDFilter("CandViewCountFilter",
										src = cms.InputTag("leptonicV"),
										minNumber = cms.uint32(0),
										#filter = cms.bool(False)
										)


process.leptonSequence = cms.Sequence(process.muSequence +
										process.egammaPostRecoSeq*#process.slimmedElectrons*process.slimmedPhotons+
										process.eleSequence +
										process.leptonicVSequence +
										process.leptonicVSelector +
										process.leptonicVFilter )

process.jetSequence = cms.Sequence(process.NJetsSequence)


process.load('RecoMET.METFilters.BadPFMuonFilter_cfi')
process.load("RecoMET.METFilters.BadChargedCandidateFilter_cfi")
process.BadPFMuonFilter.muons = cms.InputTag("slimmedMuons")
process.BadPFMuonFilter.PFCandidates = cms.InputTag("packedPFCandidates")
process.BadChargedCandidateFilter.muons = cms.InputTag("slimmedMuons")
process.BadChargedCandidateFilter.PFCandidates = cms.InputTag("packedPFCandidates")
process.metfilterSequence = cms.Sequence(process.BadPFMuonFilter+process.BadChargedCandidateFilter)

if chsorpuppi:
	ak4jecsrc = jecLevelsAK4chs
else:
	ak4jecsrc = jecLevelsAK4puppi

process.load("RecoEgamma/PhotonIdentification/photonIDValueMapProducer_cff")
#from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD 
## Example 1: If you only want to re-correct MET and get the proper uncertainties [e.g. when updating JEC]
#runMetCorAndUncFromMiniAOD(process,
#                           isData=False,
#                           )
   
# L1 prefiring
from PhysicsTools.PatUtils.l1ECALPrefiringWeightProducer_cfi import l1ECALPrefiringWeightProducer
process.prefiringweight = l1ECALPrefiringWeightProducer.clone(
	DataEra = cms.string("2016BtoH"), #Use 2016BtoH for 2016
	UseJetEMPt = cms.bool(False),
	PrefiringRateSystematicUncty = cms.double(0.2),
	SkipWarnings = False)

process.treeDumper = cms.EDAnalyzer("PKUTreeMaker",
									originalNEvents = cms.int32(1),
									crossSectionPb = cms.double(1),
									targetLumiInvPb = cms.double(1.0),
									PKUChannel = cms.string("VW_CHANNEL"),
									isGen = cms.bool(False),
									RunOnMC = cms.bool(runOnMC), 
									generator =  cms.InputTag("generator"),
									genJet =  cms.InputTag("slimmedGenJets"),
									lhe =  cms.InputTag("externalLHEProducer"),  #for multiple weight
									pileup  =   cms.InputTag("slimmedAddPileupInfo"),  
									leptonicVSrc = cms.InputTag("leptonicV"),
									rho = cms.InputTag("fixedGridRhoFastjetAll"),   
									ak4jetsSrc = cms.InputTag("cleanAK4Jets"),      
									#photonSrc = cms.InputTag("goodPhotons"),
									photonSrc = cms.InputTag("slimmedPhotons"),
									genSrc =  cms.InputTag("prunedGenParticles"),  
									jecAK4chsPayloadNames = cms.vstring( jecLevelsAK4chs ),
									jecAK4PayloadNames = cms.vstring( ak4jecsrc ),
									metSrc = cms.InputTag("slimmedMETs"),
									vertex = cms.InputTag("offlineSlimmedPrimaryVertices"),
									t1jetSrc_user = cms.InputTag("JetUserData"),
									t1jetSrc = cms.InputTag("slimmedJets"),      
									t1muSrc = cms.InputTag("slimmedMuons"),       
									looseelectronSrc = cms.InputTag("vetoElectrons"),
									electrons = cms.InputTag("slimmedElectrons"),
									conversions = cms.InputTag("reducedEgamma","reducedConversions",reducedConversionsName),
									beamSpot = cms.InputTag("offlineBeamSpot","","RECO"),
									loosemuonSrc = cms.InputTag("looseMuons"),

									goodmuonSrc = cms.InputTag("goodMuons"),
									goodeleSrc = cms.InputTag("goodElectrons"),

									hltToken    = cms.InputTag("TriggerResults","","HLT"),
									elPaths1     = cms.vstring("HLT_Ele23_WPTight_Gsf_v*"),
									elPaths2     = cms.vstring("HLT_Ele27_WPTight_Gsf_v*"),
									muPaths1     = cms.vstring("HLT_IsoMu20_v*","HLT_IsoTkMu20_v*"),
									muPaths2     = cms.vstring("HLT_IsoMu24_v*","HLT_IsoTkMu24_v*"),
									muPaths3     = cms.vstring("HLT_IsoMu27_v*","HLT_IsoTkMu27_v*"),
				    				
									noiseFilter = cms.InputTag('TriggerResults','', hltFiltersProcessName),
									noiseFilterSelection_HBHENoiseFilter = cms.string('Flag_HBHENoiseFilter'),
									noiseFilterSelection_HBHENoiseIsoFilter = cms.string("Flag_HBHENoiseIsoFilter"),
									noiseFilterSelection_globalTightHaloFilter = cms.string('Flag_globalTightHalo2016Filter'),
									noiseFilterSelection_EcalDeadCellTriggerPrimitiveFilter = cms.string('Flag_EcalDeadCellTriggerPrimitiveFilter'),
									noiseFilterSelection_goodVertices = cms.string('Flag_goodVertices'),
									noiseFilterSelection_eeBadScFilter = cms.string('Flag_eeBadScFilter'),
									noiseFilterSelection_badMuon = cms.InputTag('BadPFMuonFilter'),
									
									noiseFilterSelection_badChargedHadron = cms.InputTag('BadChargedCandidateFilter'),
									full5x5SigmaIEtaIEtaMap   = cms.InputTag("photonIDValueMapProducer:phoFull5x5SigmaIEtaIEta"),
									phoChargedIsolation = cms.InputTag("photonIDValueMapProducer:phoChargedIsolation"),
									phoNeutralHadronIsolation = cms.InputTag("photonIDValueMapProducer:phoNeutralHadronIsolation"),
									phoPhotonIsolation = cms.InputTag("photonIDValueMapProducer:phoPhotonIsolation"),
									effAreaChHadFile = cms.FileInPath("RecoEgamma/PhotonIdentification/data/Fall17/effAreaPhotons_cone03_pfChargedHadrons_90percentBased_V2.txt"),
									effAreaNeuHadFile= cms.FileInPath("RecoEgamma/PhotonIdentification/data/Fall17/effAreaPhotons_cone03_pfNeutralHadrons_90percentBased.txt"),
									effAreaPhoFile   = cms.FileInPath("RecoEgamma/PhotonIdentification/data/Fall17/effAreaPhotons_cone03_pfPhotons_90percentBased.txt")
                                    )

process.analysis = cms.Path(
							process.JetUserData +
							process.leptonSequence +
							process.jetSequence +
							process.metfilterSequence + #*process.treeDumper)
							process.prefiringweight*process.treeDumper)

### Source
process.load("VAJets.PKUCommon.data.RSGravitonToWW_kMpl01_M_1000_Tune4C_13TeV_pythia8")
process.source.fileNames = [
#"root://cms-xrd-global.cern.ch//store/mc/RunIISummer16MiniAODv2/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/80000/E6440217-0405-E811-8404-A0369F7F8E80.root "
"/store/mc/RunIISummer16MiniAODv3/WGJJToLNuGJJ_EWK_aQGC-FS-FM_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/60000/621BE097-93D2-E811-A989-0242AC130002.root",
"/store/mc/RunIISummer16MiniAODv3/WGJJToLNuGJJ_EWK_aQGC-FS-FM_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/60000/7A18A086-F2D2-E811-8182-E0071B73C600.root",
"/store/mc/RunIISummer16MiniAODv3/WGJJToLNuGJJ_EWK_aQGC-FS-FM_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/60000/AE7CF5AD-92D2-E811-99DA-0242AC130002.root",
"/store/mc/RunIISummer16MiniAODv3/WGJJToLNuGJJ_EWK_aQGC-FS-FM_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/60000/BC66A62C-93D2-E811-90C9-0242AC130002.root",
"/store/mc/RunIISummer16MiniAODv3/WGJJToLNuGJJ_EWK_aQGC-FS-FM_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/60000/CA3DBEDA-92D2-E811-82BB-0242AC130002.root",
"/store/mc/RunIISummer16MiniAODv3/WGJJToLNuGJJ_EWK_aQGC-FS-FM_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/60000/D4D7C4B7-92D2-E811-B030-0242AC130002.root",
"/store/mc/RunIISummer16MiniAODv3/WGJJToLNuGJJ_EWK_aQGC-FS-FM_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/60000/DE7A0BB5-92D2-E811-A437-0242AC130002.root",
"/store/mc/RunIISummer16MiniAODv3/WGJJToLNuGJJ_EWK_aQGC-FS-FM_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/60000/EA9F26FA-92D2-E811-823F-0242AC130002.root"
]

process.maxEvents.input = -1  #-1
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.MessageLogger.cerr.FwkReport.limit = 99999999

process.TFileService = cms.Service("TFileService",
									fileName = cms.string("/eos/user/j/jipeng/2016_aqgc_treePKU.root")
									)