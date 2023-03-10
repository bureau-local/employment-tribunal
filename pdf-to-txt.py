import os
from pdfminer.high_level import extract_text

# Create a txt folder if there isn't one
if not os.path.isdir("txt"):
    os.makedirs("txt")

# Get all pdfs in the pdf folder
pdf_files = [file for file in os.listdir("pdf") if file.endswith(".pdf")]
# Loop through each pdf file
for pdf in pdf_files:
    pdf_filepath = "pdf/" + pdf
    # Extract the text from the pdf
    text = extract_text(pdf_filepath)
    # Write to a txt file
    txt_filepath = "txt/" + pdf.replace(".pdf", ".txt")
    with open(txt_filepath, 'w') as outfile:
        outfile.write(text)
