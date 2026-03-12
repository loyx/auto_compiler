# === std / third-party imports ===
import unittest
from unittest.mock import patch, MagicMock
from typing import Dict, Any

# === relative imports ===
from _traverse_node_package._traverse_node_src import _traverse_node

# === type aliases ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestTraverseNode(unittest.TestCase):
    """单元测试 _traverse_node 函数的节点分发逻辑。"""

    def setUp(self) -> None:
        """每个测试前初始化通用的 symbol_table 结构。"""
        self.symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

    def _create_mock_handlers(self):
        """创建所有 7 个 handler 的 mock 对象。"""
        mocks = {}
        for handler_name in [
            "_handle_block",
            "_handle_function_def",
            "_handle_variable_decl",
            "_handle_assignment",
            "_handle_if_statement",
            "_handle_while_loop",
            "_handle_return_statement"
        ]:
            mocks[handler_name] = MagicMock()
        return mocks

    # === Happy Path Tests: 每个节点类型正确分发 ===

    @patch("_traverse_node_package._traverse_node_src._handle_block")
    def test_traverse_block_node(self, mock_handle_block: MagicMock) -> None:
        """测试 block 类型节点正确分发到 _handle_block。"""
        node: AST = {
            "type": "block",
            "children": [],
            "line": 1,
            "column": 1
        }
        _traverse_node(node, self.symbol_table)
        mock_handle_block.assert_called_once_with(node, self.symbol_table)

    @patch("_traverse_node_package._traverse_node_src._handle_function_def")
    def test_traverse_function_def_node(self, mock_handle_function_def: MagicMock) -> None:
        """测试 function_def 类型节点正确分发到 _handle_function_def。"""
        node: AST = {
            "type": "function_def",
            "name": "main",
            "return_type": "int",
            "params": [],
            "line": 1,
            "column": 1
        }
        _traverse_node(node, self.symbol_table)
        mock_handle_function_def.assert_called_once_with(node, self.symbol_table)

    @patch("_traverse_node_package._traverse_node_src._handle_variable_decl")
    def test_traverse_variable_decl_node(self, mock_handle_variable_decl: MagicMock) -> None:
        """测试 variable_decl 类型节点正确分发到 _handle_variable_decl。"""
        node: AST = {
            "type": "variable_decl",
            "name": "x",
            "data_type": "int",
            "line": 1,
            "column": 1
        }
        _traverse_node(node, self.symbol_table)
        mock_handle_variable_decl.assert_called_once_with(node, self.symbol_table)

    @patch("_traverse_node_package._traverse_node_src._handle_assignment")
    def test_traverse_assignment_node(self, mock_handle_assignment: MagicMock) -> None:
        """测试 assignment 类型节点正确分发到 _handle_assignment。"""
        node: AST = {
            "type": "assignment",
            "target": "x",
            "value": {"type": "literal", "value": 10},
            "line": 1,
            "column": 1
        }
        _traverse_node(node, self.symbol_table)
        mock_handle_assignment.assert_called_once_with(node, self.symbol_table)

    @patch("_traverse_node_package._traverse_node_src._handle_if_statement")
    def test_traverse_if_statement_node(self, mock_handle_if_statement: MagicMock) -> None:
        """测试 if_statement 类型节点正确分发到 _handle_if_statement。"""
        node: AST = {
            "type": "if_statement",
            "condition": {"type": "binary_op", "op": ">", "left": "x", "right": 0},
            "then_branch": [],
            "else_branch": [],
            "line": 1,
            "column": 1
        }
        _traverse_node(node, self.symbol_table)
        mock_handle_if_statement.assert_called_once_with(node, self.symbol_table)

    @patch("_traverse_node_package._traverse_node_src._handle_while_loop")
    def test_traverse_while_loop_node(self, mock_handle_while_loop: MagicMock) -> None:
        """测试 while_loop 类型节点正确分发到 _handle_while_loop。"""
        node: AST = {
            "type": "while_loop",
            "condition": {"type": "binary_op", "op": "<", "left": "i", "right": 10},
            "body": [],
            "line": 1,
            "column": 1
        }
        _traverse_node(node, self.symbol_table)
        mock_handle_while_loop.assert_called_once_with(node, self.symbol_table)

    @patch("_traverse_node_package._traverse_node_src._handle_return_statement")
    def test_traverse_return_statement_node(self, mock_handle_return_statement: MagicMock) -> None:
        """测试 return_statement 类型节点正确分发到 _handle_return_statement。"""
        node: AST = {
            "type": "return_statement",
            "value": {"type": "literal", "value": 0},
            "line": 1,
            "column": 1
        }
        _traverse_node(node, self.symbol_table)
        mock_handle_return_statement.assert_called_once_with(node, self.symbol_table)

    # === Edge Case Tests: 边界值和异常情况 ===

    @patch("_traverse_node_package._traverse_node_src._handle_block")
    @patch("_traverse_node_package._traverse_node_src._handle_function_def")
    @patch("_traverse_node_package._traverse_node_src._handle_variable_decl")
    @patch("_traverse_node_package._traverse_node_src._handle_assignment")
    @patch("_traverse_node_package._traverse_node_src._handle_if_statement")
    @patch("_traverse_node_package._traverse_node_src._handle_while_loop")
    @patch("_traverse_node_package._traverse_node_src._handle_return_statement")
    def test_traverse_unknown_node_type(
        self,
        mock_handle_return_statement: MagicMock,
        mock_handle_while_loop: MagicMock,
        mock_handle_if_statement: MagicMock,
        mock_handle_assignment: MagicMock,
        mock_handle_variable_decl: MagicMock,
        mock_handle_function_def: MagicMock,
        mock_handle_block: MagicMock
    ) -> None:
        """测试未知节点类型静默跳过，不调用任何 handler。"""
        node: AST = {
            "type": "unknown_type",
            "line": 1,
            "column": 1
        }
        _traverse_node(node, self.symbol_table)
        # 所有 handler 都不应被调用
        mock_handle_block.assert_not_called()
        mock_handle_function_def.assert_not_called()
        mock_handle_variable_decl.assert_not_called()
        mock_handle_assignment.assert_not_called()
        mock_handle_if_statement.assert_not_called()
        mock_handle_while_loop.assert_not_called()
        mock_handle_return_statement.assert_not_called()

    @patch("_traverse_node_package._traverse_node_src._handle_block")
    @patch("_traverse_node_package._traverse_node_src._handle_function_def")
    @patch("_traverse_node_package._traverse_node_src._handle_variable_decl")
    @patch("_traverse_node_package._traverse_node_src._handle_assignment")
    @patch("_traverse_node_package._traverse_node_src._handle_if_statement")
    @patch("_traverse_node_package._traverse_node_src._handle_while_loop")
    @patch("_traverse_node_package._traverse_node_src._handle_return_statement")
    def test_traverse_node_missing_type_field(
        self,
        mock_handle_return_statement: MagicMock,
        mock_handle_while_loop: MagicMock,
        mock_handle_if_statement: MagicMock,
        mock_handle_assignment: MagicMock,
        mock_handle_variable_decl: MagicMock,
        mock_handle_function_def: MagicMock,
        mock_handle_block: MagicMock
    ) -> None:
        """测试节点缺少 type 字段时静默处理（默认空字符串）。"""
        node: AST = {
            "children": [],
            "line": 1,
            "column": 1
        }
        _traverse_node(node, self.symbol_table)
        # 所有 handler 都不应被调用
        mock_handle_block.assert_not_called()
        mock_handle_function_def.assert_not_called()
        mock_handle_variable_decl.assert_not_called()
        mock_handle_assignment.assert_not_called()
        mock_handle_if_statement.assert_not_called()
        mock_handle_while_loop.assert_not_called()
        mock_handle_return_statement.assert_not_called()

    @patch("_traverse_node_package._traverse_node_src._handle_block")
    @patch("_traverse_node_package._traverse_node_src._handle_function_def")
    @patch("_traverse_node_package._traverse_node_src._handle_variable_decl")
    @patch("_traverse_node_package._traverse_node_src._handle_assignment")
    @patch("_traverse_node_package._traverse_node_src._handle_if_statement")
    @patch("_traverse_node_package._traverse_node_src._handle_while_loop")
    @patch("_traverse_node_package._traverse_node_src._handle_return_statement")
    def test_traverse_empty_node(
        self,
        mock_handle_return_statement: MagicMock,
        mock_handle_while_loop: MagicMock,
        mock_handle_if_statement: MagicMock,
        mock_handle_assignment: MagicMock,
        mock_handle_variable_decl: MagicMock,
        mock_handle_function_def: MagicMock,
        mock_handle_block: MagicMock
    ) -> None:
        """测试空节点字典静默处理。"""
        node: AST = {}
        _traverse_node(node, self.symbol_table)
        # 所有 handler 都不应被调用
        mock_handle_block.assert_not_called()
        mock_handle_function_def.assert_not_called()
        mock_handle_variable_decl.assert_not_called()
        mock_handle_assignment.assert_not_called()
        mock_handle_if_statement.assert_not_called()
        mock_handle_while_loop.assert_not_called()
        mock_handle_return_statement.assert_not_called()

    @patch("_traverse_node_package._traverse_node_src._handle_block")
    @patch("_traverse_node_package._traverse_node_src._handle_function_def")
    @patch("_traverse_node_package._traverse_node_src._handle_variable_decl")
    @patch("_traverse_node_package._traverse_node_src._handle_assignment")
    @patch("_traverse_node_package._traverse_node_src._handle_if_statement")
    @patch("_traverse_node_package._traverse_node_src._handle_while_loop")
    @patch("_traverse_node_package._traverse_node_src._handle_return_statement")
    def test_traverse_node_with_empty_symbol_table(
        self,
        mock_handle_return_statement: MagicMock,
        mock_handle_while_loop: MagicMock,
        mock_handle_if_statement: MagicMock,
        mock_handle_assignment: MagicMock,
        mock_handle_variable_decl: MagicMock,
        mock_handle_function_def: MagicMock,
        mock_handle_block: MagicMock
    ) -> None:
        """测试使用最小 symbol_table 结构时仍能正确分发。"""
        minimal_symbol_table: SymbolTable = {}
        node: AST = {
            "type": "block",
            "children": []
        }
        _traverse_node(node, minimal_symbol_table)
        mock_handle_block.assert_called_once_with(node, minimal_symbol_table)

    @patch("_traverse_node_package._traverse_node_src._handle_block")
    def test_traverse_node_preserves_symbol_table_reference(
        self,
        mock_handle_block: MagicMock
    ) -> None:
        """测试 symbol_table 作为引用传递给 handler（验证同一对象）。"""
        node: AST = {
            "type": "block",
            "children": []
        }
        _traverse_node(node, self.symbol_table)
        # 验证传递的是同一个对象引用
        called_symbol_table = mock_handle_block.call_args[0][1]
        self.assertIs(called_symbol_table, self.symbol_table)

    @patch("_traverse_node_package._traverse_node_src._handle_block")
    @patch("_traverse_node_package._traverse_node_src._handle_function_def")
    @patch("_traverse_node_package._traverse_node_src._handle_variable_decl")
    @patch("_traverse_node_package._traverse_node_src._handle_assignment")
    @patch("_traverse_node_package._traverse_node_src._handle_if_statement")
    @patch("_traverse_node_package._traverse_node_src._handle_while_loop")
    @patch("_traverse_node_package._traverse_node_src._handle_return_statement")
    def test_traverse_node_case_sensitive_type(
        self,
        mock_handle_return_statement: MagicMock,
        mock_handle_while_loop: MagicMock,
        mock_handle_if_statement: MagicMock,
        mock_handle_assignment: MagicMock,
        mock_handle_variable_decl: MagicMock,
        mock_handle_function_def: MagicMock,
        mock_handle_block: MagicMock
    ) -> None:
        """测试节点类型区分大小写（大写类型应被跳过）。"""
        node: AST = {
            "type": "BLOCK",  # 大写，应被跳过
            "children": []
        }
        _traverse_node(node, self.symbol_table)
        # 所有 handler 都不应被调用
        mock_handle_block.assert_not_called()
        mock_handle_function_def.assert_not_called()
        mock_handle_variable_decl.assert_not_called()
        mock_handle_assignment.assert_not_called()
        mock_handle_if_statement.assert_not_called()
        mock_handle_while_loop.assert_not_called()
        mock_handle_return_statement.assert_not_called()

    @patch("_traverse_node_package._traverse_node_src._handle_block")
    def test_traverse_node_with_complex_nested_structure(
        self,
        mock_handle_block: MagicMock
    ) -> None:
        """测试具有复杂嵌套结构的 block 节点仍能正确分发。"""
        node: AST = {
            "type": "block",
            "children": [
                {
                    "type": "variable_decl",
                    "name": "x",
                    "data_type": "int"
                },
                {
                    "type": "assignment",
                    "target": "x",
                    "value": {"type": "literal", "value": 10}
                },
                {
                    "type": "if_statement",
                    "condition": {"type": "binary_op"},
                    "then_branch": [],
                    "else_branch": []
                }
            ],
            "line": 1,
            "column": 1,
            "scope_level": 1
        }
        _traverse_node(node, self.symbol_table)
        mock_handle_block.assert_called_once_with(node, self.symbol_table)
        # 验证 node 对象完整传递
        called_node = mock_handle_block.call_args[0][0]
        self.assertEqual(called_node["type"], "block")
        self.assertEqual(len(called_node["children"]), 3)


if __name__ == "__main__":
    unittest.main()
