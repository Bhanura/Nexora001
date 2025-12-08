"""
Runner script for connection tests. 
"""
import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from nexora001.test_connections import main

if __name__ == "__main__":
    main()