# === std / third-party imports ===
import unittest
from unittest.mock import patch, MagicMock
from typing import Dict, Any

# === relative imports ===
from ._parse_or_src import _parse_or


class TestParseOr(unittest.TestCase):
    """单元测试：_parse_or 函数"""

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "<test>") -> Dict[str, Any]:
        """辅助函数：创建 parser_state"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def _create_token(self, token_type: str, value: str = "", line: int = 1, column: int = 1) -> Dict[str, Any]:
        """辅助函数：创建 token"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_ast_node(self, node_type: str, **kwargs) -> Dict[str, Any]:
        """辅助函数：创建 AST 节点"""
        node = {"type": node_type}
        node.update(kwargs)
        return node

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_or_package._parse_and_package._parse_and_src._parse_and")
    def test_simple_or_expression(self, mock_parse_and: MagicMock):
        """测试：简单的 a or b 表达式"""
        # 准备：tokens = [IDENT(a), OR, IDENT(b)]
        tokens = [
            self._create_token("IDENT", "a", 1, 1),
            self._create_token("OR", "or", 1, 3),
            self._create_token("IDENT", "b", 1, 6)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Mock _parse_and 的返回值
        left_node = self._create_ast_node("IDENT", value="a", line=1, column=1)
        right_node = self._create_ast_node("IDENT", value="b", line=1, column=6)
        
        # 第一次调用返回 left，第二次调用返回 right
        mock_parse_and.side_effect = [left_node, right_node]
        
        # 执行
        result = _parse_or(parser_state)
        
        # 验证
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "or")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0], left_node)
        self.assertEqual(result["children"][1], right_node)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)
        
        # 验证 _parse_and 被调用了 2 次
        self.assertEqual(mock_parse_and.call_count, 2)
        
        # 验证 pos 被更新到 tokens 末尾
        self.assertEqual(parser_state["pos"], 3)

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_or_package._parse_and_package._parse_and_src._parse_and")
    def test_left_associative_or(self, mock_parse_and: MagicMock):
        """测试：左结合的 a or b or c 表达式"""
        # 准备：tokens = [IDENT(a), OR, IDENT(b), OR, IDENT(c)]
        tokens = [
            self._create_token("IDENT", "a", 1, 1),
            self._create_token("OR", "or", 1, 3),
            self._create_token("IDENT", "b", 1, 6),
            self._create_token("OR", "or", 1, 9),
            self._create_token("IDENT", "c", 1, 12)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Mock _parse_and 的返回值
        node_a = self._create_ast_node("IDENT", value="a", line=1, column=1)
        node_b = self._create_ast_node("IDENT", value="b", line=1, column=6)
        node_c = self._create_ast_node("IDENT", value="c", line=1, column=12)
        
        # 三次调用分别返回 a, b, c
        mock_parse_and.side_effect = [node_a, node_b, node_c]
        
        # 执行
        result = _parse_or(parser_state)
        
        # 验证：应该是 (a or b) or c 的左结合结构
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "or")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 9)  # 第二个 OR 的位置
        
        # 左子节点应该是 (a or b)
        left_child = result["children"][0]
        self.assertEqual(left_child["type"], "BINARY_OP")
        self.assertEqual(left_child["operator"], "or")
        self.assertEqual(left_child["line"], 1)
        self.assertEqual(left_child["column"], 3)  # 第一个 OR 的位置
        self.assertEqual(left_child["children"][0], node_a)
        self.assertEqual(left_child["children"][1], node_b)
        
        # 右子节点应该是 c
        right_child = result["children"][1]
        self.assertEqual(right_child, node_c)
        
        # 验证 _parse_and 被调用了 3 次
        self.assertEqual(mock_parse_and.call_count, 3)
        
        # 验证 pos 被更新到 tokens 末尾
        self.assertEqual(parser_state["pos"], 5)

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_or_package._parse_and_package._parse_and_src._parse_and")
    def test_no_or_operator(self, mock_parse_and: MagicMock):
        """测试：没有 OR 运算符，直接返回 _parse_and 的结果"""
        # 准备：tokens = [IDENT(a)]
        tokens = [
            self._create_token("IDENT", "a", 1, 1)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Mock _parse_and 的返回值
        node_a = self._create_ast_node("IDENT", value="a", line=1, column=1)
        mock_parse_and.return_value = node_a
        
        # 执行
        result = _parse_or(parser_state)
        
        # 验证：直接返回 _parse_and 的结果
        self.assertEqual(result, node_a)
        
        # 验证 _parse_and 只被调用了 1 次
        self.assertEqual(mock_parse_and.call_count, 1)
        
        # 验证 pos 没有被更新（因为没有消费 OR token）
        self.assertEqual(parser_state["pos"], 0)

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_or_package._parse_and_package._parse_and_src._parse_and")
    def test_empty_tokens(self, mock_parse_and: MagicMock):
        """测试：空 tokens 列表"""
        # 准备：空 tokens
        tokens = []
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Mock _parse_and 的返回值（应该处理空情况）
        mock_parse_and.return_value = self._create_ast_node("EMPTY")
        
        # 执行
        result = _parse_or(parser_state)
        
        # 验证：返回 _parse_and 的结果
        self.assertEqual(result["type"], "EMPTY")
        
        # 验证 _parse_and 被调用了 1 次
        self.assertEqual(mock_parse_and.call_count, 1)

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_or_package._parse_and_package._parse_and_src._parse_and")
    def test_or_at_end_without_right_operand(self, mock_parse_and: MagicMock):
        """测试：OR 在末尾，_parse_and 处理后续（可能返回错误或空）"""
        # 准备：tokens = [IDENT(a), OR]
        tokens = [
            self._create_token("IDENT", "a", 1, 1),
            self._create_token("OR", "or", 1, 3)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Mock _parse_and 的返回值
        node_a = self._create_ast_node("IDENT", value="a", line=1, column=1)
        # 当 pos 在末尾时，_parse_and 可能返回某种节点或抛出异常
        # 这里假设它返回一个节点
        node_empty = self._create_ast_node("EMPTY")
        
        mock_parse_and.side_effect = [node_a, node_empty]
        
        # 执行
        result = _parse_or(parser_state)
        
        # 验证：构建了 BINARY_OP，即使右操作数是 EMPTY
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "or")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0], node_a)
        self.assertEqual(result["children"][1], node_empty)
        
        # 验证 _parse_and 被调用了 2 次
        self.assertEqual(mock_parse_and.call_count, 2)

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_or_package._parse_and_package._parse_and_src._parse_and")
    def test_position_at_end(self, mock_parse_and: MagicMock):
        """测试：初始 pos 已经在 tokens 末尾"""
        # 准备：tokens = [IDENT(a)]，但 pos=1（已经在末尾）
        tokens = [
            self._create_token("IDENT", "a", 1, 1)
        ]
        parser_state = self._create_parser_state(tokens, pos=1)
        
        # Mock _parse_and 的返回值
        node_a = self._create_ast_node("IDENT", value="a", line=1, column=1)
        mock_parse_and.return_value = node_a
        
        # 执行
        result = _parse_or(parser_state)
        
        # 验证：返回 _parse_and 的结果
        self.assertEqual(result, node_a)
        
        # 验证 _parse_and 被调用了 1 次
        self.assertEqual(mock_parse_and.call_count, 1)

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_or_package._parse_and_package._parse_and_src._parse_and")
    def test_token_without_line_column(self, mock_parse_and: MagicMock):
        """测试：OR token 没有 line/column 字段（使用默认值 0）"""
        # 准备：OR token 没有 line/column
        tokens = [
            self._create_token("IDENT", "a", 1, 1),
            {"type": "OR", "value": "or"},  # 没有 line/column
            self._create_token("IDENT", "b", 1, 6)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Mock _parse_and 的返回值
        node_a = self._create_ast_node("IDENT", value="a", line=1, column=1)
        node_b = self._create_ast_node("IDENT", value="b", line=1, column=6)
        mock_parse_and.side_effect = [node_a, node_b]
        
        # 执行
        result = _parse_or(parser_state)
        
        # 验证：line/column 默认为 0
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "or")
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_or_package._parse_and_package._parse_and_src._parse_and")
    def test_filename_in_parser_state(self, mock_parse_and: MagicMock):
        """测试：parser_state 包含 filename 字段"""
        # 准备：带 filename 的 parser_state
        tokens = [
            self._create_token("IDENT", "a", 1, 1),
            self._create_token("OR", "or", 1, 3),
            self._create_token("IDENT", "b", 1, 6)
        ]
        parser_state = self._create_parser_state(tokens, pos=0, filename="test.py")
        
        # Mock _parse_and 的返回值
        node_a = self._create_ast_node("IDENT", value="a", line=1, column=1)
        node_b = self._create_ast_node("IDENT", value="b", line=1, column=6)
        mock_parse_and.side_effect = [node_a, node_b]
        
        # 执行
        result = _parse_or(parser_state)
        
        # 验证：函数正常执行（filename 主要用于错误报告，不影响 AST 构建）
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "or")


if __name__ == "__main__":
    unittest.main()
