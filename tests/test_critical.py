import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import pyarrow as pa
import sys
import os

# Add the parent directory to the path so we can import critical.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# This is a simple test file to verify basic functionality
class TestCritical(unittest.TestCase):
    
    @patch('wget.download')
    @patch('pyarrow.parquet.read_table')
    @patch('sqlalchemy.create_engine')
    def test_data_processing(self, mock_create_engine, mock_read_table, mock_wget):
        """Test that the data processing pipeline works correctly with mock data"""
        
        # Mock the wget download to return a filename
        mock_wget.return_value = "test_data.parquet"
        
        # Create a mock PyArrow table with test data
        mock_table = MagicMock()
        test_data = pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})
        mock_table.to_pandas.return_value = test_data
        mock_read_table.return_value = mock_table
        
        # Mock the database connection
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine
        
        # Import the module now that we've set up our mocks
        import critical
        
        # Call the module's global code
        
        # Check that wget was called 13 times (once for initial download and then for each month)
        self.assertEqual(mock_wget.call_count, 13)
        
        # Check that read_table was called 12 times (once for each month)
        self.assertEqual(mock_read_table.call_count, 12)
        
        # Verify database connection was created
        mock_create_engine.assert_called_once_with('postgresql://admin:admin@sample_postgres/silent')
        
        # Since critical.py executes when imported, we don't need to call any functions

if __name__ == '__main__':
    unittest.main()