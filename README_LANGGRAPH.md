# LangGraph Multi-Agent AI Recruitment System

## Overview

This project has been transformed into a sophisticated multi-agent AI system using **LangGraph** for orchestration. The system now features intelligent workflow management, stateful multi-agent coordination, and enhanced scalability.

## 🚀 What's New with LangGraph

### Multi-Agent Architecture
- **Recruitment Analyzer Agent**: Analyzes employee data and identifies job openings
- **Candidate Screener Agent**: Screens candidates against job requirements using AI
- **Interview Coordinator Agent**: Manages interview scheduling and question generation
- **Decision Making Agent**: Evaluates candidates and makes hiring decisions
- **Report Generator Agent**: Creates comprehensive recruitment reports

### LangGraph Workflow Benefits
- **Orchestrated Coordination**: Agents work together in a structured workflow
- **Stateful Management**: Maintains context throughout the recruitment process
- **Error Handling**: Robust error handling and recovery mechanisms
- **Scalability**: Easy to add new agents and modify workflows
- **Real-time Monitoring**: Track workflow progress and agent interactions

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    LangGraph Workflow Engine                │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │
│  │   Analyze   │───▶│   Screen    │───▶│  Schedule   │    │
│  │Requirements │    │ Candidates  │    │ Interviews  │    │
│  └─────────────┘    └─────────────┘    └─────────────┘    │
│           │                   │                   │        │
│           ▼                   ▼                   ▼        │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │
│  │   Conduct   │───▶│   Make      │───▶│  Generate   │    │
│  │ Interviews  │    │ Decisions   │    │   Reports   │    │
│  └─────────────┘    └─────────────┘    └─────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## 📦 Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Environment Variables**:
   ```bash
   cp env_example.txt .env
   # Edit .env with your API keys
   ```

3. **Run the System**:
   ```bash
   # Start the FastAPI server
   python main.py
   
   # Or run the demo
   python demo_langgraph.py
   ```

## 🔧 Configuration

### Environment Variables
- `GROQ_API_KEY`: Your Groq API key for LLM access
- `DEBUG`: Set to "true" for debug mode

### Key Components
- **State Management**: Centralized state tracking for all agents
- **Workflow Definition**: Configurable workflow steps and transitions
- **Agent Communication**: Structured message passing between agents
- **Error Recovery**: Automatic error handling and workflow recovery

## 🎯 Usage Examples

### Starting the Recruitment Process
```python
from recruitment_orchestrator_langgraph import LangGraphRecruitmentOrchestrator

orchestrator = LangGraphRecruitmentOrchestrator()
result = orchestrator.start_recruitment_process()

print(f"Workflow Status: {result['workflow_status']}")
print(f"Job Openings: {result['job_openings_count']}")
```

### Processing Candidate Applications
```python
candidate_data = {
    "candidate_name": "John Doe",
    "position": "Senior Software Engineer",
    "experience_years": 5,
    "resume_text": "Experienced developer...",
    "cover_letter": "Passionate about..."
}

result = orchestrator.process_candidate_application(candidate_data, "Senior Software Engineer")
```

### Running the Complete Workflow
```python
# The system automatically orchestrates all agents
# 1. Analyzes job requirements
# 2. Screens candidates
# 3. Schedules interviews
# 4. Conducts interviews
# 5. Makes hiring decisions
# 6. Generates reports

final_state = orchestrator.workflow.invoke(initial_state)
```

## 🔍 Workflow Steps

### 1. Requirements Analysis
- **Agent**: Recruitment Analyzer
- **Input**: Employee CSV data
- **Output**: Job openings and requirements
- **AI Features**: Job description generation, skill identification

### 2. Candidate Screening
- **Agent**: Candidate Screener
- **Input**: Candidate data + job requirements
- **Output**: Screening scores and recommendations
- **AI Features**: Skill matching, experience evaluation, cultural fit assessment

### 3. Interview Scheduling
- **Agent**: Interview Coordinator
- **Input**: Qualified candidates + job requirements
- **Output**: Interview schedules and questions
- **AI Features**: Question generation, schedule optimization

### 4. Interview Conduction
- **Agent**: Interview Coordinator + Decision Maker
- **Input**: Interview feedback and evaluations
- **Output**: Candidate assessments
- **AI Features**: Feedback analysis, scoring algorithms

### 5. Decision Making
- **Agent**: Decision Maker
- **Input**: All candidate data and evaluations
- **Output**: Hiring decisions
- **AI Features**: Multi-factor decision algorithms

### 6. Report Generation
- **Agent**: Report Generator
- **Input**: Complete recruitment data
- **Output**: Comprehensive reports
- **AI Features**: Data analysis, insight generation

## 🚀 Advanced Features

### State Persistence
- Workflow state is maintained throughout the process
- Easy to resume interrupted workflows
- Historical data tracking and analysis

### Agent Extensibility
- Easy to add new agents to the workflow
- Configurable agent behavior and parameters
- Plugin-based architecture for custom agents

### Workflow Customization
- Modify workflow steps and transitions
- Add conditional logic and branching
- Custom error handling and recovery

### Real-time Monitoring
- Track workflow progress in real-time
- Monitor agent performance and interactions
- Debug and troubleshoot workflow issues

## 📊 Performance Metrics

The system tracks various metrics:
- **Workflow Completion Rate**: Percentage of successful workflow runs
- **Agent Response Time**: Time taken by each agent to complete tasks
- **Error Rates**: Frequency and types of errors encountered
- **Candidate Processing Speed**: Time to process each candidate
- **Interview Success Rate**: Percentage of successful interviews

## 🔧 Development

### Adding New Agents
```python
class NewAgent:
    async def process(self, state: RecruitmentState) -> RecruitmentState:
        # Agent logic here
        return state

# Add to workflow
workflow.add_node("new_agent", NewAgent().process)
workflow.add_edge("previous_step", "new_agent")
```

### Customizing Workflows
```python
# Add conditional logic
def should_continue(state: RecruitmentState) -> str:
    if state["errors"]:
        return "error_handler"
    return "next_step"

workflow.add_conditional_edges("current_step", should_continue)
```

### Error Handling
```python
async def error_handler(state: RecruitmentState) -> RecruitmentState:
    # Handle errors and recover
    state["workflow_status"] = "recovered"
    return state

workflow.add_node("error_handler", error_handler)
```

## 🧪 Testing

### Run the Demo
```bash
python demo_langgraph.py
```

### Test Individual Components
```bash
# Test the orchestrator
python -c "from recruitment_orchestrator_langgraph import LangGraphRecruitmentOrchestrator; print('Import successful')"

# Test the workflow
python -c "from recruitment_orchestrator_langgraph import LangGraphRecruitmentOrchestrator; o = LangGraphRecruitmentOrchestrator(); print('Workflow built successfully')"
```

## 📈 Future Enhancements

### Planned Features
- **Multi-language Support**: Support for different languages and regions
- **Advanced Analytics**: Machine learning-based insights and predictions
- **Integration APIs**: Connect with external HR systems
- **Mobile App**: Native mobile application for recruiters
- **AI Chatbot**: Interactive candidate communication

### Scalability Improvements
- **Distributed Processing**: Handle multiple recruitment processes simultaneously
- **Cloud Deployment**: Deploy to cloud platforms for scalability
- **Database Integration**: Persistent storage for large-scale operations
- **API Rate Limiting**: Handle high-volume API requests

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the documentation and examples
- Review the error logs and debugging information

## 🎉 Acknowledgments

- **LangGraph**: For the powerful workflow orchestration framework
- **LangChain**: For the AI agent infrastructure
- **Groq**: For the high-performance LLM API
- **FastAPI**: For the modern web framework

---

**Transform your recruitment process with the power of multi-agent AI orchestration! 🚀**
