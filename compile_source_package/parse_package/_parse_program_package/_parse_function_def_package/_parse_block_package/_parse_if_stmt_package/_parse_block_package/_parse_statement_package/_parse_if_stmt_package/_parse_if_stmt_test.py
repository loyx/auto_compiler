# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Dict, Any

# === relative import of UUT ===
from ._parse_if_stmt_src import _parse_if_stmt

# === Test Data Helpers ===
def make_token(token_type: str, value: str = "", line: int = 1, column: int = 1) -> Dict[str, Any]:
    """Helper to create a token dict."""
    return {
        "type": token_type,
        "value": value,
        "line": line,
        "column": column
    }

def make_parser_state(tokens: list, filename: str = "test.txt", pos: int = 0) -> Dict[str, Any]:
    """Helper to create a parser state dict."""
    return {
        "tokens": tokens,
        "filename": filename,
        "pos": pos
    }

def make_expression_ast(value: str = "cond", line: int = 1, column: int = 5) -> Dict[str, Any]:
    """Helper to create a mock expression AST node."""
    return {
        "type": "EXPR",
        "value": value,
        "line": line,
        "column": column
    }

def make_block_ast(statements: list = None, line: int = 1, column: int = 10) -> Dict[str, Any]:
    """Helper to create a mock block AST node."""
    return {
        "type": "BLOCK",
        "statements": statements if statements is not None else [],
        "line": line,
        "column": column
    }

# === Test Class ===
class TestParseIfStmt(unittest.TestCase):
    
    @patch('._parse_if_stmt_src._parse_expression')
    @patch('._parse_if_stmt_src._parse_block')
    def test_parse_if_without_else(self, mock_parse_block, mock_parse_expression):
        """测试不带 else 的 if 语句：if (cond) { ... }"""
        # Setup tokens: IF, LPAREN, condition tokens, RPAREN, LBRACE, statements, RBRACE
        tokens = [
            make_token("IF", "if", 1, 1),
            make_token("LPAREN", "(", 1, 4),
            make_token("IDENT", "cond", 1, 6),
            make_token("RPAREN", ")", 1, 10),
            make_token("LBRACE", "{", 1, 12),
            make_token("IDENT", "stmt", 1, 14),
            make_token("RBRACE", "}", 1, 19)
        ]
        parser_state = make_parser_state(tokens, "test.txt", 0)
        
        # Setup mocks
        mock_parse_expression.return_value = make_expression_ast("cond", 1, 6)
        mock_parse_block.return_value = make_block_ast([], 1, 12)
        
        # Execute
        result = _parse_if_stmt(parser_state)
        
        # Verify result structure
        self.assertEqual(result["type"], "IF_STMT")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(result["condition"], make_expression_ast("cond", 1, 6))
        self.assertEqual(result["then_branch"], make_block_ast([], 1, 12))
        self.assertIsNone(result["else_branch"])
        
        # Verify parser_state pos was updated (should be after RBRACE, pos=6)
        self.assertEqual(parser_state["pos"], 6)
        
        # Verify mocks were called correctly
        mock_parse_expression.assert_called_once()
        self.assertEqual(mock_parse_block.call_count, 1)
    
    @patch('._parse_if_stmt_src._parse_expression')
    @patch('._parse_if_stmt_src._parse_block')
    def test_parse_if_with_else(self, mock_parse_block, mock_parse_expression):
        """测试带 else 的 if 语句：if (cond) { ... } else { ... }"""
        # Setup tokens with ELSE branch
        tokens = [
            make_token("IF", "if", 2, 1),
            make_token("LPAREN", "(", 2, 4),
            make_token("IDENT", "x", 2, 6),
            make_token("RPAREN", ")", 2, 7),
            make_token("LBRACE", "{", 2, 9),
            make_token("IDENT", "stmt1", 2, 11),
            make_token("RBRACE", "}", 2, 17),
            make_token("ELSE", "else", 3, 1),
            make_token("LBRACE", "{", 3, 6),
            make_token("IDENT", "stmt2", 3, 8),
            make_token("RBRACE", "}", 3, 14)
        ]
        parser_state = make_parser_state(tokens, "test.txt", 0)
        
        # Setup mocks - parse_block will be called twice (then and else)
        mock_parse_expression.return_value = make_expression_ast("x", 2, 6)
        mock_parse_block.side_effect = [
            make_block_ast([], 2, 9),  # then branch
            make_block_ast([], 3, 6)   # else branch
        ]
        
        # Execute
        result = _parse_if_stmt(parser_state)
        
        # Verify result structure
        self.assertEqual(result["type"], "IF_STMT")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 1)
        self.assertEqual(result["condition"], make_expression_ast("x", 2, 6))
        self.assertEqual(result["then_branch"], make_block_ast([], 2, 9))
        self.assertIsNotNone(result["else_branch"])
        self.assertEqual(result["else_branch"], make_block_ast([], 3, 6))
        
        # Verify parser_state pos was updated (should be after final RBRACE, pos=10)
        self.assertEqual(parser_state["pos"], 10)
        
        # Verify mocks were called correctly
        mock_parse_expression.assert_called_once()
        self.assertEqual(mock_parse_block.call_count, 2)
    
    @patch('._parse_if_stmt_src._parse_expression')
    @patch('._parse_if_stmt_src._parse_block')
    def test_parse_if_nested(self, mock_parse_block, mock_parse_expression):
        """测试嵌套 if 语句"""
        tokens = [
            make_token("IF", "if", 1, 1),
            make_token("LPAREN", "(", 1, 4),
            make_token("IDENT", "a", 1, 6),
            make_token("RPAREN", ")", 1, 7),
            make_token("LBRACE", "{", 1, 9),
            make_token("IF", "if", 1, 11),  # nested if
            make_token("LPAREN", "(", 1, 14),
            make_token("IDENT", "b", 1, 16),
            make_token("RPAREN", ")", 1, 17),
            make_token("LBRACE", "{", 1, 19),
            make_token("IDENT", "stmt", 1, 21),
            make_token("RBRACE", "}", 1, 26),
            make_token("RBRACE", "}", 1, 28)
        ]
        parser_state = make_parser_state(tokens, "test.txt", 0)
        
        # Setup mocks
        mock_parse_expression.return_value = make_expression_ast("a", 1, 6)
        inner_block = make_block_ast([], 1, 19)
        outer_block = make_block_ast([], 1, 9)
        mock_parse_block.side_effect = [outer_block, inner_block]
        
        # Execute
        result = _parse_if_stmt(parser_state)
        
        # Verify
        self.assertEqual(result["type"], "IF_STMT")
        self.assertEqual(result["condition"], make_expression_ast("a", 1, 6))
        self.assertEqual(parser_state["pos"], 12)
    
    def test_parse_if_missing_lparen_raises_error(self):
        """测试缺少左括号时抛出 SyntaxError"""
        tokens = [
            make_token("IF", "if", 1, 1),
            make_token("IDENT", "cond", 1, 4),  # Should be LPAREN
            make_token("RPAREN", ")", 1, 8)
        ]
        parser_state = make_parser_state(tokens, "error_test.txt", 0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_if_stmt(parser_state)
        
        # Verify error message format
        error_msg = str(context.exception)
        self.assertIn("error_test.txt", error_msg)
        self.assertIn("Expected 'LPAREN'", error_msg)
    
    def test_parse_if_missing_rparen_raises_error(self):
        """测试缺少右括号时抛出 SyntaxError"""
        tokens = [
            make_token("IF", "if", 1, 1),
            make_token("LPAREN", "(", 1, 4),
            make_token("IDENT", "cond", 1, 6),
            make_token("LBRACE", "{", 1, 11)  # Should be RPAREN
        ]
        parser_state = make_parser_state(tokens, "error_test.txt", 0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_if_stmt(parser_state)
        
        error_msg = str(context.exception)
        self.assertIn("error_test.txt", error_msg)
        self.assertIn("Expected 'RPAREN'", error_msg)
    
    def test_parse_if_unexpected_end_raises_error(self):
        """测试输入意外结束时抛出 SyntaxError"""
        tokens = [
            make_token("IF", "if", 1, 1),
            make_token("LPAREN", "(", 1, 4)
        ]
        parser_state = make_parser_state(tokens, "error_test.txt", 0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_if_stmt(parser_state)
        
        error_msg = str(context.exception)
        self.assertIn("error_test.txt", error_msg)
        self.assertIn("Unexpected end of input", error_msg)
    
    @patch('._parse_if_stmt_src._parse_expression')
    def test_parse_if_preserves_token_position_info(self, mock_parse_expression):
        """测试 IF_STMT 节点保留 IF 关键字的行列信息"""
        tokens = [
            make_token("IF", "if", 5, 10),  # line 5, column 10
            make_token("LPAREN", "(", 5, 13),
            make_token("IDENT", "x", 5, 15),
            make_token("RPAREN", ")", 5, 16),
            make_token("LBRACE", "{", 5, 18),
            make_token("RBRACE", "}", 5, 20)
        ]
        parser_state = make_parser_state(tokens, "test.txt", 0)
        
        mock_parse_expression.return_value = make_expression_ast()
        with patch('._parse_if_stmt_src._parse_block', return_value=make_block_ast()):
            result = _parse_if_stmt(parser_state)
        
        # Verify line and column come from IF token
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)
    
    @patch('._parse_if_stmt_src._parse_expression')
    @patch('._parse_if_stmt_src._parse_block')
    def test_parse_if_only_consumes_else_when_present(self, mock_parse_block, mock_parse_expression):
        """测试只有存在 ELSE token 时才解析 else 分支"""
        tokens = [
            make_token("IF", "if", 1, 1),
            make_token("LPAREN", "(", 1, 4),
            make_token("IDENT", "x", 1, 6),
            make_token("RPAREN", ")", 1, 7),
            make_token("LBRACE", "{", 1, 9),
            make_token("RBRACE", "}", 1, 11),
            make_token("IDENT", "next_stmt", 2, 1)  # Not ELSE
        ]
        parser_state = make_parser_state(tokens, "test.txt", 0)
        
        mock_parse_expression.return_value = make_expression_ast()
        mock_parse_block.return_value = make_block_ast()
        
        result = _parse_if_stmt(parser_state)
        
        # Should not have else branch
        self.assertIsNone(result["else_branch"])
        # parse_block should only be called once (for then branch)
        self.assertEqual(mock_parse_block.call_count, 1)
        # pos should be at 6 (after then block's RBRACE)
        self.assertEqual(parser_state["pos"], 6)


# === Run Tests ===
if __name__ == "__main__":
    unittest.main()
