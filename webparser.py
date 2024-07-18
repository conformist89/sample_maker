from bs4 import BeautifulSoup
import json
import argparse
import os

# Parse arguments
parser = argparse.ArgumentParser(description='Parse HTML files from the CMS DAS website')
parser.add_argument("--era", help="Run 2 data taking period", type=str)
args = parser.parse_args()

f = open('config.json')
data = json.load(f)

html_files = []

for i in data[args.era]:
    html_files.append(i)

def get_nickname(inp_str):

    data_units = ["Tau", 'EGamma', 'SingleMuon',
                  'DoubleMuon', ]
    
    inp_str = inp_str.replace('\n', '')

    first_part = inp_str.split("/")[1]
    second_part = inp_str.split("/")[2]

    nicknm = ""

    if first_part not in data_units:

        pos = second_part.find('X')
        
        third_part = second_part[:pos + 1]

        nicknm = first_part + third_part.replace("MiniAODv2", "NanoAODv12")

        # return first_part + third_part.replace("MiniAODv2", "NanoAODv12")
    else:
        mn = second_part.find("MiniAO")
        nicknm = first_part + second_part[:mn-1].replace("MiniAODv2", "NanoAODv12")

    if "ext1" in inp_str:
        nicknm += "_ext1"
    return nicknm


def get_folder_name(inp_str):
    pos = inp_str.find('TuneCP5')

    if inp_str.startswith("/\n"):
        return inp_str[2:pos-1]

    return inp_str[:pos-1]


def get_xsec(sampledatabase_path, era):

    sample_typer = {
        'data' : ['SingleMuon', 'SingleElectron', 'EGamma', 'DoubleMuon', 'MuonEG', 'DoubleEG', ],
        'diboson': ['WZTo2Q2L_mllmin4p0_TuneCP5_13TeV-amcatnloFXFX', 'WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX', 'ZZTo2Q2L_mllmin4p0_TuneCP5_13TeV-amcatnloFXFX', 'ZZTo4L_TuneCP5_13TeV_powheg_pythia8'],
        
        'ttbar' : ['TTTo2L2Nu', 'TTToHadronic', 'TTToSemiLeptonic'],
        
        'singletop' : ['ST_t-channel_antitop_4f_InclusiveDecays', 'ST_t-channel_top_4f_InclusiveDecays', 'ST_tW_antitop_5f_inclusiveDecays', 'ST_tW_top_5f_inclusiveDecays'],
        
        'wjets' : ['WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8', 'WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8', 'WJetsToLNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8',
                   'WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia', 'WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8', 'WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8',
                   'WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8', 'WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8', 'WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8',
                   'WJetsToLNu_HT-70To100_TuneCP5_13TeV-madgraphMLM-pythia8','TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8', 
                   'WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8','WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8', 'WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8',
                   ],
        'dyjets' : ['DYJetsToLL_M-10to50_TuneCP5_13TeV-amcatnloFXFX-pythia8', 'DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8', 'DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8',
                    'DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8', 'DYJetsToLL_M-500to700_TuneCP5_13TeV-amcatnloFXFX-pythia8']
    }
    xsec = {}
    for key, value in sample_typer.items():

        directory = os.fsencode(sampledatabase_path+era+"/"+key)
    
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            f = open(sampledatabase_path+era+"/"+key+"/"+filename)
            data = json.load(f)

            for v in value:
                if v in data['nick']:
                    xsec[v] = data['xsec']

    return xsec

prefix = "/work/olavoryk/king_maker_setup/boosted_setup_upd/KingMaker/sample_database/"
xsec_dict = get_xsec(prefix, args.era)

def sample_xsec(sample_name, xsec_dict):
    xs = 1.0
    for key, value in xsec_dict.items():
        if key in sample_name:
            xs = value
            break
    return xs

def sample_typer(inp_str):

    inp_str = inp_str.replace('\n', '')
    sample_typer = {
        'data' : ['SingleMuon', 'SingleElectron', 'EGamma', 'DoubleMuon', 'MuonEG', 'DoubleEG', ],
        'diboson': ['WZTo2Q2L_mllmin4p0_TuneCP5_13TeV-amcatnloFXFX', 'WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX', 'ZZTo2Q2L_mllmin4p0_TuneCP5_13TeV-amcatnloFXFX', 'ZZTo4L_TuneCP5_13TeV_powheg_pythia8'],
        
        'ttbar' : ['TTTo2L2Nu', 'TTToHadronic', 'TTToSemiLeptonic'],
        
        'singletop' : ['ST_t-channel_antitop_4f_InclusiveDecays', 'ST_t-channel_top_4f_InclusiveDecays', 'ST_tW_antitop_5f_inclusiveDecays', 'ST_tW_top_5f_inclusiveDecays'],
        
        'wjets' : ['WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8', 'WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8', ],
        'dyjets' : ['DYJetsToLL_M-10to50_TuneCP5_13TeV-amcatnloFXFX-pythia8', 'DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8', 'DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8',
                    'DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8']
    }
        

    sample_type = 'unknown'
    for key, value in sample_typer.items():
        for v in value:
            if v in inp_str:
                sample_type = key
                break

    return sample_type     


for fullpath in html_files:
    
    with open(fullpath) as html_file:
        soup = BeautifulSoup(html_file, 'lxml')

        dataset_info = []
        dataset_dict = {}

        # Extract data from each row
        rows = soup.select('.jsgrid-table tbody tr.jsgrid-row, .jsgrid-table tbody tr.jsgrid-alt-row')
        for row in rows:
            columns = row.find_all('td')
            dataset_name = columns[1].text.strip()
            num_files = int(columns[3].text.strip())
            num_selected_events = int(columns[4].text.strip())
            sample_type = sample_typer(dataset_name)
            if sample_type != 'unknown':
                dataset_info.append((dataset_name, num_files, num_selected_events))
                dataset_dict["era"] = args.era
                dataset_dict["dbs"] = "/sample/not/published"
                dataset_dict["generator_weight"] = 1.0
                dataset_dict["nevents"] = num_selected_events
                dataset_dict["nfiles"] = num_files
                dataset_dict["nick"] = get_nickname(dataset_name)
                dataset_dict["sample_type"] = sample_type
                dataset_dict["xsec"] = sample_xsec(dataset_name, xsec_dict)
                # dataset_dict["filelist"] = ["root://eoscms.cern.ch//eos/cms/store/group/phys_higgs/HLepRare/HTT_skim_v1"+"Run2_2018"+get_folder_name(dataset_name)+"nanoHTT_"+str(i)+".root" for i in num_files]

                print(dataset_dict)
