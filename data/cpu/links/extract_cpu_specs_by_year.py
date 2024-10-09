import re
import os

def extract_cpu_specs_by_year(directory, output_file):
    # Dictionary to store lists of CPU specs URLs grouped by year
    cpu_specs_by_year = {}

    # Regular expression pattern to match the CPU specs URLs
    pattern = r'/cpu-specs/[^"]*'

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
                    if year not in cpu_specs_by_year:
                        cpu_specs_by_year[year] = []
                    cpu_specs_by_year[year].extend(matches)

            except FileNotFoundError:
                print(f"File {filename} not found.")
    
    # Write the aggregated CPU specs into a new file, grouped by year
    with open(output_file, 'w') as f:
        for year, specs in cpu_specs_by_year.items():
            f.write(f"cpu_{year} = [\n")
            for idx, spec in enumerate(specs):
                if idx == len(specs) - 1:
                    f.write(f"    '{spec}'\n")  # Last item, no trailing comma
                else:
                    f.write(f"    '{spec}',\n")
            f.write("]\n\n")
    
    print(f"Aggregated CPU specs by year saved to {output_file}")

if __name__ == "__main__":
    # Specify the directory containing the text files
    directory = r"C:\Users\howla\OneDrive\Documents\GitHub\csca5622_final_project\data\cpu"
    
    # Specify the output file
    output_file = os.path.join(directory, 'cpu_specs_links_list.txt')

    # Call the function to extract and aggregate CPU specs by year
    extract_cpu_specs_by_year(directory, output_file)
