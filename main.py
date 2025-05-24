#!/usr/bin/env python3
"""
CV Agent - Main Entry Point
Run this script to analyze your CV and match it against job descriptions
"""

import os
import sys
from cv_agent.core import CompleteCVAgent
from cv_agent.config import Config

cv_path = "external_lib/resume.pdf"

def get_file_path():
    """Get CV file path from user with validation"""
    while True:
        file_path = "external_lib/resume.pdf"
        
        if not file_path:
            print("❌ Please enter a file path")
            continue
            
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            print("💡 Try dragging the file into the terminal or use full path")
            continue
            
        # Check file extension using config
        ext = file_path.lower().split('.')[-1]
        if ext not in Config.SUPPORTED_FORMATS:
            print(f"❌ Unsupported file type: {ext}")
            print(f"💡 Supported formats: {', '.join(Config.SUPPORTED_FORMATS).upper()}")
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
        # cv_path = get_file_path()
        print(f"\n⏳ Analyzing CV...")
        
        results = agent.analyze_cv_from_file(cv_path)
        
        # Step 2: Optional job matching
        while True:
            print(f"\n" + "=" * 50)
            choice = input("What would you like to do next?\n"
                  "1. Test against a job description\n"
                  "2. Initialize AI rewriter (requires HuggingFace token)\n"
                  "3. Rewrite CV section with AI\n"
                  "4. Optimize CV for specific role\n"
                  "5. Get AI improvement suggestions\n"
                  "6. Save results to JSON\n"
                  "7. View CV summary again\n"
                  "8. Exit\n"
                  "Enter choice (1-8): ").strip()
            
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
                # Initialize LLM rewriter
                print("🤖 AI REWRITER SETUP")
                print("=" * 30)
                token = input(f"Enter your HuggingFace token (or press Enter to use env var): ").strip()
                if not token:
                    token = Config.HUGGINGFACE_TOKEN
                
                use_local = input("Use local models? (y/n): ").lower().startswith('y')
                if not use_local:
                    use_local = Config.USE_LOCAL_MODELS
                
                if token or use_local:
                    success = agent.initialize_llm_rewriter(token, use_local)
                    if success:
                        print("✅ AI rewriter ready! You can now use options 3-5.")
                else:
                    print("⚠️ Skipping AI rewriter setup - no token provided")
                    
            elif choice == '3':
                # Rewrite single CV section
                if not agent.llm_rewriter:
                    print("❌ Please initialize AI rewriter first (option 2)")
                    continue
                    
                print("📝 CV SECTION REWRITER")
                print("=" * 30)
                available_sections = [s for s, content in agent.cv_results['sections'].items() if content.strip()]
                print(f"Available sections: {available_sections}")
                
                section = input("Enter section to rewrite: ").strip().lower()
                if section not in available_sections:
                    print(f"❌ Section '{section}' not found or empty")
                    continue
                    
                target_role = input("Target role (optional): ").strip() or None
                tone_options = ['professional', 'confident', 'humble']
                tone = input(f"Tone ({'/'.join(tone_options)}): ").strip() or Config.DEFAULT_TONE
                focus_options = ['general', 'achievements', 'skills', 'responsibilities']
                focus = input(f"Focus ({'/'.join(focus_options)}): ").strip() or 'general'
                
                response = agent.rewrite_cv_content(section, target_role, tone, focus)
                
            elif choice == '4':
                # Optimize entire CV for specific role
                if not agent.llm_rewriter:
                    print("❌ Please initialize AI rewriter first (option 2)")
                    continue
                    
                print("🎯 CV OPTIMIZATION FOR SPECIFIC ROLE")
                print("=" * 40)
                target_role = input("Enter target role: ").strip()
                if target_role:
                    results = agent.optimize_cv_for_role(target_role)
                    print(f"\n✅ Optimized {len(results)} sections for '{target_role}' role")
                else:
                    print("❌ Please enter a target role")
                    
            elif choice == '5':
                # Get improvement suggestions
                print("💡 CV IMPROVEMENT SUGGESTIONS")
                print("=" * 35)
                suggestions = agent.get_cv_improvement_suggestions()
                if suggestions:
                    for i, suggestion in enumerate(suggestions, 1):
                        print(f"   {i}. {suggestion}")
                else:
                    print("   ✅ No specific improvements needed!")
                    
            elif choice == '6':
                # Save results
                save_path = input("Enter save path (or press Enter for default): ").strip()
                if not save_path:
                    save_path = None
                agent.save_results_to_json(save_path)
                
            elif choice == '7':
                # Show summary again
                agent.print_cv_summary()
                
            elif choice == '8':
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Please enter 1-8.")
                
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("💡 Please check your file path and format")

def quick_test():
    """Enhanced quick test function for development - tests all features"""
    print("🧪 RUNNING COMPREHENSIVE QUICK TEST")
    print("=" * 50)
    
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
    - Lead development teams
    - Implement CI/CD pipelines
    """
    
    try:
        # Step 1: Analyze CV
        print("🔍 Step 1: Analyzing CV...")
        results = agent.analyze_cv_from_file(cv_path)
        
        # Step 2: Test job matching
        print("\n🎯 Step 2: Testing job matching...")
        match_results = agent.test_job_matching(sample_job)
        
        # Step 3: Initialize AI rewriter (using config defaults)
        print("\n🤖 Step 3: Initializing AI rewriter...")
        # Try to use environment token or local models
        token = Config.HUGGINGFACE_TOKEN
        use_local = Config.USE_LOCAL_MODELS
        
        ai_initialized = agent.initialize_llm_rewriter(token, use_local)
        
        if ai_initialized:
            # Step 4: Test AI improvement suggestions (Choice 5)
            print("\n💡 Step 4: Getting AI improvement suggestions...")
            suggestions = agent.get_cv_improvement_suggestions()
            print("AI Suggestions:")
            for i, suggestion in enumerate(suggestions, 1):
                print(f"   {i}. {suggestion}")
            
            # Step 5: Test single section rewrite (Choice 3)
            print("\n📝 Step 5: Testing section rewrite...")
            # Try to rewrite the experience section
            if 'experience' in results['sections'] and results['sections']['experience'].strip():
                response = agent.rewrite_cv_content(
                    section='experience',
                    target_role='Senior Python Developer',
                    tone=Config.DEFAULT_TONE,
                    focus='achievements'
                )
                if response:
                    print("✅ Section rewrite completed")
            else:
                print("⚠️ No experience section found to rewrite")
            
            # Step 6: Test CV optimization for role (Choice 4)
            print("\n🎯 Step 6: Testing CV optimization for role...")
            optimization_results = agent.optimize_cv_for_role('Senior Python Developer')
            print(f"✅ Optimized {len(optimization_results)} sections for target role")
            
        else:
            print("⚠️ AI rewriter not initialized - skipping AI-powered tests")
            print("💡 To test AI features, set HUGGINGFACE_TOKEN environment variable")
            print("   or enable USE_LOCAL_MODELS in config.py")
        
        print("\n✅ QUICK TEST COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Quick test error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Check for quick test mode
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        quick_test()
    else:
        main()