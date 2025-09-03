# AI Recruitment System

A multi-agent AI-powered recruitment system that automates the entire hiring process from job posting to candidate selection using Groq API.

## 🚀 Features

- **Intelligent Job Analysis**: Automatically analyzes employee data to identify job openings
- **AI-Powered Job Descriptions**: Generates comprehensive job descriptions using Groq AI
- **Smart Candidate Screening**: Evaluates candidates based on skills, experience, and cultural fit
- **Automated Interview Coordination**: Creates interview schedules and generates relevant questions
- **Multi-Agent Architecture**: Coordinated AI agents for different recruitment tasks
- **Web Interface**: Modern web application for managing the recruitment process
- **Comprehensive Reporting**: Detailed analytics and insights throughout the process

## 🏗️ Architecture

The system consists of three main AI agents:

1. **Recruitment Analyzer**: Analyzes employee data and creates job requirements
2. **Candidate Screener**: Evaluates candidate applications using AI
3. **Interview Coordinator**: Manages interview process and generates questions

All agents are coordinated by a central **Recruitment Orchestrator** that manages the workflow.

## 📋 Prerequisites

- Python 3.8+
- Groq API key
- Virtual environment (recommended)

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd "job automation using website"
   ```

2. **Create and activate virtual environment**:
   ```bash
   python3 -m venv recruitment_ai_env
   source recruitment_ai_env/bin/activate  # On Windows: recruitment_ai_env\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   export GROQ_API_KEY="your_groq_api_key_here"
   ```

   Or create a `.env` file:
   ```bash
   echo "GROQ_API_KEY=your_groq_api_key_here" > .env
   ```

## 🚀 Usage

### Option 1: Run Demo Script

Test the system functionality without the web interface:

```bash
python demo.py
```

This will:
- Analyze the employee data
- Create job openings
- Process sample candidate applications
- Simulate the interview process
- Generate a recruitment summary

### Option 2: Run Web Interface

Start the web application:

```bash
python main.py
```

Then open your browser and navigate to: `http://localhost:8000`

## 📊 How It Works

### 1. Employee Data Analysis
The system reads `employees.csv` to identify employees who have quit (have a `last_working_day`). For each quit employee, it:
- Analyzes their position and department
- Generates a comprehensive job description using Groq AI
- Identifies required skills and experience levels
- Calculates appropriate salary ranges
- Determines hiring priority

### 2. Candidate Screening
When candidates apply, the AI:
- Analyzes resume text for skill matches
- Evaluates experience levels
- Assesses cultural fit from cover letters
- Calculates overall scores
- Provides detailed feedback and recommendations

### 3. Interview Management
For qualified candidates, the system:
- Creates interview schedules with multiple stages
- Generates relevant questions for each stage
- Tracks interview progress
- Provides next steps and recommendations

### 4. Final Selection
The system:
- Evaluates candidates after all interviews
- Calculates final scores
- Provides hiring recommendations
- Tracks the complete recruitment process

## 🔧 Configuration

The system can be configured through `config.py`:

- **Groq API Settings**: Model selection and API configuration
- **Job Categories**: Skills mapping for different departments
- **Interview Stages**: Customizable interview process
- **Evaluation Criteria**: Weighted scoring for different factors

## 📁 Project Structure

```
├── agents/                     # AI Agent modules
│   ├── __init__.py
│   ├── recruitment_analyzer.py # Job analysis agent
│   ├── candidate_screener.py   # Candidate evaluation agent
│   └── interview_coordinator.py # Interview management agent
├── templates/                  # Web interface templates
│   └── index.html             # Main web page
├── static/                     # Static web assets
├── reports/                    # Generated reports
├── uploads/                    # File uploads
├── config.py                   # Configuration settings
├── recruitment_orchestrator.py # Main orchestrator
├── main.py                     # FastAPI web application
├── demo.py                     # Demo script
├── requirements.txt            # Python dependencies
├── employees.csv               # Sample employee data
└── README.md                   # This file
```

## 🌟 Sample Data

The system comes with sample employee data in `employees.csv`:

- **20 employees** across various departments
- **1 quit employee** (Sanjay Reddy - Senior Software Engineer)
- **Multiple departments**: Engineering, IT, Marketing, HR, Finance, etc.

## 🔍 API Endpoints

The web interface provides these API endpoints:

- `GET /` - Main dashboard
- `POST /api/start-recruitment` - Start recruitment process
- `GET /api/job-openings` - Get current job openings
- `POST /api/apply` - Submit candidate application
- `GET /api/candidates` - Get all candidates
- `POST /api/interview/{candidate_id}/{stage}` - Conduct interview
- `POST /api/select/{candidate_id}` - Make final selection
- `GET /api/summary` - Get recruitment summary
- `GET /api/status` - Get system status

## 📈 Reports Generated

The system automatically generates:

1. **Recruitment Analysis Report** (`recruitment_analysis.md`)
   - Job opening details
   - Required skills and qualifications
   - AI-generated job descriptions

2. **Recruitment Summary** (`recruitment_summary.json`)
   - Candidate statistics
   - Interview completion rates
   - Hiring success metrics
   - Performance insights

## 🎯 Use Cases

- **HR Departments**: Automate routine recruitment tasks
- **Startups**: Scale hiring without proportional HR overhead
- **Large Organizations**: Standardize recruitment processes
- **Recruitment Agencies**: Streamline candidate evaluation
- **Educational Institutions**: Hire faculty and staff efficiently

## 🔒 Security Considerations

- API keys are stored in environment variables
- Input validation on all forms
- No sensitive data is logged or stored insecurely
- HTTPS recommended for production use

## 🚧 Limitations

- Requires Groq API key and internet connection
- AI-generated content should be reviewed by humans
- Limited to text-based resume analysis
- No integration with external HR systems

## 🚀 Future Enhancements

- **Multi-language Support**: Process resumes in different languages
- **Video Interview Analysis**: AI-powered video interview evaluation
- **Integration APIs**: Connect with job boards and HR systems
- **Advanced Analytics**: Machine learning insights and predictions
- **Mobile App**: Native mobile application for recruiters

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues:

1. Check that your Groq API key is valid
2. Ensure all dependencies are installed
3. Verify the virtual environment is activated
4. Check the console for error messages

## 🙏 Acknowledgments

- **Groq**: For providing the AI language model API
- **FastAPI**: For the modern web framework
- **Tailwind CSS**: For the beautiful UI components
- **Open Source Community**: For the various Python packages used

---

**Note**: This is a demonstration system. For production use, additional security measures, error handling, and testing should be implemented.
