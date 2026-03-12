# === std / third-party imports ===
import unittest
from typing import Any, Dict

# === sub function imports ===
from ._handle_assignment_src import _handle_assignment, _record_error

# === ADT defines ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]

# === Test Class ===
class TestHandleAssignment(unittest.TestCase):
    """测试 _handle_assignment 函数的各种场景"""
    
    def setUp(self) -> None:
        """每个测试前的准备工作"""
        self.symbol_table = {
            'variables': {},
            'functions': {},
            'current_scope': 1,
            'errors': []
        }
    
    def test_happy_path_types_match(self) -> None:
        """正常路径：变量已声明且类型匹配"""
        self.symbol_table['variables'] = {
            'x': {'data_type': 'int', 'is_declared': True, 'line': 1, 'column': 1, 'scope_level': 1}
        }
        
        node = {
            'type': 'assignment',
            'children': [
                {'type': 'identifier', 'value': 'x', 'line': 5, 'column': 10},
                {'type': 'expression', 'value': 10, 'data_type': 'int', 'line': 5, 'column': 15}
            ],
            'line': 5,
            'column': 10
        }
        
        _handle_assignment(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table['errors']), 0)
    
    def test_happy_path_char_type_match(self) -> None:
        """正常路径：char 类型变量且类型匹配"""
        self.symbol_table['variables'] = {
            'c': {'data_type': 'char', 'is_declared': True, 'line': 1, 'column': 1, 'scope_level': 1}
        }
        
        node = {
            'type': 'assignment',
            'children': [
                {'type': 'identifier', 'value': 'c', 'line': 3, 'column': 5},
                {'type': 'expression', 'value': 'a', 'data_type': 'char', 'line': 3, 'column': 9}
            ],
            'line': 3,
            'column': 5
        }
        
        _handle_assignment(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table['errors']), 0)
    
    def test_undeclared_variable(self) -> None:
        """错误路径：变量未声明"""
        self.symbol_table['variables'] = {
            'y': {'data_type': 'int', 'is_declared': True, 'line': 1, 'column': 1, 'scope_level': 1}
        }
        
        node = {
            'type': 'assignment',
            'children': [
                {'type': 'identifier', 'value': 'x', 'line': 5, 'column': 10},
                {'type': 'expression', 'value': 10, 'data_type': 'int', 'line': 5, 'column': 15}
            ],
            'line': 5,
            'column': 10
        }
        
        _handle_assignment(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table['errors']), 1)
        error = self.symbol_table['errors'][0]
        self.assertIn("未声明变量", error['message'])
        self.assertIn("'x'", error['message'])
        self.assertEqual(error['line'], 5)
        self.assertEqual(error['column'], 10)
        self.assertEqual(error['node_type'], 'assignment')
    
    def test_type_mismatch_int_to_char(self) -> None:
        """错误路径：类型不匹配 - 变量为 int 但赋值为 char"""
        self.symbol_table['variables'] = {
            'x': {'data_type': 'int', 'is_declared': True, 'line': 1, 'column': 1, 'scope_level': 1}
        }
        
        node = {
            'type': 'assignment',
            'children': [
                {'type': 'identifier', 'value': 'x', 'line': 5, 'column': 10},
                {'type': 'expression', 'value': 'a', 'data_type': 'char', 'line': 5, 'column': 15}
            ],
            'line': 5,
            'column': 10
        }
        
        _handle_assignment(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table['errors']), 1)
        error = self.symbol_table['errors'][0]
        self.assertIn("类型不匹配", error['message'])
        self.assertIn("'x'", error['message'])
        self.assertIn("'int'", error['message'])
        self.assertIn("'char'", error['message'])
        self.assertEqual(error['line'], 5)
        self.assertEqual(error['column'], 10)
    
    def test_type_mismatch_char_to_int(self) -> None:
        """错误路径：类型不匹配 - 变量为 char 但赋值为 int"""
        self.symbol_table['variables'] = {
            'c': {'data_type': 'char', 'is_declared': True, 'line': 1, 'column': 1, 'scope_level': 1}
        }
        
        node = {
            'type': 'assignment',
            'children': [
                {'type': 'identifier', 'value': 'c', 'line': 3, 'column': 5},
                {'type': 'expression', 'value': 10, 'data_type': 'int', 'line': 3, 'column': 9}
            ],
            'line': 3,
            'column': 5
        }
        
        _handle_assignment(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table['errors']), 1)
        error = self.symbol_table['errors'][0]
        self.assertIn("类型不匹配", error['message'])
        self.assertIn("'c'", error['message'])
        self.assertIn("'char'", error['message'])
        self.assertIn("'int'", error['message'])
    
    def test_missing_children(self) -> None:
        """错误路径：节点缺少 children"""
        node = {
            'type': 'assignment',
            'line': 5,
            'column': 10
        }
        
        _handle_assignment(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table['errors']), 1)
        error = self.symbol_table['errors'][0]
        self.assertIn("赋值语句格式错误", error['message'])
        self.assertEqual(error['line'], 5)
        self.assertEqual(error['column'], 10)
    
    def test_insufficient_children(self) -> None:
        """错误路径：节点 children 数量不足"""
        node = {
            'type': 'assignment',
            'children': [
                {'type': 'identifier', 'value': 'x', 'line': 5, 'column': 10}
            ],
            'line': 5,
            'column': 10
        }
        
        _handle_assignment(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table['errors']), 1)
        error = self.symbol_table['errors'][0]
        self.assertIn("赋值语句格式错误", error['message'])
    
    def test_invalid_variable_name_none(self) -> None:
        """错误路径：变量名为 None"""
        node = {
            'type': 'assignment',
            'children': [
                {'type': 'identifier', 'value': None, 'line': 5, 'column': 10},
                {'type': 'expression', 'value': 10, 'data_type': 'int', 'line': 5, 'column': 15}
            ],
            'line': 5,
            'column': 10
        }
        
        _handle_assignment(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table['errors']), 1)
        error = self.symbol_table['errors'][0]
        self.assertIn("赋值语句变量名无效", error['message'])
    
    def test_invalid_variable_name_not_string(self) -> None:
        """错误路径：变量名不是字符串"""
        node = {
            'type': 'assignment',
            'children': [
                {'type': 'identifier', 'value': 123, 'line': 5, 'column': 10},
                {'type': 'expression', 'value': 10, 'data_type': 'int', 'line': 5, 'column': 15}
            ],
            'line': 5,
            'column': 10
        }
        
        _handle_assignment(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table['errors']), 1)
        error = self.symbol_table['errors'][0]
        self.assertIn("赋值语句变量名无效", error['message'])
    
    def test_empty_variable_name(self) -> None:
        """错误路径：变量名为空字符串"""
        node = {
            'type': 'assignment',
            'children': [
                {'type': 'identifier', 'value': '', 'line': 5, 'column': 10},
                {'type': 'expression', 'value': 10, 'data_type': 'int', 'line': 5, 'column': 15}
            ],
            'line': 5,
            'column': 10
        }
        
        _handle_assignment(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table['errors']), 1)
        error = self.symbol_table['errors'][0]
        self.assertIn("赋值语句变量名无效", error['message'])
    
    def test_initializes_errors_list(self) -> None:
        """边界值：symbol_table 没有 errors 列表时自动初始化"""
        symbol_table_no_errors = {
            'variables': {
                'x': {'data_type': 'int', 'is_declared': True, 'line': 1, 'column': 1, 'scope_level': 1}
            }
        }
        
        node = {
            'type': 'assignment',
            'children': [
                {'type': 'identifier', 'value': 'x', 'line': 5, 'column': 10},
                {'type': 'expression', 'value': 10, 'data_type': 'int', 'line': 5, 'column': 15}
            ],
            'line': 5,
            'column': 10
        }
        
        _handle_assignment(node, symbol_table_no_errors)
        
        self.assertIn('errors', symbol_table_no_errors)
        self.assertEqual(len(symbol_table_no_errors['errors']), 0)
    
    def test_empty_variables_dict(self) -> None:
        """边界值：variables 为空字典"""
        self.symbol_table['variables'] = {}
        
        node = {
            'type': 'assignment',
            'children': [
                {'type': 'identifier', 'value': 'x', 'line': 5, 'column': 10},
                {'type': 'expression', 'value': 10, 'data_type': 'int', 'line': 5, 'column': 15}
            ],
            'line': 5,
            'column': 10
        }
        
        _handle_assignment(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table['errors']), 1)
        error = self.symbol_table['errors'][0]
        self.assertIn("未声明变量", error['message'])
    
    def test_missing_variables_key(self) -> None:
        """边界值：symbol_table 没有 variables 键"""
        symbol_table_no_vars = {
            'functions': {},
            'current_scope': 1,
            'errors': []
        }
        
        node = {
            'type': 'assignment',
            'children': [
                {'type': 'identifier', 'value': 'x', 'line': 5, 'column': 10},
                {'type': 'expression', 'value': 10, 'data_type': 'int', 'line': 5, 'column': 15}
            ],
            'line': 5,
            'column': 10
        }
        
        _handle_assignment(node, symbol_table_no_vars)
        
        self.assertEqual(len(symbol_table_no_vars['errors']), 1)
        error = symbol_table_no_vars['errors'][0]
        self.assertIn("未声明变量", error['message'])
    
    def test_missing_data_type_in_var_info(self) -> None:
        """边界值：变量信息中没有 data_type"""
        self.symbol_table['variables'] = {
            'x': {'is_declared': True, 'line': 1, 'column': 1, 'scope_level': 1}
        }
        
        node = {
            'type': 'assignment',
            'children': [
                {'type': 'identifier', 'value': 'x', 'line': 5, 'column': 10},
                {'type': 'expression', 'value': 10, 'data_type': 'int', 'line': 5, 'column': 15}
            ],
            'line': 5,
            'column': 10
        }
        
        _handle_assignment(node, self.symbol_table)
        
        # 没有类型信息时不应报错
        self.assertEqual(len(self.symbol_table['errors']), 0)
    
    def test_missing_data_type_in_expr(self) -> None:
        """边界值：表达式没有 data_type"""
        self.symbol_table['variables'] = {
            'x': {'data_type': 'int', 'is_declared': True, 'line': 1, 'column': 1, 'scope_level': 1}
        }
        
        node = {
            'type': 'assignment',
            'children': [
                {'type': 'identifier', 'value': 'x', 'line': 5, 'column': 10},
                {'type': 'expression', 'value': 10, 'line': 5, 'column': 15}
            ],
            'line': 5,
            'column': 10
        }
        
        _handle_assignment(node, self.symbol_table)
        
        # 没有类型信息时不应报错
        self.assertEqual(len(self.symbol_table['errors']), 0)
    
    def test_no_side_effects_on_success(self) -> None:
        """验证：成功时不修改 symbol_table 的其他字段"""
        original_vars = {
            'x': {'data_type': 'int', 'is_declared': True, 'line': 1, 'column': 1, 'scope_level': 1}
        }
        original_functions = {'main': {'return_type': 'int', 'params': [], 'line': 1, 'column': 1}}
        original_scope = 1
        
        self.symbol_table['variables'] = original_vars
        self.symbol_table['functions'] = original_functions
        self.symbol_table['current_scope'] = original_scope
        
        node = {
            'type': 'assignment',
            'children': [
                {'type': 'identifier', 'value': 'x', 'line': 5, 'column': 10},
                {'type': 'expression', 'value': 10, 'data_type': 'int', 'line': 5, 'column': 15}
            ],
            'line': 5,
            'column': 10
        }
        
        _handle_assignment(node, self.symbol_table)
        
        self.assertEqual(self.symbol_table['variables'], original_vars)
        self.assertEqual(self.symbol_table['functions'], original_functions)
        self.assertEqual(self.symbol_table['current_scope'], original_scope)
    
    def test_multiple_assignments_accumulate_errors(self) -> None:
        """验证：多次调用会累积错误"""
        self.symbol_table['variables'] = {}
        
        node1 = {
            'type': 'assignment',
            'children': [
                {'type': 'identifier', 'value': 'x', 'line': 5, 'column': 10},
                {'type': 'expression', 'value': 10, 'data_type': 'int', 'line': 5, 'column': 15}
            ],
            'line': 5,
            'column': 10
        }
        
        node2 = {
            'type': 'assignment',
            'children': [
                {'type': 'identifier', 'value': 'y', 'line': 6, 'column': 10},
                {'type': 'expression', 'value': 20, 'data_type': 'int', 'line': 6, 'column': 15}
            ],
            'line': 6,
            'column': 10
        }
        
        _handle_assignment(node1, self.symbol_table)
        _handle_assignment(node2, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table['errors']), 2)
        self.assertIn("'x'", self.symbol_table['errors'][0]['message'])
        self.assertIn("'y'", self.symbol_table['errors'][1]['message'])


class TestRecordError(unittest.TestCase):
    """测试 _record_error 辅助函数"""
    
    def test_record_error_basic(self) -> None:
        """正常记录错误"""
        symbol_table = {'errors': []}
        node = {
            'type': 'assignment',
            'line': 10,
            'column': 5
        }
        message = "测试错误消息"
        
        _record_error(symbol_table, node, message)
        
        self.assertEqual(len(symbol_table['errors']), 1)
        error = symbol_table['errors'][0]
        self.assertEqual(error['message'], message)
        self.assertEqual(error['line'], 10)
        self.assertEqual(error['column'], 5)
        self.assertEqual(error['node_type'], 'assignment')
    
    def test_record_error_missing_line_column(self) -> None:
        """节点缺少行号列号时使用默认值"""
        symbol_table = {'errors': []}
        node = {
            'type': 'expression'
        }
        message = "测试错误消息"
        
        _record_error(symbol_table, node, message)
        
        error = symbol_table['errors'][0]
        self.assertEqual(error['line'], -1)
        self.assertEqual(error['column'], -1)
        self.assertEqual(error['node_type'], 'expression')
    
    def test_record_error_appends_to_existing(self) -> None:
        """错误追加到已有列表"""
        symbol_table = {
            'errors': [
                {'message': '已有错误', 'line': 1, 'column': 1, 'node_type': 'test'}
            ]
        }
        node = {
            'type': 'assignment',
            'line': 10,
            'column': 5
        }
        message = "新错误消息"
        
        _record_error(symbol_table, node, message)
        
        self.assertEqual(len(symbol_table['errors']), 2)
        self.assertEqual(symbol_table['errors'][1]['message'], message)


if __name__ == '__main__':
    unittest.main()
