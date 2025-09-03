#!/usr/bin/env python3
"""
Simple test script to verify the AI Recruitment System components
"""

import os
import sys
import pandas as pd

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all modules can be imported"""
    print("🧪 Testing module imports...")
    
    try:
        from config import APP_NAME, APP_VERSION
        print(f"✅ Config: {APP_NAME} v{APP_VERSION}")
    except Exception as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        from agents.recruitment_analyzer import RecruitmentAnalyzer
        print("✅ Recruitment Analyzer imported")
    except Exception as e:
        print(f"❌ Recruitment Analyzer import failed: {e}")
        return False
    
    try:
        from agents.candidate_screener import CandidateScreener
        print("✅ Candidate Screener imported")
    except Exception as e:
        print(f"❌ Candidate Screener import failed: {e}")
        return False
    
    try:
        from agents.interview_coordinator import InterviewCoordinator
        print("✅ Interview Coordinator imported")
    except Exception as e:
        print(f"❌ Interview Coordinator import failed: {e}")
        return False
    
    try:
        from recruitment_orchestrator import RecruitmentOrchestrator
        print("✅ Recruitment Orchestrator imported")
    except Exception as e:
        print(f"❌ Recruitment Orchestrator import failed: {e}")
        return False
    
    return True

def test_data_loading():
    """Test if employee data can be loaded"""
    print("\n📊 Testing data loading...")
    
    try:
        df = pd.read_csv('employees.csv')
        print(f"✅ Employee data loaded: {len(df)} records")
        
        # Check for quit employees
        quit_employees = df[df['last_working_day'].notna()]
        print(f"✅ Found {len(quit_employees)} quit employee(s)")
        
        if len(quit_employees) > 0:
            for _, employee in quit_employees.iterrows():
                print(f"   - {employee['name']} ({employee['position']}) quit on {employee['last_working_day']}")
        
        return True
    except Exception as e:
        print(f"❌ Data loading failed: {e}")
        return False

def test_orchestrator_creation():
    """Test if orchestrator can be created"""
    print("\n🏗️ Testing orchestrator creation...")
    
    try:
        # Import here to avoid circular import issues
        from recruitment_orchestrator import RecruitmentOrchestrator
        orchestrator = RecruitmentOrchestrator()
        print("✅ Recruitment Orchestrator created successfully")
        print(f"   - Job openings: {len(orchestrator.job_openings)}")
        print(f"   - Candidates: {len(orchestrator.candidates)}")
        return True
    except Exception as e:
        print(f"❌ Orchestrator creation failed: {e}")
        return False

def test_web_app_import():
    """Test if web app can be imported"""
    print("\n🌐 Testing web app import...")
    
    try:
        from main import app
        print("✅ FastAPI app imported successfully")
        return True
    except Exception as e:
        print(f"❌ Web app import failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 AI Recruitment System - System Test")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("Data Loading", test_data_loading),
        ("Orchestrator Creation", test_orchestrator_creation),
        ("Web App Import", test_web_app_import)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        print("\nNext steps:")
        print("1. Set your GROQ_API_KEY in .env file")
        print("2. Run: python demo.py (for demo)")
        print("3. Run: python main.py (for web interface)")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
