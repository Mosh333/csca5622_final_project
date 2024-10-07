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

# Base URLs for TechPowerUp GPU and CPU Specs by year
gpu_base_url = 'https://www.techpowerup.com/gpu-specs/?released='
cpu_base_url = 'https://www.techpowerup.com/cpu-specs/?released='

# List of years from 2004 to 2024
years = list(range(2004, 2024 + 1))

def get_filename_from_year_and_type(year, spec_type):
    # Generate the filename in the format <year>_<type>_database_TechPowerUp.html
    return f'{year}_{spec_type}_database_TechPowerUp.html'

def download_html_for_year(year, spec_type, base_url, directory):
    full_url = f'{base_url}{year}&sort=name'
    file_name = get_filename_from_year_and_type(year, spec_type)
    file_path = os.path.join(directory, file_name)

    # If file already exists, skip downloading
    if os.path.exists(file_path):
        print(f"{file_name} already exists. Skipping download.")
        return file_path

    try:
        print(f"Downloading {full_url}...")
        response = requests.get(full_url, timeout=10)  # Set a 10-second timeout for the request

        # Check if request was successful
        if response.status_code == 200:
            # Write the HTML content to a file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(response.text)
            print(f"Saved {file_name}")
            return file_path
        else:
            print(f"Error downloading {full_url}: {response.status_code}")
    except requests.exceptions.Timeout:
        print(f"Timeout error occurred for {year}. Retrying...")
        raise  # Raise the exception to trigger the retry
    except Exception as e:
        print(f"Failed to download {full_url}: {e}")
    return None

# Function to handle downloading for both GPU and CPU
def download_specs(spec_type, base_url, directory):
    idx = 0
    retries = 0
    while idx < len(years):
        year = years[idx]

        try:
            download_html_for_year(year, spec_type, base_url, directory)
            idx += 1  # Move to the next year only if the download is successful
            retries = 0  # Reset retries after successful download
        except requests.exceptions.Timeout:
            print(f"Retrying download for {spec_type} year {year} due to timeout...")
            retries += 1
            if retries >= 3:
                print(f"Skipping year {year} after 3 failed attempts.")
                idx += 1  # Move to the next year after 3 failed attempts
                retries = 0  # Reset retries for the next year
            else:
                # Decrement idx so it retries the same year
                print(f"Decrementing index to retry for year {year}")
                idx = max(0, idx - 1)  # Ensure idx doesn't go below 0

        time.sleep(1)  # Add a delay between requests to avoid overwhelming the server

        # Pause for 1 minute after every 7 iterations
        if idx % 7 == 0 and idx != 0:
            print(f"Pausing for 1 minute after {idx} {spec_type} iterations...")
            time.sleep(60)  # Sleep for 1 minute

# Start downloading GPU and CPU specs
download_specs('GPU', gpu_base_url, gpu_html_directory)
download_specs('CPU', cpu_base_url, cpu_html_directory)
