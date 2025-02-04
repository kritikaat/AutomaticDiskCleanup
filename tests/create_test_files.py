import os
from pathlib import Path
import time

def create_test_files():
    # Create test directory
    test_dir = Path("test_cleanup")
    test_dir.mkdir(exist_ok=True)
    
    # Create sample files
    files = [
        ("test1.tmp", "test content", 0),  # Current file
        ("test2.log", "log content", 31),  # 31 days old
        ("important.doc", "important", 0),  # Won't delete (wrong extension)
        ("small.tmp", "x", 31),            # Won't delete (too small)
    ]
    
    for filename, content, days_old in files:
        file_path = test_dir / filename
        with open(file_path, "w") as f:
            f.write(content)
        
        if days_old > 0:
            # Set file modification time to X days ago
            old_time = time.time() - (days_old * 24 * 60 * 60)
            os.utime(file_path, (old_time, old_time))
    
    print(f"Created test files in {test_dir}")

if __name__ == "__main__":
    create_test_files() 