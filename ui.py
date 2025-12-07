import streamlit as st
from app.api.agent import run_agent
from io import BytesIO
import fitz
import docx

# ----------------- Page Setup -----------------
st.set_page_config(page_title="AI Job Agent", layout="wide")
st.markdown(
    """
    <style>
        .stApp {
            background-color: #f5f5f5;
        }
        .card {
            padding: 1rem;
            margin-bottom: 1rem;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .job-title {
            font-weight: bold;
            font-size: 1.2rem;
        }
        .company {
            color: #555;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("💼 AI Job Search & Ranking Agent")
st.markdown("Upload your resume and tell me what job you're looking for. I'll rank the best matches for you!")

# ----------------- Helper Functions -----------------
def extract_text(file):
    if file.type == "application/pdf":
        doc = fitz.open(stream=file.read(), filetype="pdf")
        return "".join([page.get_text() for page in doc])
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return "\n".join([p.text for p in docx.Document(BytesIO(file.read())).paragraphs])
    else:  # txt
        return file.read().decode("utf-8")

def display_jobs(jobs):
    for job in jobs:
        st.markdown(
            f"""
            <div class="card">
                <div class="job-title">{job.get('title', 'Unknown')}</div>
                <div class="company">{job.get('company', 'Unknown Company')}</div>
                <div>{job.get('location', '')}</div>
                <div>{job.get('summary', '')}</div>
                <a href="{job.get('link', '#')}" target="_blank">Apply here</a>
            </div>
            """,
            unsafe_allow_html=True
        )

# ----------------- UI Layout -----------------
with st.sidebar:
    st.header("Upload & Query")
    uploaded_file = st.file_uploader("Upload your resume (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
    query = st.text_input("Job title / keywords", "")

# ----------------- Main Interaction -----------------
if uploaded_file and query:
    with st.spinner("Extracting resume and finding best jobs..."):
        try:
            resume_text = extract_text(uploaded_file)

            # FIXED: Call run_agent with correct named arguments
            result = run_agent(
                query=query,
                resume_text=resume_text
            )
            
            st.subheader("Recommended Jobs 🏆")
            if isinstance(result, list) and result:
                display_jobs(result)
            else:
                st.info("No jobs found. Try a different query or update your resume.")
        except Exception as e:
            st.error(f"Error: {str(e)}")
