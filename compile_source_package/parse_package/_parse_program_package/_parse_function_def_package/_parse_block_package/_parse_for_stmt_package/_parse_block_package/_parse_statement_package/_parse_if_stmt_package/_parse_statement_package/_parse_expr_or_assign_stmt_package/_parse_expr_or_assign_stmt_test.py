# -*- coding: utf-8 -*-
"""
单元测试文件：_parse_expr_or_assign_stmt
测试以 IDENTIFIER 开头的语句解析（表达式语句或赋值语句）
"""

from unittest.mock import patch

# 相对导入被测模块
from ._parse_expr_or_assign_stmt_src import _parse_expr_or_assign_stmt


class TestParseExprOrAssignStmt:
    """测试 _parse_expr_or_assign_stmt 函数"""

    def test_assignment_statement_simple(self):
        """测试简单赋值语句：x = 5;"""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "ASSIGN", "value": "=", "line": 1, "column": 3},
            {"type": "LITERAL", "value": 5, "line": 1, "column": 5},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 6},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        left_expr = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        right_expr = {"type": "LITERAL", "value": 5, "line": 1, "column": 5}
        
        with patch("._parse_expr_or_assign_stmt_src._parse_expression") as mock_parse_expr:
            with patch("._parse_expr_or_assign_stmt_src._expect_token") as mock_expect:
                # 第一次调用返回 left_expr，第二次调用返回 right_expr
                mock_parse_expr.side_effect = [left_expr, right_expr]
                # _expect_token 被调用两次：ASSIGN 和 SEMICOLON
                mock_expect.return_value = None
                
                result = _parse_expr_or_assign_stmt(parser_state)
                
                assert result["type"] == "ASSIGN_STMT"
                assert result["value"] == "="
                assert len(result["children"]) == 2
                assert result["children"][0] == left_expr
                assert result["children"][1] == right_expr
                assert result["line"] == 1
                assert result["column"] == 1
                
                # 验证 _parse_expression 被调用 2 次
                assert mock_parse_expr.call_count == 2
                # 验证 _expect_token 被调用 2 次 (ASSIGN 和 SEMICOLON)
                assert mock_expect.call_count == 2

    def test_expression_statement_identifier(self):
        """测试表达式语句（仅标识符）：x;"""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 2},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        left_expr = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        
        with patch("._parse_expr_or_assign_stmt_src._parse_expression") as mock_parse_expr:
            with patch("._parse_expr_or_assign_stmt_src._expect_token") as mock_expect:
                mock_parse_expr.return_value = left_expr
                mock_expect.return_value = None
                
                result = _parse_expr_or_assign_stmt(parser_state)
                
                assert result["type"] == "EXPR_STMT"
                assert result["value"] is None
                assert len(result["children"]) == 1
                assert result["children"][0] == left_expr
                assert result["line"] == 1
                assert result["column"] == 1
                
                # 验证 _parse_expression 被调用 1 次
                assert mock_parse_expr.call_count == 1
                # 验证 _expect_token 被调用 1 次 (SEMICOLON)
                assert mock_expect.call_count == 1

    def test_expression_statement_binary_op(self):
        """测试表达式语句（二元运算）：x + y;"""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "PLUS", "value": "+", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 5},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 6},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        left_expr = {
            "type": "BINARY_OP",
            "value": "+",
            "children": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 5}
            ],
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_expr_or_assign_stmt_src._parse_expression") as mock_parse_expr:
            with patch("._parse_expr_or_assign_stmt_src._expect_token") as mock_expect:
                mock_parse_expr.return_value = left_expr
                mock_expect.return_value = None
                
                result = _parse_expr_or_assign_stmt(parser_state)
                
                assert result["type"] == "EXPR_STMT"
                assert result["value"] is None
                assert len(result["children"]) == 1
                assert result["children"][0] == left_expr

    def test_assignment_statement_complex_expr(self):
        """测试赋值语句（复杂表达式）：x = a + b * c;"""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 2, "column": 1},
            {"type": "ASSIGN", "value": "=", "line": 2, "column": 3},
            {"type": "IDENTIFIER", "value": "a", "line": 2, "column": 5},
            {"type": "PLUS", "value": "+", "line": 2, "column": 7},
            {"type": "IDENTIFIER", "value": "b", "line": 2, "column": 9},
            {"type": "MULT", "value": "*", "line": 2, "column": 11},
            {"type": "IDENTIFIER", "value": "c", "line": 2, "column": 13},
            {"type": "SEMICOLON", "value": ";", "line": 2, "column": 14},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        left_expr = {"type": "IDENTIFIER", "value": "x", "line": 2, "column": 1}
        right_expr = {
            "type": "BINARY_OP",
            "value": "+",
            "line": 2,
            "column": 5
        }
        
        with patch("._parse_expr_or_assign_stmt_src._parse_expression") as mock_parse_expr:
            with patch("._parse_expr_or_assign_stmt_src._expect_token") as mock_expect:
                mock_parse_expr.side_effect = [left_expr, right_expr]
                mock_expect.return_value = None
                
                result = _parse_expr_or_assign_stmt(parser_state)
                
                assert result["type"] == "ASSIGN_STMT"
                assert result["value"] == "="
                assert len(result["children"]) == 2
                assert result["line"] == 2
                assert result["column"] == 1

    def test_assignment_statement_function_call(self):
        """测试赋值语句（函数调用）：result = func(a, b);"""
        tokens = [
            {"type": "IDENTIFIER", "value": "result", "line": 3, "column": 1},
            {"type": "ASSIGN", "value": "=", "line": 3, "column": 8},
            {"type": "IDENTIFIER", "value": "func", "line": 3, "column": 10},
            {"type": "SEMICOLON", "value": ";", "line": 3, "column": 20},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        left_expr = {"type": "IDENTIFIER", "value": "result", "line": 3, "column": 1}
        right_expr = {
            "type": "CALL",
            "value": "func",
            "line": 3,
            "column": 10
        }
        
        with patch("._parse_expr_or_assign_stmt_src._parse_expression") as mock_parse_expr:
            with patch("._parse_expr_or_assign_stmt_src._expect_token") as mock_expect:
                mock_parse_expr.side_effect = [left_expr, right_expr]
                mock_expect.return_value = None
                
                result = _parse_expr_or_assign_stmt(parser_state)
                
                assert result["type"] == "ASSIGN_STMT"
                assert result["value"] == "="
                assert len(result["children"]) == 2

    def test_pos_updated_after_parsing(self):
        """测试 pos 在解析后被正确更新"""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "ASSIGN", "value": "=", "line": 1, "column": 3},
            {"type": "LITERAL", "value": 10, "line": 1, "column": 5},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 7},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        left_expr = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        right_expr = {"type": "LITERAL", "value": 10, "line": 1, "column": 5}
        
        with patch("._parse_expr_or_assign_stmt_src._parse_expression") as mock_parse_expr:
            with patch("._parse_expr_or_assign_stmt_src._expect_token") as mock_expect:
                mock_parse_expr.side_effect = [left_expr, right_expr]
                
                def expect_token_side_effect(state, token_type):
                    state["pos"] += 1
                
                mock_expect.side_effect = expect_token_side_effect
                
                result = _parse_expr_or_assign_stmt(parser_state)
                
                # 验证 pos 被更新（至少消耗了 ASSIGN 和 SEMICOLON）
                assert parser_state["pos"] >= 2

    def test_multiple_statements_sequential(self):
        """测试连续解析多个语句"""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "ASSIGN", "value": "=", "line": 1, "column": 3},
            {"type": "LITERAL", "value": 1, "line": 1, "column": 5},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 6},
            {"type": "IDENTIFIER", "value": "y", "line": 2, "column": 1},
            {"type": "ASSIGN", "value": "=", "line": 2, "column": 3},
            {"type": "LITERAL", "value": 2, "line": 2, "column": 5},
            {"type": "SEMICOLON", "value": ";", "line": 2, "column": 6},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_expr_or_assign_stmt_src._parse_expression") as mock_parse_expr:
            with patch("._parse_expr_or_assign_stmt_src._expect_token") as mock_expect:
                # 模拟 pos 更新
                call_count = [0]
                
                def parse_expr_side_effect(state):
                    call_count[0] += 1
                    pos = state["pos"]
                    if call_count[0] == 1:
                        return {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
                    elif call_count[0] == 2:
                        return {"type": "LITERAL", "value": 1, "line": 1, "column": 5}
                    elif call_count[0] == 3:
                        return {"type": "IDENTIFIER", "value": "y", "line": 2, "column": 1}
                    else:
                        return {"type": "LITERAL", "value": 2, "line": 2, "column": 5}
                
                def expect_token_side_effect(state, token_type):
                    state["pos"] += 1
                
                mock_parse_expr.side_effect = parse_expr_side_effect
                mock_expect.side_effect = expect_token_side_effect
                
                # 解析第一个语句
                result1 = _parse_expr_or_assign_stmt(parser_state)
                assert result1["type"] == "ASSIGN_STMT"
                assert result1["children"][0]["value"] == "x"
                
                # 解析第二个语句
                result2 = _parse_expr_or_assign_stmt(parser_state)
                assert result2["type"] == "ASSIGN_STMT"
                assert result2["children"][0]["value"] == "y"

    def test_ast_node_structure_assignment(self):
        """测试 ASSIGN_STMT AST 节点结构完整性"""
        tokens = [
            {"type": "IDENTIFIER", "value": "var", "line": 5, "column": 10},
            {"type": "ASSIGN", "value": "=", "line": 5, "column": 14},
            {"type": "LITERAL", "value": 42, "line": 5, "column": 16},
            {"type": "SEMICOLON", "value": ";", "line": 5, "column": 18},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        left_expr = {"type": "IDENTIFIER", "value": "var", "line": 5, "column": 10}
        right_expr = {"type": "LITERAL", "value": 42, "line": 5, "column": 16}
        
        with patch("._parse_expr_or_assign_stmt_src._parse_expression") as mock_parse_expr:
            with patch("._parse_expr_or_assign_stmt_src._expect_token") as mock_expect:
                mock_parse_expr.side_effect = [left_expr, right_expr]
                mock_expect.return_value = None
                
                result = _parse_expr_or_assign_stmt(parser_state)
                
                # 验证所有必需字段存在
                assert "type" in result
                assert "children" in result
                assert "value" in result
                assert "line" in result
                assert "column" in result
                
                # 验证字段值
                assert result["type"] == "ASSIGN_STMT"
                assert isinstance(result["children"], list)
                assert len(result["children"]) == 2
                assert result["value"] == "="
                assert result["line"] == 5
                assert result["column"] == 10

    def test_ast_node_structure_expression(self):
        """测试 EXPR_STMT AST 节点结构完整性"""
        tokens = [
            {"type": "IDENTIFIER", "value": "func", "line": 10, "column": 5},
            {"type": "SEMICOLON", "value": ";", "line": 10, "column": 9},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        left_expr = {"type": "CALL", "value": "func", "line": 10, "column": 5}
        
        with patch("._parse_expr_or_assign_stmt_src._parse_expression") as mock_parse_expr:
            with patch("._parse_expr_or_assign_stmt_src._expect_token") as mock_expect:
                mock_parse_expr.return_value = left_expr
                mock_expect.return_value = None
                
                result = _parse_expr_or_assign_stmt(parser_state)
                
                # 验证所有必需字段存在
                assert "type" in result
                assert "children" in result
                assert "value" in result
                assert "line" in result
                assert "column" in result
                
                # 验证字段值
                assert result["type"] == "EXPR_STMT"
                assert isinstance(result["children"], list)
                assert len(result["children"]) == 1
                assert result["value"] is None
                assert result["line"] == 10
                assert result["column"] == 5

    def test_parser_state_filename_preserved(self):
        """测试 parser_state 中的 filename 不被修改"""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 2},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "my_source.py"
        }
        
        left_expr = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        
        with patch("._parse_expr_or_assign_stmt_src._parse_expression") as mock_parse_expr:
            with patch("._parse_expr_or_assign_stmt_src._expect_token") as mock_expect:
                mock_parse_expr.return_value = left_expr
                mock_expect.return_value = None
                
                _parse_expr_or_assign_stmt(parser_state)
                
                assert parser_state["filename"] == "my_source.py"

    def test_empty_tokens_after_expression(self):
        """测试表达式后无 token 的情况（应识别为表达式语句）"""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        left_expr = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        
        with patch("._parse_expr_or_assign_stmt_src._parse_expression") as mock_parse_expr:
            with patch("._parse_expr_or_assign_stmt_src._expect_token") as mock_expect:
                mock_parse_expr.return_value = left_expr
                mock_expect.return_value = None
                
                # 解析表达式后 pos 会更新，导致没有下一个 token
                mock_parse_expr.side_effect = lambda state: (
                    state.update({"pos": 1}) or left_expr
                )
                
                result = _parse_expr_or_assign_stmt(parser_state)
                
                # 应该尝试消耗 SEMICOLON（即使会失败，由 _expect_token 处理）
                assert mock_expect.called

    def test_assignment_with_string_literal(self):
        """测试赋值语句（字符串字面量）：name = "hello";"""
        tokens = [
            {"type": "IDENTIFIER", "value": "name", "line": 1, "column": 1},
            {"type": "ASSIGN", "value": "=", "line": 1, "column": 6},
            {"type": "LITERAL", "value": "hello", "line": 1, "column": 8},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 15},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        left_expr = {"type": "IDENTIFIER", "value": "name", "line": 1, "column": 1}
        right_expr = {"type": "LITERAL", "value": "hello", "line": 1, "column": 8}
        
        with patch("._parse_expr_or_assign_stmt_src._parse_expression") as mock_parse_expr:
            with patch("._parse_expr_or_assign_stmt_src._expect_token") as mock_expect:
                mock_parse_expr.side_effect = [left_expr, right_expr]
                mock_expect.return_value = None
                
                result = _parse_expr_or_assign_stmt(parser_state)
                
                assert result["type"] == "ASSIGN_STMT"
                assert result["children"][1]["value"] == "hello"

    def test_assignment_with_nested_expression(self):
        """测试赋值语句（嵌套表达式）：x = (a + b) * c;"""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "ASSIGN", "value": "=", "line": 1, "column": 3},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 5},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 15},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        left_expr = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        right_expr = {
            "type": "BINARY_OP",
            "value": "*",
            "line": 1,
            "column": 5
        }
        
        with patch("._parse_expr_or_assign_stmt_src._parse_expression") as mock_parse_expr:
            with patch("._parse_expr_or_assign_stmt_src._expect_token") as mock_expect:
                mock_parse_expr.side_effect = [left_expr, right_expr]
                mock_expect.return_value = None
                
                result = _parse_expr_or_assign_stmt(parser_state)
                
                assert result["type"] == "ASSIGN_STMT"
                assert len(result["children"]) == 2
