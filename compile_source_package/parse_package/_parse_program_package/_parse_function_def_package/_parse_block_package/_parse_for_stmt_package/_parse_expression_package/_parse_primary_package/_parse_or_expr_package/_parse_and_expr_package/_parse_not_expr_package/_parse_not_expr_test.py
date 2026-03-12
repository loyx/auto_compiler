import unittest
from unittest.mock import patch

# Relative import for the function under test
from ._parse_not_expr_src import _parse_not_expr


class TestParseNotExpr(unittest.TestCase):
    """单元测试：_parse_not_expr 函数"""

    def test_not_expression_basic(self):
        """测试基本 NOT 表达式解析"""
        tokens = [
            {"type": "NOT", "value": "not", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.src"
        }
        
        # Mock _parse_atom_expr to return a simple identifier
        with patch('._parse_atom_expr_src._parse_atom_expr') as mock_atom:
            mock_atom.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "line": 1,
                "column": 5
            }
            
            result = _parse_not_expr(parser_state)
            
            # Verify AST node structure
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "not")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0]["type"], "IDENTIFIER")
            
            # Verify pos was updated (NOT token consumed)
            self.assertEqual(parser_state["pos"], 1)
            
            # Verify _parse_atom_expr was called
            mock_atom.assert_called_once()

    def test_not_expression_nested(self):
        """测试嵌套 NOT 表达式 (NOT NOT x)"""
        tokens = [
            {"type": "NOT", "value": "not", "line": 1, "column": 1},
            {"type": "NOT", "value": "not", "line": 1, "column": 5},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 9},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.src"
        }
        
        with patch('._parse_atom_expr_src._parse_atom_expr') as mock_atom:
            mock_atom.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "line": 1,
                "column": 9
            }
            
            result = _parse_not_expr(parser_state)
            
            # Outer NOT
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "not")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            
            # Inner NOT
            inner = result["children"][0]
            self.assertEqual(inner["type"], "UNARY_OP")
            self.assertEqual(inner["value"], "not")
            self.assertEqual(inner["line"], 1)
            self.assertEqual(inner["column"], 5)
            
            # Innermost identifier
            self.assertEqual(inner["children"][0]["type"], "IDENTIFIER")
            
            # Verify pos was updated
            self.assertEqual(parser_state["pos"], 2)
            
            # _parse_atom_expr called once for innermost expression
            self.assertEqual(mock_atom.call_count, 1)

    def test_no_not_token_delegates_to_atom(self):
        """测试当前 token 不是 NOT 时，委托给 _parse_atom_expr"""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.src"
        }
        
        expected_atom = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        with patch('._parse_atom_expr_src._parse_atom_expr') as mock_atom:
            mock_atom.return_value = expected_atom
            
            result = _parse_not_expr(parser_state)
            
            # Should return what _parse_atom_expr returns
            self.assertEqual(result, expected_atom)
            
            # Verify _parse_atom_expr was called
            mock_atom.assert_called_once()
            
            # pos should not be changed by _parse_not_expr itself
            self.assertEqual(parser_state["pos"], 0)

    def test_position_at_end_delegates_to_atom(self):
        """测试 pos 在 tokens 末尾时，委托给 _parse_atom_expr"""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 1,  # At end
            "filename": "test.src"
        }
        
        expected_atom = {
            "type": "LITERAL",
            "value": "None",
            "line": 1,
            "column": 1
        }
        
        with patch('._parse_atom_expr_src._parse_atom_expr') as mock_atom:
            mock_atom.return_value = expected_atom
            
            result = _parse_not_expr(parser_state)
            
            # Should delegate to _parse_atom_expr
            self.assertEqual(result, expected_atom)
            mock_atom.assert_called_once()

    def test_pos_updated_after_consuming_not(self):
        """测试消费 NOT token 后 pos 正确更新"""
        tokens = [
            {"type": "NOT", "value": "not", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.src"
        }
        
        with patch('._parse_atom_expr_src._parse_atom_expr') as mock_atom:
            def atom_side_effect(state):
                # _parse_atom_expr should consume the IDENTIFIER
                state["pos"] = 2
                return {
                    "type": "IDENTIFIER",
                    "value": "x",
                    "line": 1,
                    "column": 5
                }
            
            mock_atom.side_effect = atom_side_effect
            
            result = _parse_not_expr(parser_state)
            
            # After parsing NOT and operand, pos should be at 2
            self.assertEqual(parser_state["pos"], 2)

    def test_ast_node_complete_structure(self):
        """测试 NOT 表达式 AST 节点的完整结构"""
        tokens = [
            {"type": "NOT", "value": "not", "line": 2, "column": 10},
            {"type": "IDENTIFIER", "value": "flag", "line": 2, "column": 14},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.src"
        }
        
        with patch('._parse_atom_expr_src._parse_atom_expr') as mock_atom:
            mock_atom.return_value = {
                "type": "IDENTIFIER",
                "value": "flag",
                "line": 2,
                "column": 14
            }
            
            result = _parse_not_expr(parser_state)
            
            # Verify all required fields exist
            self.assertIn("type", result)
            self.assertIn("value", result)
            self.assertIn("children", result)
            self.assertIn("line", result)
            self.assertIn("column", result)
            
            # Verify values
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "not")
            self.assertIsInstance(result["children"], list)
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["line"], 2)
            self.assertEqual(result["column"], 10)

    def test_not_with_literal_operand(self):
        """测试 NOT 后跟字面量"""
        tokens = [
            {"type": "NOT", "value": "not", "line": 3, "column": 5},
            {"type": "LITERAL", "value": "True", "line": 3, "column": 9},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.src"
        }
        
        with patch('._parse_atom_expr_src._parse_atom_expr') as mock_atom:
            mock_atom.return_value = {
                "type": "LITERAL",
                "value": "True",
                "line": 3,
                "column": 9
            }
            
            result = _parse_not_expr(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "not")
            self.assertEqual(result["children"][0]["type"], "LITERAL")
            self.assertEqual(parser_state["pos"], 1)

    def test_not_token_without_line_column_info(self):
        """测试 NOT token 缺少行号列号信息时的处理"""
        tokens = [
            {"type": "NOT", "value": "not"},
            {"type": "IDENTIFIER", "value": "x"},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.src"
        }
        
        with patch('._parse_atom_expr_src._parse_atom_expr') as mock_atom:
            mock_atom.return_value = {
                "type": "IDENTIFIER",
                "value": "x"
            }
            
            result = _parse_not_expr(parser_state)
            
            # Should default to 0 for missing line/column
            self.assertEqual(result["line"], 0)
            self.assertEqual(result["column"], 0)


if __name__ == '__main__':
    unittest.main()
