# -*- coding: utf-8 -*-
"""
单元测试：_parse_if_stmt
测试 if 语句解析功能，覆盖正常路径、边界情况和错误处理。
"""

import unittest
from unittest.mock import patch
from typing import Dict, Any

# 相对导入被测模块
from ._parse_if_stmt_src import _parse_if_stmt, ParserState


def make_token(token_type: str, value: str = "", line: int = 1, column: int = 1) -> Dict[str, Any]:
    """辅助函数：创建 token 字典"""
    return {
        "type": token_type,
        "value": value,
        "line": line,
        "column": column
    }


def make_parser_state(tokens: list, pos: int = 0, filename: str = "test.c") -> ParserState:
    """辅助函数：创建 parser_state 字典"""
    return {
        "tokens": tokens,
        "pos": pos,
        "filename": filename
    }


class TestParseIfStmt(unittest.TestCase):
    """_parse_if_stmt 单元测试类"""

    def test_happy_path_if_only(self):
        """测试：基本的 if 语句（无 else）"""
        tokens = [
            make_token("IF", "if", 1, 1),
            make_token("LPAREN", "(", 1, 3),
            make_token("IDENTIFIER", "x", 1, 5),
            make_token("RPAREN", ")", 1, 6),
            make_token("LBRACE", "{", 1, 8),
            make_token("RBRACE", "}", 1, 9),
        ]
        parser_state = make_parser_state(tokens, 0)
        
        # Mock _parse_expression 和 _parse_block
        with patch("._parse_if_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_expr, \
             patch("._parse_if_stmt_package._parse_block_package._parse_block_src._parse_block") as mock_block:
            
            condition_ast = {"type": "EXPR", "children": [], "value": "x", "line": 1, "column": 5}
            then_block_ast = {"type": "BLOCK", "children": [], "value": None, "line": 1, "column": 8}
            
            mock_expr.return_value = condition_ast
            mock_block.side_effect = [then_block_ast]  # then block only
            
            result = _parse_if_stmt(parser_state)
            
            # 验证返回的 AST 结构
            self.assertEqual(result["type"], "IF_STMT")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(result["value"], None)
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][0], condition_ast)
            self.assertEqual(result["children"][1], then_block_ast)
            
            # 验证 pos 更新到语句结束（after RBRACE）
            self.assertEqual(parser_state["pos"], 6)
            
            # 验证调用
            mock_expr.assert_called_once()
            self.assertEqual(mock_block.call_count, 1)

    def test_happy_path_if_else(self):
        """测试：if-else 语句"""
        tokens = [
            make_token("IF", "if", 2, 1),
            make_token("LPAREN", "(", 2, 3),
            make_token("IDENTIFIER", "y", 2, 5),
            make_token("RPAREN", ")", 2, 6),
            make_token("LBRACE", "{", 2, 8),
            make_token("RBRACE", "}", 2, 9),
            make_token("ELSE", "else", 2, 11),
            make_token("LBRACE", "{", 2, 16),
            make_token("RBRACE", "}", 2, 17),
        ]
        parser_state = make_parser_state(tokens, 0)
        
        with patch("._parse_if_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_expr, \
             patch("._parse_if_stmt_package._parse_block_package._parse_block_src._parse_block") as mock_block:
            
            condition_ast = {"type": "EXPR", "children": [], "value": "y", "line": 2, "column": 5}
            then_block_ast = {"type": "BLOCK", "children": [], "value": None, "line": 2, "column": 8}
            else_block_ast = {"type": "BLOCK", "children": [], "value": None, "line": 2, "column": 16}
            
            mock_expr.return_value = condition_ast
            mock_block.side_effect = [then_block_ast, else_block_ast]
            
            result = _parse_if_stmt(parser_state)
            
            # 验证返回的 AST 结构（包含 else 分支）
            self.assertEqual(result["type"], "IF_STMT")
            self.assertEqual(len(result["children"]), 3)
            self.assertEqual(result["children"][0], condition_ast)
            self.assertEqual(result["children"][1], then_block_ast)
            self.assertEqual(result["children"][2], else_block_ast)
            
            # 验证 pos 更新到语句结束（after else block RBRACE）
            self.assertEqual(parser_state["pos"], 9)
            
            # 验证调用：_parse_block 被调用 2 次（then 和 else）
            self.assertEqual(mock_block.call_count, 2)

    def test_error_eof_before_if(self):
        """测试：错误处理 - 文件开头就是 EOF"""
        tokens = []
        parser_state = make_parser_state(tokens, 0)
        
        with self.assertRaises(SyntaxError) as ctx:
            _parse_if_stmt(parser_state)
        
        self.assertIn("预期 IF 关键字", str(ctx.exception))
        self.assertIn("已到达文件末尾", str(ctx.exception))

    def test_error_wrong_token_not_if(self):
        """测试：错误处理 - 当前 token 不是 IF"""
        tokens = [
            make_token("WHILE", "while", 3, 1),
        ]
        parser_state = make_parser_state(tokens, 0)
        
        with self.assertRaises(SyntaxError) as ctx:
            _parse_if_stmt(parser_state)
        
        self.assertIn("预期 IF 关键字", str(ctx.exception))
        self.assertIn("WHILE", str(ctx.exception))

    def test_error_eof_after_if(self):
        """测试：错误处理 - IF 之后就是 EOF（缺少 '('）"""
        tokens = [
            make_token("IF", "if", 4, 1),
        ]
        parser_state = make_parser_state(tokens, 0)
        
        with patch("._parse_if_stmt_package._parse_expression_package._parse_expression_src._parse_expression"):
            with self.assertRaises(SyntaxError) as ctx:
                _parse_if_stmt(parser_state)
            
            self.assertIn("预期 '('", str(ctx.exception))
            self.assertIn("已到达文件末尾", str(ctx.exception))

    def test_error_missing_lparen(self):
        """测试：错误处理 - IF 之后不是 '('"""
        tokens = [
            make_token("IF", "if", 5, 1),
            make_token("IDENTIFIER", "x", 5, 3),
        ]
        parser_state = make_parser_state(tokens, 0)
        
        with patch("._parse_if_stmt_package._parse_expression_package._parse_expression_src._parse_expression"):
            with self.assertRaises(SyntaxError) as ctx:
                _parse_if_stmt(parser_state)
            
            self.assertIn("预期 '('", str(ctx.exception))
            self.assertIn("IDENTIFIER", str(ctx.exception))

    def test_error_eof_after_lparen(self):
        """测试：错误处理 - '(' 之后就是 EOF（缺少条件表达式）"""
        tokens = [
            make_token("IF", "if", 6, 1),
            make_token("LPAREN", "(", 6, 3),
        ]
        parser_state = make_parser_state(tokens, 0)
        
        with patch("._parse_if_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_expr:
            # _parse_expression 会消耗 token 并更新 pos，但这里 EOF 在 LPAREN 之后
            # 实际上 _parse_expression 会在内部处理，我们模拟它不改变 pos
            mock_expr.return_value = {"type": "EXPR", "children": [], "value": None, "line": 6, "column": 4}
            
            with self.assertRaises(SyntaxError) as ctx:
                _parse_if_stmt(parser_state)
            
            self.assertIn("预期 ')'", str(ctx.exception))
            self.assertIn("已到达文件末尾", str(ctx.exception))

    def test_error_missing_rparen(self):
        """测试：错误处理 - 条件表达式之后不是 ')'"""
        tokens = [
            make_token("IF", "if", 7, 1),
            make_token("LPAREN", "(", 7, 3),
            make_token("IDENTIFIER", "x", 7, 5),
            make_token("SEMICOLON", ";", 7, 6),  # 应该是 RPAREN
        ]
        parser_state = make_parser_state(tokens, 0)
        
        with patch("._parse_if_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_expr, \
             patch("._parse_if_stmt_package._parse_block_package._parse_block_src._parse_block"):
            
            mock_expr.return_value = {"type": "EXPR", "children": [], "value": "x", "line": 7, "column": 5}
            
            with self.assertRaises(SyntaxError) as ctx:
                _parse_if_stmt(parser_state)
            
            self.assertIn("预期 ')'", str(ctx.exception))
            self.assertIn("SEMICOLON", str(ctx.exception))

    def test_error_eof_after_rparen(self):
        """测试：错误处理 - ')' 之后就是 EOF（缺少语句块）"""
        tokens = [
            make_token("IF", "if", 8, 1),
            make_token("LPAREN", "(", 8, 3),
            make_token("IDENTIFIER", "x", 8, 5),
            make_token("RPAREN", ")", 8, 6),
        ]
        parser_state = make_parser_state(tokens, 0)
        
        with patch("._parse_if_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_expr, \
             patch("._parse_if_stmt_package._parse_block_package._parse_block_src._parse_block") as mock_block:
            
            mock_expr.return_value = {"type": "EXPR", "children": [], "value": "x", "line": 8, "column": 5}
            mock_block.side_effect = SyntaxError("模拟语句块解析错误")
            
            with self.assertRaises(SyntaxError):
                _parse_if_stmt(parser_state)

    def test_pos_update_correctness(self):
        """测试：验证 pos 在解析过程中正确更新"""
        tokens = [
            make_token("IF", "if", 9, 1),
            make_token("LPAREN", "(", 9, 3),
            make_token("IDENTIFIER", "z", 9, 5),
            make_token("RPAREN", ")", 9, 6),
            make_token("LBRACE", "{", 9, 8),
            make_token("STATEMENT", "stmt", 9, 9),
            make_token("RBRACE", "}", 9, 15),
        ]
        parser_state = make_parser_state(tokens, 0)
        
        with patch("._parse_if_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_expr, \
             patch("._parse_if_stmt_package._parse_block_package._parse_block_src._parse_block") as mock_block:
            
            def expr_side_effect(state):
                state["pos"] = 3  # 消耗 IDENTIFIER
                return {"type": "EXPR", "children": [], "value": "z", "line": 9, "column": 5}
            
            def block_side_effect(state):
                state["pos"] = 7  # 消耗 LBRACE, STATEMENT, RBRACE
                return {"type": "BLOCK", "children": [], "value": None, "line": 9, "column": 8}
            
            mock_expr.side_effect = expr_side_effect
            mock_block.side_effect = block_side_effect
            
            result = _parse_if_stmt(parser_state)
            
            # 验证最终 pos 在 RBRACE 之后
            self.assertEqual(parser_state["pos"], 7)
            self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
