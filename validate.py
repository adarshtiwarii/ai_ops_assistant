"""
Simple validation script to check if all components are properly set up
"""

import os
import sys


def check_structure():
    """Check if all required files and directories exist"""
    print("🔍 Checking project structure...")
    
    required_items = [
        ("agents", True),
        ("agents/__init__.py", False),
        ("agents/planner_agent.py", False),
        ("agents/executor_agent.py", False),
        ("agents/verifier_agent.py", False),
        ("tools", True),
        ("tools/__init__.py", False),
        ("tools/base_tool.py", False),
        ("tools/github_tool.py", False),
        ("tools/weather_tool.py", False),
        ("tools/news_tool.py", False),
        ("llm", True),
        ("llm/__init__.py", False),
        ("llm/provider.py", False),
        ("main.py", False),
        ("requirements.txt", False),
        ("env.example", False),
        ("README.md", False),
    ]
    
    all_exist = True
    for item, is_dir in required_items:
        if is_dir:
            exists = os.path.isdir(item)
            item_type = "Directory"
        else:
            exists = os.path.isfile(item)
            item_type = "File"
        
        status = "✓" if exists else "✗"
        print(f"  {status} {item_type}: {item}")
        
        if not exists:
            all_exist = False
    
    return all_exist


def check_imports():
    """Check if all modules can be imported"""
    print("\n🔍 Checking module imports...")
    
    modules = [
        ("llm", "LLMProvider"),
        ("tools", "GitHubTool"),
        ("tools", "WeatherTool"),
        ("tools", "NewsTool"),
        ("agents", "PlannerAgent"),
        ("agents", "ExecutorAgent"),
        ("agents", "VerifierAgent"),
    ]
    
    all_imported = True
    for module_name, class_name in modules:
        try:
            module = __import__(module_name, fromlist=[class_name])
            getattr(module, class_name)
            print(f"  ✓ {module_name}.{class_name}")
        except ImportError as e:
            print(f"  ✗ {module_name}.{class_name} - {str(e)}")
            all_imported = False
        except AttributeError as e:
            print(f"  ✗ {module_name}.{class_name} - {str(e)}")
            all_imported = False
    
    return all_imported


def check_dependencies():
    """Check if required packages are installed"""
    print("\n🔍 Checking dependencies...")
    
    dependencies = ["openai", "requests", "dotenv", "pydantic"]
    all_installed = True
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"  ✓ {dep}")
        except ImportError:
            print(f"  ✗ {dep} - Not installed")
            all_installed = False
    
    return all_installed


def check_env():
    """Check environment configuration"""
    print("\n🔍 Checking environment configuration...")
    
    if os.path.exists(".env"):
        print("  ✓ .env file exists")
        
        from dotenv import load_dotenv
        load_dotenv()
        
        if os.getenv("OPENAI_API_KEY"):
            print("  ✓ OPENAI_API_KEY is set")
            return True
        else:
            print("  ✗ OPENAI_API_KEY is not set in .env")
            return False
    else:
        print("  ⚠ .env file not found (copy from env.example)")
        return False


def main():
    """Run all validation checks"""
    print("\n" + "="*60)
    print("AI OPERATIONS ASSISTANT - VALIDATION CHECK")
    print("="*60 + "\n")
    
    checks = [
        ("Project Structure", check_structure),
        ("Dependencies", check_dependencies),
        ("Module Imports", check_imports),
        ("Environment Config", check_env),
    ]
    
    results = {}
    for check_name, check_func in checks:
        results[check_name] = check_func()
    
    print("\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)
    
    all_passed = True
    for check_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {check_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*60)
    
    if all_passed:
        print("✅ All checks passed! Ready to run the assistant.")
        print("\nRun: python main.py")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Create .env file: cp env.example .env")
        print("3. Add your OPENAI_API_KEY to .env")
    
    print()
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
