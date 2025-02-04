# Disk Cleanup Utility

A Python-based disk cleanup utility that safely manages temporary files while protecting system files and user data.

## 🚀 Features

- Safe cleanup of temporary files and directories
- Configurable file age and size thresholds
- Protection for system directories and critical files
- Files are moved to Recycle Bin (recoverable)
- Detailed logging of all operations
- Dry run mode for safe testing

## 📋 Requirements

- Python 3.6 or higher
- Windows operating system
- Required packages:
  - send2trash>=1.8.0
  - pathlib>=1.0.1

## 🔧 Installation

1. Clone or download this repository
2. Create a virtual environment: python -m venv venv
3. Activate the virtual environment: # Windows
.\venv\Scripts\activate
4. Install required packages: pip install -r requirements.txt
   
## 💻 Usage

### Quick Start

python tests/test_cleanup.py

### Test with Sample Files

# Create test files
python tests/create_test_files.py

Run cleanup
python tests/test_cleanup.py

## ⚙️ Configuration

Edit `src/config/settings.json` to customize cleanup behavior:

json
{
"cleanup": {
"min_file_age_days": 7, // Minimum file age
"min_size_mb": 0.1, // Minimum file size
"target_extensions": [ // File types to clean
".tmp",
".temp",
".cache"
]
}
}

## 📁 Project Structure
disk_cleanup_project/
├── src/
│ ├── cleanup_agent.py # Main cleanup logic
│ ├── config/
│ │ └── settings.json # Configuration file
│ └── utils/ # Utility modules
├── tests/
│ ├── test_cleanup.py # Test script
│ └── create_test_files.py
├── scripts/
│ └── startup_cleanup.bat # Startup script
└── logs/ # Log files

## 📝 Logging

- All operations are logged to `logs/cleanup.log`
- Includes:
  - Files cleaned
  - Protected files skipped
  - Files in use
  - Errors and warnings

## ⚠️ Safety Features

1. Files are moved to Recycle Bin (not permanently deleted)
2. Protected system directories:
   - Windows
   - Program Files
   - System32
3. Protected file types:
   - .exe
   - .dll
   - .sys
4. Files in use are skipped
5. Dry run mode available for testing

## 🔍 Troubleshooting

1. Check logs at `logs/cleanup.log`
2. Files marked as "in use" - close related programs
3. Protected directories - check settings.json
4. Files can be recovered from Recycle Bin if needed
