# -*- coding: utf-8 -*-
"""
单元测试文件：_parse_while_stmt
测试 while 语句解析函数的正确性
"""

import unittest
from unittest.mock import patch, call

# 相对导入被测模块
from ._parse_while_stmt_src import _parse_while_stmt


class TestParseWhileStmt(unittest.TestCase):
    """测试 _parse_while_stmt 函数"""

    def setUp(self):
        """每个测试前的准备工作"""
        self.maxDiff = None

    def test_happy_path_basic_while(self):
        """测试基本 while 语句解析：while ( expr ) block"""
        # 构造 parser_state
        while_token = {"type": "WHILE", "value": "while", "line": 10, "column": 5}
        lparen_token = {"type": "LPAREN", "value": "(", "line": 10, "column": 11}
        rparen_token = {"type": "RPAREN", "value": ")", "line": 10, "column": 20}
        
        parser_state = {
            "tokens": [while_token, lparen_token, rparen_token],
            "pos": 0,
            "filename": "test.c"
        }
        
        # Mock 子函数
        mock_condition_ast = {"type": "EXPR", "value": "x > 0", "line": 10, "column": 12}
        mock_body_ast = {"type": "BLOCK", "children": [], "line": 10, "column": 22}
        
        with patch("._expect_token_package._expect_token_src._expect_token") as mock_expect, \
             patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr, \
             patch("._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
            
            mock_parse_expr.return_value = mock_condition_ast
            mock_parse_block.return_value = mock_body_ast
            
            result = _parse_while_stmt(parser_state)
            
            # 验证返回的 AST 节点结构
            self.assertEqual(result["type"], "WHILE_STMT")
            self.assertEqual(result["value"], "while")
            self.assertEqual(result["line"], 10)
            self.assertEqual(result["column"], 5)
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][0], mock_condition_ast)
            self.assertEqual(result["children"][1], mock_body_ast)
            
            # 验证 _expect_token 被调用 3 次 (WHILE, LPAREN, RPAREN)
            self.assertEqual(mock_expect.call_count, 3)
            mock_expect.assert_has_calls([
                call(parser_state, "WHILE"),
                call(parser_state, "LPAREN"),
                call(parser_state, "RPAREN")
            ])
            
            # 验证 _parse_expression 和 _parse_block 各被调用 1 次
            mock_parse_expr.assert_called_once_with(parser_state)
            mock_parse_block.assert_called_once_with(parser_state)

    def test_happy_path_complex_condition(self):
        """测试复杂条件表达式的 while 语句"""
        while_token = {"type": "WHILE", "value": "while", "line": 5, "column": 1}
        parser_state = {
            "tokens": [while_token],
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_condition_ast = {
            "type": "BINARY_EXPR",
            "children": [
                {"type": "IDENT", "value": "count"},
                {"type": "LITERAL", "value": "10"}
            ],
            "value": "<",
            "line": 5,
            "column": 8
        }
        mock_body_ast = {
            "type": "BLOCK",
            "children": [
                {"type": "STMT", "value": "count++"}
            ],
            "line": 5,
            "column": 20
        }
        
        with patch("._expect_token_package._expect_token_src._expect_token"), \
             patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr, \
             patch("._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
            
            mock_parse_expr.return_value = mock_condition_ast
            mock_parse_block.return_value = mock_body_ast
            
            result = _parse_while_stmt(parser_state)
            
            self.assertEqual(result["type"], "WHILE_STMT")
            self.assertEqual(result["children"][0], mock_condition_ast)
            self.assertEqual(result["children"][1], mock_body_ast)

    def test_happy_path_nested_while(self):
        """测试嵌套 while 语句作为循环体"""
        while_token = {"type": "WHILE", "value": "while", "line": 1, "column": 0}
        parser_state = {
            "tokens": [while_token],
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_condition_ast = {"type": "EXPR", "value": "i < 10"}
        nested_while_ast = {"type": "WHILE_STMT", "value": "while", "children": []}
        mock_body_ast = {
            "type": "BLOCK",
            "children": [nested_while_ast],
            "line": 1,
            "column": 15
        }
        
        with patch("._expect_token_package._expect_token_src._expect_token"), \
             patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr, \
             patch("._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
            
            mock_parse_expr.return_value = mock_condition_ast
            mock_parse_block.return_value = mock_body_ast
            
            result = _parse_while_stmt(parser_state)
            
            self.assertEqual(result["type"], "WHILE_STMT")
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][1]["children"][0], nested_while_ast)

    def test_boundary_empty_block(self):
        """测试空代码块的 while 语句"""
        while_token = {"type": "WHILE", "value": "while", "line": 1, "column": 0}
        parser_state = {
            "tokens": [while_token],
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_condition_ast = {"type": "EXPR", "value": "true"}
        mock_body_ast = {"type": "BLOCK", "children": [], "line": 1, "column": 15}
        
        with patch("._expect_token_package._expect_token_src._expect_token"), \
             patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr, \
             patch("._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
            
            mock_parse_expr.return_value = mock_condition_ast
            mock_parse_block.return_value = mock_body_ast
            
            result = _parse_while_stmt(parser_state)
            
            self.assertEqual(result["type"], "WHILE_STMT")
            self.assertEqual(result["children"][1]["children"], [])

    def test_boundary_token_missing_line_column(self):
        """测试 WHILE token 缺少 line/column 信息时的默认值处理"""
        while_token = {"type": "WHILE", "value": "while"}  # 没有 line 和 column
        parser_state = {
            "tokens": [while_token],
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_condition_ast = {"type": "EXPR"}
        mock_body_ast = {"type": "BLOCK", "children": []}
        
        with patch("._expect_token_package._expect_token_src._expect_token"), \
             patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr, \
             patch("._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
            
            mock_parse_expr.return_value = mock_condition_ast
            mock_parse_block.return_value = mock_body_ast
            
            result = _parse_while_stmt(parser_state)
            
            # 应该使用默认值 0
            self.assertEqual(result["line"], 0)
            self.assertEqual(result["column"], 0)

    def test_error_expect_token_raises_syntax_error(self):
        """测试当 _expect_token 抛出 SyntaxError 时的异常传播"""
        while_token = {"type": "WHILE", "value": "while", "line": 1, "column": 0}
        parser_state = {
            "tokens": [while_token],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("._expect_token_package._expect_token_src._expect_token") as mock_expect:
            mock_expect.side_effect = SyntaxError("Expected WHILE token")
            
            with self.assertRaises(SyntaxError) as context:
                _parse_while_stmt(parser_state)
            
            self.assertEqual(str(context.exception), "Expected WHILE token")
            # 验证 _expect_token 只被调用了一次（在 WHILE 处失败）
            mock_expect.assert_called_once_with(parser_state, "WHILE")

    def test_error_parse_expression_raises(self):
        """测试当 _parse_expression 抛出异常时的异常传播"""
        while_token = {"type": "WHILE", "value": "while", "line": 1, "column": 0}
        parser_state = {
            "tokens": [while_token],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("._expect_token_package._expect_token_src._expect_token"), \
             patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            
            mock_parse_expr.side_effect = SyntaxError("Invalid expression")
            
            with self.assertRaises(SyntaxError) as context:
                _parse_while_stmt(parser_state)
            
            self.assertEqual(str(context.exception), "Invalid expression")

    def test_error_parse_block_raises(self):
        """测试当 _parse_block 抛出异常时的异常传播"""
        while_token = {"type": "WHILE", "value": "while", "line": 1, "column": 0}
        parser_state = {
            "tokens": [while_token],
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_condition_ast = {"type": "EXPR", "value": "true"}
        
        with patch("._expect_token_package._expect_token_src._expect_token"), \
             patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr, \
             patch("._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
            
            mock_parse_expr.return_value = mock_condition_ast
            mock_parse_block.side_effect = SyntaxError("Invalid block")
            
            with self.assertRaises(SyntaxError) as context:
                _parse_while_stmt(parser_state)
            
            self.assertEqual(str(context.exception), "Invalid block")
            # 验证 _parse_block 确实被调用了
            mock_parse_block.assert_called_once_with(parser_state)

    def test_parser_state_pos_updated(self):
        """测试 parser_state 的 pos 被正确更新（通过 mock 验证调用顺序）"""
        while_token = {"type": "WHILE", "value": "while", "line": 1, "column": 0}
        parser_state = {
            "tokens": [while_token],
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_condition_ast = {"type": "EXPR"}
        mock_body_ast = {"type": "BLOCK", "children": []}
        
        call_order = []
        
        def track_expect(state, token_type):
            call_order.append(f"expect_{token_type}")
            state["pos"] = state.get("pos", 0) + 1
        
        def track_parse_expr(state):
            call_order.append("parse_expr")
            state["pos"] = state.get("pos", 0) + 1
            return mock_condition_ast
        
        def track_parse_block(state):
            call_order.append("parse_block")
            state["pos"] = state.get("pos", 0) + 1
            return mock_body_ast
        
        with patch("._expect_token_package._expect_token_src._expect_token", side_effect=track_expect), \
             patch("._parse_expression_package._parse_expression_src._parse_expression", side_effect=track_parse_expr), \
             patch("._parse_block_package._parse_block_src._parse_block", side_effect=track_parse_block):
            
            _parse_while_stmt(parser_state)
            
            # 验证调用顺序：WHILE -> LPAREN -> parse_expr -> RPAREN -> parse_block
            expected_order = ["expect_WHILE", "expect_LPAREN", "parse_expr", "expect_RPAREN", "parse_block"]
            self.assertEqual(call_order, expected_order)
            
            # 验证 pos 被更新了 5 次
            self.assertEqual(parser_state["pos"], 5)

    def test_ast_node_complete_structure(self):
        """测试返回的 AST 节点包含所有必需字段"""
        while_token = {"type": "WHILE", "value": "while", "line": 100, "column": 50}
        parser_state = {
            "tokens": [while_token],
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_condition_ast = {"type": "EXPR", "value": "x"}
        mock_body_ast = {"type": "BLOCK", "children": []}
        
        with patch("._expect_token_package._expect_token_src._expect_token"), \
             patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr, \
             patch("._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
            
            mock_parse_expr.return_value = mock_condition_ast
            mock_parse_block.return_value = mock_body_ast
            
            result = _parse_while_stmt(parser_state)
            
            # 验证所有必需字段存在
            self.assertIn("type", result)
            self.assertIn("children", result)
            self.assertIn("value", result)
            self.assertIn("line", result)
            self.assertIn("column", result)
            
            # 验证字段值正确
            self.assertEqual(result["type"], "WHILE_STMT")
            self.assertEqual(result["value"], "while")
            self.assertEqual(result["line"], 100)
            self.assertEqual(result["column"], 50)
            self.assertIsInstance(result["children"], list)
            self.assertEqual(len(result["children"]), 2)


if __name__ == "__main__":
    unittest.main()
