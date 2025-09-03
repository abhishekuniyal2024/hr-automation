#!/usr/bin/env python3
"""
Demo script for the AI Recruitment System
This script demonstrates the key functionality without requiring the web interface
"""

import os
import sys
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from recruitment_orchestrator import RecruitmentOrchestrator

def main():
    print("🚀 AI Recruitment System Demo")
    print("=" * 50)
    
    # Check if GROQ_API_KEY is set
    if not os.getenv("GROQ_API_KEY"):
        print("❌ Error: GROQ_API_KEY environment variable not set")
        print("Please set your Groq API key:")
        print("export GROQ_API_KEY='your_api_key_here'")
        return
    
    try:
        # Initialize the orchestrator
        print("📋 Initializing recruitment system...")
        orchestrator = RecruitmentOrchestrator()
        
        # Step 1: Start recruitment process
        print("\n🔍 Step 1: Starting recruitment process...")
        result = orchestrator.start_recruitment_process()
        
        if result["status"] != "success":
            print(f"❌ Failed to start recruitment: {result['message']}")
            return
        
        print(f"✅ Recruitment started successfully!")
        print(f"📊 Found {result['job_openings_count']} job opening(s)")
        print(f"📄 Report saved to: {result['report_path']}")
        
        # Step 2: Display job openings
        print("\n📋 Step 2: Job Openings")
        print("-" * 30)
        for i, opening in enumerate(orchestrator.job_openings, 1):
            print(f"{i}. {opening['position']} - {opening['department']}")
            print(f"   Salary: {opening['salary_range']}")
            print(f"   Experience: {opening['experience_level']}")
            print(f"   Priority: {opening['priority']}")
            print(f"   Skills: {', '.join(opening['required_skills'][:5])}")
            print()
        
        # Step 3: Simulate candidate applications
        print("👥 Step 3: Processing candidate applications...")
        
        # Sample candidate 1 - Good match
        candidate1 = {
            "candidate_id": "demo_candidate_1",
            "candidate_name": "John Smith",
            "email": "john.smith@email.com",
            "phone": "+1-555-0123",
            "position": "Senior Software Engineer",
            "experience_years": 7,
            "resume_text": """
            Senior Software Engineer with 7+ years of experience in Python, JavaScript, SQL, Git, and Agile methodologies.
            Led development teams and designed system architecture for scalable applications.
            Experience with cloud platforms and microservices architecture.
            Strong problem-solving skills and team collaboration experience.
            """,
            "cover_letter": """
            I am excited to apply for the Senior Software Engineer position. 
            I have extensive experience in software development and team leadership.
            I am passionate about creating innovative solutions and mentoring junior developers.
            I believe my technical skills and leadership experience make me an excellent fit for this role.
            """
        }
        
        print(f"📝 Processing application for {candidate1['candidate_name']}...")
        result1 = orchestrator.process_candidate_application(candidate1, "Senior Software Engineer")
        
        if result1["status"] == "success":
            print(f"✅ {candidate1['candidate_name']}: {result1['message']}")
            if "interview_scheduled" in result1["message"]:
                print(f"📅 Interview scheduled with {len(result1['interview_schedule']['interview_stages'])} stages")
        else:
            print(f"❌ {candidate1['candidate_name']}: {result1['message']}")
        
        # Sample candidate 2 - Moderate match
        candidate2 = {
            "candidate_id": "demo_candidate_2",
            "candidate_name": "Sarah Johnson",
            "email": "sarah.johnson@email.com",
            "phone": "+1-555-0456",
            "position": "Senior Software Engineer",
            "experience_years": 4,
            "resume_text": """
            Software developer with 4 years of experience in Python and web development.
            Basic knowledge of JavaScript and SQL. Some experience with Git.
            Worked in small teams using Agile methodology.
            """,
            "cover_letter": """
            I am interested in the Senior Software Engineer position.
            I have good programming skills and enjoy learning new technologies.
            I work well in teams and am eager to grow in my career.
            """
        }
        
        print(f"\n📝 Processing application for {candidate2['candidate_name']}...")
        result2 = orchestrator.process_candidate_application(candidate2, "Senior Software Engineer")
        
        if result2["status"] == "success":
            print(f"✅ {candidate2['candidate_name']}: {result2['message']}")
        else:
            print(f"❌ {candidate2['candidate_name']}: {result2['message']}")
        
        # Step 4: Simulate interview process
        print("\n🎯 Step 4: Simulating interview process...")
        
        # Find the first candidate who passed screening
        passed_candidates = [c for c in orchestrator.candidates if c.get("status") == "interview_scheduled"]
        
        if passed_candidates:
            candidate = passed_candidates[0]
            print(f"📞 Conducting interviews for {candidate['candidate_name']}...")
            
            # Simulate completing interview stages
            interview_stages = candidate['interview_schedule']['interview_stages']
            
            for stage in interview_stages:
                print(f"   🔄 Completing {stage}...")
                feedback = f"Good performance in {stage}. Candidate showed strong technical knowledge and communication skills."
                
                result = orchestrator.conduct_interview(candidate['candidate_id'], stage, feedback)
                if result["status"] == "success":
                    print(f"   ✅ {stage} completed")
                    print(f"   📋 Next steps: {', '.join(result['next_steps'])}")
                else:
                    print(f"   ❌ Error in {stage}: {result['message']}")
        
        # Step 5: Generate summary
        print("\n📊 Step 5: Generating recruitment summary...")
        summary = orchestrator.generate_recruitment_summary()
        
        if summary.get("status") != "error":
            print(f"📈 Total candidates: {summary['total_candidates']}")
            print(f"🎯 Interview completion rate: {summary['interview_completion_rate']}%")
            print(f"✅ Hiring success rate: {summary['hiring_success_rate']}%")
            print(f"⏱️  Average time to hire: {summary['average_time_to_hire']}")
            
            if summary['top_performing_candidates']:
                print(f"\n🏆 Top performing candidates:")
                for i, candidate in enumerate(summary['top_performing_candidates'][:3], 1):
                    print(f"   {i}. {candidate['candidate_name']} - Score: {candidate['score']}")
            
            if summary['recruitment_insights']:
                print(f"\n💡 Recruitment insights:")
                for insight in summary['recruitment_insights']:
                    print(f"   • {insight}")
        else:
            print(f"❌ Error generating summary: {summary['message']}")
        
        print("\n🎉 Demo completed successfully!")
        print("\nTo run the web interface:")
        print("1. Make sure your GROQ_API_KEY is set")
        print("2. Run: python main.py")
        print("3. Open http://localhost:8000 in your browser")
        
    except Exception as e:
        print(f"❌ Error during demo: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
