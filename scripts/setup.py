#!/usr/bin/env python3
"""
Setup script for the Kite Trading Bot project.
"""

import sys
import subprocess
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required, found {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def create_virtual_environment():
    """Create virtual environment if it doesn't exist."""
    venv_path = Path("venv")
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    print("🔄 Creating virtual environment...")
    return run_command("python3 -m venv venv", "Creating virtual environment")

def install_dependencies():
    """Install project dependencies."""
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("❌ requirements.txt not found")
        return False
    
    # Activate virtual environment and install dependencies
    if os.name == 'nt':  # Windows
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix/Linux/Mac
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
    
    install_cmd = f"{activate_cmd} && {pip_cmd} install -r requirements.txt"
    return run_command(install_cmd, "Installing dependencies")

def create_directories():
    """Create necessary directories."""
    print("📁 Creating project directories...")
    
    directories = [
        "data/raw",
        "data/processed", 
        "data/results",
        "reports/analysis",
        "reports/performance",
        "reports/comparisons",
        "logs",
        "tests/unit",
        "tests/integration",
        "tests/performance"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def setup_environment_file():
    """Create .env file from example if it doesn't exist."""
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if env_example.exists():
        print("📝 Creating .env file from example...")
        with open(env_example, 'r') as f:
            example_content = f.read()
        
        with open(env_file, 'w') as f:
            f.write(example_content)
        
        print("✅ .env file created from example")
        print("⚠️  Please update .env file with your actual API credentials")
        return True
    else:
        print("❌ env.example file not found")
        return False

def verify_setup():
    """Verify that setup was successful."""
    print("\n🔍 Verifying setup...")
    
    # Check if virtual environment exists
    venv_path = Path("venv")
    if not venv_path.exists():
        print("❌ Virtual environment not found")
        return False
    
    # Check if key directories exist
    key_dirs = ["src", "data", "reports", "config", "scripts"]
    for directory in key_dirs:
        if not Path(directory).exists():
            print(f"❌ Directory {directory} not found")
            return False
    
    # Check if key files exist
    key_files = ["requirements.txt", "README.md", "config/settings.py"]
    for file in key_files:
        if not Path(file).exists():
            print(f"❌ File {file} not found")
            return False
    
    print("✅ Setup verification completed successfully")
    return True

def main():
    """Main setup function."""
    print("🚀 Setting up Kite Trading Bot project...")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Setup environment file
    setup_environment_file()
    
    # Verify setup
    if not verify_setup():
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Update .env file with your Kite API credentials")
    print("2. Activate virtual environment: source venv/bin/activate")
    print("3. Run a backtest: python scripts/run_backtest.py --strategy v3")
    print("4. Analyze results: python scripts/analyze_results.py")
    
    print("\n📚 Documentation:")
    print("- README.md: Project overview and quick start")
    print("- docs/reports/: Strategy reports and analysis")
    print("- config/: Configuration files")

if __name__ == "__main__":
    main()
