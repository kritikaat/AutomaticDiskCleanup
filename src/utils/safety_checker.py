import os
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
            return False