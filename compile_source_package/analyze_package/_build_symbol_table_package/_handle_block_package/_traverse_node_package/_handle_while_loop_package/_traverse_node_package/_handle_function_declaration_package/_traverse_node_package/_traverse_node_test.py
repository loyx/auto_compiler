# -*- coding: utf-8 -*-
"""单元测试文件：_traverse_node 函数的单元测试。"""

from unittest.mock import patch
from typing import Dict, Any

# 相对导入被测函数
from ._traverse_node_src import _traverse_node

# 类型别名，与源文件保持一致
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestTraverseNode:
    """_traverse_node 分发器函数的测试用例。"""

    def setup_method(self):
        """每个测试方法前的准备工作。"""
        self.symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

    def test_function_declaration_dispatch(self):
        """测试 function_declaration 类型节点正确分发到对应 handler。"""
        with patch("_handle_function_declaration_package._handle_function_declaration_src._handle_function_declaration") as mock_handler:
            node = {"type": "function_declaration", "name": "test_func", "params": [], "return_type": "int"}
            _traverse_node(node, self.symbol_table)
            mock_handler.assert_called_once_with(node, self.symbol_table)

    def test_variable_declaration_dispatch(self):
        """测试 variable_declaration 类型节点正确分发到对应 handler。"""
        with patch("_handle_variable_declaration_package._handle_variable_declaration_src._handle_variable_declaration") as mock_handler:
            node = {"type": "variable_declaration", "name": "x", "var_type": "int"}
            _traverse_node(node, self.symbol_table)
            mock_handler.assert_called_once_with(node, self.symbol_table)

    def test_assignment_dispatch(self):
        """测试 assignment 类型节点正确分发到对应 handler。"""
        with patch("_handle_assignment_package._handle_assignment_src._handle_assignment") as mock_handler:
            node = {"type": "assignment", "target": "x", "value": {"type": "literal", "value": 5}}
            _traverse_node(node, self.symbol_table)
            mock_handler.assert_called_once_with(node, self.symbol_table)

    def test_if_statement_dispatch(self):
        """测试 if_statement 类型节点正确分发到对应 handler。"""
        with patch("_handle_if_statement_package._handle_if_statement_src._handle_if_statement") as mock_handler:
            node = {
                "type": "if_statement",
                "condition": {"type": "binary_op", "op": ">", "left": {"type": "identifier", "name": "x"}, "right": {"type": "literal", "value": 0}},
                "then_branch": {"type": "block", "statements": []}
            }
            _traverse_node(node, self.symbol_table)
            mock_handler.assert_called_once_with(node, self.symbol_table)

    def test_if_statement_with_else_branch_dispatch(self):
        """测试带 else_branch 的 if_statement 节点正确分发。"""
        with patch("_handle_if_statement_package._handle_if_statement_src._handle_if_statement") as mock_handler:
            node = {
                "type": "if_statement",
                "condition": {"type": "literal", "value": True},
                "then_branch": {"type": "block", "statements": []},
                "else_branch": {"type": "block", "statements": []}
            }
            _traverse_node(node, self.symbol_table)
            mock_handler.assert_called_once_with(node, self.symbol_table)

    def test_while_loop_dispatch(self):
        """测试 while_loop 类型节点正确分发到对应 handler。"""
        with patch("_handle_while_loop_package._handle_while_loop_src._handle_while_loop") as mock_handler:
            node = {
                "type": "while_loop",
                "condition": {"type": "literal", "value": True},
                "body": {"type": "block", "statements": []}
            }
            _traverse_node(node, self.symbol_table)
            mock_handler.assert_called_once_with(node, self.symbol_table)

    def test_for_loop_dispatch(self):
        """测试 for_loop 类型节点正确分发到对应 handler。"""
        with patch("_handle_for_loop_package._handle_for_loop_src._handle_for_loop") as mock_handler:
            node = {
                "type": "for_loop",
                "iterator": "i",
                "iterable": {"type": "identifier", "name": "range"},
                "body": {"type": "block", "statements": []}
            }
            _traverse_node(node, self.symbol_table)
            mock_handler.assert_called_once_with(node, self.symbol_table)

    def test_return_statement_dispatch(self):
        """测试 return_statement 类型节点正确分发到对应 handler。"""
        with patch("_handle_return_statement_package._handle_return_statement_src._handle_return_statement") as mock_handler:
            node = {"type": "return_statement", "value": {"type": "literal", "value": 42}}
            _traverse_node(node, self.symbol_table)
            mock_handler.assert_called_once_with(node, self.symbol_table)

    def test_return_statement_without_value_dispatch(self):
        """测试无返回值的 return_statement 节点正确分发。"""
        with patch("_handle_return_statement_package._handle_return_statement_src._handle_return_statement") as mock_handler:
            node = {"type": "return_statement"}
            _traverse_node(node, self.symbol_table)
            mock_handler.assert_called_once_with(node, self.symbol_table)

    def test_expression_statement_dispatch(self):
        """测试 expression_statement 类型节点正确分发到对应 handler。"""
        with patch("_handle_expression_statement_package._handle_expression_statement_src._handle_expression_statement") as mock_handler:
            node = {"type": "expression_statement", "expression": {"type": "call", "function": "print", "args": []}}
            _traverse_node(node, self.symbol_table)
            mock_handler.assert_called_once_with(node, self.symbol_table)

    def test_block_type_iterates_statements(self):
        """测试 block 类型节点遍历 statements 列表并递归调用 _traverse_node。"""
        node = {
            "type": "block",
            "statements": [
                {"type": "variable_declaration", "name": "x", "var_type": "int"},
                {"type": "assignment", "target": "y", "value": {"type": "literal", "value": 5}},
                {"type": "return_statement", "value": {"type": "identifier", "name": "x"}}
            ]
        }

        with patch("_handle_variable_declaration_package._handle_variable_declaration_src._handle_variable_declaration") as mock_var:
            with patch("_handle_assignment_package._handle_assignment_src._handle_assignment") as mock_assign:
                with patch("_handle_return_statement_package._handle_return_statement_src._handle_return_statement") as mock_return:
                    _traverse_node(node, self.symbol_table)

                    assert mock_var.call_count == 1
                    assert mock_assign.call_count == 1
                    assert mock_return.call_count == 1

    def test_empty_block(self):
        """测试空 block 节点正确处理。"""
        node = {"type": "block", "statements": []}

        # 不应抛出异常
        _traverse_node(node, self.symbol_table)

        # 符号表应保持不变
        assert self.symbol_table == {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

    def test_block_without_statements_field(self):
        """测试缺少 statements 字段的 block 节点使用空列表默认值。"""
        node = {"type": "block"}

        # 不应抛出异常
        _traverse_node(node, self.symbol_table)

    def test_unknown_type_silently_skipped(self):
        """测试未知节点类型静默跳过，不抛出异常。"""
        node = {"type": "unknown_type", "data": "some_data"}

        # 不应抛出异常
        _traverse_node(node, self.symbol_table)

        # 符号表应保持不变
        assert self.symbol_table == {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

    def test_node_without_type_field(self):
        """测试缺少 type 字段的节点静默跳过。"""
        node = {"name": "test", "value": 5}

        # 不应抛出异常
        _traverse_node(node, self.symbol_table)

    def test_none_type_silently_skipped(self):
        """测试 type 为 None 的节点静默跳过。"""
        node = {"type": None, "data": "test"}

        # 不应抛出异常
        _traverse_node(node, self.symbol_table)

    def test_multiple_dispatches_in_sequence(self):
        """测试多个不同类型节点按顺序分发。"""
        nodes = [
            {"type": "function_declaration", "name": "func1", "params": [], "return_type": "void"},
            {"type": "variable_declaration", "name": "var1", "var_type": "int"},
            {"type": "assignment", "target": "var2", "value": {"type": "literal", "value": 10}},
            {"type": "expression_statement", "expression": {"type": "literal", "value": 42}}
        ]

        with patch("_handle_function_declaration_package._handle_function_declaration_src._handle_function_declaration") as mock_func:
            with patch("_handle_variable_declaration_package._handle_variable_declaration_src._handle_variable_declaration") as mock_var:
                with patch("_handle_assignment_package._handle_assignment_src._handle_assignment") as mock_assign:
                    with patch("_handle_expression_statement_package._handle_expression_statement_src._handle_expression_statement") as mock_expr:
                        for node in nodes:
                            _traverse_node(node, self.symbol_table)

                        mock_func.assert_called_once()
                        mock_var.assert_called_once()
                        mock_assign.assert_called_once()
                        mock_expr.assert_called_once()

    def test_nested_block_recursion(self):
        """测试嵌套 block 节点正确递归处理。"""
        node = {
            "type": "block",
            "statements": [
                {
                    "type": "block",
                    "statements": [
                        {"type": "variable_declaration", "name": "inner_var", "var_type": "string"}
                    ]
                },
                {"type": "assignment", "target": "outer_var", "value": {"type": "literal", "value": "test"}}
            ]
        }

        with patch("_handle_variable_declaration_package._handle_variable_declaration_src._handle_variable_declaration") as mock_var:
            with patch("_handle_assignment_package._handle_assignment_src._handle_assignment") as mock_assign:
                _traverse_node(node, self.symbol_table)

                # 内层变量声明和外层赋值都应被处理
                assert mock_var.call_count == 1
                assert mock_assign.call_count == 1

    def test_mixed_block_with_control_flow(self):
        """测试 block 中包含控制流语句的混合场景。"""
        node = {
            "type": "block",
            "statements": [
                {"type": "variable_declaration", "name": "i", "var_type": "int"},
                {
                    "type": "while_loop",
                    "condition": {"type": "binary_op", "op": "<", "left": {"type": "identifier", "name": "i"}, "right": {"type": "literal", "value": 10}},
                    "body": {
                        "type": "block",
                        "statements": [
                            {"type": "assignment", "target": "i", "value": {"type": "binary_op", "op": "+", "left": {"type": "identifier", "name": "i"}, "right": {"type": "literal", "value": 1}}}
                        ]
                    }
                },
                {"type": "return_statement", "value": {"type": "identifier", "name": "i"}}
            ]
        }

        with patch("_handle_variable_declaration_package._handle_variable_declaration_src._handle_variable_declaration") as mock_var:
            with patch("_handle_while_loop_package._handle_while_loop_src._handle_while_loop") as mock_while:
                with patch("_handle_assignment_package._handle_assignment_src._handle_assignment") as mock_assign:
                    with patch("_handle_return_statement_package._handle_return_statement_src._handle_return_statement") as mock_return:
                        _traverse_node(node, self.symbol_table)

                        assert mock_var.call_count == 1
                        assert mock_while.call_count == 1
                        assert mock_assign.call_count == 1
                        assert mock_return.call_count == 1

    def test_handler_receives_correct_symbol_table(self):
        """测试 handler 接收到正确的符号表引用。"""
        with patch("_handle_function_declaration_package._handle_function_declaration_src._handle_function_declaration") as mock_handler:
            node = {"type": "function_declaration", "name": "test"}
            _traverse_node(node, self.symbol_table)

            # 验证传递的是同一个符号表对象
            call_args = mock_handler.call_args
            assert call_args[0][1] is self.symbol_table

    def test_all_node_types_coverage(self):
        """测试所有已知节点类型都能被正确处理。"""
        test_cases = [
            ("function_declaration", {"type": "function_declaration", "name": "f", "params": [], "return_type": "int"}),
            ("variable_declaration", {"type": "variable_declaration", "name": "x", "var_type": "int"}),
            ("assignment", {"type": "assignment", "target": "x", "value": {"type": "literal", "value": 1}}),
            ("if_statement", {"type": "if_statement", "condition": {"type": "literal", "value": True}, "then_branch": {"type": "block", "statements": []}}),
            ("while_loop", {"type": "while_loop", "condition": {"type": "literal", "value": True}, "body": {"type": "block", "statements": []}}),
            ("for_loop", {"type": "for_loop", "iterator": "i", "iterable": {"type": "literal", "value": 10}, "body": {"type": "block", "statements": []}}),
            ("return_statement", {"type": "return_statement", "value": {"type": "literal", "value": 0}}),
            ("expression_statement", {"type": "expression_statement", "expression": {"type": "literal", "value": 42}}),
            ("block", {"type": "block", "statements": []}),
        ]

        for type_name, node in test_cases:
            # 不应抛出异常
            _traverse_node(node, self.symbol_table)
