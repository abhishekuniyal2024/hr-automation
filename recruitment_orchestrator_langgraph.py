import pandas as pd
from typing import Dict, List, Optional, TypedDict, Annotated
from datetime import datetime
import json
import os
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq

from agents.recruitment_analyzer import RecruitmentAnalyzer
from agents.candidate_screener import CandidateScreener
from agents.interview_coordinator import InterviewCoordinator
from config import GROQ_API_KEY, GROQ_MODEL, EMPLOYEES_CSV, UPLOADS_DIR, REPORTS_DIR

# Define the state structure for the LangGraph workflow
class RecruitmentState(TypedDict):
    """State structure for the recruitment workflow"""
    messages: Annotated[List, "List of messages in the conversation"]
    job_openings: Annotated[List, "List of identified job openings"]
    candidates: Annotated[List, "List of candidates being processed"]
    current_candidate: Annotated[Optional[Dict], "Current candidate being processed"]
    screening_results: Annotated[List, "List of screening results"]
    interview_schedules: Annotated[List, "List of interview schedules"]
    final_selections: Annotated[List, "List of final hiring decisions"]
    workflow_status: Annotated[str, "Current status of the workflow"]
    errors: Annotated[List, "List of any errors encountered"]
    reports: Annotated[List, "List of generated reports"]

class LangGraphRecruitmentOrchestrator:
    """
    Multi-agent AI recruitment system using LangGraph for orchestration
    """
    
    def __init__(self):
        # Initialize the LLM
        self.llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name=GROQ_MODEL
        )
        
        # Initialize individual agents
        self.analyzer = RecruitmentAnalyzer()
        self.screener = CandidateScreener()
        self.interview_coordinator = InterviewCoordinator()
        
        # Ensure directories exist
        os.makedirs(UPLOADS_DIR, exist_ok=True)
        os.makedirs(REPORTS_DIR, exist_ok=True)
        
        # Build the LangGraph workflow
        self.workflow = self._build_workflow()
        
        # Initialize state
        self.state = {
            "messages": [],
            "job_openings": [],
            "candidates": [],
            "current_candidate": None,
            "screening_results": [],
            "interview_schedules": [],
            "final_selections": [],
            "workflow_status": "initialized",
            "errors": [],
            "reports": []
        }
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow for recruitment"""
        
        # Define the workflow graph
        workflow = StateGraph(RecruitmentState)
        
        # Add nodes for each step
        workflow.add_node("analyze_requirements", self._analyze_job_requirements)
        workflow.add_node("screen_candidates", self._screen_candidates)
        workflow.add_node("schedule_interviews", self._schedule_interviews)
        workflow.add_node("conduct_interviews", self._conduct_interviews)
        workflow.add_node("make_decisions", self._make_hiring_decisions)
        workflow.add_node("generate_reports", self._generate_reports)
        
        # Define the workflow edges
        workflow.set_entry_point("analyze_requirements")
        
        workflow.add_edge("analyze_requirements", "screen_candidates")
        workflow.add_edge("screen_candidates", "schedule_interviews")
        workflow.add_edge("schedule_interviews", "conduct_interviews")
        workflow.add_edge("conduct_interviews", "make_decisions")
        workflow.add_edge("make_decisions", "generate_reports")
        workflow.add_edge("generate_reports", END)
        
        # Compile the workflow
        return workflow.compile()
    
    def _analyze_job_requirements(self, state: RecruitmentState) -> RecruitmentState:
        """Analyze employee data and identify job openings"""
        try:
            # Add message to state
            state["messages"].append(HumanMessage(content="Starting job requirements analysis..."))
            
            # Use the analyzer agent
            analysis_result = self.analyzer.analyze_employee_data(EMPLOYEES_CSV)
            
            if analysis_result["status"] == "openings_found":
                state["job_openings"] = analysis_result["job_openings"]
                state["workflow_status"] = "requirements_analyzed"
                
                # Generate recruitment report
                report = self.analyzer.generate_recruitment_report(analysis_result["job_openings"])
                state["reports"].append({
                    "type": "recruitment_analysis",
                    "content": report,
                    "timestamp": datetime.now().isoformat()
                })
                
                state["messages"].append(AIMessage(content=f"Found {len(analysis_result['job_openings'])} job openings. Moving to candidate screening."))
            else:
                state["errors"].append(f"No job openings found: {analysis_result.get('message', 'Unknown error')}")
                state["workflow_status"] = "no_openings"
            
        except Exception as e:
            state["errors"].append(f"Error in requirements analysis: {str(e)}")
            state["workflow_status"] = "error"
        
        return state
    
    def _screen_candidates(self, state: RecruitmentState) -> RecruitmentState:
        """Screen candidates for job openings"""
        try:
            state["messages"].append(HumanMessage(content="Starting candidate screening process..."))
            
            # For now, we'll process any existing candidates
            # In a real scenario, this would come from external applications
            if state["candidates"]:
                for candidate in state["candidates"]:
                    # Find matching job requirements
                    job_requirements = self._find_job_requirements(candidate.get("position", ""))
                    if job_requirements:
                        screening_result = self.screener.screen_candidate(candidate, job_requirements)
                        state["screening_results"].append(screening_result)
                        
                        # Update candidate status
                        candidate["screening_result"] = screening_result
                        if screening_result.get("recommendation", "").startswith(("Strongly Recommend", "Recommend")):
                            candidate["status"] = "passed_screening"
                        else:
                            candidate["status"] = "rejected"
            
            state["workflow_status"] = "candidates_screened"
            state["messages"].append(AIMessage(content=f"Screened {len(state['candidates'])} candidates. Moving to interview scheduling."))
            
        except Exception as e:
            state["errors"].append(f"Error in candidate screening: {str(e)}")
            state["workflow_status"] = "error"
        
        return state
    
    def _schedule_interviews(self, state: RecruitmentState) -> RecruitmentState:
        """Schedule interviews for qualified candidates"""
        try:
            state["messages"].append(HumanMessage(content="Scheduling interviews for qualified candidates..."))
            
            qualified_candidates = [c for c in state["candidates"] if c.get("status") == "passed_screening"]
            
            for candidate in qualified_candidates:
                job_requirements = self._find_job_requirements(candidate.get("position", ""))
                if job_requirements:
                    interview_schedule = self.interview_coordinator.create_interview_schedule(
                        candidate, job_requirements
                    )
                    state["interview_schedules"].append(interview_schedule)
                    
                    # Update candidate with interview schedule
                    candidate["interview_schedule"] = interview_schedule
                    candidate["status"] = "interview_scheduled"
            
            state["workflow_status"] = "interviews_scheduled"
            state["messages"].append(AIMessage(content=f"Scheduled interviews for {len(qualified_candidates)} candidates. Moving to interview conduction."))
            
        except Exception as e:
            state["errors"].append(f"Error in interview scheduling: {str(e)}")
            state["workflow_status"] = "error"
        
        return state
    
    def _conduct_interviews(self, state: RecruitmentState) -> RecruitmentState:
        """Conduct interviews and collect feedback"""
        try:
            state["messages"].append(HumanMessage(content="Conducting interviews and collecting feedback..."))
            
            # Simulate interview conduction
            # In a real scenario, this would involve actual interview sessions
            for candidate in state["candidates"]:
                if candidate.get("status") == "interview_scheduled":
                    # Simulate interview completion
                    candidate["status"] = "interviews_completed"
                    candidate["interview_feedback"] = {
                        "overall_rating": "Good",
                        "technical_skills": "Strong",
                        "communication": "Excellent",
                        "cultural_fit": "Good",
                        "recommendation": "Proceed to next stage"
                    }
            
            state["workflow_status"] = "interviews_completed"
            state["messages"].append(AIMessage(content="All interviews completed. Moving to hiring decisions."))
            
        except Exception as e:
            state["errors"].append(f"Error in interview conduction: {str(e)}")
            state["workflow_status"] = "error"
        
        return state
    
    def _make_hiring_decisions(self, state: RecruitmentState) -> RecruitmentState:
        """Make final hiring decisions based on all collected data"""
        try:
            state["messages"].append(HumanMessage(content="Making final hiring decisions..."))
            
            for candidate in state["candidates"]:
                if candidate.get("status") == "interviews_completed":
                    # Evaluate candidate for final decision
                    final_evaluation = self._evaluate_final_candidate(candidate)
                    candidate["final_evaluation"] = final_evaluation
                    
                    # Make decision based on evaluation
                    if final_evaluation["final_score"] >= 70:
                        decision = "hired"
                        state["final_selections"].append({
                            "candidate_id": candidate.get("candidate_id"),
                            "candidate_name": candidate.get("candidate_name"),
                            "position": candidate.get("position"),
                            "decision": decision,
                            "final_score": final_evaluation["final_score"],
                            "timestamp": datetime.now().isoformat()
                        })
                    else:
                        decision = "not_hired"
                    
                    candidate["status"] = decision
                    candidate["decision_date"] = datetime.now().isoformat()
            
            state["workflow_status"] = "decisions_made"
            state["messages"].append(AIMessage(content=f"Made hiring decisions for {len([c for c in state['candidates'] if c.get('status') in ['hired', 'not_hired']])} candidates. Moving to report generation."))
            
        except Exception as e:
            state["errors"].append(f"Error in hiring decisions: {str(e)}")
            state["workflow_status"] = "error"
        
        return state
    
    def _generate_reports(self, state: RecruitmentState) -> RecruitmentState:
        """Generate comprehensive recruitment reports"""
        try:
            state["messages"].append(HumanMessage(content="Generating comprehensive recruitment reports..."))
            
            # Generate summary report
            summary = self._generate_recruitment_summary(state)
            state["reports"].append({
                "type": "recruitment_summary",
                "content": summary,
                "timestamp": datetime.now().isoformat()
            })
            
            # Save reports to files
            self._save_reports(state["reports"])
            
            state["workflow_status"] = "completed"
            state["messages"].append(AIMessage(content="Recruitment workflow completed successfully. All reports generated."))
            
        except Exception as e:
            state["errors"].append(f"Error in report generation: {str(e)}")
            state["workflow_status"] = "error"
        
        return state
    
    def start_recruitment_process(self) -> Dict:
        """Start the complete recruitment process using LangGraph"""
        try:
            print("🚀 Starting LangGraph Multi-Agent Recruitment Process...")
            
            initial_state = RecruitmentState(
                messages=[],
                job_openings=[],
                candidates=[],
                current_candidate=None,
                screening_results=[],
                interview_schedules=[],
                final_selections=[],
                workflow_status="started",
                errors=[],
                reports=[]
            )
            
            final_state = self.workflow.invoke(initial_state)
            
            # Update the orchestrator's state with the workflow results
            self.state.update(final_state)
            
            return {
                "status": "success",
                "message": "Recruitment process completed successfully",
                "workflow_status": final_state["workflow_status"],
                "job_openings_count": len(final_state["job_openings"]),
                "candidates_count": len(final_state["candidates"]),
                "hired_count": len([c for c in final_state["candidates"] if c.get("status") == "hired"]),
                "reports_generated": len(final_state["reports"]),
                "errors": final_state["errors"]
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error in recruitment process: {str(e)}"
            }
    
    def generate_recruitment_summary(self) -> Dict:
        """Generate a comprehensive summary of the recruitment process"""
        try:
            summary = {
                "total_job_openings": len(self.state["job_openings"]),
                "total_candidates": len(self.state["candidates"]),
                "candidates_by_status": self._count_candidates_by_status(),
                "interview_completion_rate": self._calculate_interview_completion_rate(),
                "hiring_success_rate": self._calculate_hiring_success_rate(),
                "average_time_to_hire": self._calculate_average_time_to_hire(),
                "top_performing_candidates": self._get_top_performing_candidates(),
                "recruitment_insights": self._generate_recruitment_insights(),
                "workflow_status": self.state["workflow_status"],
                "reports_generated": len(self.state["reports"]),
                "errors_encountered": len(self.state["errors"])
            }
            
            self._save_report("recruitment_summary.json", json.dumps(summary, indent=2))
            
            return summary
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error generating recruitment summary: {str(e)}"
            }
    
    def score_candidate_resume(self, candidate_data: Dict) -> Dict:
        """Score a candidate resume using AI analysis"""
        try:
            # Use the candidate screener to analyze the resume
            job_requirements = self._find_job_requirements(candidate_data.get("position", "Senior Software Engineer"))
            if not job_requirements:
                job_requirements = {
                    "position": "Senior Software Engineer",
                    "required_skills": ["Python", "JavaScript", "SQL", "Git", "Agile", "System Design"],
                    "experience_required": 5,
                    "department": "Engineering"
                }
            
            screening_result = self.screener.screen_candidate(candidate_data, job_requirements)
            
            return {
                "overall_score": screening_result.get("overall_score", 0.0),
                "skill_match_score": screening_result.get("skill_match_score", 0.0),
                "experience_match_score": screening_result.get("experience_match_score", 0.0),
                "cultural_fit_score": screening_result.get("cultural_fit_score", 0.0),
                "ai_feedback": screening_result.get("ai_feedback", "No feedback available"),
                "recommendation": screening_result.get("recommendation", "No recommendation")
            }
            
        except Exception as e:
            return {
                "overall_score": 0.0,
                "skill_match_score": 0.0,
                "experience_match_score": 0.0,
                "cultural_fit_score": 0.0,
                "ai_feedback": f"Error analyzing resume: {str(e)}",
                "recommendation": "Error in analysis"
            }
    
    def process_candidate_application(self, candidate_data: Dict, job_position: str) -> Dict:
        """Process a candidate's application for a specific job position"""
        try:
            # Find the job requirements
            job_requirements = self._find_job_requirements(job_position)
            if not job_requirements:
                return {
                    "status": "error",
                    "message": f"Job position '{job_position}' not found"
                }
            
            # Add candidate to state
            candidate_data["candidate_id"] = f"candidate_{len(self.state['candidates']) + 1}"
            candidate_data["application_date"] = datetime.now().isoformat()
            candidate_data["status"] = "applied"
            
            self.state["candidates"].append(candidate_data)
            
            # Screen the candidate
            screening_result = self.screener.screen_candidate(candidate_data, job_requirements)
            
            if screening_result["screening_status"] == "error":
                return screening_result
            
            # Update candidate with screening result
            candidate_data["screening_result"] = screening_result
            
            # Create interview schedule if candidate passes screening
            if screening_result["recommendation"].startswith(("Strongly Recommend", "Recommend")):
                interview_schedule = self.interview_coordinator.create_interview_schedule(
                    candidate_data, job_requirements
                )
                
                candidate_data["interview_schedule"] = interview_schedule
                candidate_data["status"] = "interview_scheduled"
                
                return {
                    "status": "success",
                    "message": "Candidate passed screening and interview scheduled",
                    "screening_result": screening_result,
                    "interview_schedule": interview_schedule
                }
            else:
                candidate_data["status"] = "rejected"
                
                return {
                    "status": "success",
                    "message": "Candidate screened but did not meet requirements",
                    "screening_result": screening_result
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error processing candidate application: {str(e)}"
            }
    
    def conduct_interview(self, candidate_id: str, stage: str, feedback: str = "") -> Dict:
        """Conduct an interview stage and update status"""
        try:
            # Find the candidate
            candidate = self._find_candidate(candidate_id)
            if not candidate:
                return {
                    "status": "error",
                    "message": f"Candidate with ID {candidate_id} not found"
                }
            
            # Update interview status
            status_update = self.interview_coordinator.update_interview_status(
                candidate_id, stage, "completed", feedback
            )
            
            # Update candidate status
            candidate["interview_status"] = candidate.get("interview_status", {})
            candidate["interview_status"][stage] = status_update
            
            # Check if all interview stages are completed
            if self._all_interviews_completed(candidate):
                candidate["status"] = "all_interviews_completed"
                candidate["final_evaluation"] = self._evaluate_final_candidate(candidate)
            
            return {
                "status": "success",
                "message": f"Interview stage '{stage}' completed",
                "candidate_status": candidate["status"],
                "next_steps": self._get_next_steps(candidate, stage)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error conducting interview: {str(e)}"
            }
    
    def make_final_selection(self, candidate_id: str, decision: str, notes: str = "") -> Dict:
        """Make final selection decision for a candidate"""
        try:
            candidate = self._find_candidate(candidate_id)
            if not candidate:
                return {
                    "status": "error",
                    "message": f"Candidate with ID {candidate_id} not found"
                }
            
            # Update candidate status
            candidate["status"] = decision
            candidate["selection_notes"] = notes
            candidate["selection_date"] = datetime.now().isoformat()
            
            if decision == "hired":
                self.state["final_selections"].append({
                    "candidate_id": candidate_id,
                    "candidate_name": candidate.get("candidate_name"),
                    "position": candidate.get("position"),
                    "hiring_date": datetime.now().isoformat(),
                    "notes": notes
                })
            
            return {
                "status": "success",
                "message": f"Final selection made: {decision}",
                "candidate_status": candidate["status"]
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error making final selection: {str(e)}"
            }
    
    def add_candidate_from_scoring(self, candidate_id: str, decision: str, notes: str) -> Dict:
        """Add a candidate from the scoring process to the main candidate list"""
        try:
            # Create a new candidate entry
            candidate_data = {
                "candidate_id": candidate_id,
                "candidate_name": f"Candidate {candidate_id}",
                "email": "candidate@example.com",
                "phone": "Not provided",
                "position": "Senior Software Engineer",
                "experience_years": 3,
                "resume_text": "Resume from scoring process",
                "cover_letter": "Not provided",
                "application_date": datetime.now().isoformat(),
                "status": decision,
                "selection_notes": notes,
                "selection_date": datetime.now().isoformat()
            }
            
            self.state["candidates"].append(candidate_data)
            
            return {
                "status": "success",
                "message": f"Candidate {candidate_id} has been {decision}",
                "candidate_id": candidate_id
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error adding candidate: {str(e)}"
            }
    
    # Helper methods
    def _find_job_requirements(self, job_position: str) -> Optional[Dict]:
        """Find job requirements for a specific position"""
        # First try exact match
        for opening in self.state["job_openings"]:
            if opening['position'].lower() == job_position.lower():
                return opening
        
        # If no exact match, try partial match or return a default
        for opening in self.state["job_openings"]:
            if any(keyword in opening['position'].lower() for keyword in job_position.lower().split()):
                return opening
        
        # If still no match, return the first available job opening as fallback
        if self.state["job_openings"]:
            return self.state["job_openings"][0]
        
        return None
    
    def _find_candidate(self, candidate_id: str) -> Optional[Dict]:
        """Find a candidate by ID"""
        for candidate in self.state["candidates"]:
            if candidate.get('candidate_id') == candidate_id:
                return candidate
        return None
    
    def _all_interviews_completed(self, candidate: Dict) -> bool:
        """Check if all interview stages are completed"""
        interview_status = candidate.get("interview_status", {})
        interview_schedule = candidate.get("interview_schedule", {})
        
        if not interview_schedule:
            return False
        
        required_stages = interview_schedule.get("interview_stages", [])
        completed_stages = [stage for stage, status in interview_status.items() 
                          if status.get("status") == "completed"]
        
        return len(completed_stages) == len(required_stages)
    
    def _evaluate_final_candidate(self, candidate: Dict) -> Dict:
        """Evaluate candidate after all interviews are completed"""
        screening_result = candidate.get("screening_result", {})
        interview_status = candidate.get("interview_status", {})
        
        # Calculate final score based on screening and interview feedback
        final_score = screening_result.get("overall_score", 0)
        
        # Adjust score based on interview performance
        interview_scores = []
        for stage, status in interview_status.items():
            if status.get("status") == "completed":
                # Simple scoring based on feedback length (more detailed feedback = better)
                feedback = status.get("feedback", "")
                score = min(100, len(feedback.split()) * 2)  # 2 points per word, max 100
                interview_scores.append(score)
        
        if interview_scores:
            interview_average = sum(interview_scores) / len(interview_scores)
            final_score = (final_score * 0.6) + (interview_average * 0.4)
        
        return {
            "final_score": round(final_score, 2),
            "interview_performance": interview_scores,
            "recommendation": self._get_final_recommendation(final_score)
        }
    
    def _get_final_recommendation(self, final_score: float) -> str:
        """Get final recommendation based on score"""
        if final_score >= 80:
            return "Strongly Recommend Hiring"
        elif final_score >= 70:
            return "Recommend Hiring"
        elif final_score >= 60:
            return "Consider Hiring"
        else:
            return "Do Not Recommend Hiring"
    
    def _get_next_steps(self, candidate: Dict, current_stage: str) -> List[str]:
        """Get next steps for a candidate"""
        interview_schedule = candidate.get("interview_schedule", {})
        stages = interview_schedule.get("interview_stages", [])
        
        try:
            current_index = stages.index(current_stage)
            if current_index + 1 < len(stages):
                next_stage = stages[current_index + 1]
                return [f"Schedule {next_stage} interview"]
            else:
                return ["Complete final evaluation", "Make hiring decision"]
        except ValueError:
            return ["Review interview schedule"]
    
    def _count_candidates_by_status(self) -> Dict:
        """Count candidates by their current status"""
        status_counts = {}
        for candidate in self.state["candidates"]:
            status = candidate.get("status", "unknown")
            status_counts[status] = status_counts.get(status, 0) + 1
        return status_counts
    
    def _calculate_interview_completion_rate(self) -> float:
        """Calculate interview completion rate"""
        if not self.state["candidates"]:
            return 0.0
        
        completed_interviews = sum(1 for candidate in self.state["candidates"] 
                                 if candidate.get("status") in ["all_interviews_completed", "hired"])
        return round((completed_interviews / len(self.state["candidates"])) * 100, 2)
    
    def _calculate_hiring_success_rate(self) -> float:
        """Calculate hiring success rate"""
        if not self.state["candidates"]:
            return 0.0
        
        hired_candidates = sum(1 for candidate in self.state["candidates"] 
                              if candidate.get("status") == "hired")
        return round((hired_candidates / len(self.state["candidates"])) * 100, 2)
    
    def _calculate_average_time_to_hire(self) -> str:
        """Calculate average time to hire"""
        return "N/A"  # Simplified for demo
    
    def _get_top_performing_candidates(self) -> List[Dict]:
        """Get top performing candidates"""
        candidates_with_scores = []
        for candidate in self.state["candidates"]:
            screening_result = candidate.get("screening_result", {})
            score = screening_result.get("overall_score", 0)
            candidates_with_scores.append({
                "candidate_id": candidate.get("candidate_id"),
                "candidate_name": candidate.get("candidate_name"),
                "position": candidate.get("position"),
                "score": score,
                "status": candidate.get("status")
            })
        
        candidates_with_scores.sort(key=lambda x: x["score"], reverse=True)
        return candidates_with_scores[:5]
    
    def _generate_recruitment_insights(self) -> List[str]:
        """Generate insights about the recruitment process"""
        insights = []
        
        if self.state["candidates"]:
            insights.append(f"Total candidates processed: {len(self.state['candidates'])}")
            insights.append(f"Workflow status: {self.state['workflow_status']}")
        
        return insights
    
    def _save_report(self, filename: str, content: str) -> None:
        """Save a report to the reports directory"""
        filepath = os.path.join(REPORTS_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"📄 Report saved: {filepath}")
    
    def _save_reports(self, reports: List[Dict]) -> None:
        """Save all reports to files"""
        for report in reports:
            report_type = report.get("type", "unknown")
            timestamp = report.get("timestamp", datetime.now().isoformat())
            filename = f"{report_type}_{timestamp[:10]}.md"
            
            if report_type == "recruitment_summary":
                filename = f"{report_type}_{timestamp[:10]}.json"
            
            self._save_report(filename, str(report.get("content", "")))
    
    def _generate_recruitment_summary(self, state: RecruitmentState) -> Dict:
        """Generate summary from the current state"""
        return {
            "total_job_openings": len(state["job_openings"]),
            "total_candidates": len(state["candidates"]),
            "candidates_by_status": self._count_candidates_by_status(),
            "interview_completion_rate": self._calculate_interview_completion_rate(),
            "hiring_success_rate": self._calculate_hiring_success_rate(),
            "average_time_to_hire": self._calculate_average_time_to_hire(),
            "top_performing_candidates": self._get_top_performing_candidates(),
            "recruitment_insights": self._generate_recruitment_insights(),
            "workflow_status": state["workflow_status"],
            "reports_generated": len(state["reports"]),
            "errors_encountered": len(state["errors"])
        }

# Keep the old class for backward compatibility
class RecruitmentOrchestrator(LangGraphRecruitmentOrchestrator):
    """Backward compatibility wrapper"""
    pass
