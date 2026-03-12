import unittest
from unittest.mock import patch, MagicMock

# Relative import from the same package
from ._traverse_node_src import _traverse_node


class TestTraverseNode(unittest.TestCase):
    """单元测试：_traverse_node 函数 - AST 节点遍历分发器"""

    def setUp(self) -> None:
        """每个测试前重置 mock"""
        pass

    def _create_mock_handlers(self):
        """创建所有 handler 的 mock 对象"""
        mocks = {}
        mocks['program'] = MagicMock()
        mocks['function_declaration'] = MagicMock()
        mocks['block'] = MagicMock()
        mocks['variable_declaration'] = MagicMock()
        mocks['assignment'] = MagicMock()
        mocks['if_statement'] = MagicMock()
        mocks['while_statement'] = MagicMock()
        mocks['return_statement'] = MagicMock()
        mocks['expression'] = MagicMock()
        return mocks

    def test_dispatch_program_node(self) -> None:
        """测试：program 类型节点正确分发到 _handle_program"""
        mocks = self._create_mock_handlers()
        
        node = {"type": "program", "children": [], "line": 1, "column": 1}
        symbol_table = {"variables": {}, "functions": {}, "current_scope": 0}
        
        with patch('._traverse_node_src._handle_program', mocks['program']), \
             patch('._traverse_node_src._handle_function_declaration', mocks['function_declaration']), \
             patch('._traverse_node_src._handle_block', mocks['block']), \
             patch('._traverse_node_src._handle_variable_declaration', mocks['variable_declaration']), \
             patch('._traverse_node_src._handle_assignment', mocks['assignment']), \
             patch('._traverse_node_src._handle_if_statement', mocks['if_statement']), \
             patch('._traverse_node_src._handle_while_statement', mocks['while_statement']), \
             patch('._traverse_node_src._handle_return_statement', mocks['return_statement']), \
             patch('._traverse_node_src._handle_expression', mocks['expression']):
            
            _traverse_node(node, symbol_table)
        
        mocks['program'].assert_called_once_with(node, symbol_table)
        for handler_name, mock_obj in mocks.items():
            if handler_name != 'program':
                mock_obj.assert_not_called()

    def test_dispatch_function_declaration_node(self) -> None:
        """测试：function_declaration 类型节点正确分发到 _handle_function_declaration"""
        mocks = self._create_mock_handlers()
        
        node = {
            "type": "function_declaration",
            "name": "foo",
            "return_type": "int",
            "params": [],
            "line": 1,
            "column": 1
        }
        symbol_table = {"variables": {}, "functions": {}, "current_scope": 0}
        
        with patch('._traverse_node_src._handle_program', mocks['program']), \
             patch('._traverse_node_src._handle_function_declaration', mocks['function_declaration']), \
             patch('._traverse_node_src._handle_block', mocks['block']), \
             patch('._traverse_node_src._handle_variable_declaration', mocks['variable_declaration']), \
             patch('._traverse_node_src._handle_assignment', mocks['assignment']), \
             patch('._traverse_node_src._handle_if_statement', mocks['if_statement']), \
             patch('._traverse_node_src._handle_while_statement', mocks['while_statement']), \
             patch('._traverse_node_src._handle_return_statement', mocks['return_statement']), \
             patch('._traverse_node_src._handle_expression', mocks['expression']):
            
            _traverse_node(node, symbol_table)
        
        mocks['function_declaration'].assert_called_once_with(node, symbol_table)
        for handler_name, mock_obj in mocks.items():
            if handler_name != 'function_declaration':
                mock_obj.assert_not_called()

    def test_dispatch_block_node(self) -> None:
        """测试：block 类型节点正确分发到 _handle_block"""
        mocks = self._create_mock_handlers()
        
        node = {"type": "block", "children": [], "line": 1, "column": 1}
        symbol_table = {"variables": {}, "functions": {}, "current_scope": 0}
        
        with patch('._traverse_node_src._handle_program', mocks['program']), \
             patch('._traverse_node_src._handle_function_declaration', mocks['function_declaration']), \
             patch('._traverse_node_src._handle_block', mocks['block']), \
             patch('._traverse_node_src._handle_variable_declaration', mocks['variable_declaration']), \
             patch('._traverse_node_src._handle_assignment', mocks['assignment']), \
             patch('._traverse_node_src._handle_if_statement', mocks['if_statement']), \
             patch('._traverse_node_src._handle_while_statement', mocks['while_statement']), \
             patch('._traverse_node_src._handle_return_statement', mocks['return_statement']), \
             patch('._traverse_node_src._handle_expression', mocks['expression']):
            
            _traverse_node(node, symbol_table)
        
        mocks['block'].assert_called_once_with(node, symbol_table)
        for handler_name, mock_obj in mocks.items():
            if handler_name != 'block':
                mock_obj.assert_not_called()

    def test_dispatch_variable_declaration_node(self) -> None:
        """测试：variable_declaration 类型节点正确分发到 _handle_variable_declaration"""
        mocks = self._create_mock_handlers()
        
        node = {
            "type": "variable_declaration",
            "name": "x",
            "data_type": "int",
            "line": 1,
            "column": 1
        }
        symbol_table = {"variables": {}, "functions": {}, "current_scope": 0}
        
        with patch('._traverse_node_src._handle_program', mocks['program']), \
             patch('._traverse_node_src._handle_function_declaration', mocks['function_declaration']), \
             patch('._traverse_node_src._handle_block', mocks['block']), \
             patch('._traverse_node_src._handle_variable_declaration', mocks['variable_declaration']), \
             patch('._traverse_node_src._handle_assignment', mocks['assignment']), \
             patch('._traverse_node_src._handle_if_statement', mocks['if_statement']), \
             patch('._traverse_node_src._handle_while_statement', mocks['while_statement']), \
             patch('._traverse_node_src._handle_return_statement', mocks['return_statement']), \
             patch('._traverse_node_src._handle_expression', mocks['expression']):
            
            _traverse_node(node, symbol_table)
        
        mocks['variable_declaration'].assert_called_once_with(node, symbol_table)
        for handler_name, mock_obj in mocks.items():
            if handler_name != 'variable_declaration':
                mock_obj.assert_not_called()

    def test_dispatch_assignment_node(self) -> None:
        """测试：assignment 类型节点正确分发到 _handle_assignment"""
        mocks = self._create_mock_handlers()
        
        node = {
            "type": "assignment",
            "target": "x",
            "expression": {"type": "expression", "value": 5},
            "line": 1,
            "column": 1
        }
        symbol_table = {"variables": {}, "functions": {}, "current_scope": 0}
        
        with patch('._traverse_node_src._handle_program', mocks['program']), \
             patch('._traverse_node_src._handle_function_declaration', mocks['function_declaration']), \
             patch('._traverse_node_src._handle_block', mocks['block']), \
             patch('._traverse_node_src._handle_variable_declaration', mocks['variable_declaration']), \
             patch('._traverse_node_src._handle_assignment', mocks['assignment']), \
             patch('._traverse_node_src._handle_if_statement', mocks['if_statement']), \
             patch('._traverse_node_src._handle_while_statement', mocks['while_statement']), \
             patch('._traverse_node_src._handle_return_statement', mocks['return_statement']), \
             patch('._traverse_node_src._handle_expression', mocks['expression']):
            
            _traverse_node(node, symbol_table)
        
        mocks['assignment'].assert_called_once_with(node, symbol_table)
        for handler_name, mock_obj in mocks.items():
            if handler_name != 'assignment':
                mock_obj.assert_not_called()

    def test_dispatch_if_statement_node(self) -> None:
        """测试：if_statement 类型节点正确分发到 _handle_if_statement"""
        mocks = self._create_mock_handlers()
        
        node = {
            "type": "if_statement",
            "condition": {"type": "expression"},
            "then_branch": {"type": "block"},
            "else_branch": None,
            "line": 1,
            "column": 1
        }
        symbol_table = {"variables": {}, "functions": {}, "current_scope": 0}
        
        with patch('._traverse_node_src._handle_program', mocks['program']), \
             patch('._traverse_node_src._handle_function_declaration', mocks['function_declaration']), \
             patch('._traverse_node_src._handle_block', mocks['block']), \
             patch('._traverse_node_src._handle_variable_declaration', mocks['variable_declaration']), \
             patch('._traverse_node_src._handle_assignment', mocks['assignment']), \
             patch('._traverse_node_src._handle_if_statement', mocks['if_statement']), \
             patch('._traverse_node_src._handle_while_statement', mocks['while_statement']), \
             patch('._traverse_node_src._handle_return_statement', mocks['return_statement']), \
             patch('._traverse_node_src._handle_expression', mocks['expression']):
            
            _traverse_node(node, symbol_table)
        
        mocks['if_statement'].assert_called_once_with(node, symbol_table)
        for handler_name, mock_obj in mocks.items():
            if handler_name != 'if_statement':
                mock_obj.assert_not_called()

    def test_dispatch_while_statement_node(self) -> None:
        """测试：while_statement 类型节点正确分发到 _handle_while_statement"""
        mocks = self._create_mock_handlers()
        
        node = {
            "type": "while_statement",
            "condition": {"type": "expression"},
            "body": {"type": "block"},
            "line": 1,
            "column": 1
        }
        symbol_table = {"variables": {}, "functions": {}, "current_scope": 0}
        
        with patch('._traverse_node_src._handle_program', mocks['program']), \
             patch('._traverse_node_src._handle_function_declaration', mocks['function_declaration']), \
             patch('._traverse_node_src._handle_block', mocks['block']), \
             patch('._traverse_node_src._handle_variable_declaration', mocks['variable_declaration']), \
             patch('._traverse_node_src._handle_assignment', mocks['assignment']), \
             patch('._traverse_node_src._handle_if_statement', mocks['if_statement']), \
             patch('._traverse_node_src._handle_while_statement', mocks['while_statement']), \
             patch('._traverse_node_src._handle_return_statement', mocks['return_statement']), \
             patch('._traverse_node_src._handle_expression', mocks['expression']):
            
            _traverse_node(node, symbol_table)
        
        mocks['while_statement'].assert_called_once_with(node, symbol_table)
        for handler_name, mock_obj in mocks.items():
            if handler_name != 'while_statement':
                mock_obj.assert_not_called()

    def test_dispatch_return_statement_node(self) -> None:
        """测试：return_statement 类型节点正确分发到 _handle_return_statement"""
        mocks = self._create_mock_handlers()
        
        node = {
            "type": "return_statement",
            "value": {"type": "expression", "value": 42},
            "line": 1,
            "column": 1
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "current_function": "main"
        }
        
        with patch('._traverse_node_src._handle_program', mocks['program']), \
             patch('._traverse_node_src._handle_function_declaration', mocks['function_declaration']), \
             patch('._traverse_node_src._handle_block', mocks['block']), \
             patch('._traverse_node_src._handle_variable_declaration', mocks['variable_declaration']), \
             patch('._traverse_node_src._handle_assignment', mocks['assignment']), \
             patch('._traverse_node_src._handle_if_statement', mocks['if_statement']), \
             patch('._traverse_node_src._handle_while_statement', mocks['while_statement']), \
             patch('._traverse_node_src._handle_return_statement', mocks['return_statement']), \
             patch('._traverse_node_src._handle_expression', mocks['expression']):
            
            _traverse_node(node, symbol_table)
        
        mocks['return_statement'].assert_called_once_with(node, symbol_table)
        for handler_name, mock_obj in mocks.items():
            if handler_name != 'return_statement':
                mock_obj.assert_not_called()

    def test_dispatch_expression_node(self) -> None:
        """测试：expression 类型节点正确分发到 _handle_expression"""
        mocks = self._create_mock_handlers()
        
        node = {
            "type": "expression",
            "operator": "+",
            "left": {"type": "expression", "value": 1},
            "right": {"type": "expression", "value": 2},
            "line": 1,
            "column": 1
        }
        symbol_table = {"variables": {}, "functions": {}, "current_scope": 0}
        
        with patch('._traverse_node_src._handle_program', mocks['program']), \
             patch('._traverse_node_src._handle_function_declaration', mocks['function_declaration']), \
             patch('._traverse_node_src._handle_block', mocks['block']), \
             patch('._traverse_node_src._handle_variable_declaration', mocks['variable_declaration']), \
             patch('._traverse_node_src._handle_assignment', mocks['assignment']), \
             patch('._traverse_node_src._handle_if_statement', mocks['if_statement']), \
             patch('._traverse_node_src._handle_while_statement', mocks['while_statement']), \
             patch('._traverse_node_src._handle_return_statement', mocks['return_statement']), \
             patch('._traverse_node_src._handle_expression', mocks['expression']):
            
            _traverse_node(node, symbol_table)
        
        mocks['expression'].assert_called_once_with(node, symbol_table)
        for handler_name, mock_obj in mocks.items():
            if handler_name != 'expression':
                mock_obj.assert_not_called()

    def test_unknown_node_type_records_error(self) -> None:
        """测试：未知节点类型记录错误到 symbol_table['errors']"""
        mocks = self._create_mock_handlers()
        
        node = {"type": "unknown_type", "line": 10, "column": 5}
        symbol_table = {"variables": {}, "functions": {}, "current_scope": 0}
        
        with patch('._traverse_node_src._handle_program', mocks['program']), \
             patch('._traverse_node_src._handle_function_declaration', mocks['function_declaration']), \
             patch('._traverse_node_src._handle_block', mocks['block']), \
             patch('._traverse_node_src._handle_variable_declaration', mocks['variable_declaration']), \
             patch('._traverse_node_src._handle_assignment', mocks['assignment']), \
             patch('._traverse_node_src._handle_if_statement', mocks['if_statement']), \
             patch('._traverse_node_src._handle_while_statement', mocks['while_statement']), \
             patch('._traverse_node_src._handle_return_statement', mocks['return_statement']), \
             patch('._traverse_node_src._handle_expression', mocks['expression']):
            
            _traverse_node(node, symbol_table)
        
        # 验证所有 handler 都未被调用
        for mock_obj in mocks.values():
            mock_obj.assert_not_called()
        
        # 验证错误被记录
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["message"], "Unknown node type 'unknown_type' at line 10, column 5")
        self.assertEqual(error["line"], 10)
        self.assertEqual(error["column"], 5)
        self.assertEqual(error["type"], "unknown_node_type")

    def test_unknown_node_type_initializes_errors_list(self) -> None:
        """测试：当 symbol_table 没有 errors 字段时，自动初始化 errors 列表"""
        mocks = self._create_mock_handlers()
        
        node = {"type": "unknown_type", "line": 10, "column": 5}
        symbol_table = {"variables": {}, "functions": {}, "current_scope": 0}
        # 故意不初始化 errors 字段
        
        with patch('._traverse_node_src._handle_program', mocks['program']), \
             patch('._traverse_node_src._handle_function_declaration', mocks['function_declaration']), \
             patch('._traverse_node_src._handle_block', mocks['block']), \
             patch('._traverse_node_src._handle_variable_declaration', mocks['variable_declaration']), \
             patch('._traverse_node_src._handle_assignment', mocks['assignment']), \
             patch('._traverse_node_src._handle_if_statement', mocks['if_statement']), \
             patch('._traverse_node_src._handle_while_statement', mocks['while_statement']), \
             patch('._traverse_node_src._handle_return_statement', mocks['return_statement']), \
             patch('._traverse_node_src._handle_expression', mocks['expression']):
            
            _traverse_node(node, symbol_table)
        
        # 验证 errors 列表被创建
        self.assertIn("errors", symbol_table)
        self.assertIsInstance(symbol_table["errors"], list)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_missing_type_field_treated_as_unknown(self) -> None:
        """测试：缺少 type 字段的节点被视为未知类型"""
        mocks = self._create_mock_handlers()
        
        node = {"line": 10, "column": 5}  # 没有 type 字段
        symbol_table = {"variables": {}, "functions": {}, "current_scope": 0}
        
        with patch('._traverse_node_src._handle_program', mocks['program']), \
             patch('._traverse_node_src._handle_function_declaration', mocks['function_declaration']), \
             patch('._traverse_node_src._handle_block', mocks['block']), \
             patch('._traverse_node_src._handle_variable_declaration', mocks['variable_declaration']), \
             patch('._traverse_node_src._handle_assignment', mocks['assignment']), \
             patch('._traverse_node_src._handle_if_statement', mocks['if_statement']), \
             patch('._traverse_node_src._handle_while_statement', mocks['while_statement']), \
             patch('._traverse_node_src._handle_return_statement', mocks['return_statement']), \
             patch('._traverse_node_src._handle_expression', mocks['expression']):
            
            _traverse_node(node, symbol_table)
        
        # 验证所有 handler 都未被调用
        for mock_obj in mocks.values():
            mock_obj.assert_not_called()
        
        # 验证错误被记录
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertIn("Unknown node type ''", error["message"])

    def test_unknown_node_type_without_line_column(self) -> None:
        """测试：未知节点类型没有 line/column 字段时的错误记录"""
        mocks = self._create_mock_handlers()
        
        node = {"type": "unknown_type"}  # 没有 line 和 column
        symbol_table = {"variables": {}, "functions": {}, "current_scope": 0}
        
        with patch('._traverse_node_src._handle_program', mocks['program']), \
             patch('._traverse_node_src._handle_function_declaration', mocks['function_declaration']), \
             patch('._traverse_node_src._handle_block', mocks['block']), \
             patch('._traverse_node_src._handle_variable_declaration', mocks['variable_declaration']), \
             patch('._traverse_node_src._handle_assignment', mocks['assignment']), \
             patch('._traverse_node_src._handle_if_statement', mocks['if_statement']), \
             patch('._traverse_node_src._handle_while_statement', mocks['while_statement']), \
             patch('._traverse_node_src._handle_return_statement', mocks['return_statement']), \
             patch('._traverse_node_src._handle_expression', mocks['expression']):
            
            _traverse_node(node, symbol_table)
        
        # 验证错误被记录
        self.assertIn("errors", symbol_table)
        error = symbol_table["errors"][0]
        self.assertIn("unknown", error["message"])


if __name__ == "__main__":
    unittest.main()
