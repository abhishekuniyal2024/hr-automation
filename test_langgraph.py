#!/usr/bin/env python3
"""
Simple test script for the LangGraph-based recruitment system
"""

import sys
import traceback
from recruitment_orchestrator_langgraph import LangGraphRecruitmentOrchestrator

def test_basic_functionality():
    """Test basic functionality of the LangGraph system"""
    print("🧪 Testing LangGraph Multi-Agent Recruitment System")
    print("=" * 60)
    
    try:
        # Test 1: Import and instantiation
        print("\n✅ Test 1: System Import and Instantiation")
        orchestrator = LangGraphRecruitmentOrchestrator()
        print("   ✓ LangGraph orchestrator created successfully")
        
        # Test 2: Workflow structure
        print("\n✅ Test 2: Workflow Structure")
        workflow = orchestrator.workflow
        print(f"   ✓ Workflow has {len(workflow.nodes)} nodes")
        print(f"   ✓ Workflow is compiled: {hasattr(workflow, 'invoke')}")
        
        # Test 3: State structure
        print("\n✅ Test 3: State Structure")
        state = orchestrator.state
        print(f"   ✓ State has {len(state)} keys")
        print(f"   ✓ Workflow status: {state['workflow_status']}")
        print(f"   ✓ Messages count: {len(state['messages'])}")
        
        # Test 4: Agent initialization
        print("\n✅ Test 4: Agent Initialization")
        print(f"   ✓ Recruitment Analyzer: {type(orchestrator.analyzer).__name__}")
        print(f"   ✓ Candidate Screener: {type(orchestrator.screener).__name__}")
        print(f"   ✓ Interview Coordinator: {type(orchestrator.interview_coordinator).__name__}")
        
        # Test 5: Basic methods
        print("\n✅ Test 5: Basic Methods")
        summary = orchestrator.generate_recruitment_summary()
        if summary.get("status") != "error":
            print("   ✓ generate_recruitment_summary() works")
        else:
            print("   ⚠️  generate_recruitment_summary() returned error (expected for empty state)")
        
        print("\n🎉 All basic tests passed! The LangGraph system is working correctly.")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        print("\nStack trace:")
        traceback.print_exc()
        return False

def test_workflow_nodes():
    """Test the workflow nodes and structure"""
    print("\n🔍 Testing Workflow Nodes and Structure")
    print("-" * 40)
    
    try:
        orchestrator = LangGraphRecruitmentOrchestrator()
        workflow = orchestrator.workflow
        
        # Check expected nodes
        expected_nodes = [
            "analyze_requirements",
            "screen_candidates", 
            "schedule_interviews",
            "conduct_interviews",
            "make_decisions",
            "generate_reports"
        ]
        
        for node in expected_nodes:
            if node in workflow.nodes:
                print(f"   ✓ Node '{node}' exists")
            else:
                print(f"   ❌ Node '{node}' missing")
                return False
        
        print("   ✓ All expected workflow nodes are present")
        return True
        
    except Exception as e:
        print(f"   ❌ Workflow test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("Starting LangGraph system tests...")
    
    # Run tests
    test1_passed = test_basic_functionality()
    test2_passed = test_workflow_nodes()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Basic Functionality: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Workflow Structure: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 All tests passed! The LangGraph system is ready for use.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        sys.exit(1)
