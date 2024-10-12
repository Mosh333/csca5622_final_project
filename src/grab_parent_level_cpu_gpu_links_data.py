import os
import requests
import time

# Define the relative paths to save HTML files for GPU and CPU
gpu_html_directory = os.path.join('..', 'data', 'gpu')
cpu_html_directory = os.path.join('..', 'data', 'cpu')

# Create the directories if they don't exist
for directory in [gpu_html_directory, cpu_html_directory]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Base URLs for TechPowerUp GPU and CPU Specs by year and manufacturer
gpu_base_url = 'https://www.techpowerup.com/gpu-specs/?mfgr={}&released={}&sort=name'
cpu_base_url = 'https://www.techpowerup.com/cpu-specs/?mfgr={}&released={}&sort=name'
cpu_mobile_filter_url = 'https://www.techpowerup.com/cpu-specs/?mfgr={}&released={}&mobile={}&sort=name'

# Intel hard-coded queries for 2023 (socket types)
intel_2023_queries = [
    'https://www.techpowerup.com/cpu-specs/?mfgr=Intel&released=2023&mobile=No&socket=Intel%20BGA%202579&sort=name',
    'https://www.techpowerup.com/cpu-specs/?mfgr=Intel&released=2023&mobile=No&socket=Intel%20Socket%201700&sort=name',
    'https://www.techpowerup.com/cpu-specs/?mfgr=Intel&released=2023&mobile=No&socket=Intel%20Socket%204677&sort=name'
]

intel_server_queries = {
    2021: [
        'https://www.techpowerup.com/cpu-specs/?mfgr=Intel&released=2021&mobile=No&server=No&sort=name',
        'https://www.techpowerup.com/cpu-specs/?mfgr=Intel&released=2021&mobile=No&server=Yes&sort=name'
    ],
    2014: [
        'https://www.techpowerup.com/cpu-specs/?mfgr=Intel&released=2014&mobile=No&server=No&sort=name',
        'https://www.techpowerup.com/cpu-specs/?mfgr=Intel&released=2014&mobile=No&server=Yes&sort=name'
    ],
    2012: [
        'https://www.techpowerup.com/cpu-specs/?mfgr=Intel&released=2012&mobile=No&server=No&sort=name',
        'https://www.techpowerup.com/cpu-specs/?mfgr=Intel&released=2012&mobile=No&server=Yes&sort=name'
    ]
}

# List of years from 2004 to 2024
years = list(range(2004, 2024 + 1))
gpu_manufacturers = ['AMD', 'Intel', 'NVIDIA']
cpu_manufacturers = ['AMD', 'Intel']

# List of years with more than 100 CPUs for Intel and AMD, techpowerup limits query result to 100 max
intel_cpu_years_over_100 = [2024, 2023, 2021, 2015, 2014, 2013, 2012, 2011, 2010]
amd_cpu_years_over_100 = [2005, 2023]

# Intel filtering for years with more than 100 CPUs and mobile=no
intel_additional_filters = {
    2023: {
        'mobile_no': ['Intel BGA 2579', 'Intel BGA 1700', 'Intel BGA 4677']
    },
    2021: {
        'mobile_no': ['server_yes', 'server_no']
    },
    2014: {
        'mobile_no': ['server_yes', 'server_no']
    },
    2012: {
        'mobile_no': ['server_yes', 'server_no']
    }
}

# Helper function to generate filenames based on year, spec type, and manufacturer
def get_filename_from_year_and_type(year, spec_type, manufacturer=None, mobile=None, filter_type=None):
    file_name = f'{year}_{manufacturer}_{spec_type}_database_TechPowerUp.html'
    if mobile is not None:
        file_name = file_name.replace('.html', f'_{mobile}_mobile.html')
    if filter_type:
        file_name = file_name.replace('.html', f'_{filter_type}.html')
    return file_name

# Function to download HTML for a specific year and manufacturer (handles GPU)
def download_html_for_year_and_manufacturer(year, manufacturer, spec_type, base_url, directory):
    full_url = base_url.format(manufacturer, year)
    file_name = get_filename_from_year_and_type(year, spec_type, manufacturer)
    file_path = os.path.join(directory, file_name)

    if os.path.exists(file_path):
        print(f"{file_name} already exists. Skipping download.")
        return True

    try:
        print(f"Downloading {full_url}...")
        response = requests.get(full_url, timeout=10)
        if response.status_code == 200:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(response.text)
            print(f"Saved {file_name}")
            return True
        else:
            print(f"Error downloading {full_url}: {response.status_code}")
            return False
    except requests.exceptions.Timeout:
        print(f"Timeout error for {year} - {manufacturer}. Retrying...")
        return False
    except Exception as e:
        print(f"Failed to download {full_url}: {e}")
        return False

# Function to download HTML for Intel 2023 using hard-coded queries
def download_html_for_intel_2023(directory):
    for url in intel_2023_queries:
        # Extract the socket name to use in the filename
        socket_name = url.split('socket=')[1].replace('%20', '_')
        file_name = f'2023_Intel_CPU_database_TechPowerUp_No_mobile_{socket_name}.html'
        file_path = os.path.join(directory, file_name)

        if os.path.exists(file_path):
            print(f"{file_name} already exists. Skipping download.")
            continue

        try:
            print(f"Downloading {url}...")
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(response.text)
                print(f"Saved {file_name}")
            else:
                print(f"Error downloading {url}: {response.status_code}")
        except requests.exceptions.Timeout:
            print(f"Timeout error for Intel 2023 socket query {url}. Retrying...")
        except Exception as e:
            print(f"Failed to download {url}: {e}")

# Function to download HTML for CPU with mobile and additional filters
def download_html_for_year_and_manufacturer_with_filters(year, manufacturer, spec_type, base_url, directory, mobile=None, filter_type=None):
    mobile_filter = 'Yes' if mobile else 'No' if mobile is not None else ''
    additional_filter = f'&socket={filter_type}' if filter_type and 'socket' in filter_type else f'&server={filter_type}' if filter_type and 'server' in filter_type else ''
    
    full_url = base_url.format(manufacturer, year, mobile_filter) + additional_filter
    file_name = get_filename_from_year_and_type(year, spec_type, manufacturer, mobile_filter, filter_type)
    file_path = os.path.join(directory, file_name)

    if os.path.exists(file_path):
        print(f"{file_name} already exists. Skipping download.")
        return True

    try:
        print(f"Downloading {full_url}...")
        response = requests.get(full_url, timeout=10)
        if response.status_code == 200:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(response.text)
            print(f"Saved {file_name}")
            return True
        else:
            print(f"Error downloading {full_url}: {response.status_code}")
            return False
    except requests.exceptions.Timeout:
        print(f"Timeout error for {year} - {manufacturer}. Retrying...")
        return False
    except Exception as e:
        print(f"Failed to download {full_url}: {e}")
        return False

# Function to download GPU specs
def download_gpu_specs():
    idx = 0
    retries = 0
    total_iterations = len(years) * len(gpu_manufacturers)
    iteration_count = 0

    while idx < len(years):
        year = years[idx]

        for manufacturer in gpu_manufacturers:
            success = download_html_for_year_and_manufacturer(year, manufacturer, 'GPU', gpu_base_url, gpu_html_directory)
            iteration_count += 1

            if success:
                retries = 0  # Reset retries after successful download
            else:
                retries += 1
                if retries >= 3:
                    print(f"Skipping year {year} - {manufacturer} after 3 failed attempts.")
                    retries = 0  # Reset retries for the next year
                else:
                    print(f"Retrying download for {manufacturer} year {year} due to error...")
                    time.sleep(1)  # Wait before retrying
                    iteration_count -= 1  # Adjust for retry

            time.sleep(1)  # Delay to avoid overwhelming the server

            # Pause every 7 iterations
            if iteration_count % 7 == 0 and iteration_count != 0:
                print(f"Pausing for after {iteration_count} GPU iterations...")
                time.sleep(0.5)

        idx += 1  # Move to the next year

# Function to download HTML for Intel 2021, 2014, and 2012 using hard-coded queries
def download_html_for_intel_with_server_filters(year, directory):
    if year not in intel_server_queries:
        return
    
    for url in intel_server_queries[year]:
        # Extract the server type from the URL for the filename
        server_type = "server_no" if "server=No" in url else "server_yes"
        file_name = f'{year}_Intel_CPU_database_TechPowerUp_No_mobile_{server_type}.html'
        file_path = os.path.join(directory, file_name)

        if os.path.exists(file_path):
            print(f"{file_name} already exists. Skipping download.")
            continue

        try:
            print(f"Downloading {url}...")
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(response.text)
                print(f"Saved {file_name}")
            else:
                print(f"Error downloading {url}: {response.status_code}")
        except requests.exceptions.Timeout:
            print(f"Timeout error for Intel {year} server query {url}. Retrying...")
        except Exception as e:
            print(f"Failed to download {url}: {e}")

# Function to download CPU specs with filtering for Intel and AMD
def download_cpu_specs_with_filters():
    for year in years:
        # Process AMD CPUs (even if they are not in amd_cpu_years_over_100)
        if year in amd_cpu_years_over_100:
            print(f"Processing AMD CPUs for year {year} with more than 100 CPUs")
            for mobile_status in [True, False]:
                download_html_for_year_and_manufacturer_with_filters(year, 'AMD', 'CPU', cpu_mobile_filter_url, cpu_html_directory, mobile=mobile_status)
        else:
            print(f"Processing AMD CPUs for year {year}")
            download_html_for_year_and_manufacturer(year, 'AMD', 'CPU', cpu_base_url, cpu_html_directory)

        # Process Intel CPUs separately (even if AMD was processed)
        if year in intel_cpu_years_over_100:
            print(f"Processing Intel CPUs for year {year}")
            for mobile_status in [True, False]:
                if year == 2023 and not mobile_status:
                    download_html_for_intel_2023(cpu_html_directory)
                elif year in intel_server_queries and not mobile_status:
                    # Use hard-coded queries for Intel 2021, 2014, 2012
                    download_html_for_intel_with_server_filters(year, cpu_html_directory)
                elif year in intel_additional_filters and not mobile_status:
                    for filter_type in intel_additional_filters[year]['mobile_no']:
                        download_html_for_year_and_manufacturer_with_filters(year, 'Intel', 'CPU', cpu_mobile_filter_url, cpu_html_directory, mobile=mobile_status, filter_type=filter_type)
                else:
                    download_html_for_year_and_manufacturer_with_filters(year, 'Intel', 'CPU', cpu_mobile_filter_url, cpu_html_directory, mobile=mobile_status)

        # Process other years (if needed)
        else:
            for manufacturer in cpu_manufacturers:
                download_html_for_year_and_manufacturer(year, manufacturer, 'CPU', cpu_base_url, cpu_html_directory)





# Start downloading GPU and CPU specs
download_gpu_specs()
download_cpu_specs_with_filters()

print("Script finished!")
