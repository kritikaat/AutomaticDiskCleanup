import os
import datetime
from pathlib import Path
import send2trash
import logging

def is_safe_to_delete(file_path):
    """Check if file is safe to delete"""
    try:
        critical_paths = ['Windows', 'Program Files', 'Program Files (x86)']
        return not any(cp.lower() in str(file_path).lower() for cp in critical_paths)
    except Exception:
        return False

def clean_folder(folder_path, days_threshold, min_file_size_mb, file_extensions):
    """Clean a single folder based on age threshold"""
    cleaned_size = 0
    files_cleaned = 0
    current_time = datetime.datetime.now()
    
    try:
        folder = Path(folder_path)
        if not folder.exists():
            return 0, 0

        for item in folder.rglob('*'):
            try:
                if item.is_file() and is_safe_to_delete(item):
                    file_age = datetime.datetime.fromtimestamp(item.stat().st_mtime)
                    days_old = (current_time - file_age).days
                    file_size_mb = item.stat().st_size / (1024 * 1024)
                    
                    if (days_old > days_threshold and 
                        file_size_mb >= min_file_size_mb and
                        any(str(item).lower().endswith(ext.lower()) 
                            for ext in file_extensions)):
                        cleaned_size += file_size_mb
                        files_cleaned += 1
                        send2trash.send2trash(str(item))
                        logging.info(f"Cleaned: {item} ({file_size_mb:.2f} MB)")
                        
            except Exception as e:
                logging.error(f"Error processing {item}: {e}")
                
    except Exception as e:
        logging.error(f"Error cleaning folder {folder_path}: {e}")
        
    return cleaned_size, files_cleaned