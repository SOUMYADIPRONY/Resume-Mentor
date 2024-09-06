from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
from PIL import Image
from PyPDF2 import PdfReader
import google.generativeai as genai



genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(extracted_text, prompt):

  model = genai.GenerativeModel("gemini-1.5-flash")
  response = model.generate_content([extracted_text, prompt])
  return response.text

def extract_text_from_pdf(uploaded_file):
    # Use PyPDF to read the PDF
    reader = PdfReader(uploaded_file)
    text = ""
    
    # Iterate over all pages and extract text
    for page in reader.pages:
        text += page.extract_text()
    
    return text
  

st.set_page_config(page_title="NER Extractor")
st.header("Named Entity Recognition")
    
uploaded_file = st.file_uploader("Upload your document", type=["pdf"])

if uploaded_file is not None:

  st.write("PDF Uploaded Successfully")

submit1 = st.button("Extract")

nerprompt = """
You are an NER(Named Entity Recognition) model. You will focus on identifying and classifying specific data points from textual content.

Task: Analyze the uploaded PDF and find the relevant entities to extract.

Instructions:

 1. For any Name/First Name/Middle Name/Last Name field you will extract and show it based on the document.
 2. Extract mobile number, email address, house address
 3. For any other entity give it a tag based on your analysis.
 4. Do not extract irrelevant entities.
 5. Output should be in Key-Value format for eg:- Name: Alex Charles, Phone Number: 273882939 etc. 


"""

if submit1:
  if uploaded_file is not None:
        # Extract text from the uploaded PDF using PyPDF
        extracted_text = extract_text_from_pdf(uploaded_file)
        
        # Get the Gemini model's response
        response = get_gemini_response(extracted_text, nerprompt)

        st.subheader("Entities of the Uploaded Document are:")
        st.write(response)
  else:
        st.write("Please upload the Document")