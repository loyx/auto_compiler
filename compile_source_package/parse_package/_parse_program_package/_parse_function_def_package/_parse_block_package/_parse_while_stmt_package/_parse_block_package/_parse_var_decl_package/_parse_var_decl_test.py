import unittest
from unittest.mock import patch
from typing import Dict, Any

# Relative import from the same package
from _parse_var_decl_package._parse_var_decl_src import _parse_var_decl


class TestParseVarDecl(unittest.TestCase):
    """单元测试：_parse_var_decl 函数"""
    
    def test_simple_var_declaration(self):
        """测试：var x; 简单变量声明"""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "VAR", "value": "var", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5},
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 6}
            ],
            "pos": 0,
            "filename": "test.txt"
        }
        
        with patch('._consume_token_package._consume_token_src._consume_token') as mock_consume:
            mock_consume.side_effect = lambda state, expected: {**state, "pos": state["pos"] + 1}
            
            result = _parse_var_decl(parser_state)
            
            self.assertEqual(result["type"], "VAR_DECL")
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0]["type"], "IDENTIFIER")
            self.assertEqual(result["children"][0]["value"], "x")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            
            # 验证 _consume_token 被调用了 3 次 (VAR, IDENTIFIER, SEMICOLON)
            self.assertEqual(mock_consume.call_count, 3)
    
    def test_var_declaration_with_initialization(self):
        """测试：var x = 5; 带初始化的变量声明"""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "VAR", "value": "var", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5},
                {"type": "ASSIGN", "value": "=", "line": 1, "column": 7},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 9},
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 10}
            ],
            "pos": 0,
            "filename": "test.txt"
        }
        
        with patch('._consume_token_package._consume_token_src._consume_token') as mock_consume:
            with patch('._parse_expression_package._parse_expression_src._parse_expression') as mock_parse_expr:
                mock_consume.side_effect = lambda state, expected: {**state, "pos": state["pos"] + 1}
                mock_parse_expr.return_value = {
                    "type": "NUMBER",
                    "value": "5",
                    "line": 1,
                    "column": 9,
                    "_parser_state": {"tokens": parser_state["tokens"], "pos": 4, "filename": "test.txt"}
                }
                
                result = _parse_var_decl(parser_state)
                
                self.assertEqual(result["type"], "VAR_DECL")
                self.assertEqual(len(result["children"]), 2)
                self.assertEqual(result["children"][0]["type"], "IDENTIFIER")
                self.assertEqual(result["children"][0]["value"], "x")
                self.assertEqual(result["children"][1]["type"], "NUMBER")
                self.assertEqual(result["children"][1]["value"], "5")
                
                # 验证 _parse_expression 被调用
                mock_parse_expr.assert_called_once()
    
    def test_unexpected_end_of_input_at_start(self):
        """测试：空 token 列表抛出 SyntaxError"""
        parser_state: Dict[str, Any] = {
            "tokens": [],
            "pos": 0,
            "filename": "test.txt"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_var_decl(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
    
    def test_missing_identifier_after_var(self):
        """测试：var 后没有标识符抛出 SyntaxError"""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "VAR", "value": "var", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.txt"
        }
        
        with patch('._consume_token_package._consume_token_src._consume_token') as mock_consume:
            mock_consume.side_effect = lambda state, expected: {**state, "pos": state["pos"] + 1}
            
            with self.assertRaises(SyntaxError) as context:
                _parse_var_decl(parser_state)
            
            self.assertIn("Expected identifier", str(context.exception))
    
    def test_wrong_token_type_instead_of_identifier(self):
        """测试：var 后跟非标识符 token 抛出 SyntaxError"""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "VAR", "value": "var", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.txt"
        }
        
        with patch('._consume_token_package._consume_token_src._consume_token') as mock_consume:
            mock_consume.side_effect = lambda state, expected: {**state, "pos": state["pos"] + 1}
            
            with self.assertRaises(SyntaxError) as context:
                _parse_var_decl(parser_state)
            
            self.assertIn("Expected identifier, got NUMBER", str(context.exception))
    
    def test_missing_semicolon(self):
        """测试：缺少分号抛出 SyntaxError"""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "VAR", "value": "var", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.txt"
        }
        
        with patch('._consume_token_package._consume_token_src._consume_token') as mock_consume:
            mock_consume.side_effect = lambda state, expected: {**state, "pos": state["pos"] + 1}
            
            with self.assertRaises(SyntaxError) as context:
                _parse_var_decl(parser_state)
            
            self.assertIn("Expected ';'", str(context.exception))
    
    def test_wrong_token_instead_of_semicolon(self):
        """测试：结尾不是分号抛出 SyntaxError"""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "VAR", "value": "var", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 7}
            ],
            "pos": 0,
            "filename": "test.txt"
        }
        
        with patch('._consume_token_package._consume_token_src._consume_token') as mock_consume:
            mock_consume.side_effect = lambda state, expected: {**state, "pos": state["pos"] + 1}
            
            with self.assertRaises(SyntaxError) as context:
                _parse_var_decl(parser_state)
            
            self.assertIn("Expected ';', got NUMBER", str(context.exception))
    
    def test_var_declaration_with_complex_expression(self):
        """测试：var x = a + b; 带复杂表达式的变量声明"""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "VAR", "value": "var", "line": 2, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 2, "column": 5},
                {"type": "ASSIGN", "value": "=", "line": 2, "column": 7},
                {"type": "IDENTIFIER", "value": "a", "line": 2, "column": 9},
                {"type": "PLUS", "value": "+", "line": 2, "column": 11},
                {"type": "IDENTIFIER", "value": "b", "line": 2, "column": 13},
                {"type": "SEMICOLON", "value": ";", "line": 2, "column": 14}
            ],
            "pos": 0,
            "filename": "test.txt"
        }
        
        with patch('._consume_token_package._consume_token_src._consume_token') as mock_consume:
            with patch('._parse_expression_package._parse_expression_src._parse_expression') as mock_parse_expr:
                mock_consume.side_effect = lambda state, expected: {**state, "pos": state["pos"] + 1}
                mock_parse_expr.return_value = {
                    "type": "BINARY_OP",
                    "children": [
                        {"type": "IDENTIFIER", "value": "a", "line": 2, "column": 9},
                        {"type": "IDENTIFIER", "value": "b", "line": 2, "column": 13}
                    ],
                    "value": "+",
                    "line": 2,
                    "column": 9,
                    "_parser_state": {"tokens": parser_state["tokens"], "pos": 6, "filename": "test.txt"}
                }
                
                result = _parse_var_decl(parser_state)
                
                self.assertEqual(result["type"], "VAR_DECL")
                self.assertEqual(len(result["children"]), 2)
                self.assertEqual(result["children"][0]["type"], "IDENTIFIER")
                self.assertEqual(result["children"][1]["type"], "BINARY_OP")
                self.assertEqual(result["line"], 2)
                self.assertEqual(result["column"], 1)
    
    def test_position_tracking(self):
        """测试：AST 节点正确记录起始位置"""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "VAR", "value": "var", "line": 5, "column": 10},
                {"type": "IDENTIFIER", "value": "count", "line": 5, "column": 14},
                {"type": "SEMICOLON", "value": ";", "line": 5, "column": 19}
            ],
            "pos": 0,
            "filename": "test.txt"
        }
        
        with patch('._consume_token_package._consume_token_src._consume_token') as mock_consume:
            mock_consume.side_effect = lambda state, expected: {**state, "pos": state["pos"] + 1}
            
            result = _parse_var_decl(parser_state)
            
            self.assertEqual(result["line"], 5)
            self.assertEqual(result["column"], 10)
            self.assertEqual(result["children"][0]["line"], 5)
            self.assertEqual(result["children"][0]["column"], 14)


if __name__ == '__main__':
    unittest.main()
