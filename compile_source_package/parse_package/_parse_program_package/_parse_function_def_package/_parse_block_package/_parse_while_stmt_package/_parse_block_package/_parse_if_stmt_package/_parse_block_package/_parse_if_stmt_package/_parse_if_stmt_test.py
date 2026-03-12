# === std / third-party imports ===
import unittest
from unittest.mock import patch

# === sub function imports ===
# Relative import from the same package
from ._parse_if_stmt_src import _parse_if_stmt


class TestParseIfStmt(unittest.TestCase):
    """测试 _parse_if_stmt 函数的单元测试类"""

    def test_if_stmt_with_else(self):
        """测试完整的 if-else 语句解析"""
        # 准备测试数据
        if_token = {"type": "IF", "line": 10, "column": 5}
        lparen_token = {"type": "LPAREN", "line": 10, "column": 7}
        rparen_token = {"type": "RPAREN", "line": 10, "column": 15}
        else_token = {"type": "ELSE", "line": 11, "column": 5}
        
        tokens = [if_token, lparen_token, rparen_token, else_token]
        parser_state = {"tokens": tokens, "pos": 0}
        
        # 准备 mock 返回值
        condition_ast = {"type": "EXPR", "children": [], "line": 10, "column": 8}
        then_block_ast = {"type": "BLOCK", "children": [], "line": 10, "column": 17}
        else_block_ast = {"type": "BLOCK", "children": [], "line": 11, "column": 9}
        
        # 执行测试
        with patch("._consume_token_package._consume_token_src._consume_token") as mock_consume, \
             patch("._parse_expr_package._parse_expr_src._parse_expr") as mock_parse_expr, \
             patch("._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
            
            # 配置 _consume_token 的返回值序列
            mock_consume.side_effect = [if_token, lparen_token, rparen_token, else_token]
            mock_parse_expr.return_value = condition_ast
            mock_parse_block.side_effect = [then_block_ast, else_block_ast]
            
            result = _parse_if_stmt(parser_state)
        
        # 验证结果
        self.assertEqual(result["type"], "IF")
        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 5)
        self.assertEqual(len(result["children"]), 3)
        self.assertEqual(result["children"][0], condition_ast)
        self.assertEqual(result["children"][1], then_block_ast)
        self.assertEqual(result["children"][2], else_block_ast)
        
        # 验证调用次数
        self.assertEqual(mock_consume.call_count, 4)
        self.assertEqual(mock_parse_expr.call_count, 1)
        self.assertEqual(mock_parse_block.call_count, 2)

    def test_if_stmt_without_else(self):
        """测试没有 else 子句的 if 语句解析"""
        # 准备测试数据
        if_token = {"type": "IF", "line": 5, "column": 1}
        lparen_token = {"type": "LPAREN", "line": 5, "column": 3}
        rparen_token = {"type": "RPAREN", "line": 5, "column": 10}
        
        tokens = [if_token, lparen_token, rparen_token]
        parser_state = {"tokens": tokens, "pos": 0}
        
        # 准备 mock 返回值
        condition_ast = {"type": "EXPR", "children": [], "line": 5, "column": 4}
        then_block_ast = {"type": "BLOCK", "children": [], "line": 5, "column": 12}
        
        # 执行测试
        with patch("._consume_token_package._consume_token_src._consume_token") as mock_consume, \
             patch("._parse_expr_package._parse_expr_src._parse_expr") as mock_parse_expr, \
             patch("._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
            
            mock_consume.side_effect = [if_token, lparen_token, rparen_token]
            mock_parse_expr.return_value = condition_ast
            mock_parse_block.return_value = then_block_ast
            
            result = _parse_if_stmt(parser_state)
        
        # 验证结果
        self.assertEqual(result["type"], "IF")
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 1)
        self.assertEqual(len(result["children"]), 3)
        self.assertEqual(result["children"][0], condition_ast)
        self.assertEqual(result["children"][1], then_block_ast)
        self.assertIsNone(result["children"][2])
        
        # 验证调用次数（只消费 3 个 token，解析 1 个 block）
        self.assertEqual(mock_consume.call_count, 3)
        self.assertEqual(mock_parse_block.call_count, 1)

    def test_if_stmt_advances_parser_position(self):
        """测试 parser_state 的 pos 被正确推进"""
        if_token = {"type": "IF", "line": 1, "column": 1}
        lparen_token = {"type": "LPAREN", "line": 1, "column": 3}
        rparen_token = {"type": "RPAREN", "line": 1, "column": 8}
        
        tokens = [if_token, lparen_token, rparen_token]
        parser_state = {"tokens": tokens, "pos": 0}
        
        condition_ast = {"type": "EXPR", "children": [], "line": 1, "column": 4}
        then_block_ast = {"type": "BLOCK", "children": [], "line": 1, "column": 10}
        
        with patch("._consume_token_package._consume_token_src._consume_token") as mock_consume, \
             patch("._parse_expr_package._parse_expr_src._parse_expr") as mock_parse_expr, \
             patch("._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
            
            # 模拟 _consume_token 会修改 parser_state['pos']
            def consume_side_effect(state, expected_type=None):
                token = tokens[state["pos"]]
                state["pos"] += 1
                return token
            
            mock_consume.side_effect = consume_side_effect
            mock_parse_expr.return_value = condition_ast
            mock_parse_block.return_value = then_block_ast
            
            result = _parse_if_stmt(parser_state)
        
        # 验证 pos 被推进到 3（消费了 IF, LPAREN, RPAREN）
        self.assertEqual(parser_state["pos"], 3)

    def test_consume_token_with_expected_type(self):
        """测试 _consume_token 被调用时传入正确的 expected_type"""
        if_token = {"type": "IF", "line": 1, "column": 1}
        lparen_token = {"type": "LPAREN", "line": 1, "column": 3}
        rparen_token = {"type": "RPAREN", "line": 1, "column": 8}
        else_token = {"type": "ELSE", "line": 2, "column": 1}
        
        tokens = [if_token, lparen_token, rparen_token, else_token]
        parser_state = {"tokens": tokens, "pos": 0}
        
        condition_ast = {"type": "EXPR", "children": [], "line": 1, "column": 4}
        then_block_ast = {"type": "BLOCK", "children": [], "line": 1, "column": 10}
        else_block_ast = {"type": "BLOCK", "children": [], "line": 2, "column": 6}
        
        with patch("._consume_token_package._consume_token_src._consume_token") as mock_consume, \
             patch("._parse_expr_package._parse_expr_src._parse_expr") as mock_parse_expr, \
             patch("._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
            
            mock_consume.side_effect = [if_token, lparen_token, rparen_token, else_token]
            mock_parse_expr.return_value = condition_ast
            mock_parse_block.side_effect = [then_block_ast, else_block_ast]
            
            result = _parse_if_stmt(parser_state)
        
        # 验证 _consume_token 被调用时传入了正确的 expected_type
        calls = mock_consume.call_args_list
        self.assertEqual(calls[0][0][1], "IF")
        self.assertEqual(calls[1][0][1], "LPAREN")
        self.assertEqual(calls[2][0][1], "RPAREN")
        self.assertEqual(calls[3][0][1], "ELSE")


class TestParseIfStmtErrorHandling(unittest.TestCase):
    """测试 _parse_if_stmt 的错误处理"""

    def test_missing_lparen_raises_syntax_error(self):
        """测试缺少 LPAREN 时抛出 SyntaxError"""
        if_token = {"type": "IF", "line": 1, "column": 1}
        tokens = [if_token]
        parser_state = {"tokens": tokens, "pos": 0}
        
        with patch("._consume_token_package._consume_token_src._consume_token") as mock_consume:
            # 第一次调用返回 IF token，第二次调用应该抛出 SyntaxError
            mock_consume.side_effect = [
                if_token,
                SyntaxError("Expected LPAREN")
            ]
            
            with self.assertRaises(SyntaxError):
                _parse_if_stmt(parser_state)

    def test_missing_rparen_raises_syntax_error(self):
        """测试缺少 RPAREN 时抛出 SyntaxError"""
        if_token = {"type": "IF", "line": 1, "column": 1}
        lparen_token = {"type": "LPAREN", "line": 1, "column": 3}
        tokens = [if_token, lparen_token]
        parser_state = {"tokens": tokens, "pos": 0}
        
        condition_ast = {"type": "EXPR", "children": [], "line": 1, "column": 4}
        
        with patch("._consume_token_package._consume_token_src._consume_token") as mock_consume, \
             patch("._parse_expr_package._parse_expr_src._parse_expr") as mock_parse_expr:
            
            mock_consume.side_effect = [if_token, lparen_token, SyntaxError("Expected RPAREN")]
            mock_parse_expr.return_value = condition_ast
            
            with self.assertRaises(SyntaxError):
                _parse_if_stmt(parser_state)

    def test_consume_token_propagates_syntax_error(self):
        """测试 _consume_token 抛出的 SyntaxError 被正确传播"""
        if_token = {"type": "IF", "line": 1, "column": 1}
        tokens = [if_token]
        parser_state = {"tokens": tokens, "pos": 0}
        
        with patch("._consume_token_package._consume_token_src._consume_token") as mock_consume:
            mock_consume.side_effect = SyntaxError("Unexpected token")
            
            with self.assertRaises(SyntaxError) as context:
                _parse_if_stmt(parser_state)
            
            self.assertEqual(str(context.exception), "Unexpected token")


if __name__ == "__main__":
    unittest.main()
