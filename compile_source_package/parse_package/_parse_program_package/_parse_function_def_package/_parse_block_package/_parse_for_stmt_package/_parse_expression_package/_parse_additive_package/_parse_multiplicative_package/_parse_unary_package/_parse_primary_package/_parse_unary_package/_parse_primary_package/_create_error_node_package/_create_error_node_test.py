# === test file for _create_error_node ===
import unittest
from ._create_error_node_src import _create_error_node


class TestCreateErrorNode(unittest.TestCase):
    """Test cases for _create_error_node function."""

    def test_basic_error_node_creation(self):
        """Test basic ERROR node creation with valid inputs."""
        result = _create_error_node("Syntax error", 10, 5)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "Syntax error")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 5)

    def test_empty_error_message(self):
        """Test ERROR node with empty error message."""
        result = _create_error_node("", 1, 1)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)

    def test_zero_line_and_column(self):
        """Test ERROR node with zero line and column numbers."""
        result = _create_error_node("Error at start", 0, 0)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "Error at start")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)

    def test_large_line_and_column_numbers(self):
        """Test ERROR node with large line and column numbers."""
        result = _create_error_node("Deep error", 9999, 999)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "Deep error")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 9999)
        self.assertEqual(result["column"], 999)

    def test_error_message_with_special_characters(self):
        """Test ERROR node with special characters in message."""
        special_msg = "Error: unexpected token ';' at line 5"
        result = _create_error_node(special_msg, 5, 20)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], special_msg)
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 20)

    def test_error_message_with_newlines(self):
        """Test ERROR node with newlines in message."""
        multiline_msg = "Error on line 1\nContinued on line 2"
        result = _create_error_node(multiline_msg, 1, 1)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], multiline_msg)
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)

    def test_returned_dict_structure(self):
        """Test that returned dict has exactly the expected keys."""
        result = _create_error_node("Test error", 42, 13)
        
        expected_keys = {"type", "value", "children", "line", "column"}
        self.assertEqual(set(result.keys()), expected_keys)

    def test_children_is_empty_list(self):
        """Test that children field is an empty list (not None or other type)."""
        result = _create_error_node("Test", 1, 1)
        
        self.assertIsInstance(result["children"], list)
        self.assertEqual(len(result["children"]), 0)

    def test_return_type_is_dict(self):
        """Test that function returns a dictionary."""
        result = _create_error_node("Test", 1, 1)
        
        self.assertIsInstance(result, dict)

    def test_multiple_calls_independence(self):
        """Test that multiple calls produce independent nodes."""
        result1 = _create_error_node("Error 1", 1, 1)
        result2 = _create_error_node("Error 2", 2, 2)
        
        self.assertEqual(result1["value"], "Error 1")
        self.assertEqual(result2["value"], "Error 2")
        self.assertEqual(result1["line"], 1)
        self.assertEqual(result2["line"], 2)
        
        # Modify one result's children, ensure other is not affected
        result1["children"].append("modified")
        self.assertEqual(len(result2["children"]), 0)


if __name__ == "__main__":
    unittest.main()
