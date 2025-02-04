import os
import json
import shutil

def create_directory_structure():
    """Create the project directory structure"""
    directories = [
        'src/utils',
        'src/config',
        'src/logs',
        'tests',
        'scripts'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created {directory}/")
        
    # Create __init__.py files
    init_files = [
        'src/__init__.py',
        'src/utils/__init__.py'
    ]
    
    for init_file in init_files:
        with open(init_file, 'w') as f:
            f.write('# Empty file to make directory a Python package\n')
        print(f"Created {init_file}")

def create_config_file():
    """Create the configuration file"""
    config = {
        "safety": {
            "protected_directories": [
                "Windows",
                "Program Files",
                "Program Files (x86)",
                "System32",
                "Program Data"
            ],
            "protected_extensions": [
                ".exe",
                ".dll",
                ".sys",
                ".bat",
                ".msi"
            ]
        },
        "cleanup": {
            "min_file_age_days": 30,
            "min_size_mb": 1,
            "target_extensions": [
                ".tmp",
                ".log",
                ".cache",
                ".temp"
            ],
            "low_disk_threshold_gb": 10
        },
        "locations": {
            "temp_cleanup": True,
            "download_cleanup": False,
            "custom_folders": []
        },
        "recycle_bin": {
            "use_recycle_bin": True,
            "cleanup_recycle_bin": False
        }
    }
    
    with open('src/config/settings.json', 'w') as f:
        json.dump(config, f, indent=4)
    print("Created configuration file")

def create_requirements_file():
    """Create requirements.txt"""
    requirements = """send2trash>=1.8.0
pathlib>=1.0.1"""
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements)
    print("Created requirements.txt")

def create_batch_script():
    """Create Windows batch script"""
    batch_content = """@echo off
echo Starting Disk Cleanup Agent...
python src/cleanup_agent.py
echo Cleanup Complete!
pause"""
    
    with open('scripts/run_cleanup.bat', 'w') as f:
        f.write(batch_content)
    print("Created batch script")

def create_source_files():
    """Create all source code files"""
    
    # Create safety_checker.py
    safety_checker = '''import os
from pathlib import Path
import logging

class SafetyChecker:
    def __init__(self, config):
        self.protected_dirs = config['safety']['protected_directories']
        self.protected_exts = config['safety']['protected_extensions']
        
    def is_safe_to_delete(self, file_path):
        """Check if file is safe to delete"""
        try:
            path = Path(file_path)
            
            # Check if file exists
            if not path.exists():
                return False
                
            # Check if in protected directory
            if any(pdir.lower() in str(path).lower() 
                  for pdir in self.protected_dirs):
                logging.warning(f"Protected directory: {file_path}")
                return False
                
            # Check if protected extension
            if path.suffix.lower() in self.protected_exts:
                logging.warning(f"Protected file type: {file_path}")
                return False
                
            # Check if file is in use
            try:
                with open(file_path, 'rb') as _:
                    pass
            except PermissionError:
                logging.warning(f"File in use: {file_path}")
                return False
                
            return True
            
        except Exception as e:
            logging.error(f"Safety check error for {file_path}: {e}")
            return False'''
    
    # Create file_manager.py
    file_manager = '''import os
import datetime
import send2trash
import logging
from pathlib import Path

class FileManager:
    def __init__(self, config, safety_checker):
        self.config = config
        self.safety_checker = safety_checker
        
    def should_delete_file(self, file_path):
        """Check if file meets deletion criteria"""
        try:
            stats = Path(file_path).stat()
            
            # Check file age
            file_age = datetime.datetime.now() - datetime.datetime.fromtimestamp(stats.st_mtime)
            if file_age.days < self.config['cleanup']['min_file_age_days']:
                return False
                
            # Check file size
            file_size_mb = stats.st_size / (1024 * 1024)
            if file_size_mb < self.config['cleanup']['min_size_mb']:
                return False
                
            # Check extension
            if not any(str(file_path).lower().endswith(ext) 
                      for ext in self.config['cleanup']['target_extensions']):
                return False
                
            return True
            
        except Exception as e:
            logging.error(f"Error checking file {file_path}: {e}")
            return False'''
    
    # Create cleanup_agent.py
    cleanup_agent = '''import os
import json
import logging
from pathlib import Path
from utils.safety_checker import SafetyChecker
from utils.file_manager import FileManager

class CleanupAgent:
    def __init__(self, config_path='config/settings.json'):
        self.setup_logging()
        self.config = self.load_config(config_path)
        self.safety_checker = SafetyChecker(self.config)
        self.file_manager = FileManager(self.config, self.safety_checker)
        
    def setup_logging(self):
        """Setup logging configuration"""
        log_file = 'logs/cleanup.log'
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Add console handler
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        logging.getLogger('').addHandler(console)
        
    def load_config(self, config_path):
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error loading config: {e}")
            raise
            
    def run(self, dry_run=True):
        """Run the cleanup process"""
        if dry_run:
            logging.info("Running in DRY RUN mode - No files will be deleted")
            
        logging.info("Starting cleanup process")
        
        # Clean temp directories
        if self.config['locations']['temp_cleanup']:
            temp_dirs = [
                os.environ.get('TEMP'),
                os.path.join(os.environ.get('WINDIR'), 'Temp')
            ]
            
            for temp_dir in temp_dirs:
                if temp_dir and os.path.exists(temp_dir):
                    logging.info(f"Cleaning temp directory: {temp_dir}")
                    if not dry_run:
                        size, count = self.file_manager.clean_directory(temp_dir)
                        logging.info(f"Cleaned {count} files ({size:.2f} MB)")
                        
        logging.info("Cleanup process completed")

if __name__ == "__main__":
    agent = CleanupAgent()
    agent.run(dry_run=True)'''
    
    # Write all source files
    files = {
        'src/utils/safety_checker.py': safety_checker,
        'src/utils/file_manager.py': file_manager,
        'src/cleanup_agent.py': cleanup_agent
    }
    
    for file_path, content in files.items():
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"Created {file_path}")

def create_test_file():
    """Create test script"""
    test_content = '''import os
import sys
from src.cleanup_agent import CleanupAgent

def test_cleanup():
    # Create agent instance
    agent = CleanupAgent()
    
    # Run in dry-run mode (won't actually delete files)
    agent.run(dry_run=True)
    
    print("\\nCheck the logs at logs/cleanup.log for details")

if __name__ == "__main__":
    test_cleanup()'''
    
    with open('tests/test_cleanup.py', 'w') as f:
        f.write(test_content)
    print("Created test script")

def setup_project():
    """Main setup function"""
    try:
        create_directory_structure()
        create_config_file()
        create_requirements_file()
        create_batch_script()
        create_source_files()
        create_test_file()
        
        print("\nSetup complete! Next steps:")
        print("1. Create virtual environment: python -m venv venv")
        print("2. Activate virtual environment:")
        print("   - Windows: .\\venv\\Scripts\\activate")
        print("   - Linux/Mac: source venv/bin/activate")
        print("3. Install requirements: pip install -r requirements.txt")
        print("4. Run test: python tests/test_cleanup.py")
        
    except Exception as e:
        print(f"Error during setup: {e}")

if __name__ == "__main__":
    setup_project() 