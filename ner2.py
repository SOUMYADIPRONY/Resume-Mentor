import google.generativeai as genai
import time

GOOGLE_API_KEY = "" # Please set your API key.
pdf_file = "F:/START OF A NEW ERA- SD/Soumyadip Dutta Resume_2024.pdf"
name = "resume"

genai.configure(api_key=GOOGLE_API_KEY)

# Check uploaded file.
try:
    pdfFile = genai.get_file(f"files/{name}")
    print(f"File URI: {pdfFile.uri}")
except:
    print(f"Uploading file...")
    pdfFile = genai.upload_file(path=pdf_file, name=name, resumable=True)
    print(f"Completed upload: {pdfFile.uri}")

# Check the state of the uploaded file.
while pdfFile.state.name == "PROCESSING":
    print(".", end="")
    time.sleep(10)
    pdfFile = genai.get_file(pdfFile.name)

if pdfFile.state.name == "FAILED":
    raise ValueError(pdfFile.state.name)


# Generate content using the uploaded file.
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    system_instruction=[
        "You are an NER(Named Entity Recognition) model. You will focus on identifying and classifying specific data points from textual content.",
        "Analyze the uploaded PDF and find the relevant entities to extract.",
    ],
)
prompt = "Please transcribe the text in this PDF document."
print("Making LLM inference request...")
response = model.generate_content([pdfFile, prompt], request_options={"timeout": 600})
print(response.text)