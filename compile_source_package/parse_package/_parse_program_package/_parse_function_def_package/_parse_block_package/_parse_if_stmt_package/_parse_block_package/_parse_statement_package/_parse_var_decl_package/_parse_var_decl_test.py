# === std / third-party imports ===
import unittest
from unittest.mock import patch

# === relative imports ===
from ._parse_var_decl_src import _parse_var_decl


class TestParseVarDecl(unittest.TestCase):
    """Test cases for _parse_var_decl function."""

    def test_var_decl_without_type_annotation(self):
        """Test: var x = 5;"""
        tokens = [
            {"type": "VAR", "value": "var", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3},
            {"type": "ASSIGN", "value": "=", "line": 1, "column": 5},
            {"type": "NUMBER", "value": "5", "line": 1, "column": 7},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 8},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.src"
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_var_decl_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = {
                "type": "NUMBER",
                "value": "5",
                "line": 1,
                "column": 7
            }

            result = _parse_var_decl(parser_state)

        self.assertEqual(result["type"], "VAR_DECL")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(result["type_annotation"], None)
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0]["type"], "IDENTIFIER")
        self.assertEqual(result["children"][0]["value"], "x")
        self.assertEqual(result["children"][1]["type"], "NUMBER")
        self.assertEqual(parser_state["pos"], 5)
        mock_parse_expr.assert_called_once()

    def test_let_decl_with_type_annotation(self):
        """Test: let x: int = 5;"""
        tokens = [
            {"type": "LET", "value": "let", "line": 2, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 2, "column": 5},
            {"type": "COLON", "value": ":", "line": 2, "column": 6},
            {"type": "INT", "value": "int", "line": 2, "column": 8},
            {"type": "ASSIGN", "value": "=", "line": 2, "column": 12},
            {"type": "NUMBER", "value": "5", "line": 2, "column": 14},
            {"type": "SEMICOLON", "value": ";", "line": 2, "column": 15},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.src"
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_var_decl_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = {
                "type": "NUMBER",
                "value": "5",
                "line": 2,
                "column": 14
            }

            result = _parse_var_decl(parser_state)

        self.assertEqual(result["type"], "VAR_DECL")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 1)
        self.assertEqual(result["type_annotation"], "int")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0]["value"], "x")
        self.assertEqual(parser_state["pos"], 7)
        mock_parse_expr.assert_called_once()

    def test_var_decl_without_initialization(self):
        """Test: var x;"""
        tokens = [
            {"type": "VAR", "value": "var", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 6},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.src"
        }

        result = _parse_var_decl(parser_state)

        self.assertEqual(result["type"], "VAR_DECL")
        self.assertEqual(result["type_annotation"], None)
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["value"], "x")
        self.assertEqual(parser_state["pos"], 3)

    def test_let_with_string_type(self):
        """Test: let name: string = "hello";"""
        tokens = [
            {"type": "LET", "value": "let", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "name", "line": 1, "column": 5},
            {"type": "COLON", "value": ":", "line": 1, "column": 9},
            {"type": "STRING", "value": "string", "line": 1, "column": 11},
            {"type": "ASSIGN", "value": "=", "line": 1, "column": 18},
            {"type": "STRING_LITERAL", "value": "hello", "line": 1, "column": 20},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 27},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.src"
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_var_decl_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = {
                "type": "STRING_LITERAL",
                "value": "hello",
                "line": 1,
                "column": 20
            }

            result = _parse_var_decl(parser_state)

        self.assertEqual(result["type_annotation"], "string")
        self.assertEqual(parser_state["pos"], 7)

    def test_let_with_bool_type(self):
        """Test: let flag: bool = true;"""
        tokens = [
            {"type": "LET", "value": "let", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "flag", "line": 1, "column": 5},
            {"type": "COLON", "value": ":", "line": 1, "column": 9},
            {"type": "BOOL", "value": "bool", "line": 1, "column": 11},
            {"type": "ASSIGN", "value": "=", "line": 1, "column": 16},
            {"type": "TRUE", "value": "true", "line": 1, "column": 18},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 22},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.src"
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_var_decl_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = {
                "type": "TRUE",
                "value": "true",
                "line": 1,
                "column": 18
            }

            result = _parse_var_decl(parser_state)

        self.assertEqual(result["type_annotation"], "bool")
        self.assertEqual(parser_state["pos"], 7)

    def test_error_unexpected_end_no_keyword(self):
        """Test: Empty tokens list"""
        tokens = []
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.src"
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_var_decl(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("expected VAR or LET", str(context.exception))

    def test_error_wrong_keyword_type(self):
        """Test: CONST instead of VAR/LET"""
        tokens = [
            {"type": "CONST", "value": "const", "line": 3, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.src"
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_var_decl(parser_state)

        self.assertIn("Expected VAR or LET", str(context.exception))
        self.assertIn("got CONST", str(context.exception))
        self.assertIn("3:1", str(context.exception))

    def test_error_missing_identifier(self):
        """Test: var ;"""
        tokens = [
            {"type": "VAR", "value": "var", "line": 1, "column": 1},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 5},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.src"
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_var_decl(parser_state)

        self.assertIn("Expected identifier", str(context.exception))

    def test_error_wrong_identifier_type(self):
        """Test: var 5 = 10;"""
        tokens = [
            {"type": "VAR", "value": "var", "line": 1, "column": 1},
            {"type": "NUMBER", "value": "5", "line": 1, "column": 5},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.src"
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_var_decl(parser_state)

        self.assertIn("Expected identifier", str(context.exception))
        self.assertIn("got NUMBER", str(context.exception))

    def test_error_missing_type_after_colon(self):
        """Test: let x: ;"""
        tokens = [
            {"type": "LET", "value": "let", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5},
            {"type": "COLON", "value": ":", "line": 1, "column": 6},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 8},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.src"
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_var_decl(parser_state)

        self.assertIn("Unexpected end of input after colon", str(context.exception))

    def test_error_invalid_type_annotation(self):
        """Test: let x: float = 1.0;"""
        tokens = [
            {"type": "LET", "value": "let", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5},
            {"type": "COLON", "value": ":", "line": 1, "column": 6},
            {"type": "FLOAT", "value": "float", "line": 1, "column": 8},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.src"
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_var_decl(parser_state)

        self.assertIn("Expected INT, STRING, or BOOL", str(context.exception))
        self.assertIn("got FLOAT", str(context.exception))

    def test_error_missing_semicolon(self):
        """Test: var x = 5 (no semicolon)"""
        tokens = [
            {"type": "VAR", "value": "var", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5},
            {"type": "ASSIGN", "value": "=", "line": 1, "column": 7},
            {"type": "NUMBER", "value": "5", "line": 1, "column": 9},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.src"
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_var_decl(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("expected semicolon", str(context.exception))

    def test_error_wrong_ending_token(self):
        """Test: var x = 5, (comma instead of semicolon)"""
        tokens = [
            {"type": "VAR", "value": "var", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5},
            {"type": "ASSIGN", "value": "=", "line": 1, "column": 7},
            {"type": "NUMBER", "value": "5", "line": 1, "column": 9},
            {"type": "COMMA", "value": ",", "line": 1, "column": 10},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.src"
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_var_decl(parser_state)

        self.assertIn("Expected semicolon", str(context.exception))
        self.assertIn("got COMMA", str(context.exception))

    def test_var_decl_position_tracking(self):
        """Test that parser_state pos is correctly updated"""
        tokens = [
            {"type": "VAR", "value": "var", "line": 5, "column": 10},
            {"type": "IDENTIFIER", "value": "count", "line": 5, "column": 14},
            {"type": "ASSIGN", "value": "=", "line": 5, "column": 20},
            {"type": "NUMBER", "value": "42", "line": 5, "column": 22},
            {"type": "SEMICOLON", "value": ";", "line": 5, "column": 24},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.src"
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_var_decl_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = {
                "type": "NUMBER",
                "value": "42",
                "line": 5,
                "column": 22
            }

            result = _parse_var_decl(parser_state)

        self.assertEqual(parser_state["pos"], 5)
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)


if __name__ == "__main__":
    unittest.main()
