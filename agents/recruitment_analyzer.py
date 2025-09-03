import pandas as pd
from typing import Dict, List, Optional
import groq
from config import GROQ_API_KEY, GROQ_MODEL, JOB_CATEGORIES

class RecruitmentAnalyzer:
    """
    AI Agent responsible for analyzing employee data and identifying job openings
    """
    
    def __init__(self):
        self.client = groq.Groq(api_key=GROQ_API_KEY)
        self.model = GROQ_MODEL
        
    def analyze_employee_data(self, csv_file: str) -> Dict:
        """
        Analyze employee CSV data to identify who has quit and create job requirements
        """
        try:
            # Read employee data
            df = pd.read_csv(csv_file)
            
            # Find employees who have quit (have last_working_day)
            quit_employees = df[df['last_working_day'].notna()].copy()
            
            if quit_employees.empty:
                return {"status": "no_openings", "message": "No job openings found"}
            
            # Analyze each quit employee
            job_openings = []
            for _, employee in quit_employees.iterrows():
                job_opening = self._analyze_job_opening(employee)
                job_openings.append(job_opening)
            
            return {
                "status": "openings_found",
                "total_openings": len(job_openings),
                "job_openings": job_openings
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _analyze_job_opening(self, employee: pd.Series) -> Dict:
        """
        Analyze individual job opening and create detailed requirements
        """
        position = employee['position']
        department = employee['department']
        salary = employee['salary']
        
        # Generate job description using Groq
        job_description = self._generate_job_description(position, department, salary)
        
        # Identify required skills
        required_skills = self._identify_required_skills(position, department)
        
        return {
            "employee_id": employee['id'],
            "employee_name": employee['name'],
            "position": position,
            "department": department,
            "salary_range": self._calculate_salary_range(position, salary),
            "last_working_day": employee['last_working_day'],
            "job_description": job_description,
            "required_skills": required_skills,
            "experience_level": self._determine_experience_level(position),
            "priority": self._determine_priority(department, position)
        }
    
    def _generate_job_description(self, position: str, department: str, salary: float) -> str:
        """
        Generate LinkedIn-style engaging job description using Groq AI
        """
        salary_range = self._calculate_salary_range(position, salary)
        experience_level = self._determine_experience_level(position)
        
        prompt = f"""
        Create a compelling LinkedIn-style job posting for a {position} position in the {department} department.
        
        Details:
        - Salary Range: {salary_range}
        - Experience Level: {experience_level}
        - Previous employee salary: ${salary:,.2f}
        
        Make it engaging and LinkedIn-worthy with:
        1. **Eye-catching headline** with emojis and compelling language
        2. **Company culture and mission** (brief mention)
        3. **What makes this role exciting** (2-3 compelling points)
        4. **Key responsibilities** (5-7 bullet points with action verbs)
        5. **What we're looking for** (required qualifications)
        6. **Bonus points** (preferred qualifications)
        7. **What's in it for you** (benefits, growth, impact)
        8. **Call to action** (encouraging application)
        
        Style guidelines:
        - Use emojis strategically (but not overdone)
        - Write in an engaging, conversational tone
        - Highlight impact and growth opportunities
        - Make it feel like an exciting opportunity, not just a job
        - Include phrases like "Join our team", "Make an impact", "Grow with us"
        - Keep it professional but approachable
        - Use bullet points for easy scanning
        - Make it shareable and engaging for LinkedIn
        """
        
        try:
            # Check if we have a valid API key
            if not GROQ_API_KEY or GROQ_API_KEY == "test_key_for_demo":
                # Return a LinkedIn-style job description template
                return self._generate_fallback_job_description(position, department, salary_range, experience_level)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            # Return fallback description if API fails
            return self._generate_fallback_job_description(position, department, salary_range, experience_level)
    
    def _generate_fallback_job_description(self, position: str, department: str, salary_range: str, experience_level: str) -> str:
        """
        Generate a LinkedIn-style job description template when API is not available
        """
        return f"""🚀 **{position}** - Join Our Growing {department} Team!

**💰 Salary Range:** {salary_range}
**⏰ Experience:** {experience_level}

---

## 🎯 **What Makes This Role Exciting?**

We're looking for a passionate **{position}** who's ready to make a real impact in our {department} department. This isn't just another job – you'll be part of a dynamic team building innovative solutions!

### 🌟 **Why You'll Love Working With Us:**
• **Innovation-Driven Culture:** Work on cutting-edge technologies
• **Growth Opportunities:** Clear path for career advancement
• **Impact:** Your work will directly improve our products and services
• **Collaboration:** Join a team of talented professionals

---

## 🔧 **What You'll Be Doing:**

• **Lead key initiatives** and contribute to strategic projects
• **Collaborate with cross-functional teams** to deliver high-quality solutions
• **Develop and implement** best practices and processes
• **Mentor junior team members** and share knowledge
• **Stay updated** with industry trends and emerging technologies
• **Contribute to** continuous improvement efforts

---

## 🎯 **What We're Looking For:**

### **Required Skills:**
• {experience_level} of relevant experience
• Strong technical and analytical skills
• Excellent communication and collaboration abilities
• Problem-solving mindset and attention to detail
• Ability to work in a fast-paced environment

### **Bonus Points:**
• Experience with modern tools and technologies
• Leadership or mentoring experience
• Industry certifications or advanced education
• Track record of successful project delivery

---

## 🎁 **What's In It For You:**

• **Competitive compensation** with performance bonuses
• **Health and wellness** benefits
• **Professional development** opportunities
• **Flexible work arrangements**
• **Collaborative team** environment
• **Work-life balance** focus

---

## 🚀 **Ready to Make an Impact?**

If you're excited about joining a dynamic team where your contributions matter, we'd love to hear from you!

**Apply now** and let's build something amazing together! 🚀

---

**#hiring #{department.lower().replace(' ', '')} #{position.lower().replace(' ', '')} #careers #jobopportunity**"""
    
    def _identify_required_skills(self, position: str, department: str) -> List[str]:
        """
        Identify required skills based on position and department
        """
        base_skills = []
        
        # Department-specific skills
        if department in JOB_CATEGORIES:
            base_skills.extend(JOB_CATEGORIES[department])
        
        # Position-specific skills
        position_skills = {
            "Software Engineer": ["Python", "JavaScript", "SQL", "Git", "Agile"],
            "Senior Software Engineer": ["Python", "JavaScript", "SQL", "Git", "Agile", "System Design", "Leadership"],
            "Data Analyst": ["SQL", "Python", "Excel", "Data Visualization", "Statistical Analysis"],
            "DevOps Engineer": ["Linux", "Docker", "Kubernetes", "AWS/Azure", "CI/CD", "Infrastructure as Code"],
            "Marketing Specialist": ["Digital Marketing", "Social Media", "Content Creation", "Analytics Tools"],
            "HR Manager": ["HRIS", "Employee Relations", "Recruitment", "Labor Law", "Performance Management"],
            "Financial Analyst": ["Financial Modeling", "Excel", "Accounting Software", "Financial Analysis"],
            "Cloud Architect": ["AWS", "Azure", "GCP", "Terraform", "Microservices", "Security"],
            "Product Designer": ["UI/UX Design", "Figma", "User Research", "Prototyping", "Design Systems"],
            "Sales Executive": ["CRM", "Sales Techniques", "Negotiation", "Relationship Building"],
            "QA Engineer": ["Testing Tools", "Automation", "Test Planning", "Bug Tracking", "Quality Standards"]
        }
        
        if position in position_skills:
            base_skills.extend(position_skills[position])
        
        # Remove duplicates and return
        return list(set(base_skills))
    
    def _calculate_salary_range(self, position: str, current_salary_usd: float) -> str:
        """
        Calculate India-appropriate salary range (annual CTC) in INR (LPA) based on role bands.
        Uses conservative Indian market bands instead of direct USD->INR conversion.
        """
        # Baseline salary bands in INR LPA by role seniority
        # Values chosen to reflect typical metro-market ranges as of 2024
        role_bands_lpa = [
            ("Intern", (3, 6)),
            ("Junior", (4, 8)),
            ("Associate", (6, 12)),
            ("Engineer", (8, 18)),
            ("Senior", (18, 35)),
            ("Lead", (28, 45)),
            ("Manager", (30, 55)),
            ("Architect", (35, 60)),
            ("Director", (55, 90)),
        ]
        
        normalized_position = position or ""
        normalized_position = normalized_position.strip()
        selected_band = (8, 18)  # default Engineer band
        for keyword, band in role_bands_lpa:
            if keyword.lower() in normalized_position.lower():
                selected_band = band
                break
        
        min_lpa, max_lpa = selected_band
        
        # Mild adjustment based on previous USD salary if present to anchor expectations
        # We cap the influence to avoid unrealistic conversion-driven ranges
        try:
            usd = float(current_salary_usd)
        except Exception:
            usd = 0.0
        if usd > 0:
            # Map USD to an influence factor within +-15% band
            # Heuristic: 100k USD maps to +10% within the band; lower/higher scaled
            influence = min(0.15, max(-0.15, (usd - 60000.0) / 400000.0))
            min_lpa = round(min_lpa * (1 + influence))
            max_lpa = round(max_lpa * (1 + influence))
            # Ensure min <= max
            if min_lpa > max_lpa:
                min_lpa, max_lpa = max_lpa - 1, max_lpa
        
        return f"₹{min_lpa}–{max_lpa} LPA"
    
    def _determine_experience_level(self, position: str) -> str:
        """
        Determine required experience level based on position
        """
        if "Senior" in position or "Manager" in position:
            return "5+ years"
        elif "Junior" in position:
            return "0-2 years"
        else:
            return "2-5 years"
    
    def _determine_priority(self, department: str, position: str) -> str:
        """
        Determine hiring priority based on department and position
        """
        critical_departments = ["Engineering", "IT", "Finance"]
        critical_positions = ["Manager", "Senior", "Lead", "Architect"]
        
        if department in critical_departments or any(crit in position for crit in critical_positions):
            return "High"
        elif department in ["Marketing", "Sales"]:
            return "Medium"
        else:
            return "Normal"
    
    def generate_recruitment_report(self, job_openings: List[Dict]) -> str:
        """
        Generate a comprehensive recruitment report
        """
        if not job_openings:
            return "No recruitment needs identified."
        
        report = f"""
# Recruitment Analysis Report

## Summary
Total job openings: {len(job_openings)}

## Job Openings Details
"""
        
        for opening in job_openings:
            report += f"""
### {opening['position']} - {opening['department']}
- **Employee**: {opening['employee_name']} (ID: {opening['employee_id']})
- **Last Working Day**: {opening['last_working_day']}
- **Salary Range**: {opening['salary_range']}
- **Priority**: {opening['priority']}
- **Experience Required**: {opening['experience_level']}

#### Required Skills:
{chr(10).join([f"- {skill}" for skill in opening['required_skills']])}

#### Job Description:
{opening['job_description']}

---
"""
        
        return report
