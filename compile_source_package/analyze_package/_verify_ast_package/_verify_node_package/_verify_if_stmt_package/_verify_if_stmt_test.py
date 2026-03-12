# === std / third-party imports ===
import unittest
from unittest.mock import patch

# === UUT imports ===
from ._verify_if_stmt_src import _verify_if_stmt


class TestVerifyIfStmt(unittest.TestCase):
    """测试 _verify_if_stmt 函数的单元测试类"""

    def setUp(self):
        """测试前的准备工作"""
        self.symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
        }
        self.context_stack = []
        self.filename = "test.py"

    def _create_if_stmt_node(self, has_else=True, else_value=None):
        """创建测试用的 if_stmt 节点"""
        node = {
            "type": "if_stmt",
            "condition": {"type": "expression", "line": 1, "column": 5},
            "then_branch": {"type": "block", "line": 2, "column": 5},
            "line": 1,
            "column": 1,
        }
        if has_else:
            if else_value is None:
                node["else_branch"] = {"type": "block", "line": 3, "column": 5}
            else:
                node["else_branch"] = else_value
        else:
            node["else_branch"] = None
        return node

    @patch("projects.cc.files.main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_node_src._verify_node")
    def test_if_stmt_with_else_branch(self, mock_verify_node):
        """测试包含 else_branch 的 if_stmt 节点"""
        node = self._create_if_stmt_node(has_else=True)
        
        _verify_if_stmt(node, self.symbol_table, self.context_stack, self.filename)
        
        # 验证 _verify_node 被调用了 3 次 (condition, then_branch, else_branch)
        self.assertEqual(mock_verify_node.call_count, 3)
        
        # 验证调用参数
        calls = mock_verify_node.call_args_list
        self.assertEqual(calls[0][0][0], node['condition'])
        self.assertEqual(calls[1][0][0], node['then_branch'])
        self.assertEqual(calls[2][0][0], node['else_branch'])
        
        # 验证其他参数一致
        for call in calls:
            self.assertEqual(call[0][1], self.symbol_table)
            self.assertEqual(call[0][2], self.context_stack)
            self.assertEqual(call[0][3], self.filename)

    @patch("projects.cc.files.main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_node_src._verify_node")
    def test_if_stmt_without_else_branch(self, mock_verify_node):
        """测试不包含 else_branch 的 if_stmt 节点 (else_branch 为 None)"""
        node = self._create_if_stmt_node(has_else=False)
        
        _verify_if_stmt(node, self.symbol_table, self.context_stack, self.filename)
        
        # 验证 _verify_node 被调用了 2 次 (condition, then_branch)
        self.assertEqual(mock_verify_node.call_count, 2)
        
        # 验证调用参数
        calls = mock_verify_node.call_args_list
        self.assertEqual(calls[0][0][0], node['condition'])
        self.assertEqual(calls[1][0][0], node['then_branch'])

    @patch("projects.cc.files.main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_node_src._verify_node")
    def test_if_stmt_condition_verification_failure(self, mock_verify_node):
        """测试 condition 验证失败时的异常传播"""
        node = self._create_if_stmt_node(has_else=True)
        mock_verify_node.side_effect = ValueError("Condition verification failed")
        
        with self.assertRaises(ValueError) as context:
            _verify_if_stmt(node, self.symbol_table, self.context_stack, self.filename)
        
        self.assertEqual(str(context.exception), "Condition verification failed")
        # 验证只调用了 1 次 (在 condition 处失败)
        self.assertEqual(mock_verify_node.call_count, 1)
        self.assertEqual(mock_verify_node.call_args[0][0], node['condition'])

    @patch("projects.cc.files.main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_node_src._verify_node")
    def test_if_stmt_then_branch_verification_failure(self, mock_verify_node):
        """测试 then_branch 验证失败时的异常传播"""
        node = self._create_if_stmt_node(has_else=True)
        
        def side_effect(arg, *args):
            if arg == node['then_branch']:
                raise ValueError("Then branch verification failed")
            return None
        
        mock_verify_node.side_effect = side_effect
        
        with self.assertRaises(ValueError) as context:
            _verify_if_stmt(node, self.symbol_table, self.context_stack, self.filename)
        
        self.assertEqual(str(context.exception), "Then branch verification failed")
        # 验证调用了 2 次 (condition 成功，then_branch 失败)
        self.assertEqual(mock_verify_node.call_count, 2)

    @patch("projects.cc.files.main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_node_src._verify_node")
    def test_if_stmt_else_branch_verification_failure(self, mock_verify_node):
        """测试 else_branch 验证失败时的异常传播"""
        node = self._create_if_stmt_node(has_else=True)
        
        def side_effect(arg, *args):
            if arg == node['else_branch']:
                raise ValueError("Else branch verification failed")
            return None
        
        mock_verify_node.side_effect = side_effect
        
        with self.assertRaises(ValueError) as context:
            _verify_if_stmt(node, self.symbol_table, self.context_stack, self.filename)
        
        self.assertEqual(str(context.exception), "Else branch verification failed")
        # 验证调用了 3 次 (condition 和 then_branch 成功，else_branch 失败)
        self.assertEqual(mock_verify_node.call_count, 3)

    @patch("projects.cc.files.main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_node_src._verify_node")
    def test_if_stmt_with_empty_context_stack(self, mock_verify_node):
        """测试在空 context_stack 下的 if_stmt 验证"""
        node = self._create_if_stmt_node(has_else=True)
        context_stack = []
        
        _verify_if_stmt(node, self.symbol_table, context_stack, self.filename)
        
        self.assertEqual(mock_verify_node.call_count, 3)

    @patch("projects.cc.files.main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_node_src._verify_node")
    def test_if_stmt_with_nested_context_stack(self, mock_verify_node):
        """测试在嵌套 context_stack 下的 if_stmt 验证"""
        node = self._create_if_stmt_node(has_else=True)
        context_stack = [
            {"type": "function", "name": "main", "return_type": "int"},
            {"type": "loop", "stmt_type": "while"},
        ]
        
        _verify_if_stmt(node, self.symbol_table, context_stack, self.filename)
        
        self.assertEqual(mock_verify_node.call_count, 3)
        # 验证 context_stack 被正确传递
        for call in mock_verify_node.call_args_list:
            self.assertEqual(call[0][2], context_stack)

    @patch("projects.cc.files.main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_node_src._verify_node")
    def test_if_stmt_with_complex_symbol_table(self, mock_verify_node):
        """测试在复杂 symbol_table 下的 if_stmt 验证"""
        node = self._create_if_stmt_node(has_else=True)
        symbol_table = {
            "variables": {
                "x": {"type": "int", "scope": 0},
                "y": {"type": "str", "scope": 1},
            },
            "functions": {
                "foo": {"return_type": "int", "params": ["a", "b"]},
            },
            "current_scope": 1,
        }
        
        _verify_if_stmt(node, symbol_table, self.context_stack, self.filename)
        
        self.assertEqual(mock_verify_node.call_count, 3)
        # 验证 symbol_table 被正确传递
        for call in mock_verify_node.call_args_list:
            self.assertEqual(call[0][1], symbol_table)

    @patch("projects.cc.files.main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_node_src._verify_node")
    def test_if_stmt_node_with_line_column_info(self, mock_verify_node):
        """测试包含行列号信息的 if_stmt 节点"""
        node = {
            "type": "if_stmt",
            "condition": {"type": "expression", "line": 10, "column": 15},
            "then_branch": {"type": "block", "line": 11, "column": 5},
            "else_branch": {"type": "block", "line": 15, "column": 5},
            "line": 10,
            "column": 1,
        }
        
        _verify_if_stmt(node, self.symbol_table, self.context_stack, self.filename)
        
        self.assertEqual(mock_verify_node.call_count, 3)
        # 验证 filename 被正确传递
        for call in mock_verify_node.call_args_list:
            self.assertEqual(call[0][3], self.filename)

    @patch("projects.cc.files.main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_node_src._verify_node")
    def test_if_stmt_multiple_invocations(self, mock_verify_node):
        """测试多次调用 _verify_if_stmt 的独立性"""
        node1 = self._create_if_stmt_node(has_else=True)
        node2 = self._create_if_stmt_node(has_else=False)
        
        _verify_if_stmt(node1, self.symbol_table, self.context_stack, self.filename)
        call_count_after_first = mock_verify_node.call_count
        
        _verify_if_stmt(node2, self.symbol_table, self.context_stack, self.filename)
        call_count_after_second = mock_verify_node.call_count
        
        # 第一次调用 3 次，第二次调用 2 次
        self.assertEqual(call_count_after_first, 3)
        self.assertEqual(call_count_after_second, 5)


if __name__ == "__main__":
    unittest.main()
