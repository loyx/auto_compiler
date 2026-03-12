import sys
import unittest
from unittest.mock import patch, mock_open
from io import StringIO

# Relative import for the main function
from .main_src import main


class TestMain(unittest.TestCase):
    
    @patch('main_package.main_src.compile_source')
    @patch('main_package.main_src.parse_arguments')
    def test_main_success_stdout(self, mock_parse, mock_compile):
        """Test successful compilation with output to stdout"""
        mock_parse.return_value = {
            "source_file": "test.c",
            "output_file": None,
            "verbose": False
        }
        mock_compile.return_value = "mov x0, #1"
        
        # Capture stdout
        captured_output = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured_output
        
        try:
            result = main()
        finally:
            sys.stdout = old_stdout
        
        self.assertEqual(result, 0)
        mock_parse.assert_called_once()
        mock_compile.assert_called_once_with(mock_parse.return_value)
        self.assertEqual(captured_output.getvalue().strip(), "mov x0, #1")
    
    @patch('main_package.main_src.compile_source')
    @patch('main_package.main_src.parse_arguments')
    @patch('builtins.open', new_callable=mock_open)
    def test_main_success_file(self, mock_file, mock_parse, mock_compile):
        """Test successful compilation with output to file"""
        mock_parse.return_value = {
            "source_file": "test.c",
            "output_file": "output.s",
            "verbose": False
        }
        mock_compile.return_value = "mov x0, #1\nret"
        
        result = main()
        
        self.assertEqual(result, 0)
        mock_file.assert_called_once_with("output.s", "w")
        mock_file().write.assert_called_once_with("mov x0, #1\nret")
    
    @patch('main_package.main_src.compile_source')
    @patch('main_package.main_src.parse_arguments')
    def test_main_file_not_found(self, mock_parse, mock_compile):
        """Test FileNotFoundError handling"""
        mock_parse.side_effect = FileNotFoundError("test.c not found")
        
        captured_stderr = StringIO()
        old_stderr = sys.stderr
        sys.stderr = captured_stderr
        
        try:
            result = main()
        finally:
            sys.stderr = old_stderr
        
        self.assertEqual(result, 1)
        self.assertIn("error:", captured_stderr.getvalue())
        mock_compile.assert_not_called()
    
    @patch('main_package.main_src.compile_source')
    @patch('main_package.main_src.parse_arguments')
    def test_main_general_exception(self, mock_parse, mock_compile):
        """Test general exception handling"""
        mock_parse.side_effect = ValueError("Invalid argument")
        
        captured_stderr = StringIO()
        old_stderr = sys.stderr
        sys.stderr = captured_stderr
        
        try:
            result = main()
        finally:
            sys.stderr = old_stderr
        
        self.assertEqual(result, 1)
        self.assertIn("error:", captured_stderr.getvalue())
        mock_compile.assert_not_called()
    
    @patch('main_package.main_src.compile_source')
    @patch('main_package.main_src.parse_arguments')
    def test_main_compile_exception(self, mock_parse, mock_compile):
        """Test exception during compilation"""
        mock_parse.return_value = {
            "source_file": "test.c",
            "output_file": None,
            "verbose": False
        }
        mock_compile.side_effect = RuntimeError("Compilation failed")
        
        captured_stderr = StringIO()
        old_stderr = sys.stderr
        sys.stderr = captured_stderr
        
        try:
            result = main()
        finally:
            sys.stderr = old_stderr
        
        self.assertEqual(result, 1)
        self.assertIn("error:", captured_stderr.getvalue())
        mock_parse.assert_called_once()
        mock_compile.assert_called_once()
    
    @patch('main_package.main_src.compile_source')
    @patch('main_package.main_src.parse_arguments')
    @patch('builtins.open', new_callable=mock_open)
    def test_main_file_write_exception(self, mock_file, mock_parse, mock_compile):
        """Test exception during file write"""
        mock_parse.return_value = {
            "source_file": "test.c",
            "output_file": "output.s",
            "verbose": False
        }
        mock_compile.return_value = "mov x0, #1"
        mock_file.side_effect = PermissionError("Cannot write to output.s")
        
        captured_stderr = StringIO()
        old_stderr = sys.stderr
        sys.stderr = captured_stderr
        
        try:
            result = main()
        finally:
            sys.stderr = old_stderr
        
        self.assertEqual(result, 1)
        self.assertIn("error:", captured_stderr.getvalue())
    
    @patch('main_package.main_src.compile_source')
    @patch('main_package.main_src.parse_arguments')
    def test_main_empty_assembly(self, mock_parse, mock_compile):
        """Test successful compilation with empty assembly output"""
        mock_parse.return_value = {
            "source_file": "empty.c",
            "output_file": None,
            "verbose": False
        }
        mock_compile.return_value = ""
        
        captured_output = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured_output
        
        try:
            result = main()
        finally:
            sys.stdout = old_stdout
        
        self.assertEqual(result, 0)
        self.assertEqual(captured_output.getvalue(), "\n")
    
    @patch('main_package.main_src.compile_source')
    @patch('main_package.main_src.parse_arguments')
    def test_main_with_verbose_flag(self, mock_parse, mock_compile):
        """Test compilation with verbose flag in config"""
        mock_parse.return_value = {
            "source_file": "test.c",
            "output_file": None,
            "verbose": True
        }
        mock_compile.return_value = ".section __TEXT,__text\nmov x0, #1"
        
        captured_output = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured_output
        
        try:
            result = main()
        finally:
            sys.stdout = old_stdout
        
        self.assertEqual(result, 0)
        config = mock_parse.return_value
        mock_compile.assert_called_once_with(config)


if __name__ == '__main__':
    unittest.main()
