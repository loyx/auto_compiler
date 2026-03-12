import unittest
from unittest.mock import patch, call
from typing import Dict, Any

# Relative import from the current package
from ._parse_object_literal_src import _parse_object_literal


def create_token(token_type: str, value: str = "", line: int = 1, column: int = 1) -> Dict[str, Any]:
    """Helper to create a token dictionary."""
    return {
        "type": token_type,
        "value": value,
        "line": line,
        "column": column
    }


def create_parser_state(tokens: list, pos: int = 0, filename: str = "test.js") -> Dict[str, Any]:
    """Helper to create a parser state dictionary."""
    return {
        "tokens": tokens,
        "pos": pos,
        "filename": filename
    }


class TestParseObjectLiteral(unittest.TestCase):
    """Test cases for _parse_object_literal function."""

    @patch("._parse_object_literal_package._parse_object_literal_src._create_ast_node")
    @patch("._parse_object_literal_package._parse_object_literal_src._parse_property")
    @patch("._parse_object_literal_package._parse_object_literal_src._consume_token")
    def test_empty_object(self, mock_consume_token, mock_parse_property, mock_create_ast_node):
        """Test parsing empty object literal: {}"""
        # Setup tokens: LEFT_BRACE, RIGHT_BRACE
        left_brace = create_token("LEFT_BRACE", "{", 1, 1)
        right_brace = create_token("RIGHT_BRACE", "}", 1, 2)
        tokens = [left_brace, right_brace]
        parser_state = create_parser_state(tokens, pos=0)
        
        # Setup mocks
        mock_consume_token.side_effect = [left_brace, right_brace]
        expected_ast = {"type": "ObjectLiteral", "children": [], "value": None, "line": 1, "column": 1}
        mock_create_ast_node.return_value = expected_ast
        
        # Execute
        result = _parse_object_literal(parser_state)
        
        # Verify
        self.assertEqual(result, expected_ast)
        self.assertEqual(mock_consume_token.call_count, 2)
        mock_consume_token.assert_has_calls([
            call(parser_state, "LEFT_BRACE"),
            call(parser_state, "RIGHT_BRACE")
        ])
        mock_parse_property.assert_not_called()
        mock_create_ast_node.assert_called_once_with(
            node_type="ObjectLiteral",
            value=None,
            children=[],
            line=1,
            column=1
        )

    @patch("._parse_object_literal_package._parse_object_literal_src._create_ast_node")
    @patch("._parse_object_literal_package._parse_object_literal_src._parse_property")
    @patch("._parse_object_literal_package._parse_object_literal_src._consume_token")
    def test_single_property(self, mock_consume_token, mock_parse_property, mock_create_ast_node):
        """Test parsing object with single property: {key: value}"""
        # Setup tokens
        left_brace = create_token("LEFT_BRACE", "{", 1, 1)
        right_brace = create_token("RIGHT_BRACE", "}", 1, 10)
        tokens = [left_brace, right_brace]
        parser_state = create_parser_state(tokens, pos=0)
        
        # Setup mocks
        property_node = {"type": "Property", "children": [], "value": "test"}
        mock_consume_token.side_effect = [left_brace, right_brace]
        mock_parse_property.return_value = property_node
        expected_ast = {"type": "ObjectLiteral", "children": [property_node], "value": None, "line": 1, "column": 1}
        mock_create_ast_node.return_value = expected_ast
        
        # Execute
        result = _parse_object_literal(parser_state)
        
        # Verify
        self.assertEqual(result, expected_ast)
        mock_parse_property.assert_called_once_with(parser_state)
        mock_create_ast_node.assert_called_once_with(
            node_type="ObjectLiteral",
            value=None,
            children=[property_node],
            line=1,
            column=1
        )

    @patch("._parse_object_literal_package._parse_object_literal_src._create_ast_node")
    @patch("._parse_object_literal_package._parse_object_literal_src._parse_property")
    @patch("._parse_object_literal_package._parse_object_literal_src._consume_token")
    def test_multiple_properties_with_commas(self, mock_consume_token, mock_parse_property, mock_create_ast_node):
        """Test parsing object with multiple properties: {k1: v1, k2: v2}"""
        # Setup tokens
        left_brace = create_token("LEFT_BRACE", "{", 1, 1)
        comma1 = create_token("COMMA", ",", 1, 5)
        comma2 = create_token("COMMA", ",", 1, 10)
        right_brace = create_token("RIGHT_BRACE", "}", 1, 15)
        tokens = [left_brace, comma1, comma2, right_brace]
        parser_state = create_parser_state(tokens, pos=0)
        
        # Setup mocks
        prop1 = {"type": "Property", "value": "prop1"}
        prop2 = {"type": "Property", "value": "prop2"}
        mock_consume_token.side_effect = [left_brace, comma1, comma2, right_brace]
        mock_parse_property.side_effect = [prop1, prop2]
        expected_ast = {"type": "ObjectLiteral", "children": [prop1, prop2], "value": None, "line": 1, "column": 1}
        mock_create_ast_node.return_value = expected_ast
        
        # Execute
        result = _parse_object_literal(parser_state)
        
        # Verify
        self.assertEqual(result, expected_ast)
        self.assertEqual(mock_parse_property.call_count, 2)
        self.assertEqual(mock_consume_token.call_count, 4)
        mock_create_ast_node.assert_called_once_with(
            node_type="ObjectLiteral",
            value=None,
            children=[prop1, prop2],
            line=1,
            column=1
        )

    @patch("._parse_object_literal_package._parse_object_literal_src._create_ast_node")
    @patch("._parse_object_literal_package._parse_object_literal_src._parse_property")
    @patch("._parse_object_literal_package._parse_object_literal_src._consume_token")
    def test_multiple_properties_no_trailing_comma(self, mock_consume_token, mock_parse_property, mock_create_ast_node):
        """Test parsing object where last property has no trailing comma"""
        # Setup tokens
        left_brace = create_token("LEFT_BRACE", "{", 1, 1)
        comma1 = create_token("COMMA", ",", 1, 5)
        right_brace = create_token("RIGHT_BRACE", "}", 1, 10)
        tokens = [left_brace, comma1, right_brace]
        parser_state = create_parser_state(tokens, pos=0)
        
        # Setup mocks
        prop1 = {"type": "Property", "value": "prop1"}
        prop2 = {"type": "Property", "value": "prop2"}
        mock_consume_token.side_effect = [left_brace, comma1, right_brace]
        mock_parse_property.side_effect = [prop1, prop2]
        expected_ast = {"type": "ObjectLiteral", "children": [prop1, prop2], "value": None, "line": 1, "column": 1}
        mock_create_ast_node.return_value = expected_ast
        
        # Execute
        result = _parse_object_literal(parser_state)
        
        # Verify
        self.assertEqual(result, expected_ast)
        self.assertEqual(mock_parse_property.call_count, 2)

    @patch("._parse_object_literal_package._parse_object_literal_src._create_ast_node")
    @patch("._parse_object_literal_package._parse_object_literal_src._parse_property")
    @patch("._parse_object_literal_package._parse_object_literal_src._consume_token")
    def test_unexpected_token_after_property(self, mock_consume_token, mock_parse_property, mock_create_ast_node):
        """Test error when unexpected token appears after property"""
        # Setup tokens
        left_brace = create_token("LEFT_BRACE", "{", 1, 1)
        unexpected = create_token("IDENTIFIER", "foo", 1, 5)
        tokens = [left_brace, unexpected]
        parser_state = create_parser_state(tokens, pos=0)
        
        # Setup mocks
        prop1 = {"type": "Property", "value": "prop1"}
        mock_consume_token.side_effect = [left_brace]
        mock_parse_property.return_value = prop1
        
        # Execute and verify
        with self.assertRaises(ValueError) as context:
            _parse_object_literal(parser_state)
        
        self.assertIn("Expected COMMA or RIGHT_BRACE", str(context.exception))
        self.assertIn("IDENTIFIER", str(context.exception))

    @patch("._parse_object_literal_package._parse_object_literal_src._create_ast_node")
    @patch("._parse_object_literal_package._parse_object_literal_src._parse_property")
    @patch("._parse_object_literal_package._parse_object_literal_src._consume_token")
    def test_unexpected_end_of_input_while_parsing(self, mock_consume_token, mock_parse_property, mock_create_ast_node):
        """Test error when input ends unexpectedly while parsing properties"""
        # Setup tokens
        left_brace = create_token("LEFT_BRACE", "{", 1, 1)
        tokens = [left_brace]
        parser_state = create_parser_state(tokens, pos=0)
        
        # Setup mocks
        prop1 = {"type": "Property", "value": "prop1"}
        mock_consume_token.side_effect = [left_brace]
        mock_parse_property.return_value = prop1
        
        # Execute and verify
        with self.assertRaises(ValueError) as context:
            _parse_object_literal(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("object literal", str(context.exception))

    @patch("._parse_object_literal_package._parse_object_literal_src._create_ast_node")
    @patch("._parse_object_literal_package._parse_object_literal_src._parse_property")
    @patch("._parse_object_literal_package._parse_object_literal_src._consume_token")
    def test_unexpected_end_before_right_brace(self, mock_consume_token, mock_parse_property, mock_create_ast_node):
        """Test error when input ends after property without RIGHT_BRACE"""
        # Setup tokens
        left_brace = create_token("LEFT_BRACE", "{", 1, 1)
        comma = create_token("COMMA", ",", 1, 5)
        tokens = [left_brace, comma]
        parser_state = create_parser_state(tokens, pos=0)
        
        # Setup mocks
        prop1 = {"type": "Property", "value": "prop1"}
        mock_consume_token.side_effect = [left_brace, comma]
        mock_parse_property.return_value = prop1
        
        # Execute and verify
        with self.assertRaises(ValueError) as context:
            _parse_object_literal(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))

    @patch("._parse_object_literal_package._parse_object_literal_src._create_ast_node")
    @patch("._parse_object_literal_package._parse_object_literal_src._parse_property")
    @patch("._parse_object_literal_package._parse_object_literal_src._consume_token")
    def test_preserves_filename_in_error(self, mock_consume_token, mock_parse_property, mock_create_ast_node):
        """Test that error messages include the filename from parser_state"""
        # Setup tokens with custom filename
        left_brace = create_token("LEFT_BRACE", "{", 1, 1)
        tokens = [left_brace]
        parser_state = create_parser_state(tokens, pos=0, filename="my_script.js")
        
        # Setup mocks
        mock_consume_token.side_effect = [left_brace]
        
        # Execute and verify
        with self.assertRaises(ValueError) as context:
            _parse_object_literal(parser_state)
        
        self.assertIn("my_script.js", str(context.exception))

    @patch("._parse_object_literal_package._parse_object_literal_src._create_ast_node")
    @patch("._parse_object_literal_package._parse_object_literal_src._parse_property")
    @patch("._parse_object_literal_package._parse_object_literal_src._consume_token")
    def test_ast_node_has_correct_start_position(self, mock_consume_token, mock_parse_property, mock_create_ast_node):
        """Test that AST node uses LEFT_BRACE position for line/column"""
        # Setup tokens with specific positions
        left_brace = create_token("LEFT_BRACE", "{", 5, 10)
        right_brace = create_token("RIGHT_BRACE", "}", 5, 20)
        tokens = [left_brace, right_brace]
        parser_state = create_parser_state(tokens, pos=0)
        
        # Setup mocks
        mock_consume_token.side_effect = [left_brace, right_brace]
        expected_ast = {"type": "ObjectLiteral", "children": [], "value": None, "line": 5, "column": 10}
        mock_create_ast_node.return_value = expected_ast
        
        # Execute
        result = _parse_object_literal(parser_state)
        
        # Verify
        mock_create_ast_node.assert_called_once_with(
            node_type="ObjectLiteral",
            value=None,
            children=[],
            line=5,
            column=10
        )

    @patch("._parse_object_literal_package._parse_object_literal_src._create_ast_node")
    @patch("._parse_object_literal_package._parse_object_literal_src._parse_property")
    @patch("._parse_object_literal_package._parse_object_literal_src._consume_token")
    def test_consume_token_called_with_correct_types(self, mock_consume_token, mock_parse_property, mock_create_ast_node):
        """Test that _consume_token is called with correct token types in order"""
        # Setup tokens
        left_brace = create_token("LEFT_BRACE", "{", 1, 1)
        comma = create_token("COMMA", ",", 1, 5)
        right_brace = create_token("RIGHT_BRACE", "}", 1, 10)
        tokens = [left_brace, comma, right_brace]
        parser_state = create_parser_state(tokens, pos=0)
        
        # Setup mocks
        mock_consume_token.side_effect = [left_brace, comma, right_brace]
        mock_parse_property.return_value = {"type": "Property"}
        mock_create_ast_node.return_value = {"type": "ObjectLiteral"}
        
        # Execute
        _parse_object_literal(parser_state)
        
        # Verify consume_token calls
        calls = [
            call(parser_state, "LEFT_BRACE"),
            call(parser_state, "COMMA"),
            call(parser_state, "RIGHT_BRACE")
        ]
        mock_consume_token.assert_has_calls(calls, any_order=False)


if __name__ == "__main__":
    unittest.main()
