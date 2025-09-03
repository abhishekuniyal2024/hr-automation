# AI Recruitment System - Quick Start Guide


### 1. Start the System
```bash
# Activate environment
source recruitment_ai_env/bin/activate

# Start web server
python main.py
```

### 2. Open Web Interface
- Go to: `http://localhost:8000`
- Click: **"Start Recruitment"**

### 3. Add Candidates
Fill out the form for each candidate:
- **Name:** Candidate's full name
- **Email:** Candidate's email
- **Phone:** Candidate's phone
- **Position:** "Senior Software Engineer"
- **Experience:** Number of years (e.g., 3, 5, 7)
- **Resume:** Paste detailed resume content
- **Cover Letter:** Motivation and fit

### 4. Make Hiring Decision
```bash
# Run the hiring decision script
python hiring_decision.py
```

### 5. View Results
```bash
# Check who got hired
curl http://localhost:8000/api/summary | python -m json.tool
```

---

## Essential Commands

| Action | Command |
|--------|---------|
| **Start System** | `python main.py` |
| **Test System** | `python test_system.py` |
| **Run Demo** | `python demo.py` |
| **Make Decision** | `python hiring_decision.py` |
| **Check Status** | `curl http://localhost:8000/api/status` |
| **View Candidates** | `curl http://localhost:8000/api/candidates \| python -m json.tool` |
| **Get Results** | `curl http://localhost:8000/api/summary \| python -m json.tool` |

---

##  Understanding Results

### AI Scoring (0-100)
- **90-100:** Excellent match 
- **70-89:** Good match 
- **50-69:** Fair match 
- **0-49:** Poor match 

### Candidate Status
- **Applied:** Submitted application
- **Screened:** AI evaluated
- **Interviewed:** Completed interviews
- **Hired:** Selected for job 
- **Rejected:** Not selected 

---

## Quick Fixes

### Common Issues
```bash
# Port in use
pkill -f "python main.py"

# Missing modules
source recruitment_ai_env/bin/activate

# Missing directories
mkdir -p static reports uploads
```

---

## Sample Resume Content

```
Resume Text:
"Experienced software engineer with 5 years of development experience. 
Proficient in Python, JavaScript, React, Node.js, and AWS. 
Led development of 3 major applications serving 10,000+ users. 
Strong problem-solving skills and team collaboration experience."

Cover Letter:
"I am excited to apply for the Senior Software Engineer position. 
My experience in full-stack development and leadership roles 
makes me an ideal candidate for this role."
```

---

## That's It!

1. **Start** → `python main.py`
2. **Add Candidates** → Web form
3. **Decide** → `python hiring_decision.py`
4. **View Winner** → Check API results

**The AI will automatically select the best candidate**
