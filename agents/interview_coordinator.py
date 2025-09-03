import groq
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from config import GROQ_API_KEY, GROQ_MODEL, INTERVIEW_STAGES

class InterviewCoordinator:
    """
    AI Agent responsible for coordinating interviews and generating interview questions
    """
    
    def __init__(self):
        self.client = groq.Groq(api_key=GROQ_API_KEY)
        self.model = GROQ_MODEL
    
    def create_interview_schedule(self, candidate_data: Dict, job_requirements: Dict) -> Dict:
        """
        Create a comprehensive interview schedule for a candidate
        """
        try:
            position = job_requirements.get('position', '')
            department = job_requirements.get('department', '')
            priority = job_requirements.get('priority', 'Normal')
            
            # Determine interview stages based on position and priority
            interview_stages = self._determine_interview_stages(position, department, priority)
            
            # Generate interview schedule
            schedule = self._generate_schedule(interview_stages, priority)
            
            # Generate questions for each stage
            stage_questions = {}
            for stage in interview_stages:
                questions = self._generate_interview_questions(stage, position, department)
                stage_questions[stage] = questions
            
            return {
                "candidate_id": candidate_data.get('candidate_id'),
                "candidate_name": candidate_data.get('candidate_name'),
                "position": position,
                "department": department,
                "interview_stages": interview_stages,
                "schedule": schedule,
                "stage_questions": stage_questions,
                "total_duration": self._calculate_total_duration(schedule),
                "status": "scheduled"
            }
            
        except Exception as e:
            return {
                "candidate_id": candidate_data.get('candidate_id'),
                "status": "error",
                "error_message": str(e)
            }
    
    def _determine_interview_stages(self, position: str, department: str, priority: str) -> List[str]:
        """
        Determine which interview stages are needed based on position and priority
        """
        base_stages = ["Initial Screening"]
        
        # Add technical assessment for technical roles
        technical_positions = ["Software Engineer", "DevOps Engineer", "Data Analyst", 
                             "QA Engineer", "Cloud Architect", "Network Engineer"]
        if position in technical_positions:
            base_stages.append("Technical Assessment")
        
        # Add HR interview for all positions
        base_stages.append("HR Interview")
        
        # Add final round for senior positions or high priority
        if "Senior" in position or "Manager" in position or priority == "High":
            base_stages.append("Final Round")
        
        # Add reference check for final candidates
        base_stages.append("Reference Check")
        
        return base_stages
    
    def _generate_schedule(self, stages: List[str], priority: str) -> Dict:
        """
        Generate interview schedule with timing
        """
        schedule = {}
        current_date = datetime.now()
        
        # Adjust timing based on priority
        if priority == "High":
            days_between = 1
        elif priority == "Medium":
            days_between = 2
        else:
            days_between = 3
        
        for i, stage in enumerate(stages):
            if i == 0:
                # First interview within 2-3 days
                interview_date = current_date + timedelta(days=2)
            else:
                interview_date = current_date + timedelta(days=2 + (i * days_between))
            
            # Determine duration based on stage
            duration = self._get_stage_duration(stage)
            
            schedule[stage] = {
                "date": interview_date.strftime("%Y-%m-%d"),
                "duration_minutes": duration,
                "type": self._get_interview_type(stage),
                "participants": self._get_stage_participants(stage)
            }
        
        return schedule
    
    def _get_stage_duration(self, stage: str) -> int:
        """
        Get duration for each interview stage
        """
        durations = {
            "Initial Screening": 30,
            "Technical Assessment": 60,
            "HR Interview": 45,
            "Final Round": 90,
            "Reference Check": 20
        }
        return durations.get(stage, 45)
    
    def _get_interview_type(self, stage: str) -> str:
        """
        Get interview type for each stage
        """
        types = {
            "Initial Screening": "Phone/Video Call",
            "Technical Assessment": "Technical Test + Discussion",
            "HR Interview": "In-person/Video Call",
            "Final Round": "Panel Interview",
            "Reference Check": "Phone Call"
        }
        return types.get(stage, "Video Call")
    
    def _get_stage_participants(self, stage: str) -> List[str]:
        """
        Get participants for each interview stage
        """
        participants = {
            "Initial Screening": ["HR Recruiter"],
            "Technical Assessment": ["Technical Lead", "Team Member"],
            "HR Interview": ["HR Manager"],
            "Final Round": ["Department Head", "HR Manager", "Technical Lead"],
            "Reference Check": ["HR Recruiter"]
        }
        return participants.get(stage, ["HR Recruiter"])
    
    def _generate_interview_questions(self, stage: str, position: str, department: str) -> Dict:
        """
        Generate AI-powered interview questions for each stage
        """
        questions = {}
        
        if stage == "Initial Screening":
            questions = self._generate_screening_questions(position, department)
        elif stage == "Technical Assessment":
            questions = self._generate_technical_questions(position, department)
        elif stage == "HR Interview":
            questions = self._generate_hr_questions(position, department)
        elif stage == "Final Round":
            questions = self._generate_final_questions(position, department)
        elif stage == "Reference Check":
            questions = self._generate_reference_questions(position, department)
        
        return questions
    
    def _generate_screening_questions(self, position: str, department: str) -> Dict:
        """
        Generate initial screening questions
        """
        prompt = f"""
        Generate 5-7 initial screening questions for a {position} position in {department}.
        
        Include questions about:
        1. Basic qualifications and experience
        2. Motivation for the role
        3. Availability and salary expectations
        4. Basic technical knowledge (if applicable)
        5. Cultural fit indicators
        
        Format as a dictionary with categories and questions.
        Keep questions concise and professional.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.7
            )
            
            # Parse the response and structure it
            content = response.choices[0].message.content
            return self._parse_questions_response(content, "Screening Questions")
            
        except Exception as e:
            return {
                "category": "Screening Questions",
                "questions": [
                    "Tell us about your experience in this field.",
                    "What interests you about this position?",
                    "What are your salary expectations?",
                    "When would you be available to start?",
                    "What do you know about our company?"
                ]
            }
    
    def _generate_technical_questions(self, position: str, department: str) -> Dict:
        """
        Generate technical assessment questions
        """
        prompt = f"""
        Generate 8-10 technical questions for a {position} position in {department}.
        
        Include:
        1. Technical knowledge questions
        2. Problem-solving scenarios
        3. Practical experience questions
        4. Technology-specific questions
        5. Code review or technical discussion topics
        
        Make questions relevant to the specific role and department.
        Include both basic and advanced questions.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            return self._parse_questions_response(content, "Technical Assessment")
            
        except Exception as e:
            return {
                "category": "Technical Assessment",
                "questions": [
                    "Describe your experience with relevant technologies.",
                    "How do you approach debugging complex issues?",
                    "Explain a challenging project you worked on.",
                    "What development methodologies do you prefer?",
                    "How do you stay updated with industry trends?"
                ]
            }
    
    def _generate_hr_questions(self, position: str, department: str) -> Dict:
        """
        Generate HR interview questions
        """
        prompt = f"""
        Generate 6-8 HR interview questions for a {position} position in {department}.
        
        Include questions about:
        1. Work style and preferences
        2. Team collaboration
        3. Conflict resolution
        4. Career goals and growth
        5. Work-life balance
        6. Company values alignment
        
        Focus on behavioral and situational questions.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            return self._parse_questions_response(content, "HR Interview")
            
        except Exception as e:
            return {
                "category": "HR Interview",
                "questions": [
                    "Describe your ideal work environment.",
                    "How do you handle conflicts with colleagues?",
                    "What motivates you in your work?",
                    "Where do you see yourself in 5 years?",
                    "How do you handle stress and pressure?"
                ]
            }
    
    def _generate_final_questions(self, position: str, department: str) -> Dict:
        """
        Generate final round questions
        """
        prompt = f"""
        Generate 5-7 final round interview questions for a {position} position in {department}.
        
        Include:
        1. Strategic thinking questions
        2. Leadership and initiative questions
        3. Company-specific questions
        4. Long-term vision questions
        5. Questions that demonstrate deep understanding
        
        Make these more challenging and comprehensive than previous rounds.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            return self._parse_questions_response(content, "Final Round")
            
        except Exception as e:
            return {
                "category": "Final Round",
                "questions": [
                    "How would you contribute to our company's growth?",
                    "What innovative ideas do you have for this role?",
                    "How do you see this department evolving?",
                    "What challenges do you anticipate in this role?",
                    "Why should we choose you over other candidates?"
                ]
            }
    
    def _generate_reference_questions(self, position: str, department: str) -> Dict:
        """
        Generate reference check questions
        """
        return {
            "category": "Reference Check",
            "questions": [
                "How long did the candidate work with you?",
                "What were their key responsibilities?",
                "How would you rate their technical skills?",
                "How did they work in a team environment?",
                "What are their strengths and weaknesses?",
                "Would you hire them again? Why or why not?",
                "How did they handle challenges and pressure?"
            ]
        }
    
    def _parse_questions_response(self, content: str, category: str) -> Dict:
        """
        Parse AI response and structure it properly
        """
        # Simple parsing - extract questions from AI response
        lines = content.split('\n')
        questions = []
        
        for line in lines:
            line = line.strip()
            if line and (line.startswith('-') or line.startswith('•') or 
                        line.startswith('1.') or line.startswith('2.') or
                        line.startswith('3.') or line.startswith('4.') or
                        line.startswith('5.') or line.startswith('6.') or
                        line.startswith('7.') or line.startswith('8.') or
                        line.startswith('9.') or line.startswith('10.')):
                # Clean up the question
                question = line.lstrip('-•1234567890.').strip()
                if question:
                    questions.append(question)
        
        # If parsing failed, provide default questions
        if not questions:
            questions = [
                "Tell us about your experience.",
                "What interests you about this role?",
                "How do you approach challenges?",
                "What are your career goals?"
            ]
        
        return {
            "category": category,
            "questions": questions
        }
    
    def _calculate_total_duration(self, schedule: Dict) -> int:
        """
        Calculate total interview duration
        """
        total = 0
        for stage_info in schedule.values():
            total += stage_info.get('duration_minutes', 0)
        return total
    
    def update_interview_status(self, candidate_id: str, stage: str, status: str, 
                               feedback: str = "") -> Dict:
        """
        Update interview status and add feedback
        """
        return {
            "candidate_id": candidate_id,
            "stage": stage,
            "status": status,  # completed, in_progress, scheduled, cancelled
            "feedback": feedback,
            "updated_at": datetime.now().isoformat()
        }
