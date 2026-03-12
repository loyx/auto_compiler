# -*- coding: utf-8 -*-
"""单元测试文件：_parse_and_expr 函数测试"""

import unittest
from unittest.mock import patch

# 相对导入被测模块
from ._parse_and_expr_src import _parse_and_expr, AST, ParserState


class TestParseAndExpr(unittest.TestCase):
    """_parse_and_expr 函数单元测试类"""

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.py") -> ParserState:
        """辅助函数：创建 parser_state 对象"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def test_single_unary_expr_no_and(self):
        """测试：单个一元表达式（无 AND 运算符）"""
        # 准备数据
        unary_result: AST = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        tokens: list = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Mock _parse_unary_expr
        with patch("_parse_and_expr_package._parse_and_expr_src._parse_unary_expr") as mock_unary:
            mock_unary.return_value = unary_result
            
            # 执行测试
            result = _parse_and_expr(parser_state)
            
            # 断言
            self.assertEqual(result, unary_result)
            self.assertEqual(mock_unary.call_count, 1)
            self.assertEqual(parser_state["pos"], 0)  # 没有消费 token

    def test_two_and_expressions(self):
        """测试：两个表达式通过 AND 连接"""
        # 准备数据
        left_unary: AST = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        right_unary: AST = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        tokens: list = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "AND", "value": "&&", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Mock _parse_unary_expr，第一次返回 left_unary，第二次返回 right_unary
        with patch("_parse_and_expr_package._parse_and_expr_src._parse_unary_expr") as mock_unary:
            mock_unary.side_effect = [left_unary, right_unary]
            
            # 执行测试
            result = _parse_and_expr(parser_state)
            
            # 断言
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "&&")
            self.assertEqual(result["left"], left_unary)
            self.assertEqual(result["right"], right_unary)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)
            self.assertEqual(mock_unary.call_count, 2)
            self.assertEqual(parser_state["pos"], 3)  # 消费了 3 个 token

    def test_three_and_expressions_left_associative(self):
        """测试：三个表达式通过 AND 连接（左结合）"""
        # 准备数据
        unary_a: AST = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        unary_b: AST = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        unary_c: AST = {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
        tokens: list = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "AND", "value": "&&", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
            {"type": "AND", "value": "&&", "line": 1, "column": 7},
            {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Mock _parse_unary_expr，依次返回 a, b, c
        with patch("_parse_and_expr_package._parse_and_expr_src._parse_unary_expr") as mock_unary:
            mock_unary.side_effect = [unary_a, unary_b, unary_c]
            
            # 执行测试
            result = _parse_and_expr(parser_state)
            
            # 断言：应该是左结合 ((a && b) && c)
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "&&")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 7)  # 最后一个 AND 的位置
            
            # 右侧应该是 c
            self.assertEqual(result["right"], unary_c)
            
            # 左侧应该是 (a && b)
            left_part = result["left"]
            self.assertEqual(left_part["type"], "BINARY_OP")
            self.assertEqual(left_part["operator"], "&&")
            self.assertEqual(left_part["left"], unary_a)
            self.assertEqual(left_part["right"], unary_b)
            self.assertEqual(left_part["line"], 1)
            self.assertEqual(left_part["column"], 3)
            
            self.assertEqual(mock_unary.call_count, 3)
            self.assertEqual(parser_state["pos"], 5)  # 消费了 5 个 token

    def test_and_at_end_missing_right_operand(self):
        """测试：AND 运算符在末尾，缺少右操作数（应抛出 SyntaxError）"""
        # 准备数据
        unary_a: AST = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        tokens: list = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "AND", "value": "&&", "line": 1, "column": 3}
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Mock _parse_unary_expr，第一次返回 a，第二次抛出 SyntaxError
        with patch("_parse_and_expr_package._parse_and_expr_src._parse_unary_expr") as mock_unary:
            mock_unary.side_effect = [
                unary_a,
                SyntaxError("Unexpected end of input in test.py")
            ]
            
            # 执行测试并断言异常
            with self.assertRaises(SyntaxError) as context:
                _parse_and_expr(parser_state)
            
            self.assertIn("Unexpected end of input", str(context.exception))
            self.assertEqual(mock_unary.call_count, 2)

    def test_empty_tokens(self):
        """测试：空 tokens 列表（应抛出 SyntaxError）"""
        tokens: list = []
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Mock _parse_unary_expr 抛出 SyntaxError
        with patch("_parse_and_expr_package._parse_and_expr_src._parse_unary_expr") as mock_unary:
            mock_unary.side_effect = SyntaxError("Unexpected end of input in test.py")
            
            # 执行测试并断言异常
            with self.assertRaises(SyntaxError):
                _parse_and_expr(parser_state)
            
            self.assertEqual(mock_unary.call_count, 1)

    def test_and_followed_by_non_unary_token(self):
        """测试：AND 后面跟着非一元表达式 token（由 _parse_unary_expr 处理）"""
        # 准备数据
        unary_a: AST = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        unary_b: AST = {"type": "LITERAL", "value": "true", "line": 1, "column": 5}
        tokens: list = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "AND", "value": "&&", "line": 1, "column": 3},
            {"type": "LITERAL", "value": "true", "line": 1, "column": 5}
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Mock _parse_unary_expr
        with patch("_parse_and_expr_package._parse_and_expr_src._parse_unary_expr") as mock_unary:
            mock_unary.side_effect = [unary_a, unary_b]
            
            # 执行测试
            result = _parse_and_expr(parser_state)
            
            # 断言
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "&&")
            self.assertEqual(result["left"], unary_a)
            self.assertEqual(result["right"], unary_b)
            self.assertEqual(mock_unary.call_count, 2)

    def test_parser_state_filename_propagation(self):
        """测试：错误信息中包含正确的文件名"""
        tokens: list = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "AND", "value": "&&", "line": 1, "column": 3}
        ]
        parser_state = self._create_parser_state(tokens, pos=0, filename="my_source.py")
        
        # Mock _parse_unary_expr，第二次调用抛出带文件名的错误
        with patch("_parse_and_expr_package._parse_and_expr_src._parse_unary_expr") as mock_unary:
            mock_unary.side_effect = [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                SyntaxError("Unexpected end of input in my_source.py")
            ]
            
            # 执行测试并断言异常包含文件名
            with self.assertRaises(SyntaxError) as context:
                _parse_and_expr(parser_state)
            
            self.assertIn("my_source.py", str(context.exception))

    def test_and_with_complex_unary_expressions(self):
        """测试：AND 连接复杂的一元表达式（如 NOT 表达式）"""
        # 准备数据：!a && !b
        not_a: AST = {
            "type": "UNARY_OP",
            "operator": "!",
            "operand": {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 2},
            "line": 1,
            "column": 1
        }
        not_b: AST = {
            "type": "UNARY_OP",
            "operator": "!",
            "operand": {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 7},
            "line": 1,
            "column": 6
        }
        tokens: list = [
            {"type": "NOT", "value": "!", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 2},
            {"type": "AND", "value": "&&", "line": 1, "column": 4},
            {"type": "NOT", "value": "!", "line": 1, "column": 6},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 7}
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Mock _parse_unary_expr
        with patch("_parse_and_expr_package._parse_and_expr_src._parse_unary_expr") as mock_unary:
            mock_unary.side_effect = [not_a, not_b]
            
            # 执行测试
            result = _parse_and_expr(parser_state)
            
            # 断言
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "&&")
            self.assertEqual(result["left"], not_a)
            self.assertEqual(result["right"], not_b)
            self.assertEqual(mock_unary.call_count, 2)


if __name__ == "__main__":
    unittest.main()
