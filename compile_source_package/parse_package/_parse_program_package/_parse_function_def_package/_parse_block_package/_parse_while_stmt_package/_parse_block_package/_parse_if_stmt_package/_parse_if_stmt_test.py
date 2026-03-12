import unittest
from unittest.mock import patch, call, MagicMock
import sys

# Add mock modules to sys.modules to prevent import errors
def setup_mock_modules():
    """Setup mock modules to prevent import errors during testing."""
    mock_consume_token = MagicMock()
    mock_parse_expression = MagicMock()
    mock_parse_block = MagicMock()
    
    # Pre-register mocks in sys.modules to satisfy imports
    base_path = 'main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package'
    
    # Mock _consume_token
    consume_token_mod = MagicMock()
    consume_token_mod._consume_token = mock_consume_token
    sys.modules[f'{base_path}._consume_token_package'] = MagicMock()
    sys.modules[f'{base_path}._consume_token_package._consume_token_src'] = consume_token_mod
    
    # Mock _parse_expression and its dependencies
    parse_expr_mod = MagicMock()
    parse_expr_mod._parse_expression = mock_parse_expression
    sys.modules[f'{base_path}._parse_expression_package'] = MagicMock()
    sys.modules[f'{base_path}._parse_expression_package._parse_expression_src'] = parse_expr_mod
    
    # Mock _parse_block
    parse_block_mod = MagicMock()
    parse_block_mod._parse_block = mock_parse_block
    sys.modules[f'{base_path}._parse_block_package'] = MagicMock()
    sys.modules[f'{base_path}._parse_block_package._parse_block_src'] = parse_block_mod

setup_mock_modules()

# Ensure relative import works within the package structure
from ._parse_if_stmt_src import _parse_if_stmt

# Import the actual modules for patching
from ._consume_token_package import _consume_token_src
from ._parse_expression_package import _parse_expression_src
from ._parse_block_package import _parse_block_src


class TestParseIfStmt(unittest.TestCase):
    """单元测试：_parse_if_stmt 函数"""

    @patch.object(_consume_token_src, '_consume_token')
    @patch.object(_parse_expression_src, '_parse_expression')
    @patch.object(_parse_block_src, '_parse_block')
    def test_if_stmt_without_else(self, mock_parse_block, mock_parse_expression, mock_consume_token):
        """测试：解析不含 else 的 if 语句"""
        # 准备 token 序列
        tokens = [
            {"type": "IF", "value": "if", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 5},
            {"type": "LBRACE", "value": "{", "line": 1, "column": 7},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 8},
        ]

        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        # 设置 mock 返回值
        condition_ast = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4}
        then_block_ast = {"type": "BLOCK", "children": [], "line": 1, "column": 7}

        mock_parse_expression.return_value = condition_ast
        mock_parse_block.return_value = then_block_ast

        # _consume_token 返回更新后的 parser_state
        def consume_token_side_effect(state, token_type):
            new_state = state.copy()
            new_state["pos"] = state["pos"] + 1
            return new_state

        mock_consume_token.side_effect = consume_token_side_effect

        # 调用被测函数
        result = _parse_if_stmt(parser_state)

        # 验证返回的 AST 结构
        self.assertEqual(result["type"], "IF_STMT")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0], condition_ast)
        self.assertEqual(result["children"][1], then_block_ast)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)

        # 验证 _consume_token 被调用 3 次：IF, LPAREN, RPAREN
        self.assertEqual(mock_consume_token.call_count, 3)
        mock_consume_token.assert_has_calls([
            call(parser_state, "IF"),
            call(mock_consume_token.return_value, "LPAREN"),
            call(mock_consume_token.return_value, "RPAREN"),
        ])

        # 验证 _parse_expression 和 _parse_block 各调用 1 次
        mock_parse_expression.assert_called_once()
        self.assertEqual(mock_parse_block.call_count, 1)

    @patch('_parse_if_stmt_src._consume_token')
    @patch('_parse_if_stmt_src._parse_expression')
    @patch('_parse_if_stmt_src._parse_block')
    def test_if_stmt_with_else(self, mock_parse_block, mock_parse_expression, mock_consume_token):
        """测试：解析含 else 的 if 语句"""
        # 准备 token 序列（包含 ELSE）
        tokens = [
            {"type": "IF", "value": "if", "line": 2, "column": 5},
            {"type": "LPAREN", "value": "(", "line": 2, "column": 7},
            {"type": "NUMBER", "value": "1", "line": 2, "column": 8},
            {"type": "RPAREN", "value": ")", "line": 2, "column": 9},
            {"type": "LBRACE", "value": "{", "line": 2, "column": 11},
            {"type": "RBRACE", "value": "}", "line": 2, "column": 12},
            {"type": "ELSE", "value": "else", "line": 3, "column": 1},
            {"type": "LBRACE", "value": "{", "line": 3, "column": 6},
            {"type": "RBRACE", "value": "}", "line": 3, "column": 7},
        ]

        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        # 设置 mock 返回值
        condition_ast = {"type": "LITERAL", "value": "1", "line": 2, "column": 8}
        then_block_ast = {"type": "BLOCK", "children": [], "line": 2, "column": 11}
        else_block_ast = {"type": "BLOCK", "children": [], "line": 3, "column": 6}

        mock_parse_expression.return_value = condition_ast
        mock_parse_block.side_effect = [then_block_ast, else_block_ast]

        # _consume_token 返回更新后的 parser_state
        def consume_token_side_effect(state, token_type):
            new_state = state.copy()
            new_state["pos"] = state["pos"] + 1
            return new_state

        mock_consume_token.side_effect = consume_token_side_effect

        # 调用被测函数
        result = _parse_if_stmt(parser_state)

        # 验证返回的 AST 结构（包含 else 块）
        self.assertEqual(result["type"], "IF_STMT")
        self.assertEqual(len(result["children"]), 3)
        self.assertEqual(result["children"][0], condition_ast)
        self.assertEqual(result["children"][1], then_block_ast)
        self.assertEqual(result["children"][2], else_block_ast)
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 5)

        # 验证 _consume_token 被调用 4 次：IF, LPAREN, RPAREN, ELSE
        self.assertEqual(mock_consume_token.call_count, 4)

        # 验证 _parse_block 被调用 2 次（then 和 else）
        self.assertEqual(mock_parse_block.call_count, 2)

    @patch('_parse_if_stmt_src._consume_token')
    @patch('_parse_if_stmt_src._parse_expression')
    @patch('_parse_if_stmt_src._parse_block')
    def test_empty_tokens_raises_error(self, mock_parse_block, mock_parse_expression, mock_consume_token):
        """测试：空 token 列表抛出 SyntaxError"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }

        # 验证抛出 SyntaxError
        with self.assertRaises(SyntaxError) as context:
            _parse_if_stmt(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))
        # 验证没有调用任何子函数
        mock_consume_token.assert_not_called()
        mock_parse_expression.assert_not_called()
        mock_parse_block.assert_not_called()

    @patch('_parse_if_stmt_src._consume_token')
    @patch('_parse_if_stmt_src._parse_expression')
    @patch('_parse_if_stmt_src._parse_block')
    def test_pos_beyond_tokens_raises_error(self, mock_parse_block, mock_parse_expression, mock_consume_token):
        """测试：pos 超出 token 列表范围抛出 SyntaxError"""
        tokens = [{"type": "IF", "value": "if", "line": 1, "column": 1}]

        parser_state = {
            "tokens": tokens,
            "pos": 5,  # pos 超出范围
            "filename": "test.py"
        }

        # 验证抛出 SyntaxError
        with self.assertRaises(SyntaxError) as context:
            _parse_if_stmt(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))

    @patch('_parse_if_stmt_src._consume_token')
    @patch('_parse_if_stmt_src._parse_expression')
    @patch('_parse_if_stmt_src._parse_block')
    def test_consume_token_failure_propagates(self, mock_parse_block, mock_parse_expression, mock_consume_token):
        """测试：_consume_token 抛出异常时正确传播"""
        tokens = [
            {"type": "IF", "value": "if", "line": 1, "column": 1},
        ]

        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        # 模拟 _consume_token 在消费 LPAREN 时失败
        def consume_token_side_effect(state, token_type):
            if token_type == "LPAREN":
                raise SyntaxError("Expected LPAREN but found something else")
            new_state = state.copy()
            new_state["pos"] = state["pos"] + 1
            return new_state

        mock_consume_token.side_effect = consume_token_side_effect

        # 验证异常传播
        with self.assertRaises(SyntaxError) as context:
            _parse_if_stmt(parser_state)

        self.assertIn("Expected LPAREN", str(context.exception))

    @patch('_parse_if_stmt_src._consume_token')
    @patch('_parse_if_stmt_src._parse_expression')
    @patch('_parse_if_stmt_src._parse_block')
    def test_complex_condition_expression(self, mock_parse_block, mock_parse_expression, mock_consume_token):
        """测试：复杂条件表达式（如二元运算）"""
        tokens = [
            {"type": "IF", "value": "if", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4},
            {"type": "OPERATOR", "value": ">", "line": 1, "column": 6},
            {"type": "NUMBER", "value": "0", "line": 1, "column": 8},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 9},
            {"type": "LBRACE", "value": "{", "line": 1, "column": 11},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 12},
        ]

        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        # 模拟复杂条件表达式 AST
        condition_ast = {
            "type": "BINARY_OP",
            "operator": ">",
            "left": {"type": "IDENTIFIER", "value": "x"},
            "right": {"type": "LITERAL", "value": "0"},
            "line": 1,
            "column": 4
        }
        then_block_ast = {"type": "BLOCK", "children": [], "line": 1, "column": 11}

        mock_parse_expression.return_value = condition_ast
        mock_parse_block.return_value = then_block_ast

        def consume_token_side_effect(state, token_type):
            new_state = state.copy()
            new_state["pos"] = state["pos"] + 1
            return new_state

        mock_consume_token.side_effect = consume_token_side_effect

        # 调用被测函数
        result = _parse_if_stmt(parser_state)

        # 验证条件表达式 AST 被正确包含
        self.assertEqual(result["type"], "IF_STMT")
        self.assertEqual(result["children"][0], condition_ast)
        self.assertEqual(result["children"][1], then_block_ast)

    @patch('_parse_if_stmt_src._consume_token')
    @patch('_parse_if_stmt_src._parse_expression')
    @patch('_parse_if_stmt_src._parse_block')
    def test_nested_block_statements(self, mock_parse_block, mock_parse_expression, mock_consume_token):
        """测试：then 块包含多条语句"""
        tokens = [
            {"type": "IF", "value": "if", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "flag", "line": 1, "column": 4},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 8},
            {"type": "LBRACE", "value": "{", "line": 1, "column": 10},
            {"type": "IDENTIFIER", "value": "stmt1", "line": 2, "column": 2},
            {"type": "IDENTIFIER", "value": "stmt2", "line": 3, "column": 2},
            {"type": "RBRACE", "value": "}", "line": 4, "column": 1},
        ]

        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        condition_ast = {"type": "IDENTIFIER", "value": "flag", "line": 1, "column": 4}
        then_block_ast = {
            "type": "BLOCK",
            "children": [
                {"type": "EXPR_STMT", "value": "stmt1"},
                {"type": "EXPR_STMT", "value": "stmt2"}
            ],
            "line": 1,
            "column": 10
        }

        mock_parse_expression.return_value = condition_ast
        mock_parse_block.return_value = then_block_ast

        def consume_token_side_effect(state, token_type):
            new_state = state.copy()
            new_state["pos"] = state["pos"] + 1
            return new_state

        mock_consume_token.side_effect = consume_token_side_effect

        # 调用被测函数
        result = _parse_if_stmt(parser_state)

        # 验证块中包含多条语句
        self.assertEqual(result["type"], "IF_STMT")
        self.assertEqual(len(result["children"][1]["children"]), 2)

    @patch('_parse_if_stmt_src._consume_token')
    @patch('_parse_if_stmt_src._parse_expression')
    @patch('_parse_if_stmt_src._parse_block')
    def test_source_location_preserved(self, mock_parse_block, mock_parse_expression, mock_consume_token):
        """测试：AST 节点保留正确的源代码位置信息"""
        tokens = [
            {"type": "IF", "value": "if", "line": 10, "column": 25},
            {"type": "LPAREN", "value": "(", "line": 10, "column": 27},
            {"type": "IDENTIFIER", "value": "x", "line": 10, "column": 28},
            {"type": "RPAREN", "value": ")", "line": 10, "column": 29},
            {"type": "LBRACE", "value": "{", "line": 10, "column": 31},
            {"type": "RBRACE", "value": "}", "line": 10, "column": 32},
        ]

        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        condition_ast = {"type": "IDENTIFIER", "value": "x", "line": 10, "column": 28}
        then_block_ast = {"type": "BLOCK", "children": [], "line": 10, "column": 31}

        mock_parse_expression.return_value = condition_ast
        mock_parse_block.return_value = then_block_ast

        def consume_token_side_effect(state, token_type):
            new_state = state.copy()
            new_state["pos"] = state["pos"] + 1
            return new_state

        mock_consume_token.side_effect = consume_token_side_effect

        # 调用被测函数
        result = _parse_if_stmt(parser_state)

        # 验证 IF_STMT 节点使用 IF token 的位置
        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 25)


if __name__ == "__main__":
    unittest.main()
