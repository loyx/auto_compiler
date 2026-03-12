# === std / third-party imports ===
import pytest
from unittest.mock import patch

# === sub function imports ===
from ._parse_def_statement_src import _parse_def_statement


class TestParseDefStatement:
    """测试 _parse_def_statement 函数"""

    def test_parse_simple_function_def(self):
        """测试简单函数定义：def foo(): pass;"""
        tokens = [
            {"type": "DEF", "value": "def", "line": 1, "column": 1},
            {"type": "IDENT", "value": "foo", "line": 1, "column": 5},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 8},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 9},
            {"type": "COLON", "value": ":", "line": 1, "column": 10},
            {"type": "PASS", "value": "pass", "line": 1, "column": 12},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 16},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.cc"}
        
        # Mock 子函数
        mock_params = {"type": "PARAMS", "children": [], "line": 1, "column": 1}
        mock_block = {"type": "BODY", "children": [{"type": "PASS_STMT"}], "line": 1, "column": 12}
        
        with patch("._parse_params_package._parse_params_src._parse_params", return_value=mock_params) as mock_parse_params, \
             patch("._parse_block_package._parse_block_src._parse_block", return_value=mock_block) as mock_parse_block:
            result = _parse_def_statement(parser_state)
        
        assert result["type"] == "DEF_STMT"
        assert result["line"] == 1
        assert result["column"] == 1
        assert len(result["children"]) == 3  # name, params, body
        assert result["children"][0]["type"] == "NAME"
        assert result["children"][0]["value"] == "foo"
        assert result["children"][1]["type"] == "PARAMS"
        assert result["children"][2]["type"] == "BODY"
        assert parser_state["pos"] == 7  # 所有 token 已消费

    def test_parse_function_with_params(self):
        """测试带参数的函数定义：def foo(a, b): pass;"""
        tokens = [
            {"type": "DEF", "value": "def", "line": 1, "column": 1},
            {"type": "IDENT", "value": "foo", "line": 1, "column": 5},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 8},
            {"type": "IDENT", "value": "a", "line": 1, "column": 9},
            {"type": "COMMA", "value": ",", "line": 1, "column": 10},
            {"type": "IDENT", "value": "b", "line": 1, "column": 12},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 13},
            {"type": "COLON", "value": ":", "line": 1, "column": 14},
            {"type": "PASS", "value": "pass", "line": 1, "column": 16},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 20},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.cc"}
        
        mock_params = {"type": "PARAMS", "children": [{"type": "PARAM", "value": "a"}, {"type": "PARAM", "value": "b"}], "line": 1, "column": 1}
        mock_block = {"type": "BODY", "children": [{"type": "PASS_STMT"}], "line": 1, "column": 16}
        
        with patch("._parse_params_package._parse_params_src._parse_params", return_value=mock_params) as mock_parse_params, \
             patch("._parse_block_package._parse_block_src._parse_block", return_value=mock_block) as mock_parse_block:
            result = _parse_def_statement(parser_state)
        
        assert result["type"] == "DEF_STMT"
        assert result["children"][0]["value"] == "foo"
        assert result["children"][1]["type"] == "PARAMS"
        assert len(result["children"][1]["children"]) == 2
        assert parser_state["pos"] == 10

    def test_parse_function_with_return_type(self):
        """测试带返回类型注解的函数：def foo() -> int: pass;"""
        tokens = [
            {"type": "DEF", "value": "def", "line": 1, "column": 1},
            {"type": "IDENT", "value": "foo", "line": 1, "column": 5},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 8},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 9},
            {"type": "ARROW", "value": "->", "line": 1, "column": 11},
            {"type": "IDENT", "value": "int", "line": 1, "column": 14},
            {"type": "COLON", "value": ":", "line": 1, "column": 17},
            {"type": "PASS", "value": "pass", "line": 1, "column": 19},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 23},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.cc"}
        
        mock_params = {"type": "PARAMS", "children": [], "line": 1, "column": 1}
        mock_return_type = {"type": "NAME", "value": "int", "line": 1, "column": 14}
        mock_block = {"type": "BODY", "children": [{"type": "PASS_STMT"}], "line": 1, "column": 19}
        
        with patch("._parse_params_package._parse_params_src._parse_params", return_value=mock_params) as mock_parse_params, \
             patch("._parse_type_annotation_package._parse_type_annotation_src._parse_type_annotation", return_value=mock_return_type) as mock_parse_type, \
             patch("._parse_block_package._parse_block_src._parse_block", return_value=mock_block) as mock_parse_block:
            result = _parse_def_statement(parser_state)
        
        assert result["type"] == "DEF_STMT"
        assert len(result["children"]) == 4  # name, params, return_type, body
        assert result["children"][0]["value"] == "foo"
        assert result["children"][1]["type"] == "PARAMS"
        assert result["children"][2]["type"] == "NAME"
        assert result["children"][2]["value"] == "int"
        assert result["children"][3]["type"] == "BODY"
        assert parser_state["pos"] == 9

    def test_parse_function_with_params_and_return_type(self):
        """测试带参数和返回类型的函数：def foo(a: int, b: str) -> bool: pass;"""
        tokens = [
            {"type": "DEF", "value": "def", "line": 1, "column": 1},
            {"type": "IDENT", "value": "foo", "line": 1, "column": 5},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 8},
            {"type": "IDENT", "value": "a", "line": 1, "column": 9},
            {"type": "COLON", "value": ":", "line": 1, "column": 10},
            {"type": "IDENT", "value": "int", "line": 1, "column": 12},
            {"type": "COMMA", "value": ",", "line": 1, "column": 15},
            {"type": "IDENT", "value": "b", "line": 1, "column": 17},
            {"type": "COLON", "value": ":", "line": 1, "column": 18},
            {"type": "IDENT", "value": "str", "line": 1, "column": 20},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 23},
            {"type": "ARROW", "value": "->", "line": 1, "column": 25},
            {"type": "IDENT", "value": "bool", "line": 1, "column": 28},
            {"type": "COLON", "value": ":", "line": 1, "column": 32},
            {"type": "PASS", "value": "pass", "line": 1, "column": 34},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 38},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.cc"}
        
        mock_params = {"type": "PARAMS", "children": [{"type": "PARAM", "value": "a"}, {"type": "PARAM", "value": "b"}], "line": 1, "column": 1}
        mock_return_type = {"type": "NAME", "value": "bool", "line": 1, "column": 28}
        mock_block = {"type": "BODY", "children": [{"type": "PASS_STMT"}], "line": 1, "column": 34}
        
        with patch("._parse_params_package._parse_params_src._parse_params", return_value=mock_params) as mock_parse_params, \
             patch("._parse_type_annotation_package._parse_type_annotation_src._parse_type_annotation", return_value=mock_return_type) as mock_parse_type, \
             patch("._parse_block_package._parse_block_src._parse_block", return_value=mock_block) as mock_parse_block:
            result = _parse_def_statement(parser_state)
        
        assert result["type"] == "DEF_STMT"
        assert len(result["children"]) == 4
        assert parser_state["pos"] == 16

    def test_error_missing_def_keyword(self):
        """测试缺少 def 关键字时抛出 SyntaxError"""
        tokens = [
            {"type": "IDENT", "value": "foo", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 4},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 5},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.cc"}
        
        with pytest.raises(SyntaxError, match="Expected 'def' keyword"):
            _parse_def_statement(parser_state)

    def test_error_missing_function_name(self):
        """测试缺少函数名时抛出 SyntaxError"""
        tokens = [
            {"type": "DEF", "value": "def", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 5},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 6},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.cc"}
        
        with pytest.raises(SyntaxError, match="Expected function name"):
            _parse_def_statement(parser_state)

    def test_error_missing_left_paren(self):
        """测试缺少左括号时抛出 SyntaxError"""
        tokens = [
            {"type": "DEF", "value": "def", "line": 1, "column": 1},
            {"type": "IDENT", "value": "foo", "line": 1, "column": 5},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 9},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.cc"}
        
        with pytest.raises(SyntaxError, match="Expected '\\('"):
            _parse_def_statement(parser_state)

    def test_error_missing_right_paren(self):
        """测试缺少右括号时抛出 SyntaxError"""
        tokens = [
            {"type": "DEF", "value": "def", "line": 1, "column": 1},
            {"type": "IDENT", "value": "foo", "line": 1, "column": 5},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 8},
            {"type": "COLON", "value": ":", "line": 1, "column": 9},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.cc"}
        
        mock_params = {"type": "PARAMS", "children": [], "line": 1, "column": 1}
        
        with patch("._parse_params_package._parse_params_src._parse_params", return_value=mock_params) as mock_parse_params:
            with pytest.raises(SyntaxError, match="Expected '\\)'"):
                _parse_def_statement(parser_state)

    def test_error_missing_colon(self):
        """测试缺少冒号时抛出 SyntaxError"""
        tokens = [
            {"type": "DEF", "value": "def", "line": 1, "column": 1},
            {"type": "IDENT", "value": "foo", "line": 1, "column": 5},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 8},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 9},
            {"type": "PASS", "value": "pass", "line": 1, "column": 11},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.cc"}
        
        mock_params = {"type": "PARAMS", "children": [], "line": 1, "column": 1}
        
        with patch("._parse_params_package._parse_params_src._parse_params", return_value=mock_params) as mock_parse_params:
            with pytest.raises(SyntaxError, match="Expected ':'"):
                _parse_def_statement(parser_state)

    def test_error_missing_function_body(self):
        """测试缺少函数体时抛出 SyntaxError"""
        tokens = [
            {"type": "DEF", "value": "def", "line": 1, "column": 1},
            {"type": "IDENT", "value": "foo", "line": 1, "column": 5},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 8},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 9},
            {"type": "COLON", "value": ":", "line": 1, "column": 10},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.cc"}
        
        mock_params = {"type": "PARAMS", "children": [], "line": 1, "column": 1}
        
        with patch("._parse_params_package._parse_params_src._parse_params", return_value=mock_params) as mock_parse_params:
            with pytest.raises(SyntaxError, match="Expected function body"):
                _parse_def_statement(parser_state)

    def test_error_missing_semicolon(self):
        """测试缺少分号时抛出 SyntaxError"""
        tokens = [
            {"type": "DEF", "value": "def", "line": 1, "column": 1},
            {"type": "IDENT", "value": "foo", "line": 1, "column": 5},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 8},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 9},
            {"type": "COLON", "value": ":", "line": 1, "column": 10},
            {"type": "PASS", "value": "pass", "line": 1, "column": 12},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.cc"}
        
        mock_params = {"type": "PARAMS", "children": [], "line": 1, "column": 1}
        mock_block = {"type": "BODY", "children": [{"type": "PASS_STMT"}], "line": 1, "column": 12}
        
        with patch("._parse_params_package._parse_params_src._parse_params", return_value=mock_params) as mock_parse_params, \
             patch("._parse_block_package._parse_block_src._parse_block", return_value=mock_block) as mock_parse_block:
            with pytest.raises(SyntaxError, match="Expected ';'"):
                _parse_def_statement(parser_state)

    def test_error_empty_tokens(self):
        """测试空 tokens 列表时抛出 SyntaxError"""
        tokens = []
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.cc"}
        
        with pytest.raises(SyntaxError, match="Expected 'def' keyword"):
            _parse_def_statement(parser_state)

    def test_position_updated_correctly(self):
        """测试 parser_state pos 正确更新"""
        tokens = [
            {"type": "DEF", "value": "def", "line": 1, "column": 1},
            {"type": "IDENT", "value": "foo", "line": 1, "column": 5},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 8},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 9},
            {"type": "COLON", "value": ":", "line": 1, "column": 10},
            {"type": "PASS", "value": "pass", "line": 1, "column": 12},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 16},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.cc"}
        
        mock_params = {"type": "PARAMS", "children": [], "line": 1, "column": 1}
        mock_block = {"type": "BODY", "children": [{"type": "PASS_STMT"}], "line": 1, "column": 12}
        
        with patch("._parse_params_package._parse_params_src._parse_params", return_value=mock_params) as mock_parse_params, \
             patch("._parse_block_package._parse_block_src._parse_block", return_value=mock_block) as mock_parse_block:
            _parse_def_statement(parser_state)
        
        assert parser_state["pos"] == 7  # 所有 7 个 token 已消费

    def test_ast_node_line_column_preserved(self):
        """测试 AST 节点的 line 和 column 信息正确保留"""
        tokens = [
            {"type": "DEF", "value": "def", "line": 5, "column": 10},
            {"type": "IDENT", "value": "foo", "line": 5, "column": 14},
            {"type": "LPAREN", "value": "(", "line": 5, "column": 17},
            {"type": "RPAREN", "value": ")", "line": 5, "column": 18},
            {"type": "COLON", "value": ":", "line": 5, "column": 19},
            {"type": "PASS", "value": "pass", "line": 5, "column": 21},
            {"type": "SEMICOLON", "value": ";", "line": 5, "column": 25},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.cc"}
        
        mock_params = {"type": "PARAMS", "children": [], "line": 5, "column": 10}
        mock_block = {"type": "BODY", "children": [{"type": "PASS_STMT"}], "line": 5, "column": 21}
        
        with patch("._parse_params_package._parse_params_src._parse_params", return_value=mock_params) as mock_parse_params, \
             patch("._parse_block_package._parse_block_src._parse_block", return_value=mock_block) as mock_parse_block:
            result = _parse_def_statement(parser_state)
        
        assert result["line"] == 5
        assert result["column"] == 10
        assert result["children"][0]["line"] == 5
        assert result["children"][0]["column"] == 14
