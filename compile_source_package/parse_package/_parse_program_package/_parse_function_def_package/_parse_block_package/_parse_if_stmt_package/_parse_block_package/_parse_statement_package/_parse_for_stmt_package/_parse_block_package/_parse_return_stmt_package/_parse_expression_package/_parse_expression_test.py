import unittest
from unittest.mock import patch, MagicMock
from typing import Dict, Any
import sys

# Mock all missing dependencies before importing _parse_expression_src
# to avoid import chain errors

# Create mock modules for the entire dependency chain
def create_mock_module(name):
    mock = MagicMock()
    mock._parse_additive = MagicMock(return_value={"type": "mock", "value": "mock", "children": []})
    mock._parse_multiplicative = MagicMock(return_value={"type": "mock", "value": "mock", "children": []})
    mock._peek_token = MagicMock(return_value=None)
    mock._consume_token = MagicMock(return_value={"type": "MOCK", "value": "mock"})
    return mock

# Pre-populate sys.modules with mocks for all dependencies
mock_packages = [
    '._parse_additive_package._parse_additive_src',
    '._parse_additive_package._peek_token_package._peek_token_src',
    '._parse_additive_package._consume_token_package._consume_token_src',
    '._parse_additive_package._parse_multiplicative_package._parse_multiplicative_src',
]

for pkg_name in mock_packages:
    if pkg_name not in sys.modules:
        sys.modules[pkg_name] = create_mock_module(pkg_name)

# Import _parse_expression and get the module reference
from ._parse_expression_src import _parse_expression
# Get the module where _parse_expression is defined
_parse_expression_module = sys.modules[_parse_expression.__module__]


class TestParseExpression(unittest.TestCase):
    """Test cases for _parse_expression function."""

    def test_parse_expression_delegates_to_parse_additive(self):
        """Test that _parse_expression delegates to _parse_additive."""
        mock_ast: Dict[str, Any] = {
            "type": "additive",
            "value": "test",
            "children": []
        }

        # Patch _parse_additive in the _parse_expression_src module where it's used
        with patch.object(_parse_expression_module, '_parse_additive', return_value=mock_ast) as mock_additive:
            parser_state = {
                "tokens": [{"type": "NUMBER", "value": "42", "line": 1, "column": 1}],
                "pos": 0,
                "filename": "test.py"
            }

            result = _parse_expression(parser_state)

            mock_additive.assert_called_once_with(parser_state)
            self.assertEqual(result, mock_ast)

    def test_parse_expression_with_empty_tokens(self):
        """Test _parse_expression with empty token list."""
        mock_ast: Dict[str, Any] = {
            "type": "empty",
            "value": None,
            "children": []
        }

        with patch.object(_parse_expression_module, '_parse_additive', return_value=mock_ast) as mock_additive:
            parser_state = {
                "tokens": [],
                "pos": 0,
                "filename": "test.py"
            }

            result = _parse_expression(parser_state)

            mock_additive.assert_called_once_with(parser_state)
            self.assertEqual(result, mock_ast)

    def test_parse_expression_with_error_state(self):
        """Test _parse_expression when parser_state has error flag."""
        mock_ast: Dict[str, Any] = {
            "type": "error",
            "value": "parse error",
            "children": []
        }

        with patch.object(_parse_expression_module, '_parse_additive', return_value=mock_ast) as mock_additive:
            parser_state = {
                "tokens": [{"type": "INVALID", "value": "?", "line": 1, "column": 1}],
                "pos": 0,
                "filename": "test.py",
                "error": True
            }

            result = _parse_expression(parser_state)

            mock_additive.assert_called_once_with(parser_state)
            self.assertEqual(result, mock_ast)

    def test_parse_expression_preserves_parser_state_reference(self):
        """Test that _parse_expression passes parser_state by reference."""
        mock_ast: Dict[str, Any] = {
            "type": "additive",
            "value": "result",
            "children": []
        }

        with patch.object(_parse_expression_module, '_parse_additive', return_value=mock_ast) as mock_additive:
            parser_state = {
                "tokens": [{"type": "NUMBER", "value": "42", "line": 1, "column": 1}],
                "pos": 0,
                "filename": "test.py"
            }

            _parse_expression(parser_state)

            passed_state = mock_additive.call_args[0][0]
            self.assertIs(passed_state, parser_state)

    def test_parse_expression_with_multiple_tokens(self):
        """Test _parse_expression with multiple tokens."""
        mock_ast: Dict[str, Any] = {
            "type": "additive",
            "value": "complex",
            "children": [
                {"type": "NUMBER", "value": "1"},
                {"type": "NUMBER", "value": "2"}
            ]
        }

        with patch.object(_parse_expression_module, '_parse_additive', return_value=mock_ast) as mock_additive:
            parser_state = {
                "tokens": [
                    {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                    {"type": "PLUS", "value": "+", "line": 1, "column": 2},
                    {"type": "NUMBER", "value": "2", "line": 1, "column": 3}
                ],
                "pos": 0,
                "filename": "test.py"
            }

            result = _parse_expression(parser_state)

            mock_additive.assert_called_once_with(parser_state)
            self.assertEqual(result, mock_ast)

    def test_parse_expression_returns_ast_dict(self):
        """Test that _parse_expression returns a dict (AST node)."""
        expected_ast: Dict[str, Any] = {
            "type": "binary_op",
            "operator": "+",
            "left": {"type": "NUMBER", "value": "5"},
            "right": {"type": "NUMBER", "value": "3"}
        }

        with patch.object(_parse_expression_module, '_parse_additive', return_value=expected_ast) as mock_additive:
            parser_state = {
                "tokens": [
                    {"type": "NUMBER", "value": "5", "line": 1, "column": 1},
                    {"type": "PLUS", "value": "+", "line": 1, "column": 2},
                    {"type": "NUMBER", "value": "3", "line": 1, "column": 3}
                ],
                "pos": 0,
                "filename": "expr.py"
            }

            result = _parse_expression(parser_state)

            self.assertIsInstance(result, dict)
            self.assertEqual(result, expected_ast)

    def test_parse_expression_with_non_zero_pos(self):
        """Test _parse_expression when pos is not at start."""
        mock_ast: Dict[str, Any] = {
            "type": "additive",
            "value": "mid_expr",
            "children": []
        }

        with patch.object(_parse_expression_module, '_parse_additive', return_value=mock_ast) as mock_additive:
            parser_state = {
                "tokens": [
                    {"type": "IDENT", "value": "x", "line": 1, "column": 1},
                    {"type": "NUMBER", "value": "10", "line": 1, "column": 3},
                    {"type": "PLUS", "value": "+", "line": 1, "column": 5},
                    {"type": "NUMBER", "value": "20", "line": 1, "column": 7}
                ],
                "pos": 1,
                "filename": "test.py"
            }

            result = _parse_expression(parser_state)

            mock_additive.assert_called_once_with(parser_state)
            self.assertEqual(result, mock_ast)

    def test_parse_expression_propagates_exception_from_additive(self):
        """Test that exceptions from _parse_additive are propagated."""
        with patch.object(_parse_expression_module, '_parse_additive', side_effect=ValueError("Parse error in additive")) as mock_additive:
            parser_state = {
                "tokens": [{"type": "INVALID", "value": "@", "line": 1, "column": 1}],
                "pos": 0,
                "filename": "test.py"
            }

            with self.assertRaises(ValueError) as context:
                _parse_expression(parser_state)

            self.assertEqual(str(context.exception), "Parse error in additive")
            mock_additive.assert_called_once_with(parser_state)


if __name__ == "__main__":
    unittest.main()
