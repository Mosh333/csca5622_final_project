import os
import pandas as pd
from bs4 import BeautifulSoup

# Function to check if the file is open
def is_file_open(file_path):
    try:
        # Try to open the file in append mode
        with open(file_path, 'a'):
            pass
        return False  # If the file opens successfully, it's not in use
    except IOError:
        return True  # If IOError occurs, the file is already open

# Function to parse and extract CPU data with flattened columns
def extract_cpu_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
    
    # Extract title (name)
    title = soup.title.string if soup.title else 'Unknown CPU'

    # Extract data from sectioncontainer
    section = soup.find('div', class_='sectioncontainer')
    
    if not section:
        return None

    specs = {'Name': title}
    
    # Extract all sections and tables inside the sectioncontainer
    for section_element in section.find_all('section', class_='details'):
        section_title = section_element.find('h1').get_text(strip=True)

        # Extracting table data (key-value pairs)
        for tr in section_element.find_all('tr'):
            th = tr.find('th')
            td = tr.find('td')
            if th and td:
                key = f"{section_title} - {th.get_text(strip=True)}"
                value = td.get_text(strip=True)
                specs[key] = value

    return specs

# Function to collect data from all CPU HTML files
def gather_cpu_data(cpu_dir):
    cpu_data = []
    for index, filename in enumerate(os.listdir(cpu_dir), 1):
        if filename.endswith(".html"):
            file_path = os.path.join(cpu_dir, filename)
            data = extract_cpu_data(file_path)
            if data:
                cpu_data.append(data)

        # Notify every 500 files processed
        if index % 500 == 0:
            print(f"Processed {index} CPU files...")
    
    # Convert list of dictionaries to a pandas DataFrame with flattened keys
    cpu_df = pd.DataFrame(cpu_data)
    
    return cpu_df

# Function to parse and extract GPU data
def extract_gpu_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
    
    # Extract title (name)
    title = soup.title.string if soup.title else 'Unknown GPU'

    # Extract data from sectioncontainer
    section = soup.find('div', class_='sectioncontainer')
    
    if not section:
        return None

    specs = {}
    # Extract key-value pairs in sectioncontainer
    for dl in section.find_all('dl'):
        dt = dl.find('dt').get_text(strip=True)
        dd = dl.find('dd').get_text(strip=True)
        specs[dt] = dd

    # Add title (GPU name) to specs
    specs['Name'] = title
    
    return specs

# Function to collect data from all GPU HTML files
def gather_gpu_data(gpu_dir):
    gpu_data = []
    for index, filename in enumerate(os.listdir(gpu_dir), 1):
        if filename.endswith(".html"):
            file_path = os.path.join(gpu_dir, filename)
            data = extract_gpu_data(file_path)
            if data:
                gpu_data.append(data)

        # Notify every 500 files processed
        if index % 500 == 0:
            print(f"Processed {index} GPU files...")

    # Convert list of dictionaries to a pandas DataFrame
    gpu_df = pd.DataFrame(gpu_data)
    return gpu_df

# Main execution
cpu_directory = os.path.join('..', 'data', 'cpu')
gpu_directory = os.path.join('..', 'data', 'gpu')

# Output file paths
cpu_csv_file = 'cpu_data_original.csv'
gpu_csv_file = 'gpu_data_original.csv'

# Check if files are open before starting
if is_file_open(cpu_csv_file):
    print(f"Error: The file {cpu_csv_file} is currently open. Please close it and try again.")
elif is_file_open(gpu_csv_file):
    print(f"Error: The file {gpu_csv_file} is currently open. Please close it and try again.")
else:
    # Proceed with the data processing
    cpu_df = gather_cpu_data(cpu_directory)
    gpu_df = gather_gpu_data(gpu_directory)

    # Save DataFrames to CSV for further analysis, appending "_original" to the filename
    cpu_df.to_csv(cpu_csv_file, index=False)
    gpu_df.to_csv(gpu_csv_file, index=False)

    # Final confirmation print
    print("CPU and GPU data have been successfully extracted and saved to CSV files.")
