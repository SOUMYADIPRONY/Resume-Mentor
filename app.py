from dotenv import load_dotenv
load_dotenv()
import base64
import io
import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):

  model = genai.GenerativeModel('gemini-1.5-flash')
  response = model.generate_content([input, pdf_content[0], prompt])
  return response.text


def input_pdf_setup(uploaded_file):
  ##convert PDF to image
  if uploaded_file is not None:
    images= pdf2image.convert_from_bytes(uploaded_file.read())

    first_page= images[0]

    img_byte_arr = io.BytesIO()
    first_page.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()


    pdf_parts = [{

      "mime_type": "image/jpeg",
      "data": base64.b64encode(img_byte_arr).decode()
    }]

    return pdf_parts
  else:
    return FileNotFoundError("File not found")

##streamlit


st.set_page_config(page_title="ATS Resume Expert")
st.header("Resume Mentor")

input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your Resume(PDF)", type=["pdf"])


if uploaded_file is not None:

  st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell me about the Resume")

submit2 = st.button("ATS score")

submit3 = st.button("How to Improve my Skills?")

submit4 = st.button("Enhance your resume")

input_prompt1 = """

You are an experienced Human Resource Manager in the field of Data Science, Big Data Enginee, DevOps, Full Stack Web Development or Java Spring Boot Developer , your task is to review the provided resume against the job description for the profile which is most relevant in the resume. Please share your professional evaluation on whether the candidate's profile aligns with the job description. Highight the strengths and weaknesses of the applicant in relation to the specified job desciption

"""

# input_prompt2 = """
# You are an highly skilled and efficient ATS (Applicant Tracking System) scanner with a deep understanding of Data Science, Full Stack WEB Development, DevOps, Data Analysts and deep ATS functionality. 

# Task: As an ATS you need to evaluate the resume against the provided job description.

# 1. Find the percentage match by evaluation the resume against job description and give the output as Percentage Match: 
# 2. Find the missing skills or experiences in the Resume (if any) provided in the Job Description and tell him/her what is employer looking for in the resume.
# 3. Give a feedback whether the Resume is ATS friendly or not. If it is not ATS friendly mention the sections which needs to be improved be it font, layout or formatting of the resume.


# """

input_prompt2 = """
You are an highly skilled and efficient ATS- Applicant Tracking System with a deep understanding of ETL tools, Snowflake, Java, AWS, SQL, Oracle. 

Task: As an ATS you need to evaluate the resume and give a ATS score.

Instructions
1. Greet with the person name mentioned in the resume
2. Give a feedback whether the Resume is ATS friendly or not. If it is not ATS friendly mention the sections which needs to be improved be it font, layout or formatting of the resume.
3. Provide the ATS Score out of 100:
  



"""


input_prompt3="""

You are expert Resume reviewer with deep knowledge in all kinds of Technical Domains- Cloud Engineer, Data Engineer, Java Spring Boot, DevOps, MERN Stack, Data Science. 
Task: Provide advise to the candidate based on the job description. Provide necessary resources to the candidate to give him/her a head start. List down the strengths and weaknesses so that the candidate can improve.

"""

input_prompt4="""
You are an expert Resume reviewer with good English writing skills.

Task: Suggest the candidate how he or she can improve the various sections of the resume if grammar, sentence or the way the resume is written.

Instructions:

1. If the resume is written without any mistake and there is little scope to improve. Greet the person, Your resume is great. Here are few suggestions you can look if you want:

2. If the resume has lot of mistakes and require lot of improvement. Greet the person politely, Your skills look great however it needs improvement. Here are the suggestions which you can implement to make your resume look the best: 


"""

if submit1:
  if uploaded_file is not None:
    pdf_content = input_pdf_setup(uploaded_file)
    response = get_gemini_response(input_prompt1, pdf_content, input_text)

    st.subheader("The response is ")
    st.write(response)
  else:
    st.write("Please upload the resume")

elif submit2:

  if uploaded_file is not None:
    pdf_content = input_pdf_setup(uploaded_file)
    response = get_gemini_response(input_prompt2, pdf_content, input_text)

    st.subheader("The response is ")
    st.write(response)
  else:
    st.write("Please upload the resume")


elif submit3:

  if uploaded_file is not None:
    pdf_content = input_pdf_setup(uploaded_file)
    response = get_gemini_response(input_prompt3, pdf_content, input_text)

    st.subheader("The response is ")
    st.write(response)
  else:
    st.write("Please upload the resume")

elif submit4:

  if uploaded_file is not None:
    pdf_content = input_pdf_setup(uploaded_file)
    response = get_gemini_response(input_prompt4, pdf_content, input_text)

    st.subheader("The response is ")
    st.write(response)
  else:
    st.write("Please upload the resume")