import os

def list_txt_files(directory, output_file):
    try:
        # Open the output file in write mode
        with open(output_file, 'w') as f:
            # Walk through the directory
            for root, dirs, files in os.walk(directory):
                for file in files:
                    # Check if the file has a .txt extension
                    if file.endswith(".txt"):
                        # Write the full file path to the output file
                        f.write(os.path.join(root, file) + '\n')
        print(f"List of .txt files written to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Directory where you want to search for .txt files
    directory = r"C:\Users\howla\OneDrive\Documents\GitHub\csca5622_final_project\data\cpu"
    
    # Output file to store the list
    output_file = r"C:\Users\howla\OneDrive\Documents\GitHub\csca5622_final_project\data\cpu\txt_file_list.txt"
    
    # Call the function to list .txt files and write to output file
    list_txt_files(directory, output_file)
