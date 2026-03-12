# -*- coding: utf-8 -*-
"""
单元测试文件：_parse_or 函数测试
测试逻辑或表达式（|| 运算符）的解析功能
"""

import unittest
from unittest.mock import patch
from typing import Dict, Any, List

# 相对导入被测模块
from ._parse_or_src import _parse_or, _current_token_is_or, _build_binary_op_node


class TestParseOr(unittest.TestCase):
    """_parse_or 函数的单元测试类"""

    def _create_parser_state(self, tokens: List[Dict[str, Any]], pos: int = 0, filename: str = "test.c") -> Dict[str, Any]:
        """辅助函数：创建 parser_state 字典"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """辅助函数：创建 token 字典"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_ast_node(self, node_type: str, value: Any = None, children: List = None, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """辅助函数：创建 AST 节点"""
        return {
            "type": node_type,
            "value": value,
            "children": children if children is not None else [],
            "line": line,
            "column": column
        }

    # ==================== Happy Path 测试 ====================

    @patch('_parse_or_package._parse_or_src._parse_and')
    @patch('_parse_or_package._parse_or_src._current_token_is_or')
    @patch('_parse_or_package._parse_or_src._consume_token')
    @patch('_parse_or_package._parse_or_src._build_binary_op_node')
    def test_single_expression_no_or(self, mock_build, mock_consume, mock_is_or, mock_parse_and):
        """测试：单个表达式，没有 || 运算符"""
        # 模拟 _parse_and 返回一个 AST 节点
        left_node = self._create_ast_node("IDENTIFIER", "x")
        mock_parse_and.return_value = left_node
        
        # 模拟当前 token 不是 OR
        mock_is_or.return_value = False
        
        parser_state = self._create_parser_state([self._create_token("IDENTIFIER", "x")])
        
        result = _parse_or(parser_state)
        
        # 应该直接返回 _parse_and 的结果
        self.assertEqual(result, left_node)
        mock_parse_and.assert_called_once_with(parser_state)
        mock_is_or.assert_called_once()
        mock_consume.assert_not_called()
        mock_build.assert_not_called()

    @patch('_parse_or_package._parse_or_src._parse_and')
    @patch('_parse_or_package._parse_or_src._current_token_is_or')
    @patch('_parse_or_package._parse_or_src._consume_token')
    @patch('_parse_or_package._parse_or_src._build_binary_op_node')
    def test_single_or_expression(self, mock_build, mock_consume, mock_is_or, mock_parse_and):
        """测试：单个 || 表达式 (a || b)"""
        # 第一次调用 _parse_and 返回左操作数
        left_node = self._create_ast_node("IDENTIFIER", "a")
        # 第二次调用 _parse_and（通过递归 _parse_or）返回右操作数
        right_node = self._create_ast_node("IDENTIFIER", "b")
        
        # 模拟 _parse_or 递归调用
        def parse_and_side_effect(state):
            if state.get("pos", 0) == 0:
                return left_node
            else:
                return right_node
        
        mock_parse_and.side_effect = parse_and_side_effect
        
        # 模拟 _current_token_is_or：第一次 True，第二次 False
        is_or_results = [True, False]
        mock_is_or.side_effect = is_or_results
        
        # 模拟 _consume_token 返回 OR token
        or_token = self._create_token("OR", "||", 1, 3)
        mock_consume.return_value = or_token
        
        # 模拟 _build_binary_op_node
        binary_node = self._create_ast_node("BINARY_OP", "||", [left_node, right_node], 1, 3)
        mock_build.return_value = binary_node
        
        parser_state = self._create_parser_state([
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OR", "||", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 6)
        ])
        
        result = _parse_or(parser_state)
        
        self.assertEqual(result, binary_node)
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "||")
        
        # _parse_and 应该被调用两次（左右操作数）
        self.assertEqual(mock_parse_and.call_count, 2)
        # _current_token_is_or 应该被调用两次
        self.assertEqual(mock_is_or.call_count, 2)
        # _consume_token 应该被调用一次
        mock_consume.assert_called_once()
        # _build_binary_op_node 应该被调用一次
        mock_build.assert_called_once()

    @patch('_parse_or_package._parse_or_src._parse_and')
    @patch('_parse_or_package._parse_or_src._current_token_is_or')
    @patch('_parse_or_package._parse_or_src._consume_token')
    @patch('_parse_or_package._parse_or_src._build_binary_op_node')
    def test_multiple_or_left_associative(self, mock_build, mock_consume, mock_is_or, mock_parse_and):
        """测试：多个 || 运算符，验证左结合性 (a || b || c)"""
        # 创建操作数节点
        node_a = self._create_ast_node("IDENTIFIER", "a")
        node_b = self._create_ast_node("IDENTIFIER", "b")
        node_c = self._create_ast_node("IDENTIFIER", "c")
        
        # 模拟 _parse_and 返回不同节点
        parse_and_calls = [0]
        def parse_and_side_effect(state):
            call_idx = parse_and_calls[0]
            parse_and_calls[0] += 1
            if call_idx == 0:
                return node_a
            elif call_idx == 1:
                return node_b
            else:
                return node_c
        
        mock_parse_and.side_effect = parse_and_side_effect
        
        # 模拟 _current_token_is_or：前两次 True，最后一次 False
        mock_is_or.side_effect = [True, True, False]
        
        # 模拟 _consume_token 返回 OR tokens
        or_token1 = self._create_token("OR", "||", 1, 3)
        or_token2 = self._create_token("OR", "||", 1, 7)
        mock_consume.side_effect = [or_token1, or_token2]
        
        # 模拟 _build_binary_op_node 返回中间结果和最终结果
        build_calls = [0]
        def build_side_effect(left, right, token):
            call_idx = build_calls[0]
            build_calls[0] += 1
            if call_idx == 0:
                # 第一次构建：(a || b)
                return self._create_ast_node("BINARY_OP", "||", [left, right], token["line"], token["column"])
            else:
                # 第二次构建：((a || b) || c)
                return self._create_ast_node("BINARY_OP", "||", [left, right], token["line"], token["column"])
        
        mock_build.side_effect = build_side_effect
        
        parser_state = self._create_parser_state([
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OR", "||", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 6),
            self._create_token("OR", "||", 1, 8),
            self._create_token("IDENTIFIER", "c", 1, 11)
        ])
        
        result = _parse_or(parser_state)
        
        # 验证左结合性：((a || b) || c)
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "||")
        
        # _parse_and 应该被调用三次
        self.assertEqual(mock_parse_and.call_count, 3)
        # _current_token_is_or 应该被调用三次
        self.assertEqual(mock_is_or.call_count, 3)
        # _consume_token 应该被调用两次
        self.assertEqual(mock_consume.call_count, 2)
        # _build_binary_op_node 应该被调用两次
        self.assertEqual(mock_build.call_count, 2)

    # ==================== 边界值测试 ====================

    @patch('_parse_or_package._parse_or_src._parse_and')
    @patch('_parse_or_package._parse_or_src._current_token_is_or')
    def test_empty_tokens(self, mock_is_or, mock_parse_and):
        """测试：空 tokens 列表"""
        mock_parse_and.return_value = self._create_ast_node("EMPTY")
        mock_is_or.return_value = False
        
        parser_state = self._create_parser_state([], pos=0)
        
        result = _parse_or(parser_state)
        
        self.assertIsNotNone(result)
        mock_parse_and.assert_called_once()

    @patch('_parse_or_package._parse_or_src._parse_and')
    @patch('_parse_or_package._parse_or_src._current_token_is_or')
    def test_pos_at_end(self, mock_is_or, mock_parse_and):
        """测试：pos 在 tokens 末尾"""
        mock_parse_and.return_value = self._create_ast_node("IDENTIFIER", "x")
        mock_is_or.return_value = False
        
        tokens = [self._create_token("IDENTIFIER", "x")]
        parser_state = self._create_parser_state(tokens, pos=1)  # pos 超出范围
        
        result = _parse_or(parser_state)
        
        self.assertIsNotNone(result)

    @patch('_parse_or_package._parse_or_src._parse_and')
    @patch('_parse_or_package._parse_or_src._current_token_is_or')
    @patch('_parse_or_package._parse_or_src._consume_token')
    @patch('_parse_or_package._parse_or_src._build_binary_op_node')
    def test_missing_line_column_info(self, mock_build, mock_consume, mock_is_or, mock_parse_and):
        """测试：token 缺少 line/column 信息时的容错"""
        mock_parse_and.return_value = self._create_ast_node("IDENTIFIER", "a")
        mock_is_or.side_effect = [True, False]
        
        # OR token 缺少 line/column
        or_token = {"type": "OR", "value": "||"}
        mock_consume.return_value = or_token
        
        def build_with_defaults(left, right, token):
            return {
                "type": "BINARY_OP",
                "children": [left, right],
                "value": "||",
                "line": token.get("line", 0),
                "column": token.get("column", 0)
            }
        
        mock_build.side_effect = build_with_defaults
        
        parser_state = self._create_parser_state([
            self._create_token("IDENTIFIER", "a"),
            {"type": "OR", "value": "||"},
            self._create_token("IDENTIFIER", "b")
        ])
        
        result = _parse_or(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["line"], 0)  # 默认值
        self.assertEqual(result["column"], 0)  # 默认值

    # ==================== 辅助函数测试 ====================

    def test_current_token_is_or_true(self):
        """测试：_current_token_is_or 返回 True"""
        parser_state = self._create_parser_state([
            self._create_token("OR", "||", 1, 1)
        ], pos=0)
        
        result = _current_token_is_or(parser_state)
        
        self.assertTrue(result)

    def test_current_token_is_or_false_different_type(self):
        """测试：_current_token_is_or 返回 False（不同类型）"""
        parser_state = self._create_parser_state([
            self._create_token("AND", "&&", 1, 1)
        ], pos=0)
        
        result = _current_token_is_or(parser_state)
        
        self.assertFalse(result)

    def test_current_token_is_or_false_pos_out_of_range(self):
        """测试：_current_token_is_or 返回 False（pos 超出范围）"""
        parser_state = self._create_parser_state([
            self._create_token("IDENTIFIER", "x", 1, 1)
        ], pos=5)
        
        result = _current_token_is_or(parser_state)
        
        self.assertFalse(result)

    def test_current_token_is_or_false_empty_tokens(self):
        """测试：_current_token_is_or 返回 False（空 tokens）"""
        parser_state = self._create_parser_state([], pos=0)
        
        result = _current_token_is_or(parser_state)
        
        self.assertFalse(result)

    def test_build_binary_op_node(self):
        """测试：_build_binary_op_node 构建正确的 AST 节点"""
        left = self._create_ast_node("IDENTIFIER", "a", line=1, column=1)
        right = self._create_ast_node("IDENTIFIER", "b", line=1, column=5)
        or_token = self._create_token("OR", "||", 1, 3)
        
        result = _build_binary_op_node(left, right, or_token)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "||")
        self.assertEqual(result["children"], [left, right])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)

    def test_build_binary_op_node_missing_token_info(self):
        """测试：_build_binary_op_node 处理缺少信息的 token"""
        left = self._create_ast_node("IDENTIFIER", "a")
        right = self._create_ast_node("IDENTIFIER", "b")
        or_token = {"type": "OR", "value": "||"}  # 缺少 line/column
        
        result = _build_binary_op_node(left, right, or_token)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "||")
        self.assertEqual(result["children"], [left, right])
        self.assertEqual(result["line"], 0)  # 默认值
        self.assertEqual(result["column"], 0)  # 默认值

    # ==================== 异常和错误处理测试 ====================

    @patch('_parse_or_package._parse_or_src._parse_and')
    def test_parse_and_raises_exception(self, mock_parse_and):
        """测试：_parse_and 抛出异常时的传播"""
        mock_parse_and.side_effect = ValueError("Parse error in _parse_and")
        
        parser_state = self._create_parser_state([self._create_token("IDENTIFIER", "x")])
        
        with self.assertRaises(ValueError) as context:
            _parse_or(parser_state)
        
        self.assertIn("Parse error in _parse_and", str(context.exception))

    @patch('_parse_or_package._parse_or_src._parse_and')
    @patch('_parse_or_package._parse_or_src._current_token_is_or')
    @patch('_parse_or_package._parse_or_src._consume_token')
    def test_consume_token_raises_exception(self, mock_consume, mock_is_or, mock_parse_and):
        """测试：_consume_token 抛出异常时的传播"""
        mock_parse_and.return_value = self._create_ast_node("IDENTIFIER", "a")
        mock_is_or.return_value = True
        mock_consume.side_effect = RuntimeError("Failed to consume OR token")
        
        parser_state = self._create_parser_state([
            self._create_token("IDENTIFIER", "a"),
            self._create_token("OR", "||")
        ])
        
        with self.assertRaises(RuntimeError) as context:
            _parse_or(parser_state)
        
        self.assertIn("Failed to consume OR token", str(context.exception))

    @patch('_parse_or_package._parse_or_src._parse_and')
    @patch('_parse_or_package._parse_or_src._current_token_is_or')
    @patch('_parse_or_package._parse_or_src._consume_token')
    @patch('_parse_or_package._parse_or_src._build_binary_op_node')
    def test_build_binary_op_node_raises_exception(self, mock_build, mock_consume, mock_is_or, mock_parse_and):
        """测试：_build_binary_op_node 抛出异常时的传播"""
        mock_parse_and.return_value = self._create_ast_node("IDENTIFIER", "a")
        mock_is_or.return_value = True
        mock_consume.return_value = self._create_token("OR", "||")
        mock_build.side_effect = TypeError("Invalid AST node")
        
        parser_state = self._create_parser_state([
            self._create_token("IDENTIFIER", "a"),
            self._create_token("OR", "||"),
            self._create_token("IDENTIFIER", "b")
        ])
        
        with self.assertRaises(TypeError) as context:
            _parse_or(parser_state)
        
        self.assertIn("Invalid AST node", str(context.exception))

    # ==================== 状态变化测试 ====================

    @patch('_parse_or_package._parse_or_src._parse_and')
    @patch('_parse_or_package._parse_or_src._current_token_is_or')
    @patch('_parse_or_package._parse_or_src._consume_token')
    @patch('_parse_or_package._parse_or_src._build_binary_op_node')
    def test_parser_state_pos_updates(self, mock_build, mock_consume, mock_is_or, mock_parse_and):
        """测试：parser_state 的 pos 在消费 token 后更新"""
        mock_parse_and.return_value = self._create_ast_node("IDENTIFIER", "a")
        mock_is_or.side_effect = [True, False]
        
        or_token = self._create_token("OR", "||", 1, 3)
        mock_consume.return_value = or_token
        mock_build.return_value = self._create_ast_node("BINARY_OP", "||", [], 1, 3)
        
        parser_state = self._create_parser_state([
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OR", "||", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 6)
        ], pos=0)
        
        _parse_or(parser_state)
        
        # 验证 _consume_token 被调用（它会更新 pos）
        mock_consume.assert_called_once()
        # 验证 _consume_token 被正确调用
        mock_consume.assert_called_with(parser_state, "OR")


class TestParseOrIntegration(unittest.TestCase):
    """_parse_or 函数的集成测试（使用真实的辅助函数）"""

    def _create_parser_state(self, tokens: List[Dict[str, Any]], pos: int = 0, filename: str = "test.c") -> Dict[str, Any]:
        """辅助函数：创建 parser_state 字典"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """辅助函数：创建 token 字典"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    @patch('_parse_or_package._parse_or_src._parse_and')
    @patch('_parse_or_package._parse_or_src._consume_token')
    def test_integration_with_real_helpers(self, mock_consume, mock_parse_and):
        """集成测试：使用真实的 _current_token_is_or 和 _build_binary_op_node"""
        # 模拟 _parse_and 返回简单节点
        node_a = {"type": "IDENTIFIER", "value": "a", "children": [], "line": 1, "column": 1}
        node_b = {"type": "IDENTIFIER", "value": "b", "children": [], "line": 1, "column": 5}
        
        call_count = [0]
        def parse_and_side_effect(state):
            call_count[0] += 1
            if call_count[0] == 1:
                return node_a
            else:
                return node_b
        
        mock_parse_and.side_effect = parse_and_side_effect
        
        or_token = self._create_token("OR", "||", 1, 3)
        mock_consume.return_value = or_token
        
        parser_state = self._create_parser_state([
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OR", "||", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5)
        ])
        
        result = _parse_or(parser_state)
        
        # 验证使用了真实的辅助函数
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "||")
        self.assertEqual(len(result["children"]), 2)


if __name__ == "__main__":
    unittest.main()