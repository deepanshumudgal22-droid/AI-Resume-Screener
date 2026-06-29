import streamlit as st
import requests

st.title("AI Resume Screening & Ranking System")
st.write("Upload candidate resumes (PDF or TXT) against your job description to see instantaneous match rankings.")

# 1. Job Description Text Box
jd_input = st.text_area("Paste Job Description Here:", height=150)

# 2. File Upload Box (Updated to accept BOTH pdf and txt)
uploaded_files = st.file_uploader("Upload Resumes (.pdf or .txt files)", type=['txt', 'pdf'], accept_multiple_files=True)

# 3. Execution Button
if st.button("Rank Candidates"):
    if not jd_input:
        st.error("Please add a job description before analyzing!")
    elif not uploaded_files:
        st.error("Please upload at least one resume file!")
    else:
        st.info("Sending documents to Backend ML Engine...")
        
        payload = {"job_description": jd_input}
        
        # Build file payloads and determine correct MIME-types dynamically
        files_payload = []
        for file in uploaded_files:
            if file.name.endswith('.pdf'):
                mime_type = "application/pdf"
            else:
                mime_type = "text/plain"
            
            files_payload.append(("files", (file.name, file.read(), mime_type)))
        
        try:
            # Send data over HTTP to our running FastAPI app
            response = requests.post("http://127.0.0.1:8000/rank", data=payload, files=files_payload)
            results = response.json()
            
            # 4. Display Ranking Table Output
            st.success("Analysis Complete!")
            st.subheader("Final Candidate Leaderboard")
            
            for rank, candidate in enumerate(results["rankings"], 1):
                st.write(f"🏆 **Rank {rank}:** {candidate['filename']} — **{candidate['score']}% Match**")
                
        except Exception as e:
            st.error(f"Could not connect to the Backend server. Make sure uvicorn is running! Error: {e}")
