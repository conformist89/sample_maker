from bs4 import BeautifulSoup

# Read the HTML file
with open('/home/olavoryk/Downloads/Skimmed datasets.html', 'r', encoding='windows-1252') as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Initialize lists to store data
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
