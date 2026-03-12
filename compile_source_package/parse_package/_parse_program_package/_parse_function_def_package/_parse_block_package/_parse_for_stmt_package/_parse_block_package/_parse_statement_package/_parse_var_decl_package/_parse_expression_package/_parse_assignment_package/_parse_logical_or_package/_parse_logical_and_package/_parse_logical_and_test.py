# -*- coding: utf-8 -*-
"""
单元测试文件：_parse_logical_and
测试逻辑与表达式解析函数
"""

import unittest
from unittest.mock import patch, MagicMock
import sys

# 先 mock 整个依赖链，再导入被测模块
# 需要 mock 所有依赖模块及其子模块

# 获取当前包名
_current_package = __name__.rsplit('.', 1)[0] if '.' in __name__ else ''

# 创建 mock 模块
def create_mock_module(name):
    if _current_package:
        full_name = _current_package + name
    else:
        full_name = name.lstrip('.')
    mock = MagicMock()
    sys.modules[full_name] = mock
    return mock

# mock _parse_equality 及其依赖链
mock_equality_pkg = create_mock_module('._parse_equality_package')
mock_equality_src = create_mock_module('._parse_equality_package._parse_equality_src')
mock_relational_pkg = create_mock_module('._parse_equality_package._parse_relational_package')
mock_relational_src = create_mock_module('._parse_equality_package._parse_relational_package._parse_relational_src')
mock_additive_pkg = create_mock_module('._parse_equality_package._parse_relational_package._parse_additive_package')
mock_additive_src = create_mock_module('._parse_equality_package._parse_relational_package._parse_additive_package._parse_additive_src')
mock_multiplicative_pkg = create_mock_module('._parse_equality_package._parse_relational_package._parse_additive_package._parse_multiplicative_package')
mock_multiplicative_src = create_mock_module('._parse_equality_package._parse_relational_package._parse_additive_package._parse_multiplicative_package._parse_multiplicative_src')

# mock _current_token
mock_current_token_pkg = create_mock_module('._current_token_package')
mock_current_token_src = create_mock_module('._current_token_package._current_token_src')

# mock _consume
mock_consume_pkg = create_mock_module('._consume_package')
mock_consume_src = create_mock_module('._consume_package._consume_src')

# 设置 mock 函数
mock_parse_equality = MagicMock()
mock_current_token = MagicMock()
mock_consume = MagicMock()

mock_equality_src._parse_equality = mock_parse_equality
mock_current_token_src._current_token = mock_current_token
mock_consume_src._consume = mock_consume
mock_multiplicative_src._parse_multiplicative = MagicMock()

# 相对导入被测模块和依赖
from ._parse_logical_and_src import _parse_logical_and

# 定义 patch 目标路径（使用绝对路径）
# 注意：patch 的目标应该是 _parse_logical_and_src 模块中的导入，而不是原始模块
PARSE_EQUALITY_PATH = _current_package + '._parse_logical_and_src._parse_equality'
CURRENT_TOKEN_PATH = _current_package + '._parse_logical_and_src._current_token'
CONSUME_PATH = _current_package + '._parse_logical_and_src._consume'


class TestParseLogicalAnd(unittest.TestCase):
    """测试 _parse_logical_and 函数"""

    def test_single_equality_no_and_operator(self):
        """测试单个相等性表达式，无 && 运算符"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        equality_node = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        with patch(PARSE_EQUALITY_PATH) as mock_parse_equality:
            mock_parse_equality.return_value = equality_node
            
            with patch(CURRENT_TOKEN_PATH) as mock_current_token:
                # 返回 None 表示没有更多 token
                mock_current_token.return_value = None
                
                result = _parse_logical_and(parser_state)
                
                self.assertEqual(result, equality_node)
                mock_parse_equality.assert_called_once_with(parser_state)
                mock_current_token.assert_called_once_with(parser_state)

    def test_one_and_operator_two_operands(self):
        """测试一个 && 运算符，两个操作数"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "&&", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        left_operand = {
            "type": "IDENTIFIER",
            "value": "a",
            "line": 1,
            "column": 1
        }
        
        right_operand = {
            "type": "IDENTIFIER",
            "value": "b",
            "line": 1,
            "column": 6
        }
        
        and_token = {
            "type": "OPERATOR",
            "value": "&&",
            "line": 1,
            "column": 3
        }
        
        with patch(PARSE_EQUALITY_PATH) as mock_parse_equality:
            mock_parse_equality.side_effect = [left_operand, right_operand]
            
            with patch(CURRENT_TOKEN_PATH) as mock_current_token:
                mock_current_token.side_effect = [and_token, None]
                
                with patch(CONSUME_PATH) as mock_consume:
                    mock_consume.return_value = and_token
                    
                    result = _parse_logical_and(parser_state)
                    
                    self.assertEqual(result["type"], "BINARY_OP")
                    self.assertEqual(result["value"], "&&")
                    self.assertEqual(result["line"], 1)
                    self.assertEqual(result["column"], 3)
                    self.assertEqual(len(result["children"]), 2)
                    self.assertEqual(result["children"][0], left_operand)
                    self.assertEqual(result["children"][1], right_operand)
                    
                    self.assertEqual(mock_parse_equality.call_count, 2)
                    self.assertEqual(mock_current_token.call_count, 2)
                    mock_consume.assert_called_once_with(parser_state, "OPERATOR", "&&")

    def test_multiple_and_operators_left_associative(self):
        """测试多个 && 运算符，验证左结合性"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "&&", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6},
                {"type": "OPERATOR", "value": "&&", "line": 1, "column": 8},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 11}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        operand_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        operand_b = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6}
        operand_c = {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 11}
        
        and_token_1 = {"type": "OPERATOR", "value": "&&", "line": 1, "column": 3}
        and_token_2 = {"type": "OPERATOR", "value": "&&", "line": 1, "column": 8}
        
        with patch(PARSE_EQUALITY_PATH) as mock_parse_equality:
            mock_parse_equality.side_effect = [operand_a, operand_b, operand_c]
            
            with patch(CURRENT_TOKEN_PATH) as mock_current_token:
                mock_current_token.side_effect = [and_token_1, and_token_2, None]
                
                with patch(CONSUME_PATH) as mock_consume:
                    mock_consume.side_effect = [and_token_1, and_token_2]
                    
                    result = _parse_logical_and(parser_state)
                    
                    # 验证左结合性：(a && b) && c
                    self.assertEqual(result["type"], "BINARY_OP")
                    self.assertEqual(result["value"], "&&")
                    self.assertEqual(result["line"], 1)
                    self.assertEqual(result["column"], 8)
                    
                    # 左子节点应该是 (a && b)
                    left_child = result["children"][0]
                    self.assertEqual(left_child["type"], "BINARY_OP")
                    self.assertEqual(left_child["value"], "&&")
                    self.assertEqual(left_child["children"][0], operand_a)
                    self.assertEqual(left_child["children"][1], operand_b)
                    
                    # 右子节点应该是 c
                    self.assertEqual(result["children"][1], operand_c)
                    
                    self.assertEqual(mock_parse_equality.call_count, 3)
                    self.assertEqual(mock_current_token.call_count, 3)
                    self.assertEqual(mock_consume.call_count, 2)

    def test_current_token_returns_none(self):
        """测试 _current_token 返回 None 的情况"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.c"
        }
        
        equality_node = {
            "type": "LITERAL",
            "value": 42,
            "line": 1,
            "column": 1
        }
        
        with patch(PARSE_EQUALITY_PATH) as mock_parse_equality:
            mock_parse_equality.return_value = equality_node
            
            with patch(CURRENT_TOKEN_PATH) as mock_current_token:
                mock_current_token.return_value = None
                
                result = _parse_logical_and(parser_state)
                
                self.assertEqual(result, equality_node)
                mock_parse_equality.assert_called_once_with(parser_state)
                mock_current_token.assert_called_once_with(parser_state)

    def test_current_token_type_not_operator(self):
        """测试当前 token 类型不是 OPERATOR"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        equality_node = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        non_operator_token = {
            "type": "IDENTIFIER",
            "value": "y",
            "line": 1,
            "column": 3
        }
        
        with patch(PARSE_EQUALITY_PATH) as mock_parse_equality:
            mock_parse_equality.return_value = equality_node
            
            with patch(CURRENT_TOKEN_PATH) as mock_current_token:
                mock_current_token.return_value = non_operator_token
                
                result = _parse_logical_and(parser_state)
                
                self.assertEqual(result, equality_node)

    def test_current_token_value_not_and(self):
        """测试当前 token 值不是 &&"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "||", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        equality_node = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        or_token = {
            "type": "OPERATOR",
            "value": "||",
            "line": 1,
            "column": 3
        }
        
        with patch(PARSE_EQUALITY_PATH) as mock_parse_equality:
            mock_parse_equality.return_value = equality_node
            
            with patch(CURRENT_TOKEN_PATH) as mock_current_token:
                mock_current_token.return_value = or_token
                
                result = _parse_logical_and(parser_state)
                
                self.assertEqual(result, equality_node)

    def test_and_operator_with_line_column_preservation(self):
        """测试 && 运算符的行号和列号正确保存"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 5, "column": 10},
                {"type": "OPERATOR", "value": "&&", "line": 5, "column": 12},
                {"type": "IDENTIFIER", "value": "b", "line": 5, "column": 15}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        left_operand = {"type": "IDENTIFIER", "value": "a", "line": 5, "column": 10}
        right_operand = {"type": "IDENTIFIER", "value": "b", "line": 5, "column": 15}
        and_token = {"type": "OPERATOR", "value": "&&", "line": 5, "column": 12}
        
        with patch(PARSE_EQUALITY_PATH) as mock_parse_equality:
            mock_parse_equality.side_effect = [left_operand, right_operand]
            
            with patch(CURRENT_TOKEN_PATH) as mock_current_token:
                mock_current_token.side_effect = [and_token, None]
                
                with patch(CONSUME_PATH) as mock_consume:
                    mock_consume.return_value = and_token
                    
                    result = _parse_logical_and(parser_state)
                    
                    self.assertEqual(result["line"], 5)
                    self.assertEqual(result["column"], 12)

    def test_parser_state_pos_updated_by_consume(self):
        """测试 parser_state['pos'] 被 _consume 正确更新"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "&&", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        left_operand = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        right_operand = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6}
        and_token = {"type": "OPERATOR", "value": "&&", "line": 1, "column": 3}
        
        with patch(PARSE_EQUALITY_PATH) as mock_parse_equality:
            mock_parse_equality.side_effect = [left_operand, right_operand]
            
            with patch(CURRENT_TOKEN_PATH) as mock_current_token:
                mock_current_token.side_effect = [and_token, None]
                
                with patch(CONSUME_PATH) as mock_consume:
                    mock_consume.return_value = and_token
                    
                    _parse_logical_and(parser_state)
                    
                    mock_consume.assert_called_once_with(parser_state, "OPERATOR", "&&")


if __name__ == "__main__":
    unittest.main()
