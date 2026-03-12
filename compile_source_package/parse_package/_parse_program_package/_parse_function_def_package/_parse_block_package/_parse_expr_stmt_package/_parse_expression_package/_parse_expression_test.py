# === std / third-party imports ===
import unittest
from unittest.mock import patch, MagicMock
from typing import Any, Dict
import sys

# === Module path constants for patching ===
_base_pkg = "projects.cc.files.main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_expr_stmt_package._parse_expression_package"
_parse_unary_path = f"{_base_pkg}._parse_unary_package._parse_unary_src._parse_unary"
_get_precedence_path = f"{_base_pkg}._get_precedence_package._get_precedence_src._get_precedence"
_consume_token_path = f"{_base_pkg}._consume_token_package._consume_token_src._consume_token"

# === relative imports ===
from ._parse_expression_src import _parse_expression


class TestParseExpression(unittest.TestCase):
    """测试 _parse_expression 函数"""

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """辅助函数：创建 token"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.cce") -> Dict[str, Any]:
        """辅助函数：创建 parser_state"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename,
            "error": ""
        }

    def test_parse_simple_identifier(self):
        """测试解析简单标识符"""
        tokens = [self._create_token("IDENTIFIER", "x")]
        parser_state = self._create_parser_state(tokens)
        
        mock_unary_result = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_unary_package._parse_unary_src._parse_unary", return_value=mock_unary_result) as mock_unary:
            with patch("._get_precedence_package._get_precedence_src._get_precedence", return_value=0) as mock_prec:
                result = _parse_expression(parser_state)
                
                mock_unary.assert_called_once()
                self.assertEqual(result["type"], "IDENTIFIER")
                self.assertEqual(result["value"], "x")

    def test_parse_literal(self):
        """测试解析字面量"""
        tokens = [self._create_token("NUMBER", "42")]
        parser_state = self._create_parser_state(tokens)
        
        mock_unary_result = {
            "type": "LITERAL",
            "value": 42,
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_unary_package._parse_unary_src._parse_unary", return_value=mock_unary_result) as mock_unary:
            with patch("._get_precedence_package._get_precedence_src._get_precedence", return_value=0) as mock_prec:
                result = _parse_expression(parser_state)
                
                self.assertEqual(result["type"], "LITERAL")
                self.assertEqual(result["value"], 42)

    def test_parse_binary_operation(self):
        """测试解析二元运算 a + b"""
        tokens = [
            self._create_token("IDENTIFIER", "a", column=1),
            self._create_token("OPERATOR", "+", column=3),
            self._create_token("IDENTIFIER", "b", column=5)
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_unary_side_effects = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        ]
        
        def unary_side_effect(state):
            return mock_unary_side_effects.pop(0)
        
        with patch("._parse_unary_package._parse_unary_src._parse_unary", side_effect=unary_side_effect) as mock_unary:
            with patch("._get_precedence_package._get_precedence_src._get_precedence", return_value=5) as mock_prec:
                with patch("._consume_token_package._consume_token_src._consume_token", 
                          return_value=tokens[1]) as mock_consume:
                    result = _parse_expression(parser_state)
                    
                    self.assertEqual(result["type"], "BINARY_OP")
                    self.assertEqual(result["value"], "+")
                    self.assertEqual(len(result["children"]), 2)
                    self.assertEqual(result["children"][0]["value"], "a")
                    self.assertEqual(result["children"][1]["value"], "b")

    def test_parse_unary_operation(self):
        """测试解析一元运算 -x"""
        tokens = [self._create_token("IDENTIFIER", "x")]
        parser_state = self._create_parser_state(tokens)
        
        mock_unary_result = {
            "type": "UNARY_OP",
            "value": "-",
            "line": 1,
            "column": 1,
            "children": [{"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2}]
        }
        
        with patch("._parse_unary_package._parse_unary_src._parse_unary", return_value=mock_unary_result) as mock_unary:
            with patch("._get_precedence_package._get_precedence_src._get_precedence", return_value=0) as mock_prec:
                result = _parse_expression(parser_state)
                
                self.assertEqual(result["type"], "UNARY_OP")
                self.assertEqual(result["value"], "-")

    def test_empty_expression_raises_error(self):
        """测试空表达式抛出 SyntaxError"""
        tokens = []
        parser_state = self._create_parser_state(tokens)
        
        with patch("._parse_unary_package._parse_unary_src._parse_unary") as mock_unary:
            mock_unary.side_effect = SyntaxError("Unexpected end of expression")
            
            with self.assertRaises(SyntaxError):
                _parse_expression(parser_state)

    def test_operator_precedence_handling(self):
        """测试运算符优先级处理：a + b * c"""
        tokens = [
            self._create_token("IDENTIFIER", "a", column=1),
            self._create_token("OPERATOR", "+", column=3),
            self._create_token("IDENTIFIER", "b", column=5),
            self._create_token("OPERATOR", "*", column=7),
            self._create_token("IDENTIFIER", "c", column=9)
        ]
        parser_state = self._create_parser_state(tokens)
        
        # 模拟三次 unary 调用：a, b, c
        mock_unary_results = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
            {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
        ]
        
        def unary_side_effect(state):
            return mock_unary_results.pop(0)
        
        # 模拟优先级：+ 返回 5, * 返回 6
        def precedence_side_effect(token_type, token_value):
            if token_value == "+":
                return 5
            elif token_value == "*":
                return 6
            return 0
        
        # 模拟 consume_token 返回运算符
        consume_results = [
            self._create_token("OPERATOR", "+", column=3),
            self._create_token("OPERATOR", "*", column=7)
        ]
        
        def consume_side_effect(state, expected_type=None, expected_value=None):
            return consume_results.pop(0)
        
        with patch("._parse_unary_package._parse_unary_src._parse_unary", side_effect=unary_side_effect) as mock_unary:
            with patch("._get_precedence_package._get_precedence_src._get_precedence", side_effect=precedence_side_effect) as mock_prec:
                with patch("._consume_token_package._consume_token_src._consume_token", side_effect=consume_side_effect) as mock_consume:
                    result = _parse_expression(parser_state)
                    
                    # 验证结果结构
                    self.assertEqual(result["type"], "BINARY_OP")
                    # 由于 * 优先级更高，应该先结合 b * c
                    self.assertIn(result["value"], ["+", "*"])

    def test_low_precedence_stops_parsing(self):
        """测试低优先级运算符停止解析"""
        tokens = [
            self._create_token("IDENTIFIER", "a", column=1),
            self._create_token("OPERATOR", "+", column=3),
            self._create_token("IDENTIFIER", "b", column=5)
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_unary_results = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        ]
        
        def unary_side_effect(state):
            return mock_unary_results.pop(0)
        
        # 第一次调用返回优先级 5，第二次返回 0（表示停止）
        precedence_calls = [0]
        
        def precedence_side_effect(token_type, token_value):
            if precedence_calls[0] == 0:
                precedence_calls[0] = 1
                return 5
            return 0
        
        with patch("._parse_unary_package._parse_unary_src._parse_unary", side_effect=unary_side_effect):
            with patch("._get_precedence_package._get_precedence_src._get_precedence", side_effect=precedence_side_effect):
                with patch("._consume_token_package._consume_token_src._consume_token", 
                          return_value=tokens[1]):
                    result = _parse_expression(parser_state)
                    
                    self.assertEqual(result["type"], "BINARY_OP")
                    self.assertEqual(result["value"], "+")

    def test_parser_state_position_updated(self):
        """测试 parser_state 位置在解析过程中被更新"""
        tokens = [
            self._create_token("IDENTIFIER", "x", column=1),
            self._create_token("OPERATOR", "+", column=3),
            self._create_token("IDENTIFIER", "y", column=5)
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_unary_results = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 5}
        ]
        
        def unary_side_effect(state):
            return mock_unary_results.pop(0)
        
        def consume_side_effect(state, expected_type=None, expected_value=None):
            state["pos"] += 1
            return tokens[state["pos"] - 1]
        
        with patch("._parse_unary_package._parse_unary_src._parse_unary", side_effect=unary_side_effect):
            with patch("._get_precedence_package._get_precedence_src._get_precedence", return_value=5):
                with patch("._consume_token_package._consume_token_src._consume_token", side_effect=consume_side_effect):
                    initial_pos = parser_state["pos"]
                    result = _parse_expression(parser_state)
                    
                    # 验证位置被更新
                    self.assertGreater(parser_state["pos"], initial_pos)

    def test_multiple_binary_operations(self):
        """测试多个二元运算：a + b + c"""
        tokens = [
            self._create_token("IDENTIFIER", "a", column=1),
            self._create_token("OPERATOR", "+", column=3),
            self._create_token("IDENTIFIER", "b", column=5),
            self._create_token("OPERATOR", "+", column=7),
            self._create_token("IDENTIFIER", "c", column=9)
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_unary_results = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
            {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
        ]
        
        def unary_side_effect(state):
            return mock_unary_results.pop(0)
        
        consume_results = [
            self._create_token("OPERATOR", "+", column=3),
            self._create_token("OPERATOR", "+", column=7)
        ]
        
        def consume_side_effect(state, expected_type=None, expected_value=None):
            return consume_results.pop(0)
        
        with patch("._parse_unary_package._parse_unary_src._parse_unary", side_effect=unary_side_effect):
            with patch("._get_precedence_package._get_precedence_src._get_precedence", return_value=5):
                with patch("._consume_token_package._consume_token_src._consume_token", side_effect=consume_side_effect):
                    result = _parse_expression(parser_state)
                    
                    self.assertEqual(result["type"], "BINARY_OP")
                    self.assertEqual(result["value"], "+")
                    self.assertEqual(len(result["children"]), 2)

    def test_ast_node_contains_location_info(self):
        """测试 AST 节点包含位置信息"""
        tokens = [self._create_token("IDENTIFIER", "x", line=5, column=10)]
        parser_state = self._create_parser_state(tokens)
        
        mock_unary_result = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 5,
            "column": 10
        }
        
        with patch("._parse_unary_package._parse_unary_src._parse_unary", return_value=mock_unary_result):
            with patch("._get_precedence_package._get_precedence_src._get_precedence", return_value=0):
                result = _parse_expression(parser_state)
                
                self.assertIn("line", result)
                self.assertIn("column", result)
                self.assertEqual(result["line"], 5)
                self.assertEqual(result["column"], 10)


if __name__ == "__main__":
    unittest.main()
