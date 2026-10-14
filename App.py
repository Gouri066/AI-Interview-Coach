#import streamlit as st
#to display the application title
#st.title("AI-Interview-Coach")
#to write a msg
#st.write("Setup Is Working !!")

from multiprocessing.spawn import prepare

import streamlit as st 
from pypdf import PdfReader
from llm import ask_ai
import os
import json
from dotenv import load_dotenv
from google import genai
from coach import analyze_profile,generate_questions

#load api key
load_dotenv()

#connect to genai
client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

#to choose the model
MODEL="gemini-3.5-flash-lite"


#next application title
st.title("AI-Interview-Coach")

#to define pdf - reading function
#to extract from all the pages
def read_pdf(file):
    reader=PdfReader(file)
    text=""
    for page in reader.pages:
        text+=page.extract_text() or ""
    return text

#to allow the users to upload a resume
Resume_file=st.file_uploader("Upload Your Resume(PDF)!!",
        type="pdf"
                )

#To allow users to paste the job description
job_description=st.text_area("Paste the job description",
            height=200
                    )
                
# To process the resume
if Resume_file is not None:
    Resume_text = read_pdf(Resume_file)

    if Resume_text.strip() == "":
        st.error(
            "The resume is empty or could not be read. "
            "Try another file."
        )
    else:
        st.success("Resume uploaded successfully!")

        with st.expander("See extracted text"):
            st.text(Resume_text)


if Resume_file is not None and Resume_text.strip():
    if st.button("Analyze my profile"):
        if job_description.strip()=="":
            st.warning("Please paste a job description first")
        else:
            with st.spinner("Analyzing your profile..!!"):
                st.session_state.pop("questions",None)
                st.session_state.Resume_text=Resume_text
                st.session_state.job_description=job_description
                st.session_state.analysis=analyze_profile(
                    Resume_text,
                    job_description
                    )
    if "analysis" in st.session_state:
                a=st.session_state.analysis
                st.header(
                    f"Profile analysis:{a.get('Role','Unknown Role')}"
                )
                st.metric(
                    "Matching score",
                    f"{a.get('Matching score',0)}%"
                )
                st.write(a.get("Summary",""))
                col1,col2=st.columns(2)
                with col1:
                    st.subheader("Matching Skills")
                    for skill in a.get("Matching Skills",[]):
                        st.write("-",skill)
                with col2:
                    st.subheader("Missing Skills")
                    for skill in a.get("Missing Skills",[]):
                        st.write("-",skill)
                with st.expander("View full JSON response"):
                    st.json(a)
                
#to analyze the resume with both inputs
if Resume_file and job_description:
    #to display a button
    if st.button("Analyze the resume"):
        prompt=f"""
        You are an expert interview coach.
        Analyze the candidate's resume against the job description.

        RESUME:
        {Resume_text}
        JOB DESCRIPTION:
        {job_description}

        Provide:
        1.A short summary of the candidate's profile.
        2.Key Skills found in the resume.
        3.Skills require by the job description.
        4.Matching skills.
        5.Missing skills.
        6.Overall suitability for the role.
        7.Areas the candidate should prepare for the interview.
        """
        #to send the prompt to the gemini 
        analysis=ask_ai(prompt)

        #to display the analysis
        st.subheader("Analysis Result:")
        st.write(analysis)
    




