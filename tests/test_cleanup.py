import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.cleanup_agent import CleanupAgent

def test_cleanup():
    # Create agent instance
    agent = CleanupAgent()
    
    print("\nWARNING: Running in ACTUAL DELETE mode!")
    print("Files will be moved to Recycle Bin\n")
    
    # Run without dry mode - will actually delete files
    agent.run(dry_run=False)
    
    print("\nCheck the logs at logs/cleanup.log for details")

if __name__ == "__main__":
    test_cleanup()