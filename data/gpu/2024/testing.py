from bs4 import BeautifulSoup

# Load the HTML file
with open(r"C:\Users\howla\OneDrive\Documents\GitHub\csca5622_final_project\data\gpu\2024\AMDRadeonRX7600XT.html", 'r', encoding='utf-8') as file:
    content = file.read()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(content, 'html.parser')

# Optional: Print the first 500 characters of the parsed HTML to verify structure
# print(soup.prettify()[:500])

# Try to find the GPU name in an h1 tag
gpu_name_tag = soup.find('h1', class_='gpudb-name')

if gpu_name_tag:
    gpu_name = gpu_name_tag.text.strip()
    print(f"GPU Name: {gpu_name}")
else:
    print("GPU Name not found. Check if the HTML structure is different or if the class name has changed.")

# Extract GPU specs from the dl (description list) elements, if available
specs = {}
for entry in soup.find_all('div', class_='gpudb-specs-large__entry'):
    key = entry.find('dt', class_='gpudb-specs-large__title')
    value = entry.find('dd', class_='gpudb-specs-large__value')
    
    if key and value:
        specs[key.text.strip()] = value.text.strip()

# Print all the extracted specs
if specs:
    print("\nGPU Specifications:")
    for key, value in specs.items():
        print(f"{key}: {value}")
else:
    print("No GPU specifications found. Verify the structure of the HTML.")

# Extract additional GPU details from other sections (e.g., clock speeds, memory)
details_sections = soup.find_all('section', class_='details')

if details_sections:
    for section in details_sections:
        section_title = section.find('h2')
        if section_title:
            print(f"\n{section_title.text.strip()}")
            for detail in section.find_all('dl', class_='clearfix'):
                key = detail.find('dt')
                value = detail.find('dd')
                if key and value:
                    print(f"{key.text.strip()}: {value.text.strip()}")
else:
    print("No additional GPU details found.")

print("\nProcessing completed successfully.")
