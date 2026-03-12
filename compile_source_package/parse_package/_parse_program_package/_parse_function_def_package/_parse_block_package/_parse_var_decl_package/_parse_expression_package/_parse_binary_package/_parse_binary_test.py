import unittest
from unittest.mock import patch

from ._parse_binary_src import _parse_binary


class TestParseBinary(unittest.TestCase):
    """测试 _parse_binary 函数的二元表达式解析逻辑。"""

    def test_single_operand_no_operator(self):
        """测试单个操作数，无运算符的情况。"""
        operand = {"type": "IDENTIFIER", "value": "x"}
        parser_state = {
            "tokens": [{"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch('._parse_binary_src._parse_unary', return_value=operand):
            with patch('._parse_binary_src._get_operator_precedence', return_value=(0, False)):
                result = _parse_binary(parser_state, 0)
                self.assertEqual(result, operand)
                self.assertEqual(parser_state["pos"], 0)

    def test_simple_binary_expression(self):
        """测试简单二元表达式：a + b"""
        operand_a = {"type": "IDENTIFIER", "value": "a"}
        operand_b = {"type": "IDENTIFIER", "value": "b"}
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 3},
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        call_count = [0]
        def parse_unary_side_effect(state):
            idx = call_count[0]
            call_count[0] += 1
            return operand_a if idx == 0 else operand_b
        
        with patch('._parse_binary_src._parse_unary', side_effect=parse_unary_side_effect):
            with patch('._parse_binary_src._get_operator_precedence') as mock_prec:
                mock_prec.return_value = (1, False)
                
                result = _parse_binary(parser_state, 0)
                
                expected = {
                    "type": "BINARY_OP",
                    "value": {"operator": "+"},
                    "children": [operand_a, operand_b],
                    "line": 1,
                    "column": 2
                }
                
                self.assertEqual(result, expected)
                self.assertEqual(parser_state["pos"], 3)

    def test_operator_precedence(self):
        """测试运算符优先级：a + b * c 应解析为 a + (b * c)"""
        operand_a = {"type": "IDENTIFIER", "value": "a"}
        operand_b = {"type": "IDENTIFIER", "value": "b"}
        operand_c = {"type": "IDENTIFIER", "value": "c"}
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 3},
                {"type": "STAR", "value": "*", "line": 1, "column": 4},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        call_count = [0]
        def parse_unary_side_effect(state):
            idx = call_count[0]
            call_count[0] += 1
            operands = [operand_a, operand_b, operand_c]
            return operands[idx] if idx < len(operands) else operands[-1]
        
        def get_precedence(token_type):
            if token_type == "PLUS":
                return (1, False)
            elif token_type == "STAR":
                return (2, False)
            return (0, False)
        
        with patch('._parse_binary_src._parse_unary', side_effect=parse_unary_side_effect):
            with patch('._parse_binary_src._get_operator_precedence', side_effect=get_precedence):
                result = _parse_binary(parser_state, 0)
                
                right_binary = {
                    "type": "BINARY_OP",
                    "value": {"operator": "*"},
                    "children": [operand_b, operand_c],
                    "line": 1,
                    "column": 4
                }
                
                expected = {
                    "type": "BINARY_OP",
                    "value": {"operator": "+"},
                    "children": [operand_a, right_binary],
                    "line": 1,
                    "column": 2
                }
                
                self.assertEqual(result, expected)

    def test_left_associativity(self):
        """测试左结合运算符：a - b - c 应解析为 (a - b) - c"""
        operand_a = {"type": "IDENTIFIER", "value": "a"}
        operand_b = {"type": "IDENTIFIER", "value": "b"}
        operand_c = {"type": "IDENTIFIER", "value": "c"}
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "MINUS", "value": "-", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 3},
                {"type": "MINUS", "value": "-", "line": 1, "column": 4},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        call_count = [0]
        def parse_unary_side_effect(state):
            idx = call_count[0]
            call_count[0] += 1
            operands = [operand_a, operand_b, operand_c]
            return operands[idx] if idx < len(operands) else operands[-1]
        
        with patch('._parse_binary_src._parse_unary', side_effect=parse_unary_side_effect):
            with patch('._parse_binary_src._get_operator_precedence') as mock_prec:
                mock_prec.return_value = (1, False)
                
                result = _parse_binary(parser_state, 0)
                
                first_minus = {
                    "type": "BINARY_OP",
                    "value": {"operator": "-"},
                    "children": [operand_a, operand_b],
                    "line": 1,
                    "column": 2
                }
                
                expected = {
                    "type": "BINARY_OP",
                    "value": {"operator": "-"},
                    "children": [first_minus, operand_c],
                    "line": 1,
                    "column": 4
                }
                
                self.assertEqual(result, expected)

    def test_right_associativity(self):
        """测试右结合运算符：a = b = c 应解析为 a = (b = c)"""
        operand_a = {"type": "IDENTIFIER", "value": "a"}
        operand_b = {"type": "IDENTIFIER", "value": "b"}
        operand_c = {"type": "IDENTIFIER", "value": "c"}
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "ASSIGN", "value": "=", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 3},
                {"type": "ASSIGN", "value": "=", "line": 1, "column": 4},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        call_count = [0]
        def parse_unary_side_effect(state):
            idx = call_count[0]
            call_count[0] += 1
            operands = [operand_a, operand_b, operand_c]
            return operands[idx] if idx < len(operands) else operands[-1]
        
        with patch('._parse_binary_src._parse_unary', side_effect=parse_unary_side_effect):
            with patch('._parse_binary_src._get_operator_precedence') as mock_prec:
                mock_prec.return_value = (0, True)
                
                result = _parse_binary(parser_state, 0)
                
                right_assign = {
                    "type": "BINARY_OP",
                    "value": {"operator": "="},
                    "children": [operand_b, operand_c],
                    "line": 1,
                    "column": 4
                }
                
                expected = {
                    "type": "BINARY_OP",
                    "value": {"operator": "="},
                    "children": [operand_a, right_assign],
                    "line": 1,
                    "column": 2
                }
                
                self.assertEqual(result, expected)

    def test_min_precedence_stops_parsing(self):
        """测试 min_precedence 参数：当运算符优先级低于阈值时停止解析。"""
        operand_a = {"type": "IDENTIFIER", "value": "a"}
        operand_b = {"type": "IDENTIFIER", "value": "b"}
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 3},
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch('._parse_binary_src._parse_unary', return_value=operand_a):
            with patch('._parse_binary_src._get_operator_precedence') as mock_prec:
                mock_prec.return_value = (1, False)
                
                result = _parse_binary(parser_state, min_precedence=2)
                
                self.assertEqual(result, operand_a)
                self.assertEqual(parser_state["pos"], 0)

    def test_multiple_operators_mixed_precedence(self):
        """测试多个不同优先级的运算符：a + b * c - d"""
        operand_a = {"type": "IDENTIFIER", "value": "a"}
        operand_b = {"type": "IDENTIFIER", "value": "b"}
        operand_c = {"type": "IDENTIFIER", "value": "c"}
        operand_d = {"type": "IDENTIFIER", "value": "d"}
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 3},
                {"type": "STAR", "value": "*", "line": 1, "column": 4},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 5},
                {"type": "MINUS", "value": "-", "line": 1, "column": 6},
                {"type": "IDENTIFIER", "value": "d", "line": 1, "column": 7},
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        call_count = [0]
        def parse_unary_side_effect(state):
            idx = call_count[0]
            call_count[0] += 1
            operands = [operand_a, operand_b, operand_c, operand_d]
            return operands[idx] if idx < len(operands) else operands[-1]
        
        def get_precedence(token_type):
            if token_type in ["PLUS", "MINUS"]:
                return (1, False)
            elif token_type == "STAR":
                return (2, False)
            return (0, False)
        
        with patch('._parse_binary_src._parse_unary', side_effect=parse_unary_side_effect):
            with patch('._parse_binary_src._get_operator_precedence', side_effect=get_precedence):
                result = _parse_binary(parser_state, 0)
                
                mul_node = {
                    "type": "BINARY_OP",
                    "value": {"operator": "*"},
                    "children": [operand_b, operand_c],
                    "line": 1,
                    "column": 4
                }
                
                add_node = {
                    "type": "BINARY_OP",
                    "value": {"operator": "+"},
                    "children": [operand_a, mul_node],
                    "line": 1,
                    "column": 2
                }
                
                expected = {
                    "type": "BINARY_OP",
                    "value": {"operator": "-"},
                    "children": [add_node, operand_d],
                    "line": 1,
                    "column": 6
                }
                
                self.assertEqual(result, expected)

    def test_mixed_precedence_and_associativity(self):
        """测试混合优先级和结合性：a = b + c"""
        operand_a = {"type": "IDENTIFIER", "value": "a"}
        operand_b = {"type": "IDENTIFIER", "value": "b"}
        operand_c = {"type": "IDENTIFIER", "value": "c"}
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "ASSIGN", "value": "=", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 3},
                {"type": "PLUS", "value": "+", "line": 1, "column": 4},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        call_count = [0]
        def parse_unary_side_effect(state):
            idx = call_count[0]
            call_count[0] += 1
            operands = [operand_a, operand_b, operand_c]
            return operands[idx] if idx < len(operands) else operands[-1]
        
        def get_precedence(token_type):
            if token_type == "PLUS":
                return (1, False)
            elif token_type == "ASSIGN":
                return (0, True)
            return (0, False)
        
        with patch('._parse_binary_package._parse_binary_src._parse_unary', side_effect=parse_unary_side_effect):
            with patch('._parse_binary_package._parse_binary_src._get_operator_precedence', side_effect=get_precedence):
                result = _parse_binary(parser_state, 0)
                
                add_node = {
                    "type": "BINARY_OP",
                    "value": {"operator": "+"},
                    "children": [operand_b, operand_c],
                    "line": 1,
                    "column": 4
                }
                
                expected = {
                    "type": "BINARY_OP",
                    "value": {"operator": "="},
                    "children": [operand_a, add_node],
                    "line": 1,
                    "column": 2
                }
                
                self.assertEqual(result, expected)

    def test_empty_tokens(self):
        """测试空 token 列表的情况。"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.c"
        }
        
        empty_operand = {"type": "IDENTIFIER", "value": "empty"}
        
        with patch('._parse_binary_package._parse_binary_src._parse_unary', return_value=empty_operand):
            result = _parse_binary(parser_state, 0)
            self.assertEqual(result, empty_operand)


if __name__ == "__main__":
    unittest.main()
