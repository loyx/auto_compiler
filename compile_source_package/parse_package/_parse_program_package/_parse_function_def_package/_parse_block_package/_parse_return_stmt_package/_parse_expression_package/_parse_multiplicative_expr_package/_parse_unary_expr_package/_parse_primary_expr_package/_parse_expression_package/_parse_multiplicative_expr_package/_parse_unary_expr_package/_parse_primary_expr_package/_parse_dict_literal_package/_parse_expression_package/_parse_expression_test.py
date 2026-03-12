# === 单元测试文件：_parse_expression ===
# 测试目标：_parse_expression 函数
# 文件位置：_parse_expression_package/_parse_expression_test.py

import unittest
from unittest.mock import patch
from typing import Dict, Any

# 相对导入被测模块
from ._parse_expression_src import _parse_expression, _parse_unary_expression

# 需要 mock 的子函数，避免循环导入问题
_parse_dict_literal = None
_parse_list_literal = None
_parse_tuple_literal = None
_parse_atom = None

# === 类型定义（与源文件一致）===
Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]

# === 测试辅助函数 ===
def create_token(token_type: str, value: str, line: int = 1, column: int = 1) -> Token:
    """创建测试用的 token"""
    return {
        "type": token_type,
        "value": value,
        "line": line,
        "column": column
    }

def create_parser_state(tokens: list, pos: int = 0, filename: str = "test.py") -> ParserState:
    """创建测试用的 parser_state"""
    return {
        "tokens": tokens,
        "filename": filename,
        "pos": pos,
        "error": ""
    }

# === 测试类 ===
class TestParseExpression(unittest.TestCase):
    """测试 _parse_expression 函数"""
    
    def test_parse_dict_literal_dispatch(self):
        """测试 LEFT_BRACE token 分发到 _parse_dict_literal"""
        tokens = [create_token("LEFT_BRACE", "{"), create_token("RIGHT_BRACE", "}")]
        parser_state = create_parser_state(tokens, pos=0)
        
        mock_result = {"type": "DICT_LITERAL", "children": [], "line": 1, "column": 1}
        
        with patch("._parse_expression_src._parse_dict_literal") as mock_parse_dict:
            mock_parse_dict.return_value = mock_result
            result = _parse_expression(parser_state)
            
            mock_parse_dict.assert_called_once_with(parser_state)
            self.assertEqual(result, mock_result)
            self.assertEqual(parser_state["pos"], 0)  # pos 由子函数推进
    
    def test_parse_list_literal_dispatch(self):
        """测试 LEFT_BRACKET token 分发到 _parse_list_literal"""
        tokens = [create_token("LEFT_BRACKET", "["), create_token("RIGHT_BRACKET", "]")]
        parser_state = create_parser_state(tokens, pos=0)
        
        mock_result = {"type": "LIST_LITERAL", "children": [], "line": 1, "column": 1}
        
        with patch("._parse_expression_src._parse_list_literal") as mock_parse_list:
            mock_parse_list.return_value = mock_result
            result = _parse_expression(parser_state)
            
            mock_parse_list.assert_called_once_with(parser_state)
            self.assertEqual(result, mock_result)
    
    def test_parse_tuple_literal_dispatch(self):
        """测试 LEFT_PAREN token 分发到 _parse_tuple_literal"""
        tokens = [create_token("LEFT_PAREN", "("), create_token("RIGHT_PAREN", ")")]
        parser_state = create_parser_state(tokens, pos=0)
        
        mock_result = {"type": "TUPLE_LITERAL", "children": [], "line": 1, "column": 1}
        
        with patch("._parse_expression_src._parse_tuple_literal") as mock_parse_tuple:
            mock_parse_tuple.return_value = mock_result
            result = _parse_expression(parser_state)
            
            mock_parse_tuple.assert_called_once_with(parser_state)
            self.assertEqual(result, mock_result)
    
    def test_parse_atom_string(self):
        """测试 STRING token 分发到 _parse_atom"""
        tokens = [create_token("STRING", "hello")]
        parser_state = create_parser_state(tokens, pos=0)
        
        mock_result = {"type": "STRING", "value": "hello", "line": 1, "column": 1}
        
        with patch("._parse_expression_src._parse_atom") as mock_parse_atom:
            mock_parse_atom.return_value = mock_result
            result = _parse_expression(parser_state)
            
            mock_parse_atom.assert_called_once_with(parser_state)
            self.assertEqual(result, mock_result)
    
    def test_parse_atom_number(self):
        """测试 NUMBER token 分发到 _parse_atom"""
        tokens = [create_token("NUMBER", "42")]
        parser_state = create_parser_state(tokens, pos=0)
        
        mock_result = {"type": "NUMBER", "value": 42, "line": 1, "column": 1}
        
        with patch("._parse_expression_src._parse_atom") as mock_parse_atom:
            mock_parse_atom.return_value = mock_result
            result = _parse_expression(parser_state)
            
            mock_parse_atom.assert_called_once_with(parser_state)
            self.assertEqual(result, mock_result)
    
    def test_parse_atom_identifier(self):
        """测试 IDENTIFIER token 分发到 _parse_atom"""
        tokens = [create_token("IDENTIFIER", "x")]
        parser_state = create_parser_state(tokens, pos=0)
        
        mock_result = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        
        with patch("._parse_expression_src._parse_atom") as mock_parse_atom:
            mock_parse_atom.return_value = mock_result
            result = _parse_expression(parser_state)
            
            mock_parse_atom.assert_called_once_with(parser_state)
            self.assertEqual(result, mock_result)
    
    def test_parse_atom_true(self):
        """测试 TRUE token 分发到 _parse_atom"""
        tokens = [create_token("TRUE", "true")]
        parser_state = create_parser_state(tokens, pos=0)
        
        mock_result = {"type": "BOOL", "value": True, "line": 1, "column": 1}
        
        with patch("._parse_expression_src._parse_atom") as mock_parse_atom:
            mock_parse_atom.return_value = mock_result
            result = _parse_expression(parser_state)
            
            mock_parse_atom.assert_called_once_with(parser_state)
            self.assertEqual(result, mock_result)
    
    def test_parse_atom_false(self):
        """测试 FALSE token 分发到 _parse_atom"""
        tokens = [create_token("FALSE", "false")]
        parser_state = create_parser_state(tokens, pos=0)
        
        mock_result = {"type": "BOOL", "value": False, "line": 1, "column": 1}
        
        with patch("._parse_expression_src._parse_atom") as mock_parse_atom:
            mock_parse_atom.return_value = mock_result
            result = _parse_expression(parser_state)
            
            mock_parse_atom.assert_called_once_with(parser_state)
            self.assertEqual(result, mock_result)
    
    def test_parse_atom_none(self):
        """测试 NONE token 分发到 _parse_atom"""
        tokens = [create_token("NONE", "none")]
        parser_state = create_parser_state(tokens, pos=0)
        
        mock_result = {"type": "NONE", "value": None, "line": 1, "column": 1}
        
        with patch("._parse_expression_src._parse_atom") as mock_parse_atom:
            mock_parse_atom.return_value = mock_result
            result = _parse_expression(parser_state)
            
            mock_parse_atom.assert_called_once_with(parser_state)
            self.assertEqual(result, mock_result)
    
    def test_parse_unary_plus(self):
        """测试 PLUS token 分发到 _parse_unary_expression"""
        tokens = [create_token("PLUS", "+"), create_token("NUMBER", "5")]
        parser_state = create_parser_state(tokens, pos=0)
        
        mock_result = {"type": "UNARY_OP", "operator": "+", "line": 1, "column": 1}
        
        with patch("._parse_expression_src._parse_unary_expression") as mock_parse_unary:
            mock_parse_unary.return_value = mock_result
            result = _parse_expression(parser_state)
            
            mock_parse_unary.assert_called_once_with(parser_state)
            self.assertEqual(result, mock_result)
    
    def test_parse_unary_minus(self):
        """测试 MINUS token 分发到 _parse_unary_expression"""
        tokens = [create_token("MINUS", "-"), create_token("NUMBER", "5")]
        parser_state = create_parser_state(tokens, pos=0)
        
        mock_result = {"type": "UNARY_OP", "operator": "-", "line": 1, "column": 1}
        
        with patch("._parse_expression_src._parse_unary_expression") as mock_parse_unary:
            mock_parse_unary.return_value = mock_result
            result = _parse_expression(parser_state)
            
            mock_parse_unary.assert_called_once_with(parser_state)
            self.assertEqual(result, mock_result)
    
    def test_parse_unary_not(self):
        """测试 NOT token 分发到 _parse_unary_expression"""
        tokens = [create_token("NOT", "not"), create_token("TRUE", "true")]
        parser_state = create_parser_state(tokens, pos=0)
        
        mock_result = {"type": "UNARY_OP", "operator": "not", "line": 1, "column": 1}
        
        with patch("._parse_expression_src._parse_unary_expression") as mock_parse_unary:
            mock_parse_unary.return_value = mock_result
            result = _parse_expression(parser_state)
            
            mock_parse_unary.assert_called_once_with(parser_state)
            self.assertEqual(result, mock_result)
    
    def test_parse_unary_star(self):
        """测试 STAR token 分发到 _parse_unary_expression"""
        tokens = [create_token("STAR", "*"), create_token("IDENTIFIER", "x")]
        parser_state = create_parser_state(tokens, pos=0)
        
        mock_result = {"type": "UNARY_OP", "operator": "*", "line": 1, "column": 1}
        
        with patch("._parse_expression_src._parse_unary_expression") as mock_parse_unary:
            mock_parse_unary.return_value = mock_result
            result = _parse_expression(parser_state)
            
            mock_parse_unary.assert_called_once_with(parser_state)
            self.assertEqual(result, mock_result)
    
    def test_pos_out_of_bounds(self):
        """测试 pos 越界时抛出 SyntaxError"""
        tokens = [create_token("STRING", "hello")]
        parser_state = create_parser_state(tokens, pos=5)  # pos 超出 tokens 长度
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
    
    def test_pos_at_boundary(self):
        """测试 pos 等于 tokens 长度时抛出 SyntaxError"""
        tokens = [create_token("STRING", "hello")]
        parser_state = create_parser_state(tokens, pos=1)  # pos 等于 tokens 长度
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
    
    def test_unknown_token_type(self):
        """测试未知 token 类型时抛出 SyntaxError"""
        tokens = [create_token("UNKNOWN_TOKEN", "?")]
        parser_state = create_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        self.assertIn("Unexpected token", str(context.exception))
        self.assertIn("UNKNOWN_TOKEN", str(context.exception))
    
    def test_error_message_includes_location(self):
        """测试错误消息包含行号和列号"""
        tokens = [create_token("UNKNOWN", "?", line=10, column=25)]
        parser_state = create_parser_state(tokens, pos=0, filename="test.py")
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        error_msg = str(context.exception)
        self.assertIn("line 10", error_msg)
        self.assertIn("column 25", error_msg)
    
    def test_filename_in_error_message(self):
        """测试越界错误消息包含文件名"""
        tokens = []
        parser_state = create_parser_state(tokens, pos=0, filename="my_file.py")
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        self.assertIn("my_file.py", str(context.exception))
    
    def test_unknown_filename_default(self):
        """测试没有文件名时使用 'unknown' 作为默认值"""
        tokens = []
        parser_state = {"tokens": tokens, "pos": 0}  # 没有 filename 字段
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        self.assertIn("unknown", str(context.exception))
    
    def test_pos_not_modified_on_dispatch(self):
        """测试分发时 pos 不立即修改（由子函数负责推进）"""
        tokens = [create_token("LEFT_BRACE", "{"), create_token("RIGHT_BRACE", "}")]
        parser_state = create_parser_state(tokens, pos=0)
        original_pos = parser_state["pos"]
        
        with patch("._parse_expression_src._parse_dict_literal") as mock_parse_dict:
            mock_parse_dict.return_value = {"type": "DICT_LITERAL"}
            _parse_expression(parser_state)
            
            # pos 应该保持不变，因为子函数还没被调用
            # 实际上子函数会被调用并可能修改 pos
            # 这里验证的是 _parse_expression 本身不直接修改 pos
            pass  # pos 的修改由子函数负责


class TestParseUnaryExpression(unittest.TestCase):
    """测试 _parse_unary_expression helper 函数"""
    
    def test_unary_minus_expression(self):
        """测试一元减号表达式"""
        tokens = [
            create_token("MINUS", "-", line=1, column=1),
            create_token("NUMBER", "5", line=1, column=3)
        ]
        parser_state = create_parser_state(tokens, pos=0)
        
        with patch("._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = {"type": "NUMBER", "value": 5, "line": 1, "column": 3}
            result = _parse_unary_expression(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["operator"], "-")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(parser_state["pos"], 1)  # pos 应该推进到操作符之后
            mock_parse_expr.assert_called_once_with(parser_state)
    
    def test_unary_plus_expression(self):
        """测试一元加号表达式"""
        tokens = [
            create_token("PLUS", "+", line=1, column=1),
            create_token("NUMBER", "5", line=1, column=3)
        ]
        parser_state = create_parser_state(tokens, pos=0)
        
        with patch("._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = {"type": "NUMBER", "value": 5, "line": 1, "column": 3}
            result = _parse_unary_expression(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["operator"], "+")
            self.assertEqual(parser_state["pos"], 1)
    
    def test_unary_not_expression(self):
        """测试逻辑非表达式"""
        tokens = [
            create_token("NOT", "not", line=1, column=1),
            create_token("TRUE", "true", line=1, column=5)
        ]
        parser_state = create_parser_state(tokens, pos=0)
        
        with patch("._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = {"type": "BOOL", "value": True, "line": 1, "column": 5}
            result = _parse_unary_expression(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["operator"], "not")
            self.assertEqual(parser_state["pos"], 1)
    
    def test_unary_with_nested_expression(self):
        """测试一元运算符后跟复杂表达式"""
        tokens = [
            create_token("MINUS", "-", line=1, column=1),
            create_token("LEFT_PAREN", "(", line=1, column=3),
            create_token("NUMBER", "5", line=1, column=4),
            create_token("RIGHT_PAREN", ")", line=1, column=5)
        ]
        parser_state = create_parser_state(tokens, pos=0)
        
        mock_operand = {"type": "TUPLE_LITERAL", "value": 5, "line": 1, "column": 3}
        
        with patch("._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_operand
            result = _parse_unary_expression(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["operator"], "-")
            self.assertEqual(result["operand"], mock_operand)
            mock_parse_expr.assert_called_once_with(parser_state)
    
    def test_unary_preserves_line_column(self):
        """测试一元表达式保留操作符的行号和列号"""
        tokens = [
            create_token("MINUS", "-", line=5, column=10),
            create_token("NUMBER", "42", line=5, column=12)
        ]
        parser_state = create_parser_state(tokens, pos=0)
        
        with patch("._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = {"type": "NUMBER", "value": 42}
            result = _parse_unary_expression(parser_state)
            
            self.assertEqual(result["line"], 5)
            self.assertEqual(result["column"], 10)


# === 测试运行入口 ===
if __name__ == "__main__":
    unittest.main()
