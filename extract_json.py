import json
import csv
import os

# Define input and output folders
input_folder = "input"
output_folder = "output"
output_filename = "output.csv"
output_filepath = os.path.join(output_folder, output_filename)

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# List all JSON files in the input folder
json_files = [f for f in os.listdir(input_folder) if f.endswith(".json")]

# Prepare data for CSV
csv_data = []

# Process each JSON file
for json_file in json_files:
    input_filepath = os.path.join(input_folder, json_file)

    try:
        # Load JSON file
        with open(input_filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Extract data
        definitions = data.get("definitions", {})

        for main_key, main_value in definitions.items():
            elements = main_value.get("elements", {})

            for element_key, element_value in elements.items():
                # Skip keys starting with "_"
                if element_key.startswith("_"):
                    continue

                label = element_value.get("@EndUserText.label", "Unknown")
                csv_data.append([main_key, element_key, label])

    except Exception as e:
        print(f"Error processing {json_file}: {e}")

# Write to CSV
with open(output_filepath, "w", newline="", encoding="utf-8") as csvfile:
    csv_writer = csv.writer(csvfile)

    # Writing header
    csv_writer.writerow(["Main Key", "Element Key", "Label"])

    # Writing data rows
    csv_writer.writerows(csv_data)

print(f"CSV file '{output_filepath}' has been created successfully with data from {len(json_files)} files!")
