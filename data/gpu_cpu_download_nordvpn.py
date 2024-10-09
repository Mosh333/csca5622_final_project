import os
import requests
from pathlib import Path
import sys
import time
import subprocess

# Add the src directory to the system path to allow importing gpu_cpu_link_web_scrape.py
sys.path.append('../src')

# Now import the GPU and CPU lists from gpu_cpu_link_web_scrape.py
from gpu_cpu_link_web_scrape import *

# Define base directories for GPU and CPU (now relative to the current data directory)
gpu_base_dir = Path('./gpu')
cpu_base_dir = Path('./cpu')

# Ensure directories exist
gpu_base_dir.mkdir(parents=True, exist_ok=True)
cpu_base_dir.mkdir(parents=True, exist_ok=True)

# Base URL for TechPowerUp
base_url = "https://www.techpowerup.com"

# List of NordVPN regions covering North America, Central America, South America, and Europe
vpn_regions = [
    'United States', 'Canada', 'Mexico',  # North America
    'Panama', 'Costa Rica',               # Central America
    'Brazil', 'Argentina', 'Chile',       # South America
    'United Kingdom', 'France', 'Germany', 'Netherlands', 'Spain', 'Italy', 'Switzerland', 'Sweden', 'Denmark', 
    'Belgium', 'Norway', 'Austria', 'Portugal', 'Poland', 'Finland', 'Ireland', 'Romania', 'Hungary'  # Europe
]
vpn_region_index = 0

def change_nordvpn_region():
    global vpn_region_index
    vpn_region_index = (vpn_region_index + 1) % len(vpn_regions)
    country = vpn_regions[vpn_region_index]
    print(f"Changing NordVPN region to {country}...")
    
    # Disconnect from current connection
    subprocess.run(["C:\\Program Files\\NordVPN\\NordVPN.exe", "-d"])
    
    # Connect to the new region
    subprocess.run(["C:\\Program Files\\NordVPN\\NordVPN.exe", "-c", "-g", country])
    
    print(f"Connected to {country}.")

def download_html(url_suffix, save_path):
    # Check if file already exists
    if save_path.exists():
        print(f"File {save_path} already exists. Skipping download.")
        return False  # No download occurred, return False
    
    # Download the file
    url = base_url + url_suffix
    print(f"Downloading {url}...")
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        # Save the HTML content to file
        save_path.write_text(response.text, encoding='utf-8')
        print(f"Saved to {save_path}")
        return True  # Download successful, return True
    except requests.exceptions.HTTPError as e:
        if response.status_code == 429:
            print(f"Error downloading {url}: {e} (Too Many Requests). Retrying without region change...")
            return 'retry'  # Retry without changing the region
    except requests.exceptions.ConnectionError as e:
        print(f"Error downloading {url}: {e} (Connection error). Changing region and retrying...")
        return 'vpn_change'  # Change VPN region on connection error
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return False  # Generic error

# Loop through years 2004 to 2024
for year in range(2004, 2025):
    # Fetch GPU and CPU list variables dynamically
    gpu_list = globals().get(f'gpu_{year}', [])
    cpu_list = globals().get(f'cpu_{year}', [])
    
    # Download and save GPU HTML files
    for gpu_suffix in gpu_list:
        gpu_file = gpu_base_dir / f'{gpu_suffix.split("/")[-1]}.html'
        result = download_html(gpu_suffix, gpu_file)
        if result == 'vpn_change':  # If connection issue, change VPN and retry
            change_nordvpn_region()
            time.sleep(60)  # Wait for 60 seconds before retrying
            download_html(gpu_suffix, gpu_file)  # Retry the download after VPN change
        elif result == 'retry':  # Retry immediately after a 429 error without region change
            download_html(gpu_suffix, gpu_file)
        elif result:  # If download was successful, wait 2 seconds
            time.sleep(2)

    # Download and save CPU HTML files
    for cpu_suffix in cpu_list:
        cpu_file = cpu_base_dir / f'{cpu_suffix.split("/")[-1]}.html'
        result = download_html(cpu_suffix, cpu_file)
        if result == 'vpn_change':  # If connection issue, change VPN and retry
            change_nordvpn_region()
            time.sleep(60)  # Wait for 60 seconds before retrying
            download_html(cpu_suffix, cpu_file)  # Retry the download after VPN change
        elif result == 'retry':  # Retry immediately after a 429 error without region change
            download_html(cpu_suffix, cpu_file)
        elif result:  # If download was successful, wait 2 seconds
            time.sleep(2)
