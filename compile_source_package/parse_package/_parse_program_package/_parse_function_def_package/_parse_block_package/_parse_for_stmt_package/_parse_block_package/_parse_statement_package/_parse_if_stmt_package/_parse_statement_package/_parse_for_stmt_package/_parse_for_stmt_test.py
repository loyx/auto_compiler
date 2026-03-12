# === imports ===
import unittest
from unittest.mock import patch

# === import unit under test ===
from ._parse_for_stmt_src import _parse_for_stmt


# === test class ===
class TestParseForStmt(unittest.TestCase):
    """Test cases for _parse_for_stmt function."""

    def test_happy_path_valid_for_statement(self):
        """Test parsing a valid for statement with all components."""
        # Arrange
        tokens = [
            {"type": "FOR", "value": "for", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 5},
            {"type": "INT", "value": "0", "line": 1, "column": 6},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 7},
            {"type": "IDENTIFIER", "value": "i", "line": 1, "column": 8},
            {"type": "LT", "value": "<", "line": 1, "column": 10},
            {"type": "INT", "value": "10", "line": 1, "column": 11},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 13},
            {"type": "IDENTIFIER", "value": "i", "line": 1, "column": 14},
            {"type": "PLUSPLUS", "value": "++", "line": 1, "column": 15},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 17},
            {"type": "LBRACE", "value": "{", "line": 1, "column": 19},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 20},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        # Mock sub-functions
        mock_init_ast = {"type": "EXPR_STMT", "children": [], "value": "init", "line": 1, "column": 6}
        mock_condition_ast = {"type": "BINARY_EXPR", "children": [], "value": "<", "line": 1, "column": 10}
        mock_update_ast = {"type": "UNARY_EXPR", "children": [], "value": "++", "line": 1, "column": 14}
        mock_body_ast = {"type": "BLOCK", "children": [], "value": "", "line": 1, "column": 19}
        
        with patch("._parse_for_stmt_src._parse_statement", return_value=mock_init_ast) as mock_parse_stmt, \
             patch("._parse_for_stmt_src._parse_expression", side_effect=[mock_condition_ast, mock_update_ast]) as mock_parse_expr, \
             patch("._parse_for_stmt_src._parse_block", return_value=mock_body_ast) as mock_parse_block, \
             patch("._parse_for_stmt_src._expect_token") as mock_expect:
            
            # Act
            result = _parse_for_stmt(parser_state)
            
            # Assert
            self.assertEqual(result["type"], "FOR_STMT")
            self.assertEqual(result["value"], "for")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 4)
            self.assertEqual(result["children"][0], mock_init_ast)
            self.assertEqual(result["children"][1], mock_condition_ast)
            self.assertEqual(result["children"][2], mock_update_ast)
            self.assertEqual(result["children"][3], mock_body_ast)
            
            # Verify _expect_token called twice for LPAREN and RPAREN
            self.assertEqual(mock_expect.call_count, 2)
            mock_expect.assert_any_call(parser_state, "LPAREN")
            mock_expect.assert_any_call(parser_state, "RPAREN")
            
            # Verify sub-functions called
            mock_parse_stmt.assert_called_once()
            self.assertEqual(mock_parse_expr.call_count, 2)
            mock_parse_block.assert_called_once()

    def test_missing_for_token(self):
        """Test that SyntaxError is raised when FOR token is missing."""
        # Arrange
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        # Act & Assert
        with self.assertRaises(SyntaxError) as context:
            _parse_for_stmt(parser_state)
        
        self.assertIn("Expected FOR token", str(context.exception))
        self.assertIn("test.c", str(context.exception))

    def test_missing_for_token_at_end_of_tokens(self):
        """Test that SyntaxError is raised when tokens list is exhausted."""
        # Arrange
        tokens = []
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "unknown.c"
        }
        
        # Act & Assert
        with self.assertRaises(SyntaxError) as context:
            _parse_for_stmt(parser_state)
        
        self.assertIn("Expected FOR token", str(context.exception))

    def test_for_token_not_at_current_position(self):
        """Test that SyntaxError is raised when FOR token is not at current pos."""
        # Arrange
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "FOR", "value": "for", "line": 1, "column": 3},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,  # Points to IDENTIFIER, not FOR
            "filename": "test.c"
        }
        
        # Act & Assert
        with self.assertRaises(SyntaxError) as context:
            _parse_for_stmt(parser_state)
        
        self.assertIn("Expected FOR token", str(context.exception))

    def test_position_updated_after_parsing(self):
        """Test that parser_state['pos'] is updated correctly."""
        # Arrange
        tokens = [
            {"type": "FOR", "value": "for", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 5},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_init_ast = {"type": "EXPR_STMT", "children": [], "value": "", "line": 1, "column": 6}
        mock_condition_ast = {"type": "BINARY_EXPR", "children": [], "value": "", "line": 1, "column": 7}
        mock_update_ast = {"type": "UNARY_EXPR", "children": [], "value": "", "line": 1, "column": 8}
        mock_body_ast = {"type": "BLOCK", "children": [], "value": "", "line": 1, "column": 9}
        
        with patch("._parse_for_stmt_src._parse_statement", return_value=mock_init_ast), \
             patch("._parse_for_stmt_src._parse_expression", side_effect=[mock_condition_ast, mock_update_ast]), \
             patch("._parse_for_stmt_src._parse_block", return_value=mock_body_ast), \
             patch("._parse_for_stmt_src._expect_token", side_effect=lambda ps, tt: setattr(ps, 'pos', ps['pos'] + 1)):
            
            # Act
            _parse_for_stmt(parser_state)
            
            # Assert: pos should be incremented at least for FOR token
            self.assertGreater(parser_state["pos"], 0)

    def test_ast_node_contains_correct_metadata(self):
        """Test that AST node contains correct line and column from FOR token."""
        # Arrange
        tokens = [
            {"type": "FOR", "value": "for", "line": 10, "column": 25},
            {"type": "LPAREN", "value": "(", "line": 10, "column": 29},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_init_ast = {"type": "EXPR_STMT", "children": [], "value": "", "line": 10, "column": 30}
        mock_condition_ast = {"type": "BINARY_EXPR", "children": [], "value": "", "line": 10, "column": 31}
        mock_update_ast = {"type": "UNARY_EXPR", "children": [], "value": "", "line": 10, "column": 32}
        mock_body_ast = {"type": "BLOCK", "children": [], "value": "", "line": 10, "column": 33}
        
        with patch("._parse_for_stmt_src._parse_statement", return_value=mock_init_ast), \
             patch("._parse_for_stmt_src._parse_expression", side_effect=[mock_condition_ast, mock_update_ast]), \
             patch("._parse_for_stmt_src._parse_block", return_value=mock_body_ast), \
             patch("._parse_for_stmt_src._expect_token"):
            
            # Act
            result = _parse_for_stmt(parser_state)
            
            # Assert
            self.assertEqual(result["line"], 10)
            self.assertEqual(result["column"], 25)

    def test_children_order_is_correct(self):
        """Test that children are in correct order: [init, condition, update, body]."""
        # Arrange
        tokens = [
            {"type": "FOR", "value": "for", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 5},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 6},
            {"type": "LBRACE", "value": "{", "line": 1, "column": 7},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 8},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_init = {"type": "INIT", "value": "init"}
        mock_condition = {"type": "COND", "value": "condition"}
        mock_update = {"type": "UPDATE", "value": "update"}
        mock_body = {"type": "BODY", "value": "body"}
        
        call_order = []
        
        def track_parse_statement(ps):
            call_order.append('statement')
            return mock_init
        
        def track_parse_expression(ps):
            call_order.append('expression')
            if len([c for c in call_order if c == 'expression']) == 1:
                return mock_condition
            return mock_update
        
        def track_parse_block(ps):
            call_order.append('block')
            return mock_body
        
        with patch("._parse_for_stmt_src._parse_statement", side_effect=track_parse_statement), \
             patch("._parse_for_stmt_src._parse_expression", side_effect=track_parse_expression), \
             patch("._parse_for_stmt_src._parse_block", side_effect=track_parse_block), \
             patch("._parse_for_stmt_src._expect_token"):
            
            # Act
            result = _parse_for_stmt(parser_state)
            
            # Assert
            self.assertEqual(result["children"][0]["type"], "INIT")
            self.assertEqual(result["children"][1]["type"], "COND")
            self.assertEqual(result["children"][2]["type"], "UPDATE")
            self.assertEqual(result["children"][3]["type"], "BODY")

    def test_expect_token_called_with_correct_types(self):
        """Test that _expect_token is called with LPAREN and RPAREN in correct order."""
        # Arrange
        tokens = [
            {"type": "FOR", "value": "for", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 5},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 6},
            {"type": "LBRACE", "value": "{", "line": 1, "column": 7},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 8},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_init_ast = {"type": "EXPR_STMT", "children": [], "value": "", "line": 1, "column": 6}
        mock_condition_ast = {"type": "BINARY_EXPR", "children": [], "value": "", "line": 1, "column": 7}
        mock_update_ast = {"type": "UNARY_EXPR", "children": [], "value": "", "line": 1, "column": 8}
        mock_body_ast = {"type": "BLOCK", "children": [], "value": "", "line": 1, "column": 9}
        
        with patch("._parse_for_stmt_src._parse_statement", return_value=mock_init_ast), \
             patch("._parse_for_stmt_src._parse_expression", side_effect=[mock_condition_ast, mock_update_ast]), \
             patch("._parse_for_stmt_src._parse_block", return_value=mock_body_ast), \
             patch("._parse_for_stmt_src._expect_token") as mock_expect:
            
            # Act
            _parse_for_stmt(parser_state)
            
            # Assert: LPAREN should be called before RPAREN
            calls = mock_expect.call_args_list
            self.assertEqual(len(calls), 2)
            self.assertEqual(calls[0][0][1], "LPAREN")
            self.assertEqual(calls[1][0][1], "RPAREN")

    def test_parse_expression_called_twice(self):
        """Test that _parse_expression is called exactly twice for condition and update."""
        # Arrange
        tokens = [
            {"type": "FOR", "value": "for", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 5},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 6},
            {"type": "LBRACE", "value": "{", "line": 1, "column": 7},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 8},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_init_ast = {"type": "EXPR_STMT", "children": [], "value": "", "line": 1, "column": 6}
        mock_condition_ast = {"type": "BINARY_EXPR", "children": [], "value": "", "line": 1, "column": 7}
        mock_update_ast = {"type": "UNARY_EXPR", "children": [], "value": "", "line": 1, "column": 8}
        mock_body_ast = {"type": "BLOCK", "children": [], "value": "", "line": 1, "column": 9}
        
        with patch("._parse_for_stmt_src._parse_statement", return_value=mock_init_ast), \
             patch("._parse_for_stmt_src._parse_expression", return_value=mock_condition_ast) as mock_parse_expr, \
             patch("._parse_for_stmt_src._parse_block", return_value=mock_body_ast), \
             patch("._parse_for_stmt_src._expect_token"):
            
            # Act
            _parse_for_stmt(parser_state)
            
            # Assert
            self.assertEqual(mock_parse_expr.call_count, 2)


# === main entry point ===
if __name__ == "__main__":
    unittest.main()
