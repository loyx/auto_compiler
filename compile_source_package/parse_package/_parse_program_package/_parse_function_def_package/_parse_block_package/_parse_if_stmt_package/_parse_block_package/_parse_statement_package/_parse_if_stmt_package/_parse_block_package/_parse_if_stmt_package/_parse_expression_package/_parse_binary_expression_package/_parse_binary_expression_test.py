# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Dict, Any

# === relative imports ===
from ._parse_binary_expression_src import _parse_binary_expression, _get_operator_precedence


class TestParseBinaryExpression(unittest.TestCase):
    """测试 _parse_binary_expression 函数的单元测试类"""

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.src") -> Dict[str, Any]:
        """辅助方法：创建 parser_state 字典"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def _create_token(self, token_type: str, value: str = "", line: int = 1, column: int = 1) -> Dict[str, Any]:
        """辅助方法：创建 token 字典"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_ast_node(self, node_type: str, **kwargs) -> Dict[str, Any]:
        """辅助方法：创建 AST 节点"""
        node = {"type": node_type}
        node.update(kwargs)
        return node

    # ==================== Happy Path Tests ====================

    @patch('._parse_binary_expression_package._parse_primary_package._parse_primary_src._parse_primary')
    def test_single_operand_no_operator(self, mock_parse_primary):
        """测试：单个操作数，无运算符"""
        # Setup
        token_ident = self._create_token("IDENT", "x", 1, 1)
        parser_state = self._create_parser_state([token_ident], 0)
        
        expected_ast = self._create_ast_node("IDENT", value="x", line=1, column=1)
        mock_parse_primary.return_value = expected_ast
        
        # Execute
        result = _parse_binary_expression(parser_state, 0)
        
        # Verify
        self.assertEqual(result, expected_ast)
        self.assertEqual(parser_state["pos"], 1)  # pos 应前进到 token 后
        mock_parse_primary.assert_called_once_with(parser_state)

    @patch('._parse_binary_expression_package._parse_primary_package._parse_primary_src._parse_primary')
    def test_simple_binary_expression_plus(self, mock_parse_primary):
        """测试：简单二元表达式 a + b"""
        # Setup
        token_a = self._create_token("IDENT", "a", 1, 1)
        token_plus = self._create_token("PLUS", "+", 1, 3)
        token_b = self._create_token("IDENT", "b", 1, 5)
        parser_state = self._create_parser_state([token_a, token_plus, token_b], 0)
        
        left_ast = self._create_ast_node("IDENT", value="a", line=1, column=1)
        right_ast = self._create_ast_node("IDENT", value="b", line=1, column=5)
        
        # _parse_primary 会被调用两次
        mock_parse_primary.side_effect = [left_ast, right_ast]
        
        # Execute
        result = _parse_binary_expression(parser_state, 0)
        
        # Verify
        self.assertEqual(result["type"], "BINOP")
        self.assertEqual(result["op"], "PLUS")
        self.assertEqual(result["left"], left_ast)
        self.assertEqual(result["right"], right_ast)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)
        self.assertEqual(parser_state["pos"], 3)  # 所有 token 已消耗

    @patch('._parse_binary_expression_package._parse_primary_package._parse_primary_src._parse_primary')
    def test_multiple_operators_same_precedence_left_assoc(self, mock_parse_primary):
        """测试：多个相同优先级运算符（左结合）：a + b - c"""
        # Setup
        tokens = [
            self._create_token("IDENT", "a", 1, 1),
            self._create_token("PLUS", "+", 1, 3),
            self._create_token("IDENT", "b", 1, 5),
            self._create_token("MINUS", "-", 1, 7),
            self._create_token("IDENT", "c", 1, 9)
        ]
        parser_state = self._create_parser_state(tokens, 0)
        
        ast_a = self._create_ast_node("IDENT", value="a", line=1, column=1)
        ast_b = self._create_ast_node("IDENT", value="b", line=1, column=5)
        ast_c = self._create_ast_node("IDENT", value="c", line=1, column=9)
        
        # 调用顺序：a, b, c
        mock_parse_primary.side_effect = [ast_a, ast_b, ast_c]
        
        # Execute
        result = _parse_binary_expression(parser_state, 0)
        
        # Verify: (a + b) - c，左结合
        self.assertEqual(result["type"], "BINOP")
        self.assertEqual(result["op"], "MINUS")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 7)
        
        # 左操作数应该是 (a + b)
        left = result["left"]
        self.assertEqual(left["type"], "BINOP")
        self.assertEqual(left["op"], "PLUS")
        self.assertEqual(left["left"], ast_a)
        self.assertEqual(left["right"], ast_b)
        
        # 右操作数应该是 c
        self.assertEqual(result["right"], ast_c)
        self.assertEqual(parser_state["pos"], 5)

    @patch('._parse_binary_expression_package._parse_primary_package._parse_primary_src._parse_primary')
    def test_pow_right_associativity(self, mock_parse_primary):
        """测试：POW 运算符右结合：a ^ b ^ c = a ^ (b ^ c)"""
        # Setup
        tokens = [
            self._create_token("IDENT", "a", 1, 1),
            self._create_token("POW", "^", 1, 3),
            self._create_token("IDENT", "b", 1, 5),
            self._create_token("POW", "^", 1, 7),
            self._create_token("IDENT", "c", 1, 9)
        ]
        parser_state = self._create_parser_state(tokens, 0)
        
        ast_a = self._create_ast_node("IDENT", value="a", line=1, column=1)
        ast_b = self._create_ast_node("IDENT", value="b", line=1, column=5)
        ast_c = self._create_ast_node("IDENT", value="c", line=1, column=9)
        
        mock_parse_primary.side_effect = [ast_a, ast_b, ast_c]
        
        # Execute
        result = _parse_binary_expression(parser_state, 0)
        
        # Verify: a ^ (b ^ c)，右结合
        self.assertEqual(result["type"], "BINOP")
        self.assertEqual(result["op"], "POW")
        self.assertEqual(result["left"], ast_a)
        
        # 右操作数应该是 (b ^ c)
        right = result["right"]
        self.assertEqual(right["type"], "BINOP")
        self.assertEqual(right["op"], "POW")
        self.assertEqual(right["left"], ast_b)
        self.assertEqual(right["right"], ast_c)
        self.assertEqual(parser_state["pos"], 5)

    @patch('._parse_binary_expression_package._parse_primary_package._parse_primary_src._parse_primary')
    def test_operator_precedence_mixed(self, mock_parse_primary):
        """测试：混合优先级：a + b * c（乘法优先级高于加法）"""
        # Setup
        tokens = [
            self._create_token("IDENT", "a", 1, 1),
            self._create_token("PLUS", "+", 1, 3),
            self._create_token("IDENT", "b", 1, 5),
            self._create_token("MUL", "*", 1, 7),
            self._create_token("IDENT", "c", 1, 9)
        ]
        parser_state = self._create_parser_state(tokens, 0)
        
        ast_a = self._create_ast_node("IDENT", value="a", line=1, column=1)
        ast_b = self._create_ast_node("IDENT", value="b", line=1, column=5)
        ast_c = self._create_ast_node("IDENT", value="c", line=1, column=9)
        
        mock_parse_primary.side_effect = [ast_a, ast_b, ast_c]
        
        # Execute
        result = _parse_binary_expression(parser_state, 0)
        
        # Verify: a + (b * c)
        self.assertEqual(result["type"], "BINOP")
        self.assertEqual(result["op"], "PLUS")
        self.assertEqual(result["left"], ast_a)
        
        # 右操作数应该是 (b * c)
        right = result["right"]
        self.assertEqual(right["type"], "BINOP")
        self.assertEqual(right["op"], "MUL")
        self.assertEqual(right["left"], ast_b)
        self.assertEqual(right["right"], ast_c)

    # ==================== Min Precedence Boundary Tests ====================

    @patch('._parse_binary_expression_package._parse_primary_package._parse_primary_src._parse_primary')
    def test_min_precedence_filters_low_priority_ops(self, mock_parse_primary):
        """测试：min_precedence 过滤低优先级运算符"""
        # Setup: a + b，但 min_precedence=6（只接受 MUL/DIV/MOD/POW）
        tokens = [
            self._create_token("IDENT", "a", 1, 1),
            self._create_token("PLUS", "+", 1, 3),  # PLUS 优先级=5 < 6
            self._create_token("IDENT", "b", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens, 0)
        
        ast_a = self._create_ast_node("IDENT", value="a", line=1, column=1)
        ast_b = self._create_ast_node("IDENT", value="b", line=1, column=5)
        
        mock_parse_primary.side_effect = [ast_a, ast_b]
        
        # Execute
        result = _parse_binary_expression(parser_state, 6)
        
        # Verify: PLUS 被过滤，只返回左操作数
        self.assertEqual(result, ast_a)
        self.assertEqual(parser_state["pos"], 1)  # 只消耗了 a
        mock_parse_primary.assert_called_once_with(parser_state)

    @patch('._parse_binary_expression_package._parse_primary_package._parse_primary_src._parse_primary')
    def test_min_precedence_accepts_high_priority_ops(self, mock_parse_primary):
        """测试：min_precedence 接受高优先级运算符"""
        # Setup: a * b，min_precedence=5（接受优先级>=5 的运算符）
        tokens = [
            self._create_token("IDENT", "a", 1, 1),
            self._create_token("MUL", "*", 1, 3),  # MUL 优先级=6 >= 5
            self._create_token("IDENT", "b", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens, 0)
        
        ast_a = self._create_ast_node("IDENT", value="a", line=1, column=1)
        ast_b = self._create_ast_node("IDENT", value="b", line=1, column=5)
        
        mock_parse_primary.side_effect = [ast_a, ast_b]
        
        # Execute
        result = _parse_binary_expression(parser_state, 5)
        
        # Verify: MUL 被接受
        self.assertEqual(result["type"], "BINOP")
        self.assertEqual(result["op"], "MUL")
        self.assertEqual(parser_state["pos"], 3)

    # ==================== Edge Cases ====================

    @patch('._parse_binary_expression_package._parse_primary_package._parse_primary_src._parse_primary')
    def test_empty_token_list(self, mock_parse_primary):
        """测试：空 token 列表"""
        parser_state = self._create_parser_state([], 0)
        
        ast_empty = self._create_ast_node("EMPTY")
        mock_parse_primary.return_value = ast_empty
        
        # Execute
        result = _parse_binary_expression(parser_state, 0)
        
        # Verify
        self.assertEqual(result, ast_empty)
        self.assertEqual(parser_state["pos"], 0)

    @patch('._parse_binary_expression_package._parse_primary_package._parse_primary_src._parse_primary')
    def test_pos_at_end_of_tokens(self, mock_parse_primary):
        """测试：pos 已在 token 列表末尾"""
        token_a = self._create_token("IDENT", "a", 1, 1)
        parser_state = self._create_parser_state([token_a], 1)  # pos=1，已在末尾
        
        ast_a = self._create_ast_node("IDENT", value="a", line=1, column=1)
        mock_parse_primary.return_value = ast_a
        
        # Execute
        result = _parse_binary_expression(parser_state, 0)
        
        # Verify
        self.assertEqual(result, ast_a)
        self.assertEqual(parser_state["pos"], 1)

    @patch('._parse_binary_expression_package._parse_primary_package._parse_primary_src._parse_primary')
    def test_unknown_operator_type(self, mock_parse_primary):
        """测试：未知运算符类型被忽略"""
        tokens = [
            self._create_token("IDENT", "a", 1, 1),
            self._create_token("UNKNOWN", "?", 1, 3),  # 未知运算符
            self._create_token("IDENT", "b", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens, 0)
        
        ast_a = self._create_ast_node("IDENT", value="a", line=1, column=1)
        ast_b = self._create_ast_node("IDENT", value="b", line=1, column=5)
        
        mock_parse_primary.side_effect = [ast_a, ast_b]
        
        # Execute
        result = _parse_binary_expression(parser_state, 0)
        
        # Verify: UNKNOWN 被忽略，只返回 a
        self.assertEqual(result, ast_a)
        self.assertEqual(parser_state["pos"], 1)

    # ==================== Error Cases ====================

    @patch('._parse_binary_expression_package._parse_primary_package._parse_primary_src._parse_primary')
    def test_parse_primary_raises_syntax_error(self, mock_parse_primary):
        """测试：_parse_primary 抛出 SyntaxError"""
        token_invalid = self._create_token("INVALID", "???", 1, 1)
        parser_state = self._create_parser_state([token_invalid], 0)
        
        mock_parse_primary.side_effect = SyntaxError("Invalid token at line 1")
        
        # Execute & Verify
        with self.assertRaises(SyntaxError) as context:
            _parse_binary_expression(parser_state, 0)
        
        self.assertIn("Invalid token", str(context.exception))
        mock_parse_primary.assert_called_once_with(parser_state)

    @patch('._parse_binary_expression_package._parse_primary_package._parse_primary_src._parse_primary')
    def test_parse_primary_raises_on_right_operand(self, mock_parse_primary):
        """测试：解析右操作数时 _parse_primary 抛出 SyntaxError"""
        tokens = [
            self._create_token("IDENT", "a", 1, 1),
            self._create_token("PLUS", "+", 1, 3),
            self._create_token("INVALID", "???", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens, 0)
        
        ast_a = self._create_ast_node("IDENT", value="a", line=1, column=1)
        mock_parse_primary.side_effect = [ast_a, SyntaxError("Invalid right operand")]
        
        # Execute & Verify
        with self.assertRaises(SyntaxError) as context:
            _parse_binary_expression(parser_state, 0)
        
        self.assertIn("Invalid right operand", str(context.exception))
        self.assertEqual(parser_state["pos"], 2)  # 已消耗 a 和 +

    # ==================== All Operator Types Tests ====================

    @patch('._parse_binary_expression_package._parse_primary_package._parse_primary_src._parse_primary')
    def test_all_binary_operators(self, mock_parse_primary):
        """测试：所有二元运算符类型"""
        operators = [
            ("OR", "||", 1),
            ("AND", "&&", 2),
            ("EQ", "==", 3),
            ("NEQ", "!=", 3),
            ("LT", "<", 4),
            ("LE", "<=", 4),
            ("GT", ">", 4),
            ("GE", ">=", 4),
            ("PLUS", "+", 5),
            ("MINUS", "-", 5),
            ("MUL", "*", 6),
            ("DIV", "/", 6),
            ("MOD", "%", 6),
            ("POW", "^", 7)
        ]
        
        for op_type, op_value, expected_prec in operators:
            with self.subTest(operator=op_type):
                tokens = [
                    self._create_token("IDENT", "a", 1, 1),
                    self._create_token(op_type, op_value, 1, 3),
                    self._create_token("IDENT", "b", 1, 5)
                ]
                parser_state = self._create_parser_state(tokens, 0)
                
                ast_a = self._create_ast_node("IDENT", value="a", line=1, column=1)
                ast_b = self._create_ast_node("IDENT", value="b", line=1, column=5)
                
                mock_parse_primary.side_effect = [ast_a, ast_b]
                
                # Execute
                result = _parse_binary_expression(parser_state, 0)
                
                # Verify
                self.assertEqual(result["type"], "BINOP", f"Failed for {op_type}")
                self.assertEqual(result["op"], op_type, f"Failed for {op_type}")
                self.assertEqual(result["left"], ast_a)
                self.assertEqual(result["right"], ast_b)


class TestGetOperatorPrecedence(unittest.TestCase):
    """测试 _get_operator_precedence 辅助函数"""

    def test_all_known_operators(self):
        """测试：所有已知运算符的优先级"""
        expected = {
            "OR": 1,
            "AND": 2,
            "EQ": 3,
            "NEQ": 3,
            "LT": 4,
            "LE": 4,
            "GT": 4,
            "GE": 4,
            "PLUS": 5,
            "MINUS": 5,
            "MUL": 6,
            "DIV": 6,
            "MOD": 6,
            "POW": 7
        }
        
        for op_type, expected_prec in expected.items():
            with self.subTest(operator=op_type):
                result = _get_operator_precedence(op_type)
                self.assertEqual(result, expected_prec, f"Wrong precedence for {op_type}")

    def test_unknown_operator_returns_none(self):
        """测试：未知运算符返回 None"""
        unknown_ops = ["UNKNOWN", "INVALID", "", "CUSTOM"]
        
        for op in unknown_ops:
            with self.subTest(operator=op):
                result = _get_operator_precedence(op)
                self.assertIsNone(result, f"Should return None for {op}")


if __name__ == "__main__":
    unittest.main()
