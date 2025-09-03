# 🤖 AI Recruitment System - Complete User Guide

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation & Setup](#installation--setup)
3. [Running the System](#running-the-system)
4. [Testing the System](#testing-the-system)
5. [Adding Resumes/Candidates](#adding-resumescandidates)
6. [Making Hiring Decisions](#making-hiring-decisions)
7. [Troubleshooting](#troubleshooting)
8. [API Reference](#api-reference)

---

## 🛠️ Prerequisites

Before starting, make sure you have:
- Python 3.8+ installed
- Git (optional, for cloning)
- A modern web browser (Chrome, Firefox, Safari, Edge)

---

## 📦 Installation & Setup

### Step 1: Clone or Download the Project
```bash
# If you have the project files, navigate to the project directory
cd "job automation using website"

# Or if you need to clone from a repository
git clone <repository-url>
cd <project-directory>
```

### Step 2: Create Virtual Environment
```bash
# Create a new virtual environment
python -m venv recruitment_ai_env

# Activate the virtual environment
# On Linux/Mac:
source recruitment_ai_env/bin/activate

# On Windows:
# recruitment_ai_env\Scripts\activate
```

### Step 3: Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables
```bash
# Copy the example environment file
cp env_example.txt .env

# Edit the .env file and add your Groq API key
# For demo purposes, you can use: GROQ_API_KEY=test_key_for_demo
```

### Step 5: Create Required Directories
```bash
# Create directories for the web application
mkdir -p static reports uploads
```

---

## 🚀 Running the System

### Method 1: Web Interface (Recommended)
```bash
# Start the web server
python main.py

# Open your browser and go to:
# http://localhost:8000 or http://0.0.0.0:8000
```

### Method 2: Demo Script
```bash
# Run the demo script to see the system in action
python demo.py
```

### Method 3: Hiring Decision Script
```bash
# Run the hiring decision process
python hiring_decision.py
```

---

## 🧪 Testing the System

### Step 1: System Health Check
```bash
# Run the system test
python test_system.py
```

Expected output:
```
✅ Module imports successful
✅ Data loading successful
✅ Orchestrator creation successful
✅ Web app import successful
```

### Step 2: API Testing
```bash
# Test the API endpoints
curl http://localhost:8000/api/status
curl http://localhost:8000/api/job-openings
```

### Step 3: Web Interface Testing
1. Open browser to `http://localhost:8000`
2. Click "Start Recruitment" button
3. Verify job openings appear
4. Test the application form

---

## 👥 Adding Resumes/Candidates

### Method 1: Web Interface (Easiest)

1. **Open the Web Application**
   - Go to `http://localhost:8000`
   - You'll see the AI Recruitment System dashboard

2. **Fill Out the Application Form**
   - **Full Name:** Enter candidate's full name
   - **Email:** Enter candidate's email address
   - **Phone:** Enter candidate's phone number
   - **Position:** Enter the job position (e.g., "Senior Software Engineer")
   - **Years of Experience:** Enter number of years (e.g., 3)
   - **Resume Text:** Paste or type the candidate's resume content
   - **Cover Letter:** Enter the candidate's cover letter

3. **Submit Application**
   - Click "Submit Application" button
   - You'll see a success message
   - The candidate count will update automatically

### Method 2: API Direct (Advanced)
```bash
# Submit a candidate via API
curl -X POST http://localhost:8000/api/apply \
  -F "candidate_name=John Doe" \
  -F "email=john@example.com" \
  -F "phone=1234567890" \
  -F "position=Senior Software Engineer" \
  -F "experience_years=5" \
  -F "resume_text=Experienced software engineer with 5 years..." \
  -F "cover_letter=I am excited to apply for this position..."
```

### Sample Resume Content
```
Resume Text Example:
"Experienced software engineer with 5 years of development experience. 
Proficient in Python, JavaScript, React, Node.js, and AWS. 
Led development of 3 major applications serving 10,000+ users. 
Strong problem-solving skills and team collaboration experience."

Cover Letter Example:
"I am excited to apply for the Senior Software Engineer position. 
My experience in full-stack development and leadership roles 
makes me an ideal candidate for this role."
```

---

## 🎯 Making Hiring Decisions

### Step 1: Review Candidates
1. **Check Current Candidates**
   ```bash
   curl http://localhost:8000/api/candidates | python -m json.tool
   ```

2. **View AI Screening Results**
   - Each candidate gets an automatic AI score
   - Review skill match, experience, and cultural fit scores

### Step 2: Conduct Interviews (Automatic)
The system automatically conducts interviews when you run the hiring decision script:

```bash
python hiring_decision.py
```

### Step 3: Make Final Selection
The AI system will:
1. **Screen all candidates** based on skills and experience
2. **Conduct technical interviews** automatically
3. **Conduct behavioral interviews** automatically
4. **Make hiring recommendations** based on all data

### Step 4: View Results
```bash
# Get final hiring summary
curl http://localhost:8000/api/summary | python -m json.tool
```

---

## 📊 Understanding the Results

### AI Scoring System
- **Overall Score:** 0-100 (higher is better)
- **Skill Match:** Percentage of required skills possessed
- **Experience Match:** How well experience matches requirements
- **Cultural Fit:** Assessment of teamwork, communication, etc.

### Candidate Status
- **Applied:** Candidate submitted application
- **Screened:** AI has evaluated the candidate
- **Interviewed:** Technical and behavioral interviews completed
- **Hired:** Selected for the position
- **Rejected:** Not selected

### Sample Results Interpretation
```
Candidate: John Doe
- Overall Score: 75.5/100 ✅
- Experience: 5 years (Required: 5+) ✅
- Skill Match: 85% ✅
- Status: HIRED ✅
```

---

## 🔧 Troubleshooting

### Common Issues & Solutions

#### 1. "Module not found" Error
```bash
# Solution: Activate virtual environment
source recruitment_ai_env/bin/activate
```

#### 2. "Port already in use" Error
```bash
# Solution: Kill existing process
pkill -f "python main.py"
# Then restart
python main.py
```

#### 3. "Invalid API Key" Error
```bash
# Solution: Check your .env file
cat .env
# Make sure GROQ_API_KEY is set
```

#### 4. Form Submission Errors
- Check browser console for JavaScript errors
- Ensure all form fields are filled
- Verify server is running

#### 5. 404 Errors
```bash
# Solution: Create missing directories
mkdir -p static reports uploads
```

### Debug Mode
```bash
# Run with debug information
python -u main.py
```

---

## 📡 API Reference

### Core Endpoints

#### 1. System Status
```bash
GET /api/status
# Returns system health and statistics
```

#### 2. Start Recruitment
```bash
POST /api/start-recruitment
# Analyzes employees.csv and creates job openings
```

#### 3. Get Job Openings
```bash
GET /api/job-openings
# Returns all available job positions
```

#### 4. Submit Application
```bash
POST /api/apply
# Submit a candidate application
# Required fields: candidate_name, email, phone, position, experience_years, resume_text, cover_letter
```

#### 5. Get Candidates
```bash
GET /api/candidates
# Returns all candidates with their screening results
```

#### 6. Conduct Interview
```bash
POST /api/interview/{candidate_id}/{stage}
# Conduct technical or behavioral interview
# Stages: technical, behavioral
```

#### 7. Make Selection
```bash
POST /api/select/{candidate_id}
# Make final hiring decision
# Decision: hired, rejected
```

#### 8. Get Summary
```bash
GET /api/summary
# Returns complete recruitment summary
```

---

## 🎯 Complete Workflow Example

### Step-by-Step Process

1. **Setup & Start**
   ```bash
   source recruitment_ai_env/bin/activate
   python main.py
   ```

2. **Open Web Interface**
   - Browser: `http://localhost:8000`
   - Click "Start Recruitment"

3. **Add Multiple Candidates**
   - Fill out application form for each candidate
   - Submit applications one by one

4. **Run Hiring Decision**
   ```bash
   python hiring_decision.py
   ```

5. **View Results**
   ```bash
   curl http://localhost:8000/api/summary | python -m json.tool
   ```

6. **Check Web Dashboard**
   - Refresh browser to see updated statistics
   - View hired candidate details

---

## 📈 Best Practices

### For Adding Candidates
- **Detailed Resume Text:** Include specific skills, technologies, and achievements
- **Realistic Experience:** Match experience years to position requirements
- **Professional Cover Letters:** Show motivation and cultural fit

### For Hiring Decisions
- **Review AI Scores:** Higher scores indicate better matches
- **Consider Experience Gap:** Candidates with required experience perform better
- **Check Interview Feedback:** Look at technical and behavioral assessments

### For System Management
- **Regular Backups:** Save important data
- **Monitor Logs:** Check for errors in terminal output
- **Update Dependencies:** Keep packages updated

---

## 🆘 Getting Help

### Quick Commands Reference
```bash
# Start system
python main.py

# Test system
python test_system.py

# Run demo
python demo.py

# Make hiring decisions
python hiring_decision.py

# Check status
curl http://localhost:8000/api/status

# View candidates
curl http://localhost:8000/api/candidates | python -m json.tool
```

### File Structure
```
project/
├── main.py                 # Web application
├── demo.py                 # Demo script
├── hiring_decision.py      # Hiring process
├── test_system.py          # System tests
├── requirements.txt        # Dependencies
├── employees.csv           # Employee data
├── templates/              # Web templates
├── static/                 # Static files
├── reports/                # Generated reports
└── uploads/                # File uploads
```

---

## 🎉 Congratulations!

You've successfully set up and used the AI Recruitment System! The system will:

✅ **Automatically analyze** employee data to identify job openings  
✅ **Create detailed job descriptions** using AI  
✅ **Screen candidates** based on skills and experience  
✅ **Conduct AI-powered interviews**  
✅ **Make data-driven hiring decisions**  

The selected candidate will be the one with the best combination of:
- Technical skills match
- Experience level
- Cultural fit
- Growth potential
- Interview performance

**Happy Hiring! 🚀**
