import re
import os

def extract_gpu_specs_by_year(directory, output_file):
    # Dictionary to store lists of GPU specs URLs grouped by year
    gpu_specs_by_year = {}

    # Regular expression pattern to match the GPU specs URLs
    pattern = r'/gpu-specs/[^"]*'

    # Loop over the files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            # Extract the year from the filename (first four digits)
            year_match = re.search(r'(\d{4})', filename)
            if not year_match:
                print(f"No valid year found in the filename {filename}.")
                continue

            year = year_match.group(1)

            try:
                # Open the file and read its content
                filepath = os.path.join(directory, filename)
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                    # Find all matches in the content
                    matches = re.findall(pattern, content)

                    # Add matches to the appropriate year's list
                    if year not in gpu_specs_by_year:
                        gpu_specs_by_year[year] = []
                    gpu_specs_by_year[year].extend(matches)

            except FileNotFoundError:
                print(f"File {filename} not found.")
    
    # Sort the years before writing to the output file
    with open(output_file, 'w') as f:
        for year in sorted(gpu_specs_by_year.keys()):
            f.write(f"gpu_{year} = [\n")
            for idx, spec in enumerate(gpu_specs_by_year[year]):
                if idx == len(gpu_specs_by_year[year]) - 1:
                    f.write(f"    '{spec}'\n")  # Last item, no trailing comma
                else:
                    f.write(f"    '{spec}',\n")
            f.write("]\n\n")
    
    print(f"Aggregated GPU specs by year saved to {output_file}")

if __name__ == "__main__":
    # Specify the directory containing the text files
    directory = r"C:\Users\howla\OneDrive\Documents\GitHub\csca5622_final_project\data\gpu"
    
    # Specify the output file
    output_file = os.path.join(directory, 'gpu_specs_links_list.txt')

    # Call the function to extract and aggregate GPU specs by year
    extract_gpu_specs_by_year(directory, output_file)
