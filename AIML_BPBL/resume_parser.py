import fitz  # PyMuPDF
import re
import csv

def parse_pdf(pdf_path):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    
    # Initialize variables to store extracted information
    data = {'Name': '', 'Mobile': '', 'Email': '', 'Post': ''}

    # Loop through each page
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text = page.get_text()

        # Extract Name
        match_name = re.search(r'Name: (.+)', text)
        if match_name:
            data['Name'] = match_name.group(1).strip()

        # Extract Mobile
        match_mobile = re.search(r'Mobile: (.+)', text)
        if match_mobile:
            data['Mobile'] = match_mobile.group(1).strip()

        # Extract Email
        match_email = re.search(r'Email: (.+)', text)
        if match_email:
            data['Email'] = match_email.group(1).strip()

        # Extract Qualification
        match_qualification = re.search(r'Post : (.+)', text)
        if match_qualification:
            data['Post'] = match_qualification.group(1).strip()

    # Close the PDF file
    doc.close()

    return data

def save_to_csv(data, csv_path):
    # Write the data to a CSV file
    with open(csv_path, 'w', newline='') as csvfile:
        fieldnames = ['Name', 'Mobile', 'Email', 'Post']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header
        writer.writeheader()

        # Write data
        writer.writerow(data)

if __name__ == "__main__":
    # The path to  PDF file
    pdf_path = 'Resume1.pdf'
    
    # CSV file path
    csv_path = 'data.csv'

    # Parse the PDF and retrieve data
    extracted_data = parse_pdf(pdf_path)

    # Save the extracted data to a CSV file
    save_to_csv(extracted_data, csv_path)

    print("Data extraction and CSV creation completed.")


