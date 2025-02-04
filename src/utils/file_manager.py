import os
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
            return False

    def clean_directory(self, directory):
        """Clean a single directory"""
        cleaned_size = 0
        files_cleaned = 0
        
        try:
            for item in Path(directory).rglob('*'):
                if (item.is_file() and 
                    self.safety_checker.is_safe_to_delete(item) and 
                    self.should_delete_file(item)):
                    
                    size_mb = item.stat().st_size / (1024 * 1024)
                    
                    try:
                        if self.config['recycle_bin']['use_recycle_bin']:
                            send2trash.send2trash(str(item))
                        else:
                            item.unlink()
                            
                        cleaned_size += size_mb
                        files_cleaned += 1
                        logging.info(f"Cleaned: {item} ({size_mb:.2f} MB)")
                        
                    except Exception as e:
                        logging.error(f"Error deleting {item}: {e}")
                        
        except Exception as e:
            logging.error(f"Error cleaning directory {directory}: {e}")
            
        return cleaned_size, files_cleaned