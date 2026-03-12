# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Dict, Any, List

# === relative imports ===
from ._parse_block_src import _parse_block


class TestParseBlock(unittest.TestCase):
    """单元测试：_parse_block 函数"""

    def _create_token(self, token_type: str, value: str = "", line: int = 1, column: int = 1) -> Dict[str, Any]:
        """辅助函数：创建 token"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_parser_state(self, tokens: List[Dict], pos: int = 0, filename: str = "test.src") -> Dict[str, Any]:
        """辅助函数：创建 parser_state"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def test_empty_block(self):
        """测试：空块 {}"""
        tokens = [
            self._create_token("LBRACE", "{", 1, 1),
            self._create_token("RBRACE", "}", 1, 2)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_block(parser_state)
        
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(result["statements"], [])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 2)  # pos 应该在 RBRACE 之后

    def test_block_with_statements(self):
        """测试：包含语句的块"""
        tokens = [
            self._create_token("LBRACE", "{", 1, 1),
            self._create_token("IDENT", "x", 2, 5),
            self._create_token("IDENT", "y", 3, 5),
            self._create_token("RBRACE", "}", 4, 1)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Mock _parse_statement 返回不同的 AST
        mock_statements = [
            {"type": "EXPR_STMT", "value": "x", "line": 2, "column": 5},
            {"type": "EXPR_STMT", "value": "y", "line": 3, "column": 5}
        ]
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_src._parse_statement") as mock_parse_stmt:
            mock_parse_stmt.side_effect = lambda state: mock_statements.pop(0)
            
            result = _parse_block(parser_state)
        
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(len(result["statements"]), 2)
        self.assertEqual(result["statements"][0]["type"], "EXPR_STMT")
        self.assertEqual(result["statements"][0]["value"], "x")
        self.assertEqual(result["statements"][1]["type"], "EXPR_STMT")
        self.assertEqual(result["statements"][1]["value"], "y")
        self.assertEqual(parser_state["pos"], 4)  # pos 应该在 RBRACE 之后

    def test_nested_blocks(self):
        """测试：嵌套块"""
        tokens = [
            self._create_token("LBRACE", "{", 1, 1),
            self._create_token("LBRACE", "{", 2, 5),
            self._create_token("RBRACE", "}", 2, 6),
            self._create_token("RBRACE", "}", 3, 1)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Mock _parse_statement 处理内层块
        mock_inner_block = {"type": "BLOCK", "statements": [], "line": 2, "column": 5}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_src._parse_statement") as mock_parse_stmt:
            mock_parse_stmt.return_value = mock_inner_block
            
            result = _parse_block(parser_state)
        
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(len(result["statements"]), 1)
        self.assertEqual(result["statements"][0]["type"], "BLOCK")
        self.assertEqual(parser_state["pos"], 4)

    def test_missing_lbrace(self):
        """测试：缺少 LBRACE 时抛出 SyntaxError"""
        tokens = [
            self._create_token("IDENT", "x", 1, 1),
            self._create_token("RBRACE", "}", 1, 2)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_block(parser_state)
        
        self.assertIn("Expected '{'", str(context.exception))
        self.assertIn("1:1", str(context.exception))

    def test_unexpected_end_of_input(self):
        """测试：输入意外结束时抛出 SyntaxError"""
        tokens = []
        parser_state = self._create_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_block(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))

    def test_unclosed_block(self):
        """测试：未闭合的块抛出 SyntaxError"""
        tokens = [
            self._create_token("LBRACE", "{", 1, 1),
            self._create_token("IDENT", "x", 2, 5)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Mock _parse_statement 消耗一个 token
        mock_stmt = {"type": "EXPR_STMT", "value": "x", "line": 2, "column": 5}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_src._parse_statement") as mock_parse_stmt:
            mock_parse_stmt.return_value = mock_stmt
            
            with self.assertRaises(SyntaxError) as context:
                _parse_block(parser_state)
        
        self.assertIn("Unclosed block", str(context.exception))
        self.assertIn("Expected '}}'", str(context.exception))

    def test_block_position_tracking(self):
        """测试：BLOCK AST 节点正确记录位置信息"""
        tokens = [
            self._create_token("LBRACE", "{", 5, 10),
            self._create_token("RBRACE", "}", 6, 1)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_block(parser_state)
        
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)

    def test_multiple_statements_sequence(self):
        """测试：多个语句的顺序解析"""
        tokens = [
            self._create_token("LBRACE", "{", 1, 1),
            self._create_token("IDENT", "a", 2, 5),
            self._create_token("IDENT", "b", 3, 5),
            self._create_token("IDENT", "c", 4, 5),
            self._create_token("RBRACE", "}", 5, 1)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        mock_statements = [
            {"type": "EXPR_STMT", "value": "a", "line": 2, "column": 5},
            {"type": "EXPR_STMT", "value": "b", "line": 3, "column": 5},
            {"type": "EXPR_STMT", "value": "c", "line": 4, "column": 5}
        ]
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_src._parse_statement") as mock_parse_stmt:
            mock_parse_stmt.side_effect = lambda state: mock_statements.pop(0)
            
            result = _parse_block(parser_state)
        
        self.assertEqual(len(result["statements"]), 3)
        self.assertEqual(result["statements"][0]["value"], "a")
        self.assertEqual(result["statements"][1]["value"], "b")
        self.assertEqual(result["statements"][2]["value"], "c")
        self.assertEqual(parser_state["pos"], 5)

    def test_parser_state_filename_default(self):
        """测试：parser_state 缺少 filename 时使用默认值"""
        tokens = [
            self._create_token("LBRACE", "{", 1, 1),
            self._create_token("RBRACE", "}", 1, 2)
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0
            # 没有 filename
        }
        
        result = _parse_block(parser_state)
        
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(parser_state["pos"], 2)


if __name__ == "__main__":
    unittest.main()
