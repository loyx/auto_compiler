import unittest
from ._verify_control_flow_stmt_src import _verify_control_flow_stmt


class TestVerifyControlFlowStmt(unittest.TestCase):
    """Test cases for _verify_control_flow_stmt function."""

    def test_break_stmt_with_loop_context_at_top(self):
        """Happy path: break_stmt with loop frame at stack top."""
        node = {"type": "break_stmt", "line": 10, "column": 5}
        context_stack = [
            {"type": "function", "name": "main", "return_type": "int"},
            {"type": "loop", "stmt_type": "for"}
        ]
        filename = "test.py"
        
        # Should not raise any exception
        _verify_control_flow_stmt(node, context_stack, filename)

    def test_continue_stmt_with_loop_context_at_top(self):
        """Happy path: continue_stmt with loop frame at stack top."""
        node = {"type": "continue_stmt", "line": 15, "column": 8}
        context_stack = [
            {"type": "function", "name": "main", "return_type": "int"},
            {"type": "loop", "stmt_type": "while"}
        ]
        filename = "test.py"
        
        # Should not raise any exception
        _verify_control_flow_stmt(node, context_stack, filename)

    def test_break_stmt_with_loop_context_in_middle(self):
        """Happy path: break_stmt with loop frame in middle of stack."""
        node = {"type": "break_stmt", "line": 20, "column": 3}
        context_stack = [
            {"type": "function", "name": "main", "return_type": "int"},
            {"type": "loop", "stmt_type": "for"},
            {"type": "function", "name": "helper", "return_type": "void"}
        ]
        filename = "test.py"
        
        # Should not raise any exception
        _verify_control_flow_stmt(node, context_stack, filename)

    def test_continue_stmt_with_loop_context_at_bottom(self):
        """Happy path: continue_stmt with loop frame at stack bottom."""
        node = {"type": "continue_stmt", "line": 25, "column": 10}
        context_stack = [
            {"type": "loop", "stmt_type": "while"},
            {"type": "function", "name": "outer", "return_type": "int"},
            {"type": "function", "name": "inner", "return_type": "void"}
        ]
        filename = "test.py"
        
        # Should not raise any exception
        _verify_control_flow_stmt(node, context_stack, filename)

    def test_break_stmt_without_loop_context(self):
        """Error path: break_stmt with only function frames in stack."""
        node = {"type": "break_stmt", "line": 30, "column": 5}
        context_stack = [
            {"type": "function", "name": "main", "return_type": "int"}
        ]
        filename = "test.py"
        
        with self.assertRaises(ValueError) as context:
            _verify_control_flow_stmt(node, context_stack, filename)
        
        self.assertEqual(str(context.exception), "test.py:30:5: error: 'break' is not allowed outside of a loop")

    def test_continue_stmt_without_loop_context(self):
        """Error path: continue_stmt with only function frames in stack."""
        node = {"type": "continue_stmt", "line": 35, "column": 12}
        context_stack = [
            {"type": "function", "name": "main", "return_type": "int"}
        ]
        filename = "test.py"
        
        with self.assertRaises(ValueError) as context:
            _verify_control_flow_stmt(node, context_stack, filename)
        
        self.assertEqual(str(context.exception), "test.py:35:12: error: 'continue' is not allowed outside of a loop")

    def test_break_stmt_with_empty_context_stack(self):
        """Edge case: break_stmt with empty context_stack."""
        node = {"type": "break_stmt", "line": 40, "column": 1}
        context_stack = []
        filename = "test.py"
        
        with self.assertRaises(ValueError) as context:
            _verify_control_flow_stmt(node, context_stack, filename)
        
        self.assertEqual(str(context.exception), "test.py:40:1: error: 'break' is not allowed outside of a loop")

    def test_continue_stmt_with_empty_context_stack(self):
        """Edge case: continue_stmt with empty context_stack."""
        node = {"type": "continue_stmt", "line": 45, "column": 2}
        context_stack = []
        filename = "test.py"
        
        with self.assertRaises(ValueError) as context:
            _verify_control_flow_stmt(node, context_stack, filename)
        
        self.assertEqual(str(context.exception), "test.py:45:2: error: 'continue' is not allowed outside of a loop")

    def test_break_stmt_with_non_dict_frame_in_stack(self):
        """Edge case: context_stack contains non-dict frames."""
        node = {"type": "break_stmt", "line": 50, "column": 7}
        context_stack = [
            "some_string",
            None,
            {"type": "loop", "stmt_type": "for"}
        ]
        filename = "test.py"
        
        # Should not raise - loop frame is found
        _verify_control_flow_stmt(node, context_stack, filename)

    def test_break_stmt_with_missing_line_column(self):
        """Edge case: node with missing line/column fields."""
        node = {"type": "break_stmt"}
        context_stack = [
            {"type": "function", "name": "main", "return_type": "int"}
        ]
        filename = "test.py"
        
        with self.assertRaises(ValueError) as context:
            _verify_control_flow_stmt(node, context_stack, filename)
        
        # Should use default value 0 for missing fields
        self.assertEqual(str(context.exception), "test.py:0:0: error: 'break' is not allowed outside of a loop")

    def test_continue_stmt_with_missing_line_column(self):
        """Edge case: node with missing line/column fields."""
        node = {"type": "continue_stmt"}
        context_stack = [
            {"type": "function", "name": "main", "return_type": "int"}
        ]
        filename = "test.py"
        
        with self.assertRaises(ValueError) as context:
            _verify_control_flow_stmt(node, context_stack, filename)
        
        # Should use default value 0 for missing fields
        self.assertEqual(str(context.exception), "test.py:0:0: error: 'continue' is not allowed outside of a loop")

    def test_break_stmt_with_missing_type_field(self):
        """Edge case: node with missing type field."""
        node = {"line": 55, "column": 3}
        context_stack = [
            {"type": "function", "name": "main", "return_type": "int"}
        ]
        filename = "test.py"
        
        # Should not raise - type is not break_stmt or continue_stmt
        _verify_control_flow_stmt(node, context_stack, filename)

    def test_multiple_loop_frames_in_stack(self):
        """Edge case: multiple loop frames in context_stack."""
        node = {"type": "break_stmt", "line": 60, "column": 5}
        context_stack = [
            {"type": "function", "name": "main", "return_type": "int"},
            {"type": "loop", "stmt_type": "for"},
            {"type": "loop", "stmt_type": "while"},
            {"type": "function", "name": "helper", "return_type": "void"}
        ]
        filename = "test.py"
        
        # Should not raise - loop frame is found
        _verify_control_flow_stmt(node, context_stack, filename)

    def test_loop_frame_without_stmt_type(self):
        """Edge case: loop frame without stmt_type field."""
        node = {"type": "break_stmt", "line": 65, "column": 8}
        context_stack = [
            {"type": "function", "name": "main", "return_type": "int"},
            {"type": "loop"}
        ]
        filename = "test.py"
        
        # Should not raise - frame has type "loop"
        _verify_control_flow_stmt(node, context_stack, filename)


if __name__ == "__main__":
    unittest.main()
