#!/usr/bin/env python3
"""
Demo script for the LangGraph-based Multi-Agent AI Recruitment System
This demonstrates the workflow orchestration capabilities of the system.
"""

import asyncio
import json
from datetime import datetime
from recruitment_orchestrator_langgraph import LangGraphRecruitmentOrchestrator

async def demo_langgraph_workflow():
    """Demonstrate the complete LangGraph workflow"""
    print("🚀 LangGraph Multi-Agent AI Recruitment System Demo")
    print("=" * 60)
    
    # Initialize the orchestrator
    orchestrator = LangGraphRecruitmentOrchestrator()
    
    print("\n📊 Step 1: Starting Recruitment Process")
    print("-" * 40)
    
    # Start the recruitment process using LangGraph workflow
    result = orchestrator.start_recruitment_process()
    
    if result["status"] == "success":
        print(f"✅ Recruitment process completed successfully!")
        print(f"📋 Job Openings Found: {result['job_openings_count']}")
        print(f"👥 Candidates Processed: {result['candidates_count']}")
        print(f"🎯 Hired Candidates: {result['hired_count']}")
        print(f"📄 Reports Generated: {result['reports_generated']}")
        print(f"🔄 Workflow Status: {result['workflow_status']}")
        
        if result.get('errors'):
            print(f"⚠️  Errors encountered: {len(result['errors'])}")
            for error in result['errors']:
                print(f"   - {error}")
    else:
        print(f"❌ Recruitment process failed: {result['message']}")
        return
    
    print("\n📝 Step 2: Processing Sample Candidate Applications")
    print("-" * 40)
    
    # Add some sample candidates to demonstrate the workflow
    sample_candidates = [
        {
            "candidate_name": "Alice Johnson",
            "email": "alice.johnson@email.com",
            "phone": "+1-555-0101",
            "position": "Senior Software Engineer",
            "experience_years": 5,
            "resume_text": "Experienced software engineer with expertise in Python, JavaScript, and cloud technologies. Led multiple successful projects and mentored junior developers.",
            "cover_letter": "I am passionate about building scalable software solutions and working with innovative teams."
        },
        {
            "candidate_name": "Bob Smith",
            "email": "bob.smith@email.com",
            "phone": "+1-555-0102",
            "position": "Data Analyst",
            "experience_years": 3,
            "resume_text": "Data analyst with strong skills in SQL, Python, and data visualization. Experience with business intelligence tools and statistical analysis.",
            "cover_letter": "I love turning data into actionable insights that drive business decisions."
        }
    ]
    
    for candidate in sample_candidates:
        print(f"\n🔍 Processing application for {candidate['candidate_name']}")
        result = orchestrator.process_candidate_application(candidate, candidate['position'])
        
        if result["status"] == "success":
            print(f"   ✅ {result['message']}")
            if "screening_result" in result:
                screening = result["screening_result"]
                print(f"   📊 Overall Score: {screening.get('overall_score', 'N/A')}")
                print(f"   💡 Recommendation: {screening.get('recommendation', 'N/A')}")
        else:
            print(f"   ❌ {result['message']}")
    
    print("\n📊 Step 3: Generating Recruitment Summary")
    print("-" * 40)
    
    # Generate comprehensive summary
    summary = orchestrator.generate_recruitment_summary()
    
    if summary.get("status") != "error":
        print("✅ Recruitment Summary Generated Successfully!")
        print(f"📋 Total Job Openings: {summary.get('total_job_openings', 0)}")
        print(f"👥 Total Candidates: {summary.get('total_candidates', 0)}")
        print(f"📈 Interview Completion Rate: {summary.get('interview_completion_rate', 0)}%")
        print(f"🎯 Hiring Success Rate: {summary.get('hiring_success_rate', 0)}%")
        print(f"⏱️  Average Time to Hire: {summary.get('average_time_to_hire', 'N/A')}")
        print(f"🔄 Workflow Status: {summary.get('workflow_status', 'Unknown')}")
        
        # Show top performing candidates
        top_candidates = summary.get('top_performing_candidates', [])
        if top_candidates:
            print(f"\n🏆 Top Performing Candidates:")
            for i, candidate in enumerate(top_candidates[:3], 1):
                print(f"   {i}. {candidate['candidate_name']} - Score: {candidate['score']}")
        
        # Show insights
        insights = summary.get('recruitment_insights', [])
        if insights:
            print(f"\n💡 Recruitment Insights:")
            for insight in insights:
                print(f"   • {insight}")
    else:
        print(f"❌ Failed to generate summary: {summary.get('message', 'Unknown error')}")
    
    print("\n🎯 Step 4: Demonstrating Agent Interactions")
    print("-" * 40)
    
    # Show how agents interact through the workflow
    print("🤖 Multi-Agent Workflow Demonstration:")
    print("   1. 📊 Recruitment Analyzer Agent: Analyzes employee data and identifies job openings")
    print("   2. 🔍 Candidate Screener Agent: Screens candidates against job requirements")
    print("   3. 📅 Interview Coordinator Agent: Schedules and manages interview processes")
    print("   4. 🎯 Decision Making Agent: Evaluates candidates and makes hiring decisions")
    print("   5. 📝 Report Generator Agent: Creates comprehensive recruitment reports")
    
    print("\n🔄 LangGraph Workflow Benefits:")
    print("   • Orchestrated multi-agent coordination")
    print("   • Stateful workflow management")
    print("   • Error handling and recovery")
    print("   • Scalable and extensible architecture")
    print("   • Real-time workflow monitoring")
    
    print("\n✨ Demo completed successfully!")
    print("The system is now ready for production use with enhanced multi-agent capabilities.")

def demo_sync_operations():
    """Demonstrate synchronous operations"""
    print("\n🔄 Synchronous Operations Demo")
    print("-" * 40)
    
    orchestrator = LangGraphRecruitmentOrchestrator()
    
    # Demo resume scoring
    print("\n📄 Resume Scoring Demo:")
    sample_resume = {
        "candidate_name": "Demo Candidate",
        "position": "Senior Software Engineer",
        "experience_years": 4,
        "resume_text": "Python developer with experience in Django, React, and AWS. Led development of microservices architecture.",
        "cover_letter": "Passionate about clean code and scalable solutions."
    }
    
    scoring_result = orchestrator.score_candidate_resume(sample_resume)
    print(f"   Candidate: {sample_resume['candidate_name']}")
    print(f"   Overall Score: {scoring_result['overall_score']}")
    print(f"   Skill Match: {scoring_result['skill_match_score']}")
    print(f"   Experience Match: {scoring_result['experience_match_score']}")
    print(f"   Cultural Fit: {scoring_result['cultural_fit_score']}")
    print(f"   AI Feedback: {scoring_result['ai_feedback'][:100]}...")
    print(f"   Recommendation: {scoring_result['recommendation']}")

if __name__ == "__main__":
    print("Starting LangGraph Multi-Agent Recruitment System Demo...")
    
    try:
        # Run the main async demo
        asyncio.run(demo_langgraph_workflow())
        
        # Run synchronous operations demo
        demo_sync_operations()
        
    except Exception as e:
        print(f"❌ Demo failed with error: {str(e)}")
        print("Please check your configuration and dependencies.")
