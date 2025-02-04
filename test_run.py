import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.agent import DiskCleanupAgent

def test_run():
    # Create agent instance
    agent = DiskCleanupAgent()
    
    # Run maintenance
    agent.run_maintenance()
    
    print("\nCheck the logs at logs/disk_cleanup.log for details")

if __name__ == "__main__":
    test_run() 