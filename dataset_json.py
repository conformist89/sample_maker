import json
import argparse
import os

main_dict = {}

# Parse arguments
parser = argparse.ArgumentParser(description='Parse sample maker json files')
parser.add_argument("--era", help="Run 2 data taking period", type=str)
parser.add_argument("--inpfold", help="Intup folder", type=str)
args = parser.parse_args()



root_path = "%s/%s" % (args.inpfold, args.era)


for path, subdirs, files in os.walk(root_path):
    for name in files:
        # print(os.path.join(path, name))

        sample_dict = {}    
        with open(os.path.join(path, name)) as json_file:
            data = json.load(json_file)
            sample_dict['dbs'] = data['dbs']
            sample_dict["era"] = data["era"]
            sample_dict["generator_weight"] = data["generator_weight"]
            sample_dict["nevents"] = data["nevents"]
            sample_dict['nfiles'] = data['nfiles']
            sample_dict['nick'] = data['nick']
            sample_dict['sample_type'] = data['sample_type']
            sample_dict['xsec'] = data['xsec']
        
        main_dict[data['nick']] = sample_dict


# Write the dictionary to a JSON file
with open( "%s/datasets.json" % (args.inpfold), 'w') as file:
    json.dump(main_dict, file, indent=4)

    