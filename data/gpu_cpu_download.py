import os
import requests
from pathlib import Path
import sys
import time

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
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}. Skipping this link.")
        return False  # Skip and continue

# Loop through years 2004 to 2024
for year in range(2004, 2025):
    # Fetch GPU and CPU list variables dynamically
    gpu_list = globals().get(f'gpu_{year}', [])
    cpu_list = globals().get(f'cpu_{year}', [])
    
    # Download and save GPU HTML files
    for gpu_suffix in gpu_list:
        gpu_file = gpu_base_dir / f'{gpu_suffix.split("/")[-1]}.html'
        if download_html(gpu_suffix, gpu_file):  # Only wait after fresh download
            time.sleep(2)  # Wait 2 seconds between requests

    # Download and save CPU HTML files
    for cpu_suffix in cpu_list:
        cpu_file = cpu_base_dir / f'{cpu_suffix.split("/")[-1]}.html'
        if download_html(cpu_suffix, cpu_file):  # Only wait after fresh download
            time.sleep(2)  # Wait 2 seconds between requests
