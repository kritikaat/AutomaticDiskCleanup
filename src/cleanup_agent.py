import os
import json
import logging
from pathlib import Path
from src.utils.safety_checker import SafetyChecker
from src.utils.file_manager import FileManager

class CleanupAgent:
    def __init__(self, config_path='src/config/settings.json'):
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
            logging.info("=" * 50)
            logging.info("STARTING DRY RUN - NO FILES WILL BE DELETED")
            logging.info("=" * 50)
        else:
            logging.info("=" * 50)
            logging.info("STARTING ACTUAL CLEANUP")
            logging.info("=" * 50)
            
        logging.info("Starting cleanup process")
        
        # Log configuration settings
        logging.info("Current settings:")
        logging.info(f"- Minimum file age: {self.config['cleanup']['min_file_age_days']} days")
        logging.info(f"- Minimum file size: {self.config['cleanup']['min_size_mb']} MB")
        logging.info(f"- Target extensions: {', '.join(self.config['cleanup']['target_extensions'])}")
        
        # Clean temp directories
        if self.config['locations']['temp_cleanup']:
            temp_dirs = [
                os.environ.get('TEMP'),
                os.path.join(os.environ.get('WINDIR'), 'Temp')
            ]
            
            for temp_dir in temp_dirs:
                if temp_dir and os.path.exists(temp_dir):
                    logging.info(f"\nScanning directory: {temp_dir}")
                    if not dry_run:
                        size, count = self.file_manager.clean_directory(temp_dir)
                        logging.info(f"Cleaned {count} files ({size:.2f} MB)")
                    else:
                        logging.info("DRY RUN - showing what would be deleted:")
                        for item in Path(temp_dir).rglob('*'):
                            if (item.is_file() and 
                                self.safety_checker.is_safe_to_delete(item) and 
                                self.file_manager.should_delete_file(item)):
                                size_mb = item.stat().st_size / (1024 * 1024)
                                logging.info(f"Would delete: {item} ({size_mb:.2f} MB)")
                        
        logging.info("\nCleanup process completed")
        logging.info("=" * 50)

if __name__ == "__main__":
    agent = CleanupAgent()
    agent.run(dry_run=True)