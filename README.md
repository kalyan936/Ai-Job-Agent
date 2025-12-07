# 💼 AI Job Search & Ranking Agent

Welcome to the AI Job Search & Ranking Agent – your personal AI-powered assistant that helps you find and rank the best job opportunities based on your resume and career goals! 🚀

# 🌟 Features

Resume Upload: Upload your resume in PDF, DOCX, or TXT format.

Intelligent Job Search: Input your desired role or keywords, and the AI searches multiple sources for matching jobs.

Smart Ranking: Jobs are ranked based on how well they match your resume and skills.

Direct Apply Links: Quickly navigate to the job portal with “Apply here” links.

User-Friendly Interface: Built with Streamlit for a clean and interactive experience.

# 📁 Project Structure
ai-job-agent/
├── app/
│   ├── api/
│   │   ├── agent.py       # LLM + tool integration
│   │   └── __init__.py
│   ├── core/
│   │   ├── job_search.py  # Job search API calls
│   │   └── ranker.py      # Resume-job matching logic
│   └── __init__.py
├── ui.py                  # Streamlit frontend
├── requirements.txt
├── README.md
└── .gitignore

# ⚙️ How It Works

Upload Your Resume: Drag & drop or browse your resume file.

Enter Job Keywords: e.g., Data Scientist, Machine Learning Engineer.

AI Processing:

Extract text from your resume.

Search for jobs using the JSearch API.

Rank jobs based on your resume and keyword match.

View Recommendations: Get a curated list of jobs with titles, companies, locations, summaries, and apply links.

# 🖼️ Example Output (Your Results)

Here’s the actual output from the app using your uploaded resume and query Data Science:

The AI successfully returned top job recommendations:

Data Science Practitioner at Accenture Federal Services

Senior Associate, Data Science at Capital One

Data Scientist, Mid Level at Planet Technologies

All jobs include direct apply links so users can instantly navigate to the job portal.
<img width="776" height="988" alt="image" src="https://github.com/user-attachments/assets/28cdf50e-fec8-430e-887d-a00d00c6bf68" />



# 🚀 Tech Stack

Frontend: Streamlit

Backend: Python 3.10

AI/LLM: Groq LLM for ranking and smart matching

APIs: JSearch RapidAPI for job listings

Libraries: fitz (PDF extraction), python-docx, requests, pydantic, langchain

# 🔧 Setup Instructions

Clone the repository:

git clone https://github.com/kalyan936/Ai-Job-Agent.git
cd Ai-Job-Agent


Install dependencies:

pip install -r requirements.txt


Set your environment variables (replace with your API keys):

# in secrets.toml or .env
JSEARCH_API_KEY = "YOUR_JSEARCH_KEY"
GROQ_API_KEY = "YOUR_GROQ_KEY"


Run the app:

streamlit run ui.py


Open the app in your browser and explore!

# 🎨 Future Enhancements

Add location-based filtering.

Support multiple resume uploads.

Enhance AI ranking using skill extraction and experience weighting.

Add dashboard analytics for saved jobs and search trends.

# 📂 Screenshots

Include your screenshots folder in your repo:

screenshots/
├── app_output.png       # Demo app screenshot
└── your_result.png      # Screenshot of your actual result

# 📝 License

MIT License © Kalyan
