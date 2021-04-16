import os
import pathlib
import argparse

from PyPDF2 import PdfFileWriter, PdfFileReader


# parse filepath argument

parser = argparse.ArgumentParser()
parser.add_argument("pdf_filepath", type=pathlib.Path)
args = parser.parse_args()

pdf_filepath = str(args.pdf_filepath)


# get output filepaths

QUOTE_CHARS = ["'", '"']

dirpath, filename = os.path.split(pdf_filepath)

for quote_char in QUOTE_CHARS:
    if filename[-1] == quote_char:
        filename = filename.strip(quote_char)

name, ext = os.path.splitext(filename)

pdf_filename_front = f"print_this_first" + ext
pdf_filename_back = f"print_this_second" + ext

pdf_filepath_front = os.path.join(os.getcwd(), pdf_filename_front)
pdf_filepath_back = os.path.join(os.getcwd(), pdf_filename_back)


# Step 1: put 2 pages per sheet of paper

temp_1_filepath = os.path.join(os.getcwd(), "temp_1.pdf")
os.system(f"pdfautonup {pdf_filepath} --size a3 --output {temp_1_filepath}")


# Step 2: split pages into 2 different PDFs (one with front pages, one with back pages)

pdf_front = PdfFileWriter()
pdf_back = PdfFileWriter()
temp_2_filepath = os.path.join(os.getcwd(), "temp_2.pdf")

with open(temp_1_filepath, "rb") as f:
    source_pdf = PdfFileReader(f)
    num_pages = source_pdf.getNumPages()

    for page in range(num_pages):
        if page % 2 == 0:
            pdf_front.addPage(source_pdf.getPage(page))
        else:
            pdf_back.addPage(source_pdf.getPage(page))

    if num_pages % 2 == 1:
        pdf_back.addBlankPage()

    with open(pdf_filepath_front, "wb") as g:
        pdf_front.write(g)

    with open(temp_2_filepath, "wb") as g:
        pdf_back.write(g)


# Step 3: invert the order of the back pages

pdf_back = PdfFileWriter()
with open(temp_2_filepath, "rb") as f:
    source_pdf = PdfFileReader(f)
    num_pages = source_pdf.getNumPages()

    for page in range(num_pages - 1, -1, -1):
        pdf_back.addPage(source_pdf.getPage(page))

    with open(pdf_filepath_back, "wb") as g:
        pdf_back.write(g)


# clean up
os.remove(temp_1_filepath)
os.remove(temp_2_filepath)
