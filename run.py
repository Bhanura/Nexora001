"""
Simple runner script for Nexora001
"""
import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__). parent / "src"
sys.path. insert(0, str(src_path))

# Now import and run
from nexora001.main import main

if __name__ == "__main__":
    main()