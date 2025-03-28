import streamlit as st
import pandas as pd
import json
from io import StringIO, BytesIO


# Function to extract the required fields from the JSON
def extract_json_fields(json_data):
    result = []
    # Access the first level of "definitions"
    if "definitions" in json_data:
        definitions = json_data["definitions"]
        for key, value in definitions.items():
            # Check if "elements" is present
            if "elements" in value:
                for element_key, element_value in value["elements"].items():
                    # Extract the required details
                    label = element_value.get("@EndUserText.label", "N/A")
                    result.append([key, element_key, label])
    return result


# Streamlit UI
st.title("JSON Field Extractor")

# Upload JSON file
uploaded_file = st.file_uploader("Choose a JSON file", type="json")

if uploaded_file is not None:
    # Load the uploaded file as JSON
    try:
        json_data = json.load(uploaded_file)
        # Extract fields
        extracted_data = extract_json_fields(json_data)

        # Create DataFrame from extracted data
        df = pd.DataFrame(extracted_data, columns=["Entity", "Field", "Label"])

        # Filter out rows where "Field" starts with an underscore
        df = df[~df["Field"].str.startswith("_")]

        # Show the extracted data
        st.write(df)

        # Ask the user for download options
        st.subheader("Choose Download Format")
        download_format = st.radio("Select download format", ["CSV", "Excel", "JSON"])

        # Convert to the chosen format
        if download_format == "CSV":
            # Convert DataFrame to CSV
            csv_data = df.to_csv(index=False)
            st.download_button("Download CSV", csv_data, file_name="extracted_fields.csv", mime="text/csv")

        elif download_format == "Excel":
            # Convert DataFrame to Excel
            excel_data = BytesIO()
            with pd.ExcelWriter(excel_data, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Extracted Data")
            excel_data.seek(0)
            st.download_button("Download Excel", excel_data, file_name="extracted_fields.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        elif download_format == "JSON":
            # Convert DataFrame to JSON
            json_data = df.to_json(orient="records")
            st.download_button("Download JSON", json_data, file_name="extracted_fields.json", mime="application/json")

    except Exception as e:
        st.error(f"Error reading JSON file: {e}")
