# pdfSplitter
## Task
<b>Given a pdf file which is a combination of multiple documents, separate the pdf into multiple document based on headings. The documents can be in textual form or can be a scanned document.</b>

## Solution
To separate a PDF file into multiple documents based on headings, We can use a combination of text extraction techniques and document segmentation methods like OCR. Here's a approach that I followed to achieve this:

1. Text Extraction:
   - If the PDF contains searchable text, we can extract the text directly using a PDF processing library like PyPDF2.
   - If the PDF is a scanned document or an image-based PDF, we need to perform Optical Character Recognition (OCR) to extract the text. OCR software like Tesseract or OCR has been used to convert the scanned document into searchable text.

2. Identify Headings:
   - Once we have the extracted text, we can use various techniques to identify headings. This could involve searching for specific patterns or using natural language processing (NLP) techniques like Named Entity Recognition (NER) or part-of-speech (POS) tagging to identify structural elements like titles or headings.
   - If the PDF has a consistent formatting style for headings, we can use regular expressions or string matching techniques to detect and extract them.

3. Document Segmentation:
   - Once we have identified the headings, we can use them as markers to split the original document into separate documents.
   - Based on the identified headings, we can define rules or patterns to segment the text into different sections or documents. we can start a new document each time a new heading appears.

4. Saving Separate Documents:
   - Finally, we can save the extracted sections as separate documents in a desired format (e.g., PDF, DOCX, TXT, etc.). We can use libraries like PyPDF2 or docx to create new documents and populate them with the extracted content.
