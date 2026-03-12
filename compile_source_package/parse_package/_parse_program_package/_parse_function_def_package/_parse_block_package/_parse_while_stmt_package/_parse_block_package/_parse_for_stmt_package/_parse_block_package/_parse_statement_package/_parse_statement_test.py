# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Dict, Any

# === sub function imports (relative) ===
from ._parse_for_statement_package._parse_for_statement_src import _parse_for_statement
from ._parse_while_statement_package._parse_while_statement_src import _parse_while_statement
from ._parse_if_statement_package._parse_if_statement_src import _parse_if_statement
from ._parse_return_statement_package._parse_return_statement_src import _parse_return_statement
from ._parse_break_statement_package._parse_break_statement_src import _parse_break_statement
from ._parse_continue_statement_package._parse_continue_statement_src import _parse_continue_statement
from ._parse_pass_statement_package._parse_pass_statement_src import _parse_pass_statement
from ._parse_assign_statement_package._parse_assign_statement_src import _parse_assign_statement
from ._parse_import_statement_package._parse_import_statement_src import _parse_import_statement
from ._parse_def_statement_package._parse_def_statement_src import _parse_def_statement
from ._parse_class_statement_package._parse_class_statement_src import _parse_class_statement
from ._parse_expression_statement_package._parse_expression_statement_src import _parse_expression_statement

# === target function import ===
from ._parse_statement_src import _parse_statement

# === helper functions ===
def create_parser_state(tokens: list, pos: int = 0, filename: str = "<test>") -> Dict[str, Any]:
    """创建测试用的 parser_state"""
    return {
        "tokens": tokens,
        "pos": pos,
        "filename": filename
    }

def create_token(token_type: str, value: str = "", line: int = 1, column: int = 1) -> Dict[str, Any]:
    """创建测试用的 token"""
    return {
        "type": token_type,
        "value": value,
        "line": line,
        "column": column
    }

# === test cases ===
class TestParseStatement(unittest.TestCase):
    """测试 _parse_statement 分发器函数"""
    
    def test_skip_leading_semicolons(self):
        """测试跳过前导分号（空语句）"""
        tokens = [
            create_token("SEMICOLON", ";"),
            create_token("SEMICOLON", ";"),
            create_token("PASS", "pass"),
            create_token("SEMICOLON", ";")
        ]
        parser_state = create_parser_state(tokens, pos=0)
        
        # Mock _parse_pass_statement
        mock_result = {"type": "PASS_STMT", "line": 1, "column": 3}
        with patch.object(_parse_pass_statement, '__call__', return_value=mock_result) as mock_pass:
            result = _parse_statement(parser_state)
        
        # 验证 pos 跳过了前导分号
        self.assertEqual(parser_state["pos"], 2)
        # 验证调用了 pass 语句解析器
        mock_pass.assert_called_once()
    
    def test_unexpected_end_of_file(self):
        """测试文件末尾抛出 SyntaxError"""
        tokens = [
            create_token("SEMICOLON", ";")
        ]
        parser_state = create_parser_state(tokens, pos=0)
        
        # 所有 token 都是分号，跳过之后到达文件末尾
        with self.assertRaises(SyntaxError) as context:
            _parse_statement(parser_state)
        
        self.assertIn("Unexpected end of file", str(context.exception))
    
    def test_dispatch_for_statement(self):
        """测试 FOR 语句分发"""
        tokens = [
            create_token("FOR", "for"),
            create_token("IDENT", "i"),
            create_token("SEMICOLON", ";")
        ]
        parser_state = create_parser_state(tokens, pos=0)
        mock_result = {"type": "FOR_STMT", "line": 1, "column": 1}
        
        with patch.object(_parse_for_statement, '__call__', return_value=mock_result) as mock_for:
            result = _parse_statement(parser_state)
        
        mock_for.assert_called_once_with(parser_state)
        self.assertEqual(result, mock_result)
    
    def test_dispatch_while_statement(self):
        """测试 WHILE 语句分发"""
        tokens = [
            create_token("WHILE", "while"),
            create_token("SEMICOLON", ";")
        ]
        parser_state = create_parser_state(tokens, pos=0)
        mock_result = {"type": "WHILE_STMT", "line": 1, "column": 1}
        
        with patch.object(_parse_while_statement, '__call__', return_value=mock_result) as mock_while:
            result = _parse_statement(parser_state)
        
        mock_while.assert_called_once_with(parser_state)
        self.assertEqual(result, mock_result)
    
    def test_dispatch_if_statement(self):
        """测试 IF 语句分发"""
        tokens = [
            create_token("IF", "if"),
            create_token("SEMICOLON", ";")
        ]
        parser_state = create_parser_state(tokens, pos=0)
        mock_result = {"type": "IF_STMT", "line": 1, "column": 1}
        
        with patch.object(_parse_if_statement, '__call__', return_value=mock_result) as mock_if:
            result = _parse_statement(parser_state)
        
        mock_if.assert_called_once_with(parser_state)
        self.assertEqual(result, mock_result)
    
    def test_dispatch_return_statement(self):
        """测试 RETURN 语句分发"""
        tokens = [
            create_token("RETURN", "return"),
            create_token("SEMICOLON", ";")
        ]
        parser_state = create_parser_state(tokens, pos=0)
        mock_result = {"type": "RETURN_STMT", "line": 1, "column": 1}
        
        with patch.object(_parse_return_statement, '__call__', return_value=mock_result) as mock_return:
            result = _parse_statement(parser_state)
        
        mock_return.assert_called_once_with(parser_state)
        self.assertEqual(result, mock_result)
    
    def test_dispatch_break_statement(self):
        """测试 BREAK 语句分发"""
        tokens = [
            create_token("BREAK", "break"),
            create_token("SEMICOLON", ";")
        ]
        parser_state = create_parser_state(tokens, pos=0)
        mock_result = {"type": "BREAK_STMT", "line": 1, "column": 1}
        
        with patch.object(_parse_break_statement, '__call__', return_value=mock_result) as mock_break:
            result = _parse_statement(parser_state)
        
        mock_break.assert_called_once_with(parser_state)
        self.assertEqual(result, mock_result)
    
    def test_dispatch_continue_statement(self):
        """测试 CONTINUE 语句分发"""
        tokens = [
            create_token("CONTINUE", "continue"),
            create_token("SEMICOLON", ";")
        ]
        parser_state = create_parser_state(tokens, pos=0)
        mock_result = {"type": "CONTINUE_STMT", "line": 1, "column": 1}
        
        with patch.object(_parse_continue_statement, '__call__', return_value=mock_result) as mock_continue:
            result = _parse_statement(parser_state)
        
        mock_continue.assert_called_once_with(parser_state)
        self.assertEqual(result, mock_result)
    
    def test_dispatch_pass_statement(self):
        """测试 PASS 语句分发"""
        tokens = [
            create_token("PASS", "pass"),
            create_token("SEMICOLON", ";")
        ]
        parser_state = create_parser_state(tokens, pos=0)
        mock_result = {"type": "PASS_STMT", "line": 1, "column": 1}
        
        with patch.object(_parse_pass_statement, '__call__', return_value=mock_result) as mock_pass:
            result = _parse_statement(parser_state)
        
        mock_pass.assert_called_once_with(parser_state)
        self.assertEqual(result, mock_result)
    
    def test_dispatch_import_statement(self):
        """测试 IMPORT 语句分发"""
        tokens = [
            create_token("IMPORT", "import"),
            create_token("SEMICOLON", ";")
        ]
        parser_state = create_parser_state(tokens, pos=0)
        mock_result = {"type": "IMPORT_STMT", "line": 1, "column": 1}
        
        with patch.object(_parse_import_statement, '__call__', return_value=mock_result) as mock_import:
            result = _parse_statement(parser_state)
        
        mock_import.assert_called_once_with(parser_state)
        self.assertEqual(result, mock_result)
    
    def test_dispatch_def_statement(self):
        """测试 DEF 语句分发"""
        tokens = [
            create_token("DEF", "def"),
            create_token("SEMICOLON", ";")
        ]
        parser_state = create_parser_state(tokens, pos=0)
        mock_result = {"type": "DEF_STMT", "line": 1, "column": 1}
        
        with patch.object(_parse_def_statement, '__call__', return_value=mock_result) as mock_def:
            result = _parse_statement(parser_state)
        
        mock_def.assert_called_once_with(parser_state)
        self.assertEqual(result, mock_result)
    
    def test_dispatch_class_statement(self):
        """测试 CLASS 语句分发"""
        tokens = [
            create_token("CLASS", "class"),
            create_token("SEMICOLON", ";")
        ]
        parser_state = create_parser_state(tokens, pos=0)
        mock_result = {"type": "CLASS_STMT", "line": 1, "column": 1}
        
        with patch.object(_parse_class_statement, '__call__', return_value=mock_result) as mock_class:
            result = _parse_statement(parser_state)
        
        mock_class.assert_called_once_with(parser_state)
        self.assertEqual(result, mock_result)
    
    def test_dispatch_assign_statement(self):
        """测试 ASSIGN 语句分发（IDENT token）"""
        tokens = [
            create_token("IDENT", "x"),
            create_token("SEMICOLON", ";")
        ]
        parser_state = create_parser_state(tokens, pos=0)
        mock_result = {"type": "ASSIGN_STMT", "line": 1, "column": 1}
        
        with patch.object(_parse_assign_statement, '__call__', return_value=mock_result) as mock_assign:
            result = _parse_statement(parser_state)
        
        mock_assign.assert_called_once_with(parser_state)
        self.assertEqual(result, mock_result)
    
    def test_dispatch_expression_statement_default(self):
        """测试其他 token 类型作为表达式语句分发"""
        # 使用 NUMBER 作为未知 token 类型的示例
        tokens = [
            create_token("NUMBER", "42"),
            create_token("SEMICOLON", ";")
        ]
        parser_state = create_parser_state(tokens, pos=0)
        mock_result = {"type": "EXPRESSION_STMT", "line": 1, "column": 1}
        
        with patch.object(_parse_expression_statement, '__call__', return_value=mock_result) as mock_expr:
            result = _parse_statement(parser_state)
        
        mock_expr.assert_called_once_with(parser_state)
        self.assertEqual(result, mock_result)
    
    def test_pos_update_after_semicolon_skip(self):
        """测试跳过前导分号后 pos 正确更新"""
        tokens = [
            create_token("SEMICOLON", ";"),
            create_token("SEMICOLON", ";"),
            create_token("PASS", "pass"),
            create_token("SEMICOLON", ";")
        ]
        parser_state = create_parser_state(tokens, pos=0)
        mock_result = {"type": "PASS_STMT", "line": 1, "column": 3}
        
        # 记录初始 pos
        initial_pos = parser_state["pos"]
        self.assertEqual(initial_pos, 0)
        
        with patch.object(_parse_pass_statement, '__call__', return_value=mock_result):
            _parse_statement(parser_state)
        
        # 验证 pos 至少跳过了前导分号（具体值取决于子函数实现）
        self.assertGreater(parser_state["pos"], initial_pos)
    
    def test_filename_in_error_message(self):
        """测试错误消息中包含文件名"""
        tokens = [
            create_token("SEMICOLON", ";")
        ]
        parser_state = create_parser_state(tokens, pos=0, filename="test_file.cc")
        
        with self.assertRaises(SyntaxError) as context:
            _parse_statement(parser_state)
        
        self.assertIn("test_file.cc", str(context.exception))


# === test runner ===
if __name__ == "__main__":
    unittest.main()
