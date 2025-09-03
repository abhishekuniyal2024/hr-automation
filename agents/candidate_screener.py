import groq
from typing import Dict, List, Optional
import re
from config import GROQ_API_KEY, GROQ_MODEL, EVALUATION_CRITERIA

class CandidateScreener:
    """
    AI Agent responsible for screening candidates and evaluating their fit for positions
    """
    
    def __init__(self):
        # Initialize Groq client only if a plausible API key is present
        # This prevents 401 errors surfacing in the UI and enables a graceful fallback
        self.client = None
        if GROQ_API_KEY and GROQ_API_KEY not in ["your_groq_api_key_here", "test_key_for_demo"]:
            try:
                self.client = groq.Groq(api_key=GROQ_API_KEY)
            except Exception:
                self.client = None
        self.model = GROQ_MODEL
    
    def screen_candidate(self, candidate_data: Dict, job_requirements: Dict) -> Dict:
        """
        Screen a candidate against job requirements
        """
        try:
            # Extract candidate information
            resume_text = candidate_data.get('resume_text', '')
            cover_letter = candidate_data.get('cover_letter', '')
            experience_years = candidate_data.get('experience_years', 0)
            
            # Extract job requirements
            required_skills = job_requirements.get('required_skills', [])
            experience_level = job_requirements.get('experience_level', '')
            position = job_requirements.get('position', '')
            department = job_requirements.get('department', '')
            
            # Perform screening analysis
            skill_match = self._analyze_skill_match(resume_text, required_skills)
            experience_match = self._evaluate_experience(experience_years, experience_level)
            cultural_fit = self._assess_cultural_fit(cover_letter, resume_text, department)
            overall_score = self._calculate_overall_score(skill_match, experience_match, cultural_fit)
            
            # Generate AI feedback
            ai_feedback = self._generate_ai_feedback(
                candidate_data, job_requirements, skill_match, experience_match, cultural_fit
            )
            
            # Determine recommendation
            recommendation = self._determine_recommendation(overall_score)
            
            return {
                "candidate_id": candidate_data.get('candidate_id'),
                "candidate_name": candidate_data.get('candidate_name'),
                "position": position,
                "overall_score": overall_score,
                "skill_match_score": skill_match['score'],
                "experience_match_score": experience_match['score'],
                "cultural_fit_score": cultural_fit['score'],
                "recommendation": recommendation,
                "ai_feedback": ai_feedback,
                "skill_analysis": skill_match,
                "experience_analysis": experience_match,
                "cultural_fit_analysis": cultural_fit,
                "screening_status": "completed"
            }
            
        except Exception as e:
            return {
                "candidate_id": candidate_data.get('candidate_id'),
                "screening_status": "error",
                "error_message": str(e)
            }
    
    def _analyze_skill_match(self, resume_text: str, required_skills: List[str]) -> Dict:
        """
        Analyze how well candidate's skills match required skills
        """
        if not resume_text or not required_skills:
            return {"score": 0, "matched_skills": [], "missing_skills": required_skills}
        
        resume_lower = resume_text.lower()
        matched_skills = []
        missing_skills = []
        
        for skill in required_skills:
            skill_lower = skill.lower()
            # Check for exact matches and variations
            if (skill_lower in resume_lower or 
                skill_lower.replace(' ', '') in resume_lower.replace(' ', '') or
                any(word in resume_lower for word in skill_lower.split())):
                matched_skills.append(skill)
            else:
                missing_skills.append(skill)
        
        # Calculate score based on percentage of skills matched
        score = len(matched_skills) / len(required_skills) * 100 if required_skills else 0
        
        return {
            "score": round(score, 2),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "match_percentage": f"{score:.1f}%"
        }
    
    def _evaluate_experience(self, candidate_years: int, required_level: str) -> Dict:
        """
        Evaluate if candidate's experience matches required level
        """
        # Parse required experience level
        if "5+" in required_level:
            required_years = 5
        elif "0-2" in required_level:
            required_years = 1
        else:  # 2-5 years
            required_years = 3.5
        
        # Calculate experience score
        if candidate_years >= required_years:
            score = min(100, (candidate_years / required_years) * 100)
        else:
            score = max(0, (candidate_years / required_years) * 100)
        
        # Determine experience assessment
        if candidate_years >= required_years * 1.5:
            assessment = "Overqualified"
        elif candidate_years >= required_years:
            assessment = "Well Qualified"
        elif candidate_years >= required_years * 0.7:
            assessment = "Moderately Qualified"
        else:
            assessment = "Underqualified"
        
        return {
            "score": round(score, 2),
            "candidate_years": candidate_years,
            "required_years": required_years,
            "assessment": assessment,
            "experience_gap": candidate_years - required_years
        }
    
    def _assess_cultural_fit(self, cover_letter: str, resume_text: str, department: str) -> Dict:
        """
        Assess cultural fit based on cover letter and resume content
        """
        # Combine text for analysis
        combined_text = f"{cover_letter} {resume_text}".lower()
        
        # Define cultural indicators
        cultural_indicators = {
            "teamwork": ["team", "collaboration", "cooperation", "partnership"],
            "leadership": ["lead", "manage", "supervise", "mentor", "guide"],
            "innovation": ["innovate", "creative", "problem-solving", "improve"],
            "communication": ["communicate", "present", "write", "speak", "explain"],
            "adaptability": ["adapt", "flexible", "change", "learn", "grow"]
        }
        
        scores = {}
        for category, keywords in cultural_indicators.items():
            count = sum(1 for keyword in keywords if keyword in combined_text)
            scores[category] = min(100, count * 20)  # Max 100 per category
        
        # Calculate overall cultural fit score
        overall_score = sum(scores.values()) / len(scores)
        
        # Determine cultural fit assessment
        if overall_score >= 80:
            assessment = "Excellent Cultural Fit"
        elif overall_score >= 60:
            assessment = "Good Cultural Fit"
        elif overall_score >= 40:
            assessment = "Moderate Cultural Fit"
        else:
            assessment = "Limited Cultural Fit"
        
        return {
            "score": round(overall_score, 2),
            "category_scores": scores,
            "assessment": assessment,
            "strengths": [k for k, v in scores.items() if v >= 60],
            "areas_for_growth": [k for k, v in scores.items() if v < 40]
        }
    
    def _calculate_overall_score(self, skill_match: Dict, experience_match: Dict, cultural_fit: Dict) -> float:
        """
        Calculate overall candidate score using weighted criteria
        """
        skill_score = skill_match['score']
        experience_score = experience_match['score']
        cultural_score = cultural_fit['score']
        
        # Apply weights from config
        overall_score = (
            skill_score * EVALUATION_CRITERIA['Technical Skills'] +
            experience_score * EVALUATION_CRITERIA['Experience'] +
            cultural_score * EVALUATION_CRITERIA['Cultural Fit']
        )
        
        return round(overall_score, 2)
    
    def _generate_ai_feedback(self, candidate_data: Dict, job_requirements: Dict, 
                             skill_match: Dict, experience_match: Dict, cultural_fit: Dict) -> str:
        """
        Generate AI-powered feedback for the candidate
        """
        prompt = f"""
        As an AI recruitment specialist, provide constructive feedback for a candidate applying for {job_requirements.get('position')} position.
        
        Candidate Profile:
        - Name: {candidate_data.get('candidate_name')}
        - Experience: {candidate_data.get('experience_years')} years
        - Skills Match: {skill_match['match_percentage']}
        - Experience Assessment: {experience_match['assessment']}
        - Cultural Fit: {cultural_fit['assessment']}
        
        Required Skills: {', '.join(job_requirements.get('required_skills', []))}
        Matched Skills: {', '.join(skill_match['matched_skills'])}
        Missing Skills: {', '.join(skill_match['missing_skills'])}
        
        Provide:
        1. Overall assessment (2-3 sentences)
        2. Strengths (3-4 bullet points)
        3. Areas for improvement (2-3 bullet points)
        4. Specific recommendations for skill development
        5. Final recommendation for next steps
        
        Keep it professional, constructive, and actionable.
        """
        
        # If no valid API key/client, return a helpful deterministic fallback
        if self.client is None:
            return self._generate_fallback_feedback(candidate_data, job_requirements, skill_match, experience_match, cultural_fit)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=600,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception:
            # Gracefully fall back if the API call fails (e.g., invalid/expired key, rate limits)
            return self._generate_fallback_feedback(candidate_data, job_requirements, skill_match, experience_match, cultural_fit)

    def _generate_fallback_feedback(self, candidate_data: Dict, job_requirements: Dict,
                                    skill_match: Dict, experience_match: Dict,
                                    cultural_fit: Dict) -> str:
        """
        Generate a deterministic, template-based feedback when LLM is unavailable.
        This ensures the UI shows helpful guidance instead of surfacing 401 errors.
        """
        strengths = skill_match.get('matched_skills', [])
        missing = skill_match.get('missing_skills', [])
        strengths_text = ", ".join(strengths) if strengths else "Communication, Collaboration"
        missing_text = ", ".join(missing) if missing else "Advanced system design"
        
        overall = (
            f"Candidate {candidate_data.get('candidate_name', 'N/A')} shows a {skill_match.get('match_percentage', 'moderate')} "
            f"skills match for the {job_requirements.get('position', 'role')} role. "
            f"Experience is assessed as {experience_match.get('assessment', 'Relevant')} with cultural fit "
            f"being {cultural_fit.get('assessment', 'Good')}."
        )
        strengths_bullets = f"- Strengths: {strengths_text}"
        improvement_bullets = f"- Areas to improve: {missing_text}"
        recommendations = (
            "- Recommendation: Prepare concrete examples demonstrating impact, strengthen missing skills, and tailor the resume "
            "to highlight achievements aligned with the job requirements."
        )
        next_steps = "- Next steps: Proceed to HR interview if role requires, or assign a short technical assessment."
        
        return "\n".join([overall, strengths_bullets, improvement_bullets, recommendations, next_steps])
    
    def _determine_recommendation(self, overall_score: float) -> str:
        """
        Determine recommendation based on overall score
        """
        if overall_score >= 85:
            return "Strongly Recommend - Move to Technical Assessment"
        elif overall_score >= 70:
            return "Recommend - Move to HR Interview"
        elif overall_score >= 55:
            return "Consider - Additional Screening Required"
        else:
            return "Not Recommended - Does Not Meet Requirements"
    
    def batch_screen_candidates(self, candidates: List[Dict], job_requirements: Dict) -> List[Dict]:
        """
        Screen multiple candidates in batch
        """
        results = []
        for candidate in candidates:
            result = self.screen_candidate(candidate, job_requirements)
            results.append(result)
        
        # Sort by overall score (descending)
        results.sort(key=lambda x: x.get('overall_score', 0), reverse=True)
        
        return results
