import sys
import pkg_resources
import os
from dotenv import load_dotenv

def check_python_version():
    required_version = (3, 11, 4)
    current_version = sys.version_info[:3]
    
    if current_version < required_version:
        print(f"❌ Python version {'.'.join(map(str, current_version))} is too old.")
        print(f"Required version: {'.'.join(map(str, required_version))}")
        return False
    print("✅ Python version check passed!")
    return True

def check_critical_dependencies():
    required_packages = {
        'fastapi': '0.109.2',
        'uvicorn': '0.27.1',
        'openai': '1.12.0',
        'python-dotenv': '1.0.1'
    }
    
    all_passed = True
    for package, version in required_packages.items():
        try:
            pkg_resources.require(f"{package}=={version}")
            print(f"✅ {package} version check passed!")
        except pkg_resources.VersionConflict:
            print(f"❌ {package} version mismatch!")
            all_passed = False
        except pkg_resources.DistributionNotFound:
            print(f"❌ {package} is not installed!")
            all_passed = False
    
    return all_passed

def check_environment_variables():
    load_dotenv()
    required_vars = ['OPENAI_API_KEY']
    
    all_passed = True
    for var in required_vars:
        if not os.getenv(var):
            print(f"❌ Missing required environment variable: {var}")
            all_passed = False
        else:
            print(f"✅ Environment variable {var} is set")
    
    return all_passed

def main():
    print("🔍 Starting environment check...\n")
    
    python_check = check_python_version()
    deps_check = check_critical_dependencies()
    env_check = check_environment_variables()
    
    print("\n📊 Check Summary:")
    print(f"Python Version: {'✅' if python_check else '❌'}")
    print(f"Dependencies: {'✅' if deps_check else '❌'}")
    print(f"Environment Variables: {'✅' if env_check else '❌'}")
    
    if all([python_check, deps_check, env_check]):
        print("\n✨ All checks passed! Your environment is ready.")
    else:
        print("\n⚠️ Some checks failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 