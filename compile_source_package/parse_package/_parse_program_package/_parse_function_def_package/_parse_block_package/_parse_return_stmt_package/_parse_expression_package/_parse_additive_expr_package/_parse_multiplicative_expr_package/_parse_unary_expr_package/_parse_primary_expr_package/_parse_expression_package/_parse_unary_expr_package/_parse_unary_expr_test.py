import pytest
from unittest.mock import patch

# Import the function under test using relative import
from ._parse_unary_expr_src import _parse_unary_expr


class TestParseUnaryExpr:
    """Test cases for _parse_unary_expr function."""
    
    def test_parse_minus_unary_operator(self):
        """Test parsing a single MINUS unary operator."""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        # Mock _parse_primary_expr to return a simple identifier AST
        with patch("._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "line": 1,
                "column": 2
            }
            
            result = _parse_unary_expr(parser_state)
            
            # Verify the result is a UNARY_OP node
            assert result["type"] == "UNARY_OP"
            assert result["operator"] == "-"
            assert result["line"] == 1
            assert result["column"] == 1
            assert result["operand"]["type"] == "IDENTIFIER"
            assert result["operand"]["value"] == "x"
            
            # Verify parser state was updated
            assert parser_state["pos"] == 1
            
            # Verify _parse_primary_expr was called
            mock_primary.assert_called_once_with(parser_state)
    
    def test_parse_not_unary_operator(self):
        """Test parsing a single NOT unary operator."""
        parser_state = {
            "tokens": [
                {"type": "NOT", "value": "!", "line": 2, "column": 5},
                {"type": "IDENTIFIER", "value": "flag", "line": 2, "column": 6}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "flag",
                "line": 2,
                "column": 6
            }
            
            result = _parse_unary_expr(parser_state)
            
            assert result["type"] == "UNARY_OP"
            assert result["operator"] == "!"
            assert result["line"] == 2
            assert result["column"] == 5
            assert result["operand"]["type"] == "IDENTIFIER"
            assert parser_state["pos"] == 1
    
    def test_chained_unary_operators_double_minus(self):
        """Test parsing chained unary operators: --x"""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 1},
                {"type": "MINUS", "value": "-", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "line": 1,
                "column": 3
            }
            
            result = _parse_unary_expr(parser_state)
            
            # Outer UNARY_OP (-)
            assert result["type"] == "UNARY_OP"
            assert result["operator"] == "-"
            assert result["line"] == 1
            assert result["column"] == 1
            
            # Inner UNARY_OP (-)
            inner = result["operand"]
            assert inner["type"] == "UNARY_OP"
            assert inner["operator"] == "-"
            assert inner["line"] == 1
            assert inner["column"] == 2
            
            # Operand (IDENTIFIER)
            assert inner["operand"]["type"] == "IDENTIFIER"
            assert inner["operand"]["value"] == "x"
            
            assert parser_state["pos"] == 2
    
    def test_chained_unary_operators_mixed(self):
        """Test parsing mixed chained unary operators: -!x"""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 1},
                {"type": "NOT", "value": "!", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "line": 1,
                "column": 3
            }
            
            result = _parse_unary_expr(parser_state)
            
            assert result["type"] == "UNARY_OP"
            assert result["operator"] == "-"
            assert result["line"] == 1
            assert result["column"] == 1
            assert result["operand"]["type"] == "UNARY_OP"
            assert result["operand"]["operator"] == "!"
            assert result["operand"]["operand"]["type"] == "IDENTIFIER"
            assert parser_state["pos"] == 2
    
    def test_no_unary_operator_delegates_to_primary(self):
        """Test that non-unary tokens delegate to _parse_primary_expr."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr") as mock_primary:
            expected_ast = {
                "type": "IDENTIFIER",
                "value": "x",
                "line": 1,
                "column": 1
            }
            mock_primary.return_value = expected_ast
            
            result = _parse_unary_expr(parser_state)
            
            assert result == expected_ast
            assert parser_state["pos"] == 0
            mock_primary.assert_called_once_with(parser_state)
    
    def test_end_of_input_raises_syntax_error(self):
        """Test that end of input raises SyntaxError."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.c"
        }
        
        with pytest.raises(SyntaxError) as exc_info:
            _parse_unary_expr(parser_state)
        
        assert "Unexpected end of input" in str(exc_info.value)
    
    def test_end_of_input_after_operator_raises_syntax_error(self):
        """Test that end of input after unary operator raises SyntaxError."""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.side_effect = SyntaxError("Unexpected end of input at line test.c")
            
            with pytest.raises(SyntaxError) as exc_info:
                _parse_unary_expr(parser_state)
            
            assert "Unexpected end of input" in str(exc_info.value)
    
    def test_position_advanced_after_consuming_operator(self):
        """Test that parser position is advanced after consuming unary operator."""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "line": 1,
                "column": 2
            }
            
            _parse_unary_expr(parser_state)
            
            assert parser_state["pos"] == 1
            mock_primary.assert_called_once()
    
    def test_literal_operand(self):
        """Test unary operator with literal operand."""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 3, "column": 10},
                {"type": "NUMBER", "value": "42", "line": 3, "column": 11}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = {
                "type": "LITERAL",
                "value": 42,
                "line": 3,
                "column": 11
            }
            
            result = _parse_unary_expr(parser_state)
            
            assert result["type"] == "UNARY_OP"
            assert result["operator"] == "-"
            assert result["operand"]["type"] == "LITERAL"
            assert result["operand"]["value"] == 42
    
    def test_parenthesized_expression_operand(self):
        """Test unary operator with parenthesized expression operand."""
        parser_state = {
            "tokens": [
                {"type": "NOT", "value": "!", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = {
                "type": "BINARY_OP",
                "operator": "+",
                "left": {"type": "IDENTIFIER", "value": "a"},
                "right": {"type": "IDENTIFIER", "value": "b"},
                "line": 1,
                "column": 2
            }
            
            result = _parse_unary_expr(parser_state)
            
            assert result["type"] == "UNARY_OP"
            assert result["operator"] == "!"
            assert result["operand"]["type"] == "BINARY_OP"
            assert result["operand"]["operator"] == "+"
