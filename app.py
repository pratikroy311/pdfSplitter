import PyPDF2
import re
import copy
from fuzzywuzzy import fuzz
import os
import time
import pytesseract
from PIL import Image
import io
start_time = time.time()






def split_pdf_by_headings(pdf_path, headings):
    current_headings = []
    current_tags = []
    with open(pdf_path, 'rb') as file:
        pdf = PyPDF2.PdfReader(file)
        num_pages = len(pdf.pages)
        output_pdfs = []
        start_page = 0
        headings_copy = copy.deepcopy(headings)

        for i, page in enumerate(pdf.pages):
            page_text = ''
            print("I m here",1)
            if '/XObject' in page['/Resources']:
                # Extract the image from the page
                xObject = page['/Resources']['/XObject'].get_object()
                for obj in xObject:
                    if xObject[obj]['/Subtype'] == '/Image':
                        # Get the image data
                        image_data = xObject[obj].get_data()

                        # Save the image data to a temporary file
                        image = Image.open(io.BytesIO(image_data))
                        image_text = pytesseract.image_to_string(image)
                        page_text= image_text
                        page_text = re.sub(r'\s+', ' ', page_text)  # Remove extra spaces and line breaks
                        page_text = page_text.strip()
            else:
                page_text= page.extract_text()
                page_text = re.sub(r'\s+', ' ', page_text)  # Remove extra spaces and line breaks
                page_text = page_text.strip()  # Remove leading/trailing spaces

            for key,value in list(headings_copy.items()):
                if isinstance(value, list):
                    # print(value)
                    for item in value:
                        # print(item)
                        if fuzz.partial_ratio(item, page_text) >= 90:
                            print("current heading:",key)
                            current_headings.append(value)
                            current_tags.append(key)
                            # headings_copy.remove(heading)
                            del headings_copy[key]
                            if i != 0:
                                output_pdf = PyPDF2.PdfWriter()
                                for j in range(start_page, i):
                                    output_pdf.add_page(pdf.pages[j])
                                output_pdfs.append(output_pdf)
                            start_page = i
                            break
                else:
                    if fuzz.partial_ratio(value, page_text) >= 90:
                            current_headings.append(value)
                            current_tags.append(key)
                            # headings_copy.remove(heading)
                            del headings_copy[key]
                            if i != 0:
                                output_pdf = PyPDF2.PdfWriter()
                                for j in range(start_page, i):
                                    output_pdf.add_page(pdf.pages[j])
                                output_pdfs.append(output_pdf)
                            start_page = i
                            break


        # Add the last section
        if start_page <= num_pages:
            output_pdf = PyPDF2.PdfWriter()
            for j in range(start_page, num_pages):
                output_pdf.add_page(pdf.pages[j])
            output_pdfs.append(output_pdf)

        # Save each section as a separate PDF file
        folder_name = "outputs"
        folder_path = os.path.join(os.getcwd(), folder_name)
        os.makedirs(folder_path, exist_ok=True)
        try:
            for i, output_pdf in enumerate(output_pdfs):
                heading = current_tags[i]
                file_name = f'{heading}.pdf'  # Use the heading as the file name
                pdf_file_path = os.path.join(folder_path, file_name)
                if 'DOCUSIGN' in pdf_file_path:
                    pass
                else:
                    with open(pdf_file_path, 'wb') as output_file:
                        output_pdf.write(output_file)
                # with open(f'output_{i}.pdf', 'wb') as output_file:
                #     output_pdf.write(output_file)
        except:
            pass



pdf_file = "7.pdf"

# for pdf_file in pdf_paths:
split_pdf_by_headings(pdf_file, headings_new)



end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")