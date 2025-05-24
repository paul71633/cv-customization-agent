#!/usr/bin/env python3
"""
CV Agent - Main Entry Point
Run this script to analyze your CV and match it against job descriptions
"""

import os
import sys
from cv_agent.core import CompleteCVAgent

def get_file_path():
    """Get CV file path from user with validation"""
    while True:
        # file_path = input("\n📁 Enter path to your CV file (PDF/DOCX): ").strip()
        
        # # Handle quotes around file path
        # file_path = file_path.strip('"').strip("'")
        
        file_path = "external_lib/resume.pdf"
        
        if not file_path:
            print("❌ Please enter a file path")
            continue
            
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            print("💡 Try dragging the file into the terminal or use full path")
            continue
            
        # Check file extension
        ext = file_path.lower().split('.')[-1]
        if ext not in ['pdf', 'docx', 'doc']:
            print(f"❌ Unsupported file type: {ext}")
            print("💡 Supported formats: PDF, DOCX, DOC")
            continue
            
        return file_path

def get_multiline_input(prompt):
    """Get multi-line input from user"""
    print(prompt)
    print("(Paste your text and press Enter twice when done)")
    lines = []
    empty_lines = 0
    
    while True:
        try:
            line = input()
            if line.strip() == "":
                empty_lines += 1
                if empty_lines >= 2:
                    break
            else:
                empty_lines = 0
            lines.append(line)
        except EOFError:
            break
    
    return '\n'.join(lines).strip()

def main():
    """Main function to run CV analysis"""
    print("🚀 CV ANALYSIS TOOL")
    print("=" * 50)
    print("This tool will analyze your CV and help match it with job descriptions")
    
    # Initialize agent
    agent = CompleteCVAgent()
    
    try:
        # Step 1: Get and analyze CV
        cv_path = get_file_path()
        print(f"\n⏳ Analyzing CV...")
        
        results = agent.analyze_cv_from_file(cv_path)
        
        # Step 2: Optional job matching
        while True:
            print(f"\n" + "=" * 50)
            choice = input("What would you like to do next?\n"
                          "1. Test against a job description\n"
                          "2. Save results to JSON\n"
                          "3. View CV summary again\n"
                          "4. Exit\n"
                          "Enter choice (1-4): ").strip()
            
            if choice == '1':
                # Job matching
                print(f"\n📋 JOB DESCRIPTION ANALYSIS")
                print("=" * 40)
                
                job_desc = get_multiline_input("📝 Paste the job description below:")
                
                if job_desc.strip():
                    agent.test_job_matching(job_desc)
                else:
                    print("❌ No job description provided")
                    
            elif choice == '2':
                # Save results
                save_path = input("Enter save path (or press Enter for default): ").strip()
                if not save_path:
                    save_path = None
                agent.save_results_to_json(save_path)
                
            elif choice == '3':
                # Show summary again
                agent.print_cv_summary()
                
            elif choice == '4':
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Please enter 1-4.")
                
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("💡 Please check your file path and format")

def quick_test():
    """Quick test function for development"""
    agent = CompleteCVAgent()
    
    # Sample job description for testing
    sample_job = """
    Senior Python Developer - Remote
    5+ years experience required

    Required Skills:
    - Python programming
    - AWS cloud services
    - Docker containerization
    - SQL databases
    - Git version control
    - React.js for frontend

    Responsibilities:
    - Build scalable web applications
    - Deploy on AWS infrastructure
    - Collaborate with team using Git
    """
    
    cv_path = "external_lib/resume.pdf"
    
    try:
        agent.analyze_cv_from_file(cv_path)
        agent.test_job_matching(sample_job)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Check for quick test mode
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        quick_test()
    else:
        main()