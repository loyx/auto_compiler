import unittest
from unittest.mock import patch

# Import the function under test using relative import
from ._verify_loop_stmt_src import _verify_loop_stmt


class TestVerifyLoopStmt(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0
        }
        self.filename = "test_file.c"
    
    @patch("projects.cc.files.main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_loop_stmt_package._verify_loop_stmt_src._verify_node")
    def test_while_stmt_happy_path(self, mock_verify_node):
        """Test while_stmt verification with normal flow."""
        node = {
            "type": "while_stmt",
            "condition": {"type": "binary_expr", "line": 10, "column": 5},
            "body": {"type": "compound_stmt", "line": 11, "column": 5},
            "line": 10,
            "column": 5
        }
        context_stack = []
        
        _verify_loop_stmt(node, self.symbol_table, context_stack, self.filename)
        
        # Should call _verify_node 2 times: condition and body
        self.assertEqual(mock_verify_node.call_count, 2)
        
        # Verify call order and parameters
        calls = mock_verify_node.call_args_list
        self.assertEqual(calls[0][0][0]["type"], "binary_expr")  # condition
        self.assertEqual(calls[1][0][0]["type"], "compound_stmt")  # body
        
        # Context stack should be balanced (empty after function completes)
        self.assertEqual(len(context_stack), 0)
    
    @patch("projects.cc.files.main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_loop_stmt_package._verify_loop_stmt_src._verify_node")
    def test_for_stmt_happy_path(self, mock_verify_node):
        """Test for_stmt verification with normal flow."""
        node = {
            "type": "for_stmt",
            "init": {"type": "assign_expr", "line": 10, "column": 5},
            "condition": {"type": "binary_expr", "line": 11, "column": 5},
            "body": {"type": "compound_stmt", "line": 12, "column": 5},
            "update": {"type": "assign_expr", "line": 13, "column": 5},
            "line": 10,
            "column": 5
        }
        context_stack = []
        
        _verify_loop_stmt(node, self.symbol_table, context_stack, self.filename)
        
        # Should call _verify_node 4 times: init, condition, body, update
        self.assertEqual(mock_verify_node.call_count, 4)
        
        # Verify call order and parameters
        calls = mock_verify_node.call_args_list
        self.assertEqual(calls[0][0][0]["type"], "assign_expr")  # init
        self.assertEqual(calls[1][0][0]["type"], "binary_expr")  # condition
        self.assertEqual(calls[2][0][0]["type"], "compound_stmt")  # body
        self.assertEqual(calls[3][0][0]["type"], "assign_expr")  # update
        
        # Context stack should be balanced
        self.assertEqual(len(context_stack), 0)
    
    @patch("projects.cc.files.main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_loop_stmt_package._verify_loop_stmt_src._verify_node")
    def test_context_stack_balance_on_exception_while(self, mock_verify_node):
        """Test that context_stack remains balanced even when body verification raises."""
        node = {
            "type": "while_stmt",
            "condition": {"type": "binary_expr", "line": 10, "column": 5},
            "body": {"type": "compound_stmt", "line": 11, "column": 5},
            "line": 10,
            "column": 5
        }
        context_stack = []
        
        # Make body verification raise an exception
        mock_verify_node.side_effect = [None, Exception("Body verification failed"), None]
        
        with self.assertRaises(Exception):
            _verify_loop_stmt(node, self.symbol_table, context_stack, self.filename)
        
        # Context stack should still be balanced (empty) due to try-finally
        self.assertEqual(len(context_stack), 0)
    
    @patch("_verify_loop_stmt_src._verify_node")
    def test_context_stack_balance_on_exception_for(self, mock_verify_node):
        """Test that context_stack remains balanced for for_stmt when body raises."""
        node = {
            "type": "for_stmt",
            "init": {"type": "assign_expr", "line": 10, "column": 5},
            "condition": {"type": "binary_expr", "line": 11, "column": 5},
            "body": {"type": "compound_stmt", "line": 12, "column": 5},
            "update": {"type": "assign_expr", "line": 13, "column": 5},
            "line": 10,
            "column": 5
        }
        context_stack = []
        
        # Make body verification raise an exception (3rd call)
        mock_verify_node.side_effect = [None, None, Exception("Body verification failed"), None]
        
        with self.assertRaises(Exception):
            _verify_loop_stmt(node, self.symbol_table, context_stack, self.filename)
        
        # Context stack should still be balanced (empty) due to try-finally
        self.assertEqual(len(context_stack), 0)
    
    def test_unknown_node_type_raises_value_error(self):
        """Test that unknown node type raises ValueError with proper error message."""
        node = {
            "type": "unknown_stmt",
            "line": 10,
            "column": 5
        }
        context_stack = []
        
        with self.assertRaises(ValueError) as context:
            _verify_loop_stmt(node, self.symbol_table, context_stack, self.filename)
        
        self.assertIn("未知的循环语句类型 unknown_stmt", str(context.exception))
        self.assertIn("test_file.c:10:5", str(context.exception))
    
    @patch("_verify_loop_stmt_src._verify_node")
    def test_while_stmt_loop_frame_content(self, mock_verify_node):
        """Test that correct loop frame is pushed for while_stmt."""
        node = {
            "type": "while_stmt",
            "condition": {"type": "binary_expr", "line": 10, "column": 5},
            "body": {"type": "compound_stmt", "line": 11, "column": 5},
            "line": 10,
            "column": 5
        }
        context_stack = []
        
        # Track what gets pushed to context_stack
        original_append = context_stack.append
        pushed_frames = []
        
        def track_append(frame):
            pushed_frames.append(frame.copy())
            original_append(frame)
        
        context_stack.append = track_append
        
        _verify_loop_stmt(node, self.symbol_table, context_stack, self.filename)
        
        # Verify the loop frame content
        self.assertEqual(len(pushed_frames), 1)
        self.assertEqual(pushed_frames[0]["type"], "loop")
        self.assertEqual(pushed_frames[0]["stmt_type"], "while")
    
    @patch("_verify_loop_stmt_src._verify_node")
    def test_for_stmt_loop_frame_content(self, mock_verify_node):
        """Test that correct loop frame is pushed for for_stmt."""
        node = {
            "type": "for_stmt",
            "init": {"type": "assign_expr", "line": 10, "column": 5},
            "condition": {"type": "binary_expr", "line": 11, "column": 5},
            "body": {"type": "compound_stmt", "line": 12, "column": 5},
            "update": {"type": "assign_expr", "line": 13, "column": 5},
            "line": 10,
            "column": 5
        }
        context_stack = []
        
        # Track what gets pushed to context_stack
        original_append = context_stack.append
        pushed_frames = []
        
        def track_append(frame):
            pushed_frames.append(frame.copy())
            original_append(frame)
        
        context_stack.append = track_append
        
        _verify_loop_stmt(node, self.symbol_table, context_stack, self.filename)
        
        # Verify the loop frame content
        self.assertEqual(len(pushed_frames), 1)
        self.assertEqual(pushed_frames[0]["type"], "loop")
        self.assertEqual(pushed_frames[0]["stmt_type"], "for")
    
    def test_missing_line_column_defaults(self):
        """Test that missing line/column default to '?' in error messages."""
        node = {
            "type": "unknown_stmt"
            # No line or column
        }
        context_stack = []
        
        with self.assertRaises(ValueError) as context:
            _verify_loop_stmt(node, self.symbol_table, context_stack, self.filename)
        
        # Should use '?' for missing line/column
        self.assertIn("test_file.c:?:?", str(context.exception))
    
    @patch("_verify_loop_stmt_src._verify_node")
    def test_symbol_table_and_filename_passed_correctly(self, mock_verify_node):
        """Test that symbol_table and filename are passed correctly to _verify_node."""
        node = {
            "type": "while_stmt",
            "condition": {"type": "binary_expr", "line": 10, "column": 5},
            "body": {"type": "compound_stmt", "line": 11, "column": 5},
            "line": 10,
            "column": 5
        }
        context_stack = []
        custom_symbol_table = {"custom": "table"}
        custom_filename = "custom_file.c"
        
        _verify_loop_stmt(node, custom_symbol_table, context_stack, custom_filename)
        
        # Verify all calls received correct symbol_table and filename
        for call in mock_verify_node.call_args_list:
            self.assertEqual(call[0][1], custom_symbol_table)
            self.assertEqual(call[0][3], custom_filename)
    
    @patch("_verify_loop_stmt_src._verify_node")
    def test_context_stack_with_existing_frames(self, mock_verify_node):
        """Test that function works correctly with pre-existing context stack frames."""
        node = {
            "type": "while_stmt",
            "condition": {"type": "binary_expr", "line": 10, "column": 5},
            "body": {"type": "compound_stmt", "line": 11, "column": 5},
            "line": 10,
            "column": 5
        }
        context_stack = [
            {"type": "function", "name": "main", "return_type": "int"}
        ]
        original_length = len(context_stack)
        
        _verify_loop_stmt(node, self.symbol_table, context_stack, self.filename)
        
        # Context stack should return to original length
        self.assertEqual(len(context_stack), original_length)
        # Original frame should still be there
        self.assertEqual(context_stack[0]["type"], "function")
        self.assertEqual(context_stack[0]["name"], "main")


if __name__ == "__main__":
    unittest.main()
