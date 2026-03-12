import unittest
from unittest.mock import patch

from ._parse_expr_stmt_src import _parse_expr_stmt


class TestParseExprStmt(unittest.TestCase):
    """测试 _parse_expr_stmt 函数"""

    def test_happy_path_no_semicolon(self):
        """测试不带分号的表达式语句"""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_expr_node = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        def mock_parse_expr_side_effect(state):
            state["pos"] = 1
            return mock_expr_node
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression", side_effect=mock_parse_expr_side_effect) as mock_parse_expr:
            result = _parse_expr_stmt(parser_state)
            
            self.assertEqual(result["type"], "EXPR_STMT")
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0], mock_expr_node)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(parser_state["pos"], 1)
            mock_parse_expr.assert_called_once_with(parser_state)

    def test_with_semicolon(self):
        """测试带分号的表达式语句（分号应被消费）"""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 2},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_expr_node = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        def mock_parse_expr_side_effect(state):
            state["pos"] = 1
            return mock_expr_node
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression", side_effect=mock_parse_expr_side_effect) as mock_parse_expr:
            result = _parse_expr_stmt(parser_state)
            
            self.assertEqual(result["type"], "EXPR_STMT")
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0], mock_expr_node)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(parser_state["pos"], 2)
            mock_parse_expr.assert_called_once_with(parser_state)

    def test_empty_input_raises_syntax_error(self):
        """测试空输入时抛出 SyntaxError"""
        tokens = []
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expr_stmt(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))

    def test_pos_at_end_raises_syntax_error(self):
        """测试 pos 在 tokens 末尾时抛出 SyntaxError"""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expr_stmt(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))

    def test_complex_expression(self):
        """测试复杂表达式（如二元运算）"""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 2, "column": 5},
            {"type": "PLUS", "value": "+", "line": 2, "column": 7},
            {"type": "NUMBER", "value": "1", "line": 2, "column": 9},
            {"type": "SEMICOLON", "value": ";", "line": 2, "column": 10},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_expr_node = {
            "type": "BINARY_OP",
            "children": [
                {"type": "IDENTIFIER", "value": "x", "line": 2, "column": 5},
                {"type": "NUMBER", "value": "1", "line": 2, "column": 9}
            ],
            "value": "+",
            "line": 2,
            "column": 5
        }
        
        def mock_parse_expr_side_effect(state):
            state["pos"] = 3
            return mock_expr_node
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression", side_effect=mock_parse_expr_side_effect) as mock_parse_expr:
            result = _parse_expr_stmt(parser_state)
            
            self.assertEqual(result["type"], "EXPR_STMT")
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0], mock_expr_node)
            self.assertEqual(result["line"], 2)
            self.assertEqual(result["column"], 5)
            self.assertEqual(parser_state["pos"], 4)
            mock_parse_expr.assert_called_once_with(parser_state)

    def test_expression_without_semicolon_at_end(self):
        """测试表达式后没有分号且已到 tokens 末尾"""
        tokens = [
            {"type": "NUMBER", "value": "42", "line": 3, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_expr_node = {
            "type": "LITERAL",
            "value": 42,
            "line": 3,
            "column": 1
        }
        
        def mock_parse_expr_side_effect(state):
            state["pos"] = 1
            return mock_expr_node
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression", side_effect=mock_parse_expr_side_effect) as mock_parse_expr:
            result = _parse_expr_stmt(parser_state)
            
            self.assertEqual(result["type"], "EXPR_STMT")
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0], mock_expr_node)
            self.assertEqual(result["line"], 3)
            self.assertEqual(result["column"], 1)
            self.assertEqual(parser_state["pos"], 1)
            mock_parse_expr.assert_called_once_with(parser_state)

    def test_different_token_types_after_expression(self):
        """测试表达式后是其他 token（不是分号）时不消费"""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "NEWLINE", "value": "\n", "line": 1, "column": 2},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_expr_node = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        def mock_parse_expr_side_effect(state):
            state["pos"] = 1
            return mock_expr_node
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression", side_effect=mock_parse_expr_side_effect) as mock_parse_expr:
            result = _parse_expr_stmt(parser_state)
            
            self.assertEqual(result["type"], "EXPR_STMT")
            self.assertEqual(parser_state["pos"], 1)
            mock_parse_expr.assert_called_once_with(parser_state)


if __name__ == "__main__":
    unittest.main()
