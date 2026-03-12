# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Dict, Any

# === sub function imports ===
from ._parse_primary_expr_src import _parse_primary_expr

# === Type Aliases ===
Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]


class TestParsePrimaryExpr(unittest.TestCase):
    """测试 _parse_primary_expr 函数解析主表达式的各种情况。"""

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Token:
        """辅助函数：创建 token 字典。"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.src") -> ParserState:
        """辅助函数：创建 parser_state 字典。"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    # ==================== Happy Path Tests ====================

    def test_parse_identifier(self):
        """测试解析标识符 token。"""
        tokens = [self._create_token("IDENTIFIER", "x", 1, 1)]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)  # pos 应该前进

    def test_parse_number_literal(self):
        """测试解析数字字面量。"""
        tokens = [self._create_token("NUMBER", "42", 1, 1)]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "42")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_string_literal(self):
        """测试解析字符串字面量。"""
        tokens = [self._create_token("STRING", '"hello"', 2, 5)]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], '"hello"')
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_boolean_literal(self):
        """测试解析布尔字面量。"""
        tokens = [self._create_token("BOOLEAN", "true", 1, 1)]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "true")
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_null_literal(self):
        """测试解析 null 字面量。"""
        tokens = [self._create_token("NULL", "null", 3, 10)]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "null")
        self.assertEqual(result["line"], 3)
        self.assertEqual(result["column"], 10)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_parenthesized_expression(self):
        """测试解析括号表达式（委托给 _parse_expression）。"""
        tokens = [
            self._create_token("LEFT_PAREN", "(", 1, 1),
            self._create_token("IDENTIFIER", "y", 1, 2),
            self._create_token("RIGHT_PAREN", ")", 1, 3)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Mock _parse_expression 返回一个 AST 节点
        mock_expr_result = {
            "type": "IDENTIFIER",
            "value": "y",
            "line": 1,
            "column": 2
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_expr_result
            
            result = _parse_primary_expr(parser_state)
            
            # 验证 _parse_expression 被调用
            mock_parse_expr.assert_called_once()
            # 验证返回的是 _parse_expression 的结果
            self.assertEqual(result, mock_expr_result)
            # 验证 pos 前进到右括号之后（消费了左括号、内部表达式、右括号）
            self.assertEqual(parser_state["pos"], 3)

    # ==================== Boundary / Edge Cases ====================

    def test_parse_identifier_at_non_zero_pos(self):
        """测试在非零位置解析标识符。"""
        tokens = [
            self._create_token("NUMBER", "1", 1, 1),
            self._create_token("IDENTIFIER", "z", 1, 3)
        ]
        parser_state = self._create_parser_state(tokens, pos=1)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "z")
        self.assertEqual(parser_state["pos"], 2)

    def test_parse_multiple_sequential_primary_exprs(self):
        """测试连续解析多个主表达式。"""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("NUMBER", "5", 1, 3),
            self._create_token("STRING", '"test"', 1, 5)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # 解析第一个
        result1 = _parse_primary_expr(parser_state)
        self.assertEqual(result1["value"], "a")
        self.assertEqual(parser_state["pos"], 1)
        
        # 解析第二个
        result2 = _parse_primary_expr(parser_state)
        self.assertEqual(result2["value"], "5")
        self.assertEqual(parser_state["pos"], 2)
        
        # 解析第三个
        result3 = _parse_primary_expr(parser_state)
        self.assertEqual(result3["value"], '"test"')
        self.assertEqual(parser_state["pos"], 3)

    # ==================== Error Cases ====================

    def test_empty_tokens_raises_syntax_error(self):
        """测试空 tokens 列表抛出 SyntaxError。"""
        parser_state = self._create_parser_state([], pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary_expr(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))

    def test_pos_beyond_tokens_raises_syntax_error(self):
        """测试 pos 超出 tokens 范围抛出 SyntaxError。"""
        tokens = [self._create_token("IDENTIFIER", "x", 1, 1)]
        parser_state = self._create_parser_state(tokens, pos=1)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary_expr(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))

    def test_unknown_token_type_raises_syntax_error(self):
        """测试未知 token 类型抛出 SyntaxError。"""
        tokens = [self._create_token("UNKNOWN_TYPE", "???", 5, 20)]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary_expr(parser_state)
        
        self.assertIn("Unexpected token 'UNKNOWN_TYPE'", str(context.exception))
        self.assertIn("line 5", str(context.exception))
        self.assertIn("column 20", str(context.exception))

    def test_missing_closing_parenthesis_raises_syntax_error(self):
        """测试缺少右括号抛出 SyntaxError。"""
        tokens = [
            self._create_token("LEFT_PAREN", "(", 1, 1),
            self._create_token("IDENTIFIER", "x", 1, 2)
            # 缺少 RIGHT_PAREN
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        mock_expr_result = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_expr_result
            
            with self.assertRaises(SyntaxError) as context:
                _parse_primary_expr(parser_state)
            
            self.assertIn("Missing closing parenthesis", str(context.exception))

    def test_wrong_token_after_left_paren_raises_syntax_error(self):
        """测试左括号后不是右括号（而是其他 token）抛出 SyntaxError。"""
        tokens = [
            self._create_token("LEFT_PAREN", "(", 2, 5),
            self._create_token("IDENTIFIER", "y", 2, 6),
            self._create_token("COMMA", ",", 2, 7)  # 应该是 RIGHT_PAREN 但不是
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        mock_expr_result = {"type": "IDENTIFIER", "value": "y", "line": 2, "column": 6}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_expr_result
            
            with self.assertRaises(SyntaxError) as context:
                _parse_primary_expr(parser_state)
            
            self.assertIn("Missing closing parenthesis", str(context.exception))
            self.assertIn("line 2", str(context.exception))
            self.assertIn("column 7", str(context.exception))


class TestParsePrimaryExprMockBehavior(unittest.TestCase):
    """测试 mock 行为和调用验证。"""

    def test_parse_expression_called_exactly_once(self):
        """测试 _parse_expression 在括号表达式中只被调用一次。"""
        tokens = [
            self._create_token("LEFT_PAREN", "(", 1, 1),
            self._create_token("NUMBER", "123", 1, 2),
            self._create_token("RIGHT_PAREN", ")", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        mock_result = {"type": "LITERAL", "value": "123", "line": 1, "column": 2}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_result
            
            _parse_primary_expr(parser_state)
            
            mock_parse_expr.assert_called_once()
            # 验证调用时传入的 parser_state 的 pos 已经前进到左括号之后
            call_args = mock_parse_expr.call_args
            self.assertEqual(call_args[0][0]["pos"], 1)

    def test_parse_expression_not_called_for_non_paren_tokens(self):
        """测试非括号 token 不会调用 _parse_expression。"""
        tokens = [self._create_token("IDENTIFIER", "foo", 1, 1)]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            _parse_primary_expr(parser_state)
            
            mock_parse_expr.assert_not_called()


if __name__ == "__main__":
    unittest.main()
