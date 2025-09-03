import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables from a .env located at the project root, regardless of CWD
_detected_env = find_dotenv(usecwd=True)
if not _detected_env:
    # Fallback to .env next to this file
    _detected_env = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(_detected_env)

# Groq API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama3-70b-8192"  # Using Llama3-70B model for better performance

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./recruitment.db")

# Application Configuration
APP_NAME = "AI Recruitment System"
APP_VERSION = "1.0.0"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# File Paths
EMPLOYEES_CSV = "employees.csv"
UPLOADS_DIR = "uploads"
REPORTS_DIR = "reports"

# Job Categories and Skills Mapping
JOB_CATEGORIES = {
    "Engineering": ["Software Development", "DevOps", "Data Engineering", "QA"],
    "Analytics": ["Data Analysis", "Business Intelligence", "Machine Learning"],
    "Marketing": ["Digital Marketing", "Content Creation", "SEO", "Social Media"],
    "IT": ["System Administration", "Network Engineering", "Cloud Computing"],
    "Human Resources": ["Recruitment", "Employee Relations", "Training"],
    "Finance": ["Financial Analysis", "Accounting", "Budgeting"],
    "Design": ["UI/UX Design", "Graphic Design", "Product Design"],
    "Sales": ["Business Development", "Account Management", "Lead Generation"],
    "Quality Assurance": ["Testing", "Quality Control", "Process Improvement"],
    "Business Development": ["Strategy", "Partnerships", "Market Research"],
    "Operations": ["Project Management", "Process Optimization", "Supply Chain"],
    "Customer Service": ["Support", "Client Relations", "Problem Resolution"]
}

# Interview Stages
INTERVIEW_STAGES = [
    "Initial Screening",
    "Technical Assessment", 
    "HR Interview",
    "Final Round",
    "Reference Check"
]

# Evaluation Criteria
EVALUATION_CRITERIA = {
    "Technical Skills": 0.3,
    "Communication": 0.2,
    "Experience": 0.2,
    "Cultural Fit": 0.15,
    "Problem Solving": 0.15
}
