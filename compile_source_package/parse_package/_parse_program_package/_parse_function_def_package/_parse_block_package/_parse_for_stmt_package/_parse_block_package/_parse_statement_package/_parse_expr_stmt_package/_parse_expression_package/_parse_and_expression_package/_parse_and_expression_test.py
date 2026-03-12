# -*- coding: utf-8 -*-
"""
单元测试：_parse_and_expression 函数
测试逻辑与表达式解析（&& 运算符）
"""
import unittest
from unittest.mock import patch

from ._parse_and_expression_src import _parse_and_expression


def create_token(type_val: str, value: str, line: int = 1, column: int = 1) -> dict:
    """辅助函数：创建 Token 字典"""
    return {
        "type": type_val,
        "value": value,
        "line": line,
        "column": column
    }


def create_ast_node(type_val: str, value: str = None, line: int = 1, column: int = 1, children: list = None) -> dict:
    """辅助函数：创建 AST 节点字典"""
    node = {
        "type": type_val,
        "line": line,
        "column": column
    }
    if value is not None:
        node["value"] = value
    if children is not None:
        node["children"] = children
    return node


class TestParseAndExpression(unittest.TestCase):
    """_parse_and_expression 函数测试类"""

    @patch('._parse_comparison_package._parse_comparison_src._parse_comparison')
    def test_no_and_operator(self, mock_parse_comparison):
        """测试：没有 && 运算符，直接返回比较表达式"""
        # 准备数据
        comparison_ast = create_ast_node("COMPARISON", "a > 0")
        mock_parse_comparison.return_value = comparison_ast
        
        tokens = [
            create_token("IDENTIFIER", "a", 1, 1),
            create_token("OPERATOR", ">", 1, 3),
            create_token("NUMBER", "0", 1, 5)
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        # 执行
        result = _parse_and_expression(parser_state)
        
        # 验证
        self.assertEqual(result, comparison_ast)
        mock_parse_comparison.assert_called_once_with(parser_state)
        self.assertEqual(parser_state["pos"], 0)  # pos 未改变（因为 mock 没推进）

    @patch('._parse_comparison_package._parse_comparison_src._parse_comparison')
    def test_single_and_operator(self, mock_parse_comparison):
        """测试：单个 && 运算符，构建二元操作节点"""
        # 准备数据：左操作数和右操作数
        left_ast = create_ast_node("COMPARISON", "a > 0", 1, 1)
        right_ast = create_ast_node("COMPARISON", "b < 10", 1, 10)
        mock_parse_comparison.side_effect = [left_ast, right_ast]
        
        tokens = [
            create_token("IDENTIFIER", "a", 1, 1),
            create_token("OPERATOR", ">", 1, 3),
            create_token("NUMBER", "0", 1, 5),
            create_token("OPERATOR", "&&", 1, 7),
            create_token("IDENTIFIER", "b", 1, 10),
            create_token("OPERATOR", "<", 1, 12),
            create_token("NUMBER", "10", 1, 14)
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        # 执行
        result = _parse_and_expression(parser_state)
        
        # 验证：构建 BINARY_OP 节点
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "&&")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 7)
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0], left_ast)
        self.assertEqual(result["children"][1], right_ast)
        
        # 验证：_parse_comparison 被调用两次
        self.assertEqual(mock_parse_comparison.call_count, 2)
        
        # 验证：pos 推进到 tokens 末尾
        self.assertEqual(parser_state["pos"], 7)

    @patch('._parse_comparison_package._parse_comparison_src._parse_comparison')
    def test_multiple_and_operators_left_associative(self, mock_parse_comparison):
        """测试：多个 && 运算符，左结合结构"""
        # 准备数据：a && b && c 应该解析为 (a && b) && c
        ast_a = create_ast_node("COMPARISON", "a", 1, 1)
        ast_b = create_ast_node("COMPARISON", "b", 1, 5)
        ast_c = create_ast_node("COMPARISON", "c", 1, 9)
        mock_parse_comparison.side_effect = [ast_a, ast_b, ast_c]
        
        tokens = [
            create_token("IDENTIFIER", "a", 1, 1),
            create_token("OPERATOR", "&&", 1, 3),
            create_token("IDENTIFIER", "b", 1, 5),
            create_token("OPERATOR", "&&", 1, 7),
            create_token("IDENTIFIER", "c", 1, 9)
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        # 执行
        result = _parse_and_expression(parser_state)
        
        # 验证：左结合结构 (a && b) && c
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "&&")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 7)  # 第二个 && 的位置
        
        # 左子节点应该是第一个 && 的 BINARY_OP
        left_child = result["children"][0]
        self.assertEqual(left_child["type"], "BINARY_OP")
        self.assertEqual(left_child["value"], "&&")
        self.assertEqual(left_child["line"], 1)
        self.assertEqual(left_child["column"], 3)  # 第一个 && 的位置
        self.assertEqual(left_child["children"][0], ast_a)
        self.assertEqual(left_child["children"][1], ast_b)
        
        # 右子节点应该是 c
        right_child = result["children"][1]
        self.assertEqual(right_child, ast_c)
        
        # 验证：_parse_comparison 被调用三次
        self.assertEqual(mock_parse_comparison.call_count, 3)
        
        # 验证：pos 推进到 tokens 末尾
        self.assertEqual(parser_state["pos"], 5)

    @patch('._parse_comparison_package._parse_comparison_src._parse_comparison')
    def test_missing_right_operand(self, mock_parse_comparison):
        """测试：&& 后缺少右操作数，抛出 SyntaxError"""
        # 准备数据
        left_ast = create_ast_node("COMPARISON", "a > 0", 1, 1)
        mock_parse_comparison.return_value = left_ast
        
        tokens = [
            create_token("IDENTIFIER", "a", 1, 1),
            create_token("OPERATOR", ">", 1, 3),
            create_token("NUMBER", "0", 1, 5),
            create_token("OPERATOR", "&&", 1, 7)
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        # 执行并验证异常
        with self.assertRaises(SyntaxError) as context:
            _parse_and_expression(parser_state)
        
        # 验证异常消息
        self.assertIn("Expected expression after '&&'", str(context.exception))
        self.assertIn("line 1", str(context.exception))
        self.assertIn("column 7", str(context.exception))
        
        # 验证：_parse_comparison 只被调用一次
        mock_parse_comparison.assert_called_once_with(parser_state)

    @patch('._parse_comparison_package._parse_comparison_src._parse_comparison')
    def test_empty_tokens(self, mock_parse_comparison):
        """测试：空 token 列表"""
        # 准备数据
        empty_ast = create_ast_node("EMPTY", "")
        mock_parse_comparison.return_value = empty_ast
        
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        # 执行
        result = _parse_and_expression(parser_state)
        
        # 验证
        self.assertEqual(result, empty_ast)
        mock_parse_comparison.assert_called_once_with(parser_state)
        self.assertEqual(parser_state["pos"], 0)

    @patch('._parse_comparison_package._parse_comparison_src._parse_comparison')
    def test_non_and_operator_breaks_loop(self, mock_parse_comparison):
        """测试：遇到非 && 运算符时停止解析"""
        # 准备数据
        left_ast = create_ast_node("COMPARISON", "a > 0", 1, 1)
        mock_parse_comparison.return_value = left_ast
        
        tokens = [
            create_token("IDENTIFIER", "a", 1, 1),
            create_token("OPERATOR", ">", 1, 3),
            create_token("NUMBER", "0", 1, 5),
            create_token("OPERATOR", "+", 1, 7),  # 不是 &&
            create_token("NUMBER", "1", 1, 9)
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        # 执行
        result = _parse_and_expression(parser_state)
        
        # 验证：直接返回左操作数
        self.assertEqual(result, left_ast)
        mock_parse_comparison.assert_called_once_with(parser_state)
        self.assertEqual(parser_state["pos"], 0)  # pos 未改变

    @patch('._parse_comparison_package._parse_comparison_src._parse_comparison')
    def test_different_operator_type(self, mock_parse_comparison):
        """测试：遇到非 OPERATOR 类型的 token 时停止解析"""
        # 准备数据
        left_ast = create_ast_node("COMPARISON", "a", 1, 1)
        mock_parse_comparison.return_value = left_ast
        
        tokens = [
            create_token("IDENTIFIER", "a", 1, 1),
            create_token("KEYWORD", "and", 1, 3),  # 类型不是 OPERATOR
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        # 执行
        result = _parse_and_expression(parser_state)
        
        # 验证：直接返回左操作数
        self.assertEqual(result, left_ast)
        mock_parse_comparison.assert_called_once_with(parser_state)
        self.assertEqual(parser_state["pos"], 0)


if __name__ == "__main__":
    unittest.main()
