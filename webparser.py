from bs4 import BeautifulSoup
import json

f = open('config.json')
data = json.load(f)

html_files = []

for i in data["2018"]:
    html_files.append(i)

def get_nickname(inp_str):

    data_units = ["Tau", 'EGamma', 'SingleMuon',
                  'DoubleMuon', ]
    
    inp_str = inp_str.replace('\n', '')

    first_part = inp_str.split("/")[1]
    second_part = inp_str.split("/")[2]

    if first_part not in data_units:

        pos = second_part.find('X')
        
        third_part = second_part[:pos + 1]

        return first_part + third_part
    else:
        mn = second_part.find("MiniAO")
        return first_part + second_part[:mn-1]


def get_folder_name(inp_str):
    pos = inp_str.find('TuneCP5')

    if inp_str.startswith("/\n"):
        return inp_str[2:pos-1]

    return inp_str[:pos-1]



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
            dataset_info.append((dataset_name, num_files, num_selected_events))
            dataset_dict["era"] = "2018"
            dataset_dict["dbs"] = "/sample/not/published"
            dataset_dict["generator_weight"] = 1.0
            dataset_dict["nevents"] = num_selected_events
            dataset_dict["nfiles"] = num_files
            dataset_dict["nick"] = get_nickname(dataset_name)
            # dataset_dict["filelist"] = ["root://eoscms.cern.ch//eos/cms/store/group/phys_higgs/HLepRare/HTT_skim_v1"+"Run2_2018"+get_folder_name(dataset_name)+"nanoHTT_"+str(i)+".root" for i in num_files]

            print(dataset_dict)
