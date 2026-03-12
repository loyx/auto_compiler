"""
单元测试文件：_parse_binary 函数测试
测试 Pratt parsing 算法解析二元表达式的各种场景
"""
import pytest
from unittest.mock import patch

from ._parse_binary_src import _parse_binary


class TestParseBinary:
    """Tests for _parse_binary function"""
    
    def test_simple_binary_expression(self):
        """Test parsing a simple binary expression: 1 + 2"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        unary_literal_1 = {"type": "LITERAL", "value": {"literal": 1}, "line": 1, "column": 1}
        unary_literal_2 = {"type": "LITERAL", "value": {"literal": 2}, "line": 1, "column": 5}
        
        with patch.object(_parse_binary, '_parse_unary') as mock_unary:
            mock_unary.side_effect = [unary_literal_1, unary_literal_2]
            
            with patch.object(_parse_binary, '_is_binary_operator') as mock_is_op:
                mock_is_op.side_effect = [True, False]
                
                with patch.object(_parse_binary, '_get_operator_precedence') as mock_prec:
                    mock_prec.return_value = (2, "left")
                    
                    result = _parse_binary(parser_state)
                    
                    assert result["type"] == "BINARY_OP"
                    assert result["value"]["operator"] == "+"
                    assert len(result["children"]) == 2
                    assert result["children"][0] == unary_literal_1
                    assert result["children"][1] == unary_literal_2
                    assert result["line"] == 1
                    assert result["column"] == 3
                    assert parser_state["pos"] == 3
    
    def test_operator_precedence(self):
        """Test operator precedence: 1 + 2 * 3 should parse as 1 + (2 * 3)"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
                {"type": "STAR", "value": "*", "line": 1, "column": 7},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 9},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        unary_1 = {"type": "LITERAL", "value": {"literal": 1}, "line": 1, "column": 1}
        unary_2 = {"type": "LITERAL", "value": {"literal": 2}, "line": 1, "column": 5}
        unary_3 = {"type": "LITERAL", "value": {"literal": 3}, "line": 1, "column": 9}
        mul_node = {
            "type": "BINARY_OP",
            "value": {"operator": "*"},
            "children": [unary_2, unary_3],
            "line": 1,
            "column": 7
        }
        
        with patch.object(_parse_binary, '_parse_unary') as mock_unary:
            mock_unary.side_effect = [unary_1, unary_2, unary_3]
            
            with patch.object(_parse_binary, '_is_binary_operator') as mock_is_op:
                mock_is_op.side_effect = [True, True, False]
                
                with patch.object(_parse_binary, '_get_operator_precedence') as mock_prec:
                    def get_prec(token):
                        if token["type"] == "PLUS":
                            return (2, "left")
                        elif token["type"] == "STAR":
                            return (3, "left")
                        return (-1, "left")
                    mock_prec.side_effect = get_prec
                    
                    result = _parse_binary(parser_state)
                    
                    assert result["type"] == "BINARY_OP"
                    assert result["value"]["operator"] == "+"
                    assert result["children"][0] == unary_1
                    assert result["children"][1] == mul_node
                    assert parser_state["pos"] == 5
    
    def test_right_associativity(self):
        """Test right associativity: 2 ** 3 ** 2 should parse as 2 ** (3 ** 2)"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "2", "line": 1, "column": 1},
                {"type": "STAR_STAR", "value": "**", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 6},
                {"type": "STAR_STAR", "value": "**", "line": 1, "column": 8},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 11},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        unary_2a = {"type": "LITERAL", "value": {"literal": 2}, "line": 1, "column": 1}
        unary_3 = {"type": "LITERAL", "value": {"literal": 3}, "line": 1, "column": 6}
        unary_2b = {"type": "LITERAL", "value": {"literal": 2}, "line": 1, "column": 11}
        inner_pow = {
            "type": "BINARY_OP",
            "value": {"operator": "**"},
            "children": [unary_3, unary_2b],
            "line": 1,
            "column": 8
        }
        
        with patch.object(_parse_binary, '_parse_unary') as mock_unary:
            mock_unary.side_effect = [unary_2a, unary_3, unary_2b]
            
            with patch.object(_parse_binary, '_is_binary_operator') as mock_is_op:
                mock_is_op.side_effect = [True, True, False]
                
                with patch.object(_parse_binary, '_get_operator_precedence') as mock_prec:
                    mock_prec.return_value = (4, "right")
                    
                    result = _parse_binary(parser_state)
                    
                    assert result["type"] == "BINARY_OP"
                    assert result["value"]["operator"] == "**"
                    assert result["children"][0] == unary_2a
                    assert result["children"][1] == inner_pow
                    assert parser_state["pos"] == 5
    
    def test_left_associativity(self):
        """Test left associativity: 1 - 2 - 3 should parse as (1 - 2) - 3"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "MINUS", "value": "-", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
                {"type": "MINUS", "value": "-", "line": 1, "column": 7},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 9},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        unary_1 = {"type": "LITERAL", "value": {"literal": 1}, "line": 1, "column": 1}
        unary_2 = {"type": "LITERAL", "value": {"literal": 2}, "line": 1, "column": 5}
        unary_3 = {"type": "LITERAL", "value": {"literal": 3}, "line": 1, "column": 9}
        first_sub = {
            "type": "BINARY_OP",
            "value": {"operator": "-"},
            "children": [unary_1, unary_2],
            "line": 1,
            "column": 3
        }
        
        with patch.object(_parse_binary, '_parse_unary') as mock_unary:
            mock_unary.side_effect = [unary_1, unary_2, unary_3]
            
            with patch.object(_parse_binary, '_is_binary_operator') as mock_is_op:
                mock_is_op.side_effect = [True, True, False]
                
                with patch.object(_parse_binary, '_get_operator_precedence') as mock_prec:
                    mock_prec.return_value = (2, "left")
                    
                    result = _parse_binary(parser_state)
                    
                    assert result["type"] == "BINARY_OP"
                    assert result["value"]["operator"] == "-"
                    assert result["children"][0] == first_sub
                    assert result["children"][1] == unary_3
                    assert parser_state["pos"] == 5
    
    def test_single_operand_no_operator(self):
        """Test parsing single operand with no operator"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        unary_result = {"type": "LITERAL", "value": {"literal": 42}, "line": 1, "column": 1}
        
        with patch.object(_parse_binary, '_parse_unary') as mock_unary:
            mock_unary.return_value = unary_result
            
            with patch.object(_parse_binary, '_is_binary_operator') as mock_is_op:
                mock_is_op.return_value = False
                
                result = _parse_binary(parser_state)
                
                assert result == unary_result
                assert parser_state["pos"] == 0
                mock_is_op.assert_called_once()
    
    def test_end_of_tokens_after_left_operand(self):
        """Test when tokens end after parsing left operand"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        unary_result = {"type": "LITERAL", "value": {"literal": 1}, "line": 1, "column": 1}
        
        with patch.object(_parse_binary, '_parse_unary') as mock_unary:
            mock_unary.return_value = unary_result
            
            with patch.object(_parse_binary, '_is_binary_operator') as mock_is_op:
                mock_is_op.return_value = False
                
                result = _parse_binary(parser_state)
                
                assert result == unary_result
                assert parser_state["pos"] == 0
    
    def test_min_precedence_stops_parsing(self):
        """Test that min_precedence parameter stops parsing when operator precedence is lower"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        unary_1 = {"type": "LITERAL", "value": {"literal": 1}, "line": 1, "column": 1}
        
        with patch.object(_parse_binary, '_parse_unary') as mock_unary:
            mock_unary.return_value = unary_1
            
            with patch.object(_parse_binary, '_is_binary_operator') as mock_is_op:
                mock_is_op.return_value = True
                
                with patch.object(_parse_binary, '_get_operator_precedence') as mock_prec:
                    mock_prec.return_value = (2, "left")
                    
                    result = _parse_binary(parser_state, min_precedence=3)
                    
                    assert result == unary_1
                    assert parser_state["pos"] == 0
                    mock_is_op.assert_called_once()
    
    def test_left_assoc_equal_precedence_stops(self):
        """Test that left-associative operator with equal precedence stops parsing"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        unary_1 = {"type": "LITERAL", "value": {"literal": 1}, "line": 1, "column": 1}
        
        with patch.object(_parse_binary, '_parse_unary') as mock_unary:
            mock_unary.return_value = unary_1
            
            with patch.object(_parse_binary, '_is_binary_operator') as mock_is_op:
                mock_is_op.return_value = True
                
                with patch.object(_parse_binary, '_get_operator_precedence') as mock_prec:
                    mock_prec.return_value = (2, "left")
                    
                    result = _parse_binary(parser_state, min_precedence=2)
                    
                    assert result == unary_1
                    assert parser_state["pos"] == 0
    
    def test_right_assoc_equal_precedence_continues(self):
        """Test that right-associative operator with equal precedence continues parsing"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "2", "line": 1, "column": 1},
                {"type": "STAR_STAR", "value": "**", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 6},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        unary_2 = {"type": "LITERAL", "value": {"literal": 2}, "line": 1, "column": 1}
        unary_3 = {"type": "LITERAL", "value": {"literal": 3}, "line": 1, "column": 6}
        
        with patch.object(_parse_binary, '_parse_unary') as mock_unary:
            mock_unary.side_effect = [unary_2, unary_3]
            
            with patch.object(_parse_binary, '_is_binary_operator') as mock_is_op:
                mock_is_op.side_effect = [True, False]
                
                with patch.object(_parse_binary, '_get_operator_precedence') as mock_prec:
                    mock_prec.return_value = (4, "right")
                    
                    result = _parse_binary(parser_state, min_precedence=4)
                    
                    assert result["type"] == "BINARY_OP"
                    assert result["value"]["operator"] == "**"
                    assert parser_state["pos"] == 3
    
    def test_parse_unary_raises_syntax_error(self):
        """Test that SyntaxError from _parse_unary propagates"""
        parser_state = {
            "tokens": [
                {"type": "INVALID", "value": "xyz", "line": 5, "column": 10},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch.object(_parse_binary, '_parse_unary') as mock_unary:
            mock_unary.side_effect = SyntaxError("test.py:5:10: Invalid token")
            
            with pytest.raises(SyntaxError) as exc_info:
                _parse_binary(parser_state)
            
            assert "test.py:5:10: Invalid token" in str(exc_info.value)
    
    def test_complex_expression_multiple_operators(self):
        """Test complex expression: 1 + 2 * 3 - 4"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
                {"type": "STAR", "value": "*", "line": 1, "column": 7},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 9},
                {"type": "MINUS", "value": "-", "line": 1, "column": 11},
                {"type": "NUMBER", "value": "4", "line": 1, "column": 13},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        unary_1 = {"type": "LITERAL", "value": {"literal": 1}, "line": 1, "column": 1}
        unary_2 = {"type": "LITERAL", "value": {"literal": 2}, "line": 1, "column": 5}
        unary_3 = {"type": "LITERAL", "value": {"literal": 3}, "line": 1, "column": 9}
        unary_4 = {"type": "LITERAL", "value": {"literal": 4}, "line": 1, "column": 13}
        
        mul_node = {
            "type": "BINARY_OP",
            "value": {"operator": "*"},
            "children": [unary_2, unary_3],
            "line": 1,
            "column": 7
        }
        
        add_node = {
            "type": "BINARY_OP",
            "value": {"operator": "+"},
            "children": [unary_1, mul_node],
            "line": 1,
            "column": 3
        }
        
        with patch.object(_parse_binary, '_parse_unary') as mock_unary:
            mock_unary.side_effect = [unary_1, unary_2, unary_3, unary_4]
            
            with patch.object(_parse_binary, '_is_binary_operator') as mock_is_op:
                mock_is_op.side_effect = [True, True, True, False]
                
                with patch.object(_parse_binary, '_get_operator_precedence') as mock_prec:
                    def get_prec(token):
                        if token["type"] in ["PLUS", "MINUS"]:
                            return (2, "left")
                        elif token["type"] == "STAR":
                            return (3, "left")
                        return (-1, "left")
                    mock_prec.side_effect = get_prec
                    
                    result = _parse_binary(parser_state)
                    
                    assert result["type"] == "BINARY_OP"
                    assert result["value"]["operator"] == "-"
                    assert result["children"][0] == add_node
                    assert result["children"][1] == unary_4
                    assert parser_state["pos"] == 7
    
    def test_position_advances_correctly(self):
        """Test that parser_state position advances correctly after consuming tokens"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        unary_1 = {"type": "LITERAL", "value": {"literal": 1}, "line": 1, "column": 1}
        unary_2 = {"type": "LITERAL", "value": {"literal": 2}, "line": 1, "column": 5}
        
        with patch.object(_parse_binary, '_parse_unary') as mock_unary:
            mock_unary.side_effect = [unary_1, unary_2]
            
            with patch.object(_parse_binary, '_is_binary_operator') as mock_is_op:
                mock_is_op.side_effect = [True, False]
                
                with patch.object(_parse_binary, '_get_operator_precedence') as mock_prec:
                    mock_prec.return_value = (2, "left")
                    
                    _parse_binary(parser_state)
                    
                    assert parser_state["pos"] == 3
    
    def test_ast_node_contains_correct_location(self):
        """Test that AST node contains correct line and column from operator token"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 10, "column": 5},
                {"type": "STAR", "value": "*", "line": 10, "column": 7},
                {"type": "NUMBER", "value": "2", "line": 10, "column": 9},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        unary_1 = {"type": "LITERAL", "value": {"literal": 1}, "line": 10, "column": 5}
        unary_2 = {"type": "LITERAL", "value": {"literal": 2}, "line": 10, "column": 9}
        
        with patch.object(_parse_binary, '_parse_unary') as mock_unary:
            mock_unary.side_effect = [unary_1, unary_2]
            
            with patch.object(_parse_binary, '_is_binary_operator') as mock_is_op:
                mock_is_op.side_effect = [True, False]
                
                with patch.object(_parse_binary, '_get_operator_precedence') as mock_prec:
                    mock_prec.return_value = (3, "left")
                    
                    result = _parse_binary(parser_state)
                    
                    assert result["line"] == 10
                    assert result["column"] == 7


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
