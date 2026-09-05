#!/usr/bin/env python
"""
Installation and Setup Script for Phishing Detection System
Run this script to set up the project and train the models
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a shell command and return success status"""
    print(f"\n{'='*60}")
    print(f"📦 {description}")
    print(f"{'='*60}")
    print(f"Running: {command}\n")
    
    try:
        result = subprocess.run(command, shell=True, check=True)
        print(f"\n✅ {description} - SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {description} - FAILED")
        print(f"Error: {e}")
        return False

def main():
    """Main setup function"""
    print("\n")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║   Phishing Website Detection System - Setup Script       ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    # Detect OS
    system = platform.system()
    print(f"\n🔍 Detected OS: {system}")
    
    # Step 1: Create virtual environment if not exists
    venv_path = ".venv"
    if not os.path.exists(venv_path):
        cmd = f"python -m venv {venv_path}"
        if not run_command(cmd, "Creating virtual environment"):
            print("\n❌ Failed to create virtual environment")
            return False
    else:
        print(f"\n✅ Virtual environment already exists at {venv_path}")
    
    # Step 2: Activate virtual environment and install dependencies
    if system == "Windows":
        activate_cmd = f"{venv_path}\\Scripts\\activate &&"
    else:
        activate_cmd = f"source {venv_path}/bin/activate &&"
    
    # Install requirements
    install_cmd = f"{activate_cmd} pip install -r requirements.txt"
    if not run_command(install_cmd, "Installing dependencies from requirements.txt"):
        print("\n❌ Failed to install dependencies")
        return False
    
    # Step 3: Create database
    migrate_cmd = f"{activate_cmd} python manage.py migrate"
    run_command(migrate_cmd, "Creating/updating Django database")
    
    # Step 4: Train models
    train_cmd = f"{activate_cmd} python train_model.py"
    print(f"\n{'='*60}")
    print("🤖 Training ML Models (Random Forest & SVM)")
    print(f"{'='*60}")
    print("This may take a few minutes depending on dataset size...\n")
    
    if not run_command(train_cmd, "Training machine learning models"):
        print("\n⚠️  Warning: Model training may have issues")
        print("Make sure phishing_site_urls.csv exists in the archive (3) (2)/ folder")
    
    # Step 5: Collect static files
    static_cmd = f"{activate_cmd} python manage.py collectstatic --noinput"
    run_command(static_cmd, "Collecting static files")
    
    # Summary
    print(f"\n{'='*60}")
    print("✅ SETUP COMPLETE!")
    print(f"{'='*60}")
    
    print("\n📋 Next Steps:")
    print("-" * 60)
    print("\n1. Activate virtual environment:")
    if system == "Windows":
        print(f"   {venv_path}\\Scripts\\activate")
    else:
        print(f"   source {venv_path}/bin/activate")
    
    print("\n2. Run the development server:")
    print("   python manage.py runserver")
    
    print("\n3. Open your browser and navigate to:")
    print("   http://127.0.0.1:8000")
    
    print("\n4. Test the phishing detection:")
    print("   - Visit the Detector page")
    print("   - Enter a URL (e.g., https://www.google.com)")
    print("   - Click 'Check URL'")
    
    print("\n5. API Testing (using curl or Postman):")
    print("   POST http://127.0.0.1:8000/detector/api/predict")
    print("   Body: {\"url\": \"https://example.com\", \"model\": \"random_forest\"}")
    
    print("\n" + "="*60)
    print("📚 Documentation:")
    print("   Read README.md for complete documentation")
    print("="*60 + "\n")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
