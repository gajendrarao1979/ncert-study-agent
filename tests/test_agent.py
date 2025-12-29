
"""
Unit tests for the NCERT Notes Agent
"""

import unittest
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import load_config


class TestAgent(unittest.TestCase):
    """Test cases for agent functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.config = load_config()
    
    def test_config_loading(self):
        """Test configuration loading"""
        self.assertIsInstance(self.config, dict)
        self.assertIn('google', self.config)
        self.assertIn('output', self.config)
    
    def test_directories_exist(self):
        """Test that required directories can be created"""
        downloads_dir = Path(self.config['output']['downloads_dir'])
        notes_dir = Path(self.config['output']['notes_dir'])
        
        downloads_dir.mkdir(parents=True, exist_ok=True)
        notes_dir.mkdir(parents=True, exist_ok=True)
        
        self.assertTrue(downloads_dir.exists())
        self.assertTrue(notes_dir.exists())


if __name__ == '__main__':
    unittest.main()