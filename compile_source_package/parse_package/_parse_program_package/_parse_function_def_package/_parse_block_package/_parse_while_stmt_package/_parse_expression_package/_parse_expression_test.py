# === std / third-party imports ===
import pytest
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_src import _parse_expression

# === Test Helpers ===
def make_parser_state(tokens: list) -> Dict[str, Any]:
    """Create a parser state from a list of token dicts."""
    return {"tokens": tokens, "pos": 0, "filename": "test.src"}

def make_token(token_type: str, value: Any, line: int = 1, column: int = 1) -> Dict[str, Any]:
    """Create a token dict."""
    return {"type": token_type, "value": value, "line": line, "column": column}

# === Test Cases ===
class TestParseExpressionLiterals:
    """测试字面量解析。"""
    
    def test_parse_integer_literal(self):
        tokens = [make_token("INTEGER", 42)]
        state = make_parser_state(tokens)
        result = _parse_expression(state)
        assert result == {"type": "LITERAL", "value": 42, "children": [], "line": 1, "column": 1}
        assert state["pos"] == 1
    
    def test_parse_float_literal(self):
        tokens = [make_token("FLOAT", 3.14)]
        state = make_parser_state(tokens)
        result = _parse_expression(state)
        assert result == {"type": "LITERAL", "value": 3.14, "children": [], "line": 1, "column": 1}
    
    def test_parse_string_literal(self):
        tokens = [make_token("STRING", "hello")]
        state = make_parser_state(tokens)
        result = _parse_expression(state)
        assert result == {"type": "LITERAL", "value": "hello", "children": [], "line": 1, "column": 1}
    
    def test_parse_boolean_literal(self):
        tokens = [make_token("BOOLEAN", True)]
        state = make_parser_state(tokens)
        result = _parse_expression(state)
        assert result == {"type": "LITERAL", "value": True, "children": [], "line": 1, "column": 1}


class TestParseExpressionIdentifiers:
    """测试标识符解析。"""
    
    def test_parse_simple_identifier(self):
        tokens = [make_token("IDENTIFIER", "x")]
        state = make_parser_state(tokens)
        result = _parse_expression(state)
        assert result == {"type": "IDENTIFIER", "value": "x", "children": [], "line": 1, "column": 1}
    
    def test_parse_long_identifier(self):
        tokens = [make_token("IDENTIFIER", "myVariable")]
        state = make_parser_state(tokens)
        result = _parse_expression(state)
        assert result == {"type": "IDENTIFIER", "value": "myVariable", "children": [], "line": 1, "column": 1}


class TestParseExpressionUnary:
    """测试一元操作符解析（右结合）。"""
    
    def test_parse_unary_minus(self):
        tokens = [make_token("MINUS", "-", column=1), make_token("INTEGER", 5, column=2)]
        state = make_parser_state(tokens)
        result = _parse_expression(state)
        assert result["type"] == "UNARY_OP"
        assert result["value"] == "-"
        assert result["children"][0] == {"type": "LITERAL", "value": 5, "children": [], "line": 1, "column": 2}
    
    def test_parse_unary_not(self):
        tokens = [make_token("NOT", "!"), make_token("BOOLEAN", True)]
        state = make_parser_state(tokens)
        result = _parse_expression(state)
        assert result["type"] == "UNARY_OP"
        assert result["value"] == "!"
    
    def test_parse_unary_tilde(self):
        tokens = [make_token("TILDE", "~"), make_token("INTEGER", 10)]
        state = make_parser_state(tokens)
        result = _parse_expression(state)
        assert result["type"] == "UNARY_OP"
        assert result["value"] == "~"
    
    def test_parse_chained_unary_right_associative(self):
        """测试一元操作符右结合：-!x 应解析为 -(!x)。"""
        tokens = [
            make_token("MINUS", "-"),
            make_token("NOT", "!"),
            make_token("IDENTIFIER", "x")
        ]
        state = make_parser_state(tokens)
        result = _parse_expression(state)
        assert result["type"] == "UNARY_OP"
        assert result["value"] == "-"
        assert result["children"][0]["type"] == "UNARY_OP"
        assert result["children"][0]["value"] == "!"
        assert result["children"][0]["children"][0]["type"] == "IDENTIFIER"


class TestParseExpressionBinary:
    """测试二元操作符解析（左结合）。"""
    
    def test_parse_addition(self):
        tokens = [
            make_token("INTEGER", 1),
            make_token("PLUS", "+"),
            make_token("INTEGER", 2)
        ]
        state = make_parser_state(tokens)
        result = _parse_expression(state)
        assert result["type"] == "BINARY_OP"
        assert result["value"] == "+"
        assert result["children"][0]["value"] == 1
        assert result["children"][1]["value"] == 2
    
    def test_parse_subtraction(self):
        tokens = [make_token("INTEGER", 5), make_token("MINUS", "-"), make_token("INTEGER", 3)]
        state = make_parser_state(tokens)
        result = _parse_expression(state)
        assert result["type"] == "BINARY_OP"
        assert result["value"] == "-"
    
    def test_parse_multiplication(self):
        tokens = [make_token("INTEGER", 4), make_token("STAR", "*"), make_token("INTEGER", 5)]
        state = make_parser_state(tokens)
        result = _parse_expression(state)
        assert result["type"] == "BINARY_OP"
        assert result["value"] == "*"
    
    def test_parse_division(self):
        tokens = [make_token("INTEGER", 10), make_token("SLASH", "/"), make_token("INTEGER", 2)]
        state = make_parser_state(tokens)
        result = _parse_expression(state)
        assert result["type"] == "BINARY_OP"
        assert result["value"] == "/"
    
    def test_parse_modulo(self):
        tokens = [make_token("INTEGER", 7), make_token("PERCENT", "%"), make_token("INTEGER", 3)]
        state = make_parser_state(tokens)
        result = _parse_expression(state)
        assert result["type"] == "BINARY_OP"
        assert result["value"] == "%"
    
    def test_parse_left_associative(self):
        """测试二元操作符左结合：1-2-3 应解析为 (1-2)-3。"""
        tokens = [
            make_token("INTEGER", 1),
            make_token("MINUS", "-"),
            make_token("INTEGER", 2),
            make_token("MINUS", "-"),
            make_token("INTEGER", 3)
        ]
        state = make_parser_state(tokens)
        result = _parse_expression(state)
        assert result["type"] == "BINARY_OP"
        assert result["value"] == "-"
        assert result["children"][0]["type"] == "BINARY_OP"
        assert result["children"][0]["value"] == "-"
        assert result["children"][0]["children"][0]["value"] == 1
        assert result["children"][0]["children"][1]["value"] == 2
        assert result["children"][1]["value"] == 3


class TestParseExpressionPrecedence:
    """测试操作符优先级。"""
    
    def test_multiplicative_higher_than_additive(self):
        """测试乘除优先级高于加减：1+2*3 应解析为 1+(2*3)。"""
        tokens = [
            make_token("INTEGER", 1),
            make_token("PLUS", "+"),
            make_token("INTEGER", 2),
            make_token("STAR", "*"),
            make_token("INTEGER", 3)
        ]
        state = make_parser_state(tokens)
        result = _parse_expression(state)
        assert result["type"] == "BINARY_OP"
        assert result["value"] == "+"
        assert result["children"][1]["type"] == "BINARY_OP"
        assert result["children"][1]["value"] == "*"
    
    def test_comparison_higher_than_logical(self):
        """测试比较优先级高于逻辑：a<b&&c>d 应解析为 (a<b)&&(c>d)。"""
        tokens = [
            make_token("IDENTIFIER", "a"),
            make_token("LT", "<"),
            make_token("IDENTIFIER", "b"),
            make_token("AND", "&&"),
            make_token("IDENTIFIER", "c"),
            make_token("GT", ">"),
            make_token("IDENTIFIER", "d")
        ]
        state = make_parser_state(tokens)
        result = _parse_expression(state)
        assert result["type"] == "BINARY_OP"
        assert result["value"] == "&&"
        assert result["children"][0]["type"] == "BINARY_OP"
        assert result["children"][0]["value"] == "<"
        assert result["children"][1]["type"] == "BINARY_OP"
        assert result["children"][1]["value"] == ">"
    
    def test_unary_highest_precedence(self):
        """测试一元操作符优先级最高：-a*b 应解析为 (-a)*b。"""
        tokens = [
            make_token("MINUS", "-"),
            make_token("IDENTIFIER", "a"),
            make_token("STAR", "*"),
            make_token("IDENTIFIER", "b")
        ]
        state = make_parser_state(tokens)
        result = _parse_expression(state)
        assert result["type"] == "BINARY_OP"
        assert result["value"] == "*"
        assert result["children"][0]["type"] == "UNARY_OP"
        assert result["children"][0]["value"] == "-"


class TestParseExpressionParentheses:
    """测试括号解析。"""
    
    def test_parse_parenthesized_expression(self):
        tokens = [
            make_token("LPAREN", "("),
            make_token("INTEGER", 42),
            make_token("RPAREN", ")")
        ]
        state = make_parser_state(tokens)
        result = _parse_expression(state)
        assert result["type"] == "LITERAL"
        assert result["value"] == 42
    
    def test_parentheses_override_precedence(self):
        """测试括号覆盖优先级：(1+2)*3。"""
        tokens = [
            make_token("LPAREN", "("),
            make_token("INTEGER", 1),
            make_token("PLUS", "+"),
            make_token("INTEGER", 2),
            make_token("RPAREN", ")"),
            make_token("STAR", "*"),
            make_token("INTEGER", 3)
        ]
        state = make_parser_state(tokens)
        result = _parse_expression(state)
        assert result["type"] == "BINARY_OP"
        assert result["value"] == "*"
        assert result["children"][0]["type"] == "BINARY_OP"
        assert result["children"][0]["value"] == "+"


class TestParseExpressionErrors:
    """测试错误处理。"""
    
    def test_unexpected_end_of_input(self):
        """测试空输入抛出 SyntaxError。"""
        tokens = []
        state = make_parser_state(tokens)
        with pytest.raises(SyntaxError, match="Unexpected end of input"):
            _parse_expression(state)
    
    def test_unexpected_token(self):
        """测试非法 token 抛出 SyntaxError。"""
        tokens = [make_token("LPAREN", "(")]
        state = make_parser_state(tokens)
        with pytest.raises(SyntaxError):
            _parse_expression(state)
    
    def test_missing_operand_after_operator(self):
        """测试操作符后缺少操作数。"""
        tokens = [make_token("INTEGER", 1), make_token("PLUS", "+")]
        state = make_parser_state(tokens)
        with pytest.raises(SyntaxError):
            _parse_expression(state)


class TestParseExpressionPosition:
    """测试解析后位置更新。"""
    
    def test_position_updated_after_simple_expression(self):
        tokens = [make_token("INTEGER", 42)]
        state = make_parser_state(tokens)
        _parse_expression(state)
        assert state["pos"] == 1
    
    def test_position_updated_after_complex_expression(self):
        tokens = [
            make_token("INTEGER", 1),
            make_token("PLUS", "+"),
            make_token("INTEGER", 2),
            make_token("STAR", "*"),
            make_token("INTEGER", 3)
        ]
        state = make_parser_state(tokens)
        _parse_expression(state)
        assert state["pos"] == 5
    
    def test_position_stops_at_unconsumed_token(self):
        """测试解析停在表达式结束处，不消耗后续 token。"""
        tokens = [
            make_token("INTEGER", 42),
            make_token("SEMICOLON", ";"),
            make_token("INTEGER", 100)
        ]
        state = make_parser_state(tokens)
        # 只解析第一个数字（SEMICOLON 不是表达式的一部分）
        result = _parse_expression(state)
        assert result["value"] == 42
        assert state["pos"] == 1
