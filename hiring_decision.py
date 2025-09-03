#!/usr/bin/env python3
"""
AI Hiring Decision Demo Script
Shows how to conduct interviews and make hiring decisions
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def get_candidates():
    """Get all candidates"""
    response = requests.get(f"{BASE_URL}/api/candidates")
    return response.json()

def conduct_interview(candidate_id, stage, feedback=""):
    """Conduct an interview stage"""
    response = requests.post(
        f"{BASE_URL}/api/interview/{candidate_id}/{stage}",
        data={"feedback": feedback}
    )
    return response.json()

def make_selection(candidate_id, decision, notes=""):
    """Make final selection decision"""
    response = requests.post(
        f"{BASE_URL}/api/select/{candidate_id}",
        data={"decision": decision, "notes": notes}
    )
    return response.json()

def get_summary():
    """Get recruitment summary"""
    response = requests.get(f"{BASE_URL}/api/summary")
    return response.json()

def main():
    print("🤖 AI Hiring Decision Process")
    print("=" * 50)
    
    # Get current candidates
    print("\n📋 Current Candidates:")
    candidates = get_candidates()
    
    if candidates["status"] == "success":
        for candidate in candidates["candidates"]:
            print(f"\n👤 {candidate['candidate_name']}")
            print(f"   Position: {candidate['position']}")
            print(f"   Experience: {candidate['experience_years']} years")
            print(f"   Status: {candidate['status']}")
            print(f"   Overall Score: {candidate['screening_result']['overall_score']}/100")
    
    print("\n🎯 Manual Interview Process:")
    print("Since both candidates were auto-rejected, let's conduct manual interviews...")
    
    # Conduct technical interviews
    print("\n🔧 Conducting Technical Interviews...")
    
    for candidate in candidates["candidates"]:
        candidate_id = candidate["candidate_id"]
        candidate_name = candidate["candidate_name"]
        
        print(f"\n📝 Interviewing {candidate_name}...")
        
        # Technical interview
        tech_result = conduct_interview(
            candidate_id, 
            "technical",
            "Strong problem-solving skills. Good understanding of software development principles. Needs improvement in system design."
        )
        print(f"   Technical Interview: {tech_result.get('status', 'Completed')}")
        
        # Behavioral interview
        behavioral_result = conduct_interview(
            candidate_id,
            "behavioral", 
            "Good communication skills. Shows potential for growth. Team player with learning attitude."
        )
        print(f"   Behavioral Interview: {behavioral_result.get('status', 'Completed')}")
        
        # Make selection decision
        print(f"\n✅ Making Selection Decision for {candidate_name}...")
        
        # For demo purposes, let's hire the first candidate
        if candidate_id == "candidate_1":
            decision = "hired"
            notes = "Strong potential despite limited experience. Good learning attitude and technical foundation."
        else:
            decision = "rejected"
            notes = "Good candidate but selected another applicant for this position."
        
        selection_result = make_selection(candidate_id, decision, notes)
        print(f"   Decision: {decision.upper()}")
        print(f"   Notes: {notes}")
    
    # Get final summary
    print("\n📊 Final Recruitment Summary:")
    summary = get_summary()
    if summary.get("status") == "success":
        print(f"   Total Candidates: {summary.get('total_candidates', 0)}")
        print(f"   Hired: {summary.get('hired_count', 0)}")
        print(f"   Rejected: {summary.get('rejected_count', 0)}")
        print(f"   Process Status: {summary.get('process_status', 'Completed')}")

if __name__ == "__main__":
    main()
