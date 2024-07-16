from bs4 import BeautifulSoup
import json

f = open('config.json')
data = json.load(f)

html_files = []

for i in data["2018"]:
    html_files.append(i)


for fullpath in html_files:
    
    with open(fullpath) as html_file:
        soup = BeautifulSoup(html_file, 'lxml')

        dataset_info = []

        # Extract data from each row
        rows = soup.select('.jsgrid-table tbody tr.jsgrid-row, .jsgrid-table tbody tr.jsgrid-alt-row')
        for row in rows:
            columns = row.find_all('td')
            dataset_name = columns[1].text.strip()
            num_files = int(columns[3].text.strip())
            num_selected_events = int(columns[4].text.strip())
            dataset_info.append((dataset_name, num_files, num_selected_events))

        # Print dataset information
        for name, files, events in dataset_info:
            print(f"Dataset Name: {name}")
            print(f"Number of Files: {files}")
            print(f"Number of Selected Events: {events}")
            print("=" * 20)
