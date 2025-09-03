import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime
import json
import os

from agents.recruitment_analyzer import RecruitmentAnalyzer
from agents.candidate_screener import CandidateScreener
from agents.interview_coordinator import InterviewCoordinator
from config import EMPLOYEES_CSV, UPLOADS_DIR, REPORTS_DIR

class RecruitmentOrchestrator:
    """
    Main orchestrator that coordinates all AI agents for the recruitment process
    """
    
    def __init__(self):
        self.analyzer = RecruitmentAnalyzer()
        self.screener = CandidateScreener()
        self.interview_coordinator = InterviewCoordinator()
        
        # Ensure directories exist
        os.makedirs(UPLOADS_DIR, exist_ok=True)
        os.makedirs(REPORTS_DIR, exist_ok=True)
        
        # Store recruitment data
        self.job_openings = []
        self.candidates = []
        self.interviews = []
        self.final_selections = []
    
    def start_recruitment_process(self) -> Dict:
        """
        Start the complete recruitment process
        """
        try:
            print("🚀 Starting AI Recruitment Process...")
            
            # Step 1: Analyze employee data and identify job openings
            print("📊 Step 1: Analyzing employee data...")
            analysis_result = self.analyzer.analyze_employee_data(EMPLOYEES_CSV)
            
            if analysis_result["status"] != "openings_found":
                return analysis_result
            
            self.job_openings = analysis_result["job_openings"]
            print(f"✅ Found {len(self.job_openings)} job opening(s)")
            
            # Step 2: Generate recruitment report
            print("📝 Step 2: Generating recruitment report...")
            report = self.analyzer.generate_recruitment_report(self.job_openings)
            self._save_report("recruitment_analysis.md", report)
            
            # Step 3: Create job postings
            print("📋 Step 3: Creating job postings...")
            job_postings = self._create_job_postings()
            
            return {
                "status": "success",
                "message": "Recruitment process started successfully",
                "job_openings_count": len(self.job_openings),
                "job_postings": job_postings,
                "report_path": f"{REPORTS_DIR}/recruitment_analysis.md"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error starting recruitment process: {str(e)}"
            }
    
    def process_candidate_application(self, candidate_data: Dict, job_position: str) -> Dict:
        """
        Process a candidate's application for a specific job position
        """
        try:
            # Find the job requirements
            job_requirements = self._find_job_requirements(job_position)
            if not job_requirements:
                return {
                    "status": "error",
                    "message": f"Job position '{job_position}' not found"
                }
            
            # Step 1: Screen the candidate
            print(f"🔍 Screening candidate: {candidate_data.get('candidate_name')}")
            screening_result = self.screener.screen_candidate(candidate_data, job_requirements)
            
            if screening_result["screening_status"] == "error":
                return screening_result
            
            # Step 2: Create interview schedule if candidate passes screening
            if screening_result["recommendation"].startswith(("Strongly Recommend", "Recommend")):
                print(f"📅 Creating interview schedule for: {candidate_data.get('candidate_name')}")
                interview_schedule = self.interview_coordinator.create_interview_schedule(
                    candidate_data, job_requirements
                )
                
                # Store candidate and interview data
                self.candidates.append({
                    **candidate_data,
                    "screening_result": screening_result,
                    "interview_schedule": interview_schedule,
                    "application_date": datetime.now().isoformat(),
                    "status": "interview_scheduled"
                })
                
                return {
                    "status": "success",
                    "message": "Candidate passed screening and interview scheduled",
                    "screening_result": screening_result,
                    "interview_schedule": interview_schedule
                }
            else:
                # Store rejected candidate
                self.candidates.append({
                    **candidate_data,
                    "screening_result": screening_result,
                    "application_date": datetime.now().isoformat(),
                    "status": "rejected"
                })
                
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
        """
        Conduct an interview stage and update status
        """
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
        """
        Make final selection decision for a candidate
        """
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
                self.final_selections.append({
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
    
    def generate_recruitment_summary(self) -> Dict:
        """
        Generate a comprehensive summary of the recruitment process
        """
        try:
            summary = {
                "total_job_openings": len(self.job_openings),
                "total_candidates": len(self.candidates),
                "candidates_by_status": self._count_candidates_by_status(),
                "interview_completion_rate": self._calculate_interview_completion_rate(),
                "hiring_success_rate": self._calculate_hiring_success_rate(),
                "average_time_to_hire": self._calculate_average_time_to_hire(),
                "top_performing_candidates": self._get_top_performing_candidates(),
                "recruitment_insights": self._generate_recruitment_insights()
            }
            
            # Save summary report
            self._save_report("recruitment_summary.json", json.dumps(summary, indent=2))
            
            return summary
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error generating recruitment summary: {str(e)}"
            }
    
    def _create_job_postings(self) -> List[Dict]:
        """
        Create job postings for each opening
        """
        job_postings = []
        
        for opening in self.job_openings:
            posting = {
                "job_id": f"job_{opening['employee_id']}",
                "title": opening['position'],
                "department": opening['department'],
                "location": "Remote/Hybrid",
                "type": "Full-time",
                "salary_range": opening['salary_range'],
                "experience_required": opening['experience_level'],
                "required_skills": opening['required_skills'],
                "job_description": opening['job_description'],
                "priority": opening['priority'],
                "posted_date": datetime.now().isoformat(),
                "status": "active"
            }
            job_postings.append(posting)
        
        return job_postings
    
    def _find_job_requirements(self, job_position: str) -> Optional[Dict]:
        """
        Find job requirements for a specific position
        """
        for opening in self.job_openings:
            if opening['position'].lower() == job_position.lower():
                return opening
        return None
    
    def _find_candidate(self, candidate_id: str) -> Optional[Dict]:
        """
        Find a candidate by ID
        """
        for candidate in self.candidates:
            if candidate.get('candidate_id') == candidate_id:
                return candidate
        return None
    
    def _all_interviews_completed(self, candidate: Dict) -> bool:
        """
        Check if all interview stages are completed
        """
        interview_status = candidate.get("interview_status", {})
        interview_schedule = candidate.get("interview_schedule", {})
        
        if not interview_schedule:
            return False
        
        required_stages = interview_schedule.get("interview_stages", [])
        completed_stages = [stage for stage, status in interview_status.items() 
                          if status.get("status") == "completed"]
        
        return len(completed_stages) == len(required_stages)
    
    def _evaluate_final_candidate(self, candidate: Dict) -> Dict:
        """
        Evaluate candidate after all interviews are completed
        """
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
        """
        Get final recommendation based on score
        """
        if final_score >= 80:
            return "Strongly Recommend Hiring"
        elif final_score >= 70:
            return "Recommend Hiring"
        elif final_score >= 60:
            return "Consider Hiring"
        else:
            return "Do Not Recommend Hiring"
    
    def _get_next_steps(self, candidate: Dict, current_stage: str) -> List[str]:
        """
        Get next steps for a candidate
        """
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
        """
        Count candidates by their current status
        """
        status_counts = {}
        for candidate in self.candidates:
            status = candidate.get("status", "unknown")
            status_counts[status] = status_counts.get(status, 0) + 1
        return status_counts
    
    def _calculate_interview_completion_rate(self) -> float:
        """
        Calculate interview completion rate
        """
        if not self.candidates:
            return 0.0
        
        completed_interviews = sum(1 for candidate in self.candidates 
                                 if candidate.get("status") in ["all_interviews_completed", "hired"])
        return round((completed_interviews / len(self.candidates)) * 100, 2)
    
    def _calculate_hiring_success_rate(self) -> float:
        """
        Calculate hiring success rate
        """
        if not self.candidates:
            return 0.0
        
        hired_candidates = sum(1 for candidate in self.candidates 
                              if candidate.get("status") == "hired")
        return round((hired_candidates / len(self.candidates)) * 100, 2)
    
    def _calculate_average_time_to_hire(self) -> str:
        """
        Calculate average time to hire
        """
        hired_candidates = [c for c in self.candidates if c.get("status") == "hired"]
        
        if not hired_candidates:
            return "N/A"
        
        total_days = 0
        for candidate in hired_candidates:
            application_date = datetime.fromisoformat(candidate.get("application_date", ""))
            selection_date = datetime.fromisoformat(candidate.get("selection_date", ""))
            days = (selection_date - application_date).days
            total_days += days
        
        average_days = total_days / len(hired_candidates)
        return f"{average_days:.1f} days"
    
    def _get_top_performing_candidates(self) -> List[Dict]:
        """
        Get top performing candidates
        """
        candidates_with_scores = []
        for candidate in self.candidates:
            screening_result = candidate.get("screening_result", {})
            score = screening_result.get("overall_score", 0)
            candidates_with_scores.append({
                "candidate_id": candidate.get("candidate_id"),
                "candidate_name": candidate.get("candidate_name"),
                "position": candidate.get("position"),
                "score": score,
                "status": candidate.get("status")
            })
        
        # Sort by score (descending) and return top 5
        candidates_with_scores.sort(key=lambda x: x["score"], reverse=True)
        return candidates_with_scores[:5]
    
    def _generate_recruitment_insights(self) -> List[str]:
        """
        Generate insights about the recruitment process
        """
        insights = []
        
        if self.candidates:
            # Skill gap analysis
            skill_gaps = {}
            for candidate in self.candidates:
                screening_result = candidate.get("screening_result", {})
                skill_analysis = screening_result.get("skill_analysis", {})
                missing_skills = skill_analysis.get("missing_skills", [])
                
                for skill in missing_skills:
                    skill_gaps[skill] = skill_gaps.get(skill, 0) + 1
            
            if skill_gaps:
                top_missing_skills = sorted(skill_gaps.items(), key=lambda x: x[1], reverse=True)[:3]
                insights.append(f"Most commonly missing skills: {', '.join([skill for skill, _ in top_missing_skills])}")
            
            # Experience level insights
            experience_levels = {}
            for candidate in self.candidates:
                screening_result = candidate.get("screening_result", {})
                experience_analysis = screening_result.get("experience_analysis", {})
                assessment = experience_analysis.get("assessment", "Unknown")
                experience_levels[assessment] = experience_levels.get(assessment, 0) + 1
            
            if experience_levels:
                insights.append(f"Candidate experience distribution: {dict(experience_levels)}")
        
        return insights
    
    def _save_report(self, filename: str, content: str) -> None:
        """
        Save a report to the reports directory
        """
        filepath = os.path.join(REPORTS_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"📄 Report saved: {filepath}")

    def score_candidate_resume(self, candidate_data: Dict) -> Dict:
        """
        Score a candidate resume using AI analysis
        """
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

    def add_candidate_from_scoring(self, candidate_id: str, decision: str, notes: str) -> Dict:
        """
        Add a candidate from the scoring process to the main candidate list
        """
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
            
            self.candidates.append(candidate_data)
            
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
