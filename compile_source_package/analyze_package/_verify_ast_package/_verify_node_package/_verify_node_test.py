"""单元测试：_verify_node 函数"""
import unittest
from unittest.mock import patch

from ._verify_node_src import _verify_node
from . import _verify_node_src


class TestVerifyNode(unittest.TestCase):
    """测试 _verify_node 函数的节点分发逻辑"""

    def setUp(self):
        """设置测试夹具"""
        self.symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": []
        }
        self.context_stack = []
        self.filename = "test.c"

    @patch.object(_verify_node_src, "_verify_literal")
    def test_verify_int_literal(self, mock_verify_literal):
        """测试 int_literal 节点类型分发"""
        node = {"type": "int_literal", "value": 42}
        _verify_node(node, self.symbol_table, self.context_stack, self.filename)
        mock_verify_literal.assert_called_once_with(node, self.filename)

    @patch.object(_verify_node_src, "_verify_literal")
    def test_verify_char_literal(self, mock_verify_literal):
        """测试 char_literal 节点类型分发"""
        node = {"type": "char_literal", "value": "a"}
        _verify_node(node, self.symbol_table, self.context_stack, self.filename)
        mock_verify_literal.assert_called_once_with(node, self.filename)

    @patch.object(_verify_node_src, "_verify_variable_ref")
    def test_verify_variable_ref(self, mock_verify_variable_ref):
        """测试 variable_ref 节点类型分发"""
        node = {"type": "variable_ref", "name": "x"}
        _verify_node(node, self.symbol_table, self.context_stack, self.filename)
        mock_verify_variable_ref.assert_called_once_with(
            node, self.symbol_table, self.filename
        )

    @patch.object(_verify_node_src, "_verify_binary_op")
    def test_verify_binary_op(self, mock_verify_binary_op):
        """测试 binary_op 节点类型分发"""
        node = {"type": "binary_op", "left": {}, "right": {}, "operator": "+"}
        _verify_node(node, self.symbol_table, self.context_stack, self.filename)
        mock_verify_binary_op.assert_called_once_with(
            node, self.symbol_table, self.context_stack, self.filename
        )

    @patch.object(_verify_node_src, "_verify_assignment")
    def test_verify_assignment(self, mock_verify_assignment):
        """测试 assignment 节点类型分发"""
        node = {"type": "assignment", "left": {}, "right": {}}
        _verify_node(node, self.symbol_table, self.context_stack, self.filename)
        mock_verify_assignment.assert_called_once_with(
            node, self.symbol_table, self.context_stack, self.filename
        )

    @patch.object(_verify_node_src, "_verify_function_call")
    def test_verify_function_call(self, mock_verify_function_call):
        """测试 function_call 节点类型分发"""
        node = {"type": "function_call", "name": "foo", "args": []}
        _verify_node(node, self.symbol_table, self.context_stack, self.filename)
        mock_verify_function_call.assert_called_once_with(
            node, self.symbol_table, self.context_stack, self.filename
        )

    @patch.object(_verify_node_src, "_verify_return_stmt")
    def test_verify_return_stmt(self, mock_verify_return_stmt):
        """测试 return_stmt 节点类型分发"""
        node = {"type": "return_stmt", "value": None}
        _verify_node(node, self.symbol_table, self.context_stack, self.filename)
        mock_verify_return_stmt.assert_called_once_with(
            node, self.symbol_table, self.context_stack, self.filename
        )

    @patch.object(_verify_node_src, "_verify_control_flow_stmt")
    def test_verify_break_stmt(self, mock_verify_control_flow_stmt):
        """测试 break_stmt 节点类型分发"""
        node = {"type": "break_stmt"}
        _verify_node(node, self.symbol_table, self.context_stack, self.filename)
        mock_verify_control_flow_stmt.assert_called_once_with(
            node, self.context_stack, self.filename
        )

    @patch.object(_verify_node_src, "_verify_control_flow_stmt")
    def test_verify_continue_stmt(self, mock_verify_control_flow_stmt):
        """测试 continue_stmt 节点类型分发"""
        node = {"type": "continue_stmt"}
        _verify_node(node, self.symbol_table, self.context_stack, self.filename)
        mock_verify_control_flow_stmt.assert_called_once_with(
            node, self.context_stack, self.filename
        )

    @patch.object(_verify_node_src, "_verify_function_def")
    def test_verify_function_def(self, mock_verify_function_def):
        """测试 function_def 节点类型分发"""
        node = {"type": "function_def", "name": "foo", "body": {}}
        _verify_node(node, self.symbol_table, self.context_stack, self.filename)
        mock_verify_function_def.assert_called_once_with(
            node, self.symbol_table, self.context_stack, self.filename
        )

    @patch.object(_verify_node_src, "_verify_loop_stmt")
    def test_verify_while_stmt(self, mock_verify_loop_stmt):
        """测试 while_stmt 节点类型分发"""
        node = {"type": "while_stmt", "condition": {}, "body": {}}
        _verify_node(node, self.symbol_table, self.context_stack, self.filename)
        mock_verify_loop_stmt.assert_called_once_with(
            node, self.symbol_table, self.context_stack, self.filename
        )

    @patch.object(_verify_node_src, "_verify_loop_stmt")
    def test_verify_for_stmt(self, mock_verify_loop_stmt):
        """测试 for_stmt 节点类型分发"""
        node = {"type": "for_stmt", "init": {}, "condition": {}, "update": {}, "body": {}}
        _verify_node(node, self.symbol_table, self.context_stack, self.filename)
        mock_verify_loop_stmt.assert_called_once_with(
            node, self.symbol_table, self.context_stack, self.filename
        )

    @patch.object(_verify_node_src, "_verify_if_stmt")
    def test_verify_if_stmt(self, mock_verify_if_stmt):
        """测试 if_stmt 节点类型分发"""
        node = {"type": "if_stmt", "condition": {}, "then_branch": {}, "else_branch": {}}
        _verify_node(node, self.symbol_table, self.context_stack, self.filename)
        mock_verify_if_stmt.assert_called_once_with(
            node, self.symbol_table, self.context_stack, self.filename
        )

    @patch.object(_verify_node_src, "_verify_children")
    def test_verify_unknown_node_type(self, mock_verify_children):
        """测试未知节点类型，应回退到 _verify_children"""
        node = {"type": "unknown_type", "children": []}
        _verify_node(node, self.symbol_table, self.context_stack, self.filename)
        mock_verify_children.assert_called_once_with(
            node, self.symbol_table, self.context_stack, self.filename
        )

    @patch.object(_verify_node_src, "_verify_children")
    def test_verify_node_missing_type(self, mock_verify_children):
        """测试缺失 type 字段的节点，应回退到 _verify_children"""
        node = {"children": []}
        _verify_node(node, self.symbol_table, self.context_stack, self.filename)
        mock_verify_children.assert_called_once_with(
            node, self.symbol_table, self.context_stack, self.filename
        )

    @patch.object(_verify_node_src, "_verify_children")
    def test_verify_node_empty_type(self, mock_verify_children):
        """测试空 type 字段的节点，应回退到 _verify_children"""
        node = {"type": "", "children": []}
        _verify_node(node, self.symbol_table, self.context_stack, self.filename)
        mock_verify_children.assert_called_once_with(
            node, self.symbol_table, self.context_stack, self.filename
        )


if __name__ == "__main__":
    unittest.main()
