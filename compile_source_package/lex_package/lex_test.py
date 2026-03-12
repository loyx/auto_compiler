#!/usr/bin/env python3
"""Unit tests for the lex function - C language lexical analyzer."""

import unittest

# Relative import from the same package
from .lex_src import lex


class TestLexHappyPath(unittest.TestCase):
    """Test happy path scenarios for lex function."""

    def test_empty_source(self):
        """Test empty source code returns empty token list."""
        result = lex("", "test.c")
        self.assertEqual(result, [])

    def test_single_identifier(self):
        """Test single identifier token."""
        result = lex("x", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "IDENTIFIER")
        self.assertEqual(result[0]["value"], "x")
        self.assertEqual(result[0]["line"], 1)
        self.assertEqual(result[0]["column"], 1)

    def test_keyword_int(self):
        """Test int keyword."""
        result = lex("int", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "KEYWORD_int")
        self.assertEqual(result[0]["value"], "int")

    def test_keyword_char(self):
        """Test char keyword."""
        result = lex("char", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "KEYWORD_char")
        self.assertEqual(result[0]["value"], "char")

    def test_keyword_if(self):
        """Test if keyword."""
        result = lex("if", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "KEYWORD_if")
        self.assertEqual(result[0]["value"], "if")

    def test_keyword_else(self):
        """Test else keyword."""
        result = lex("else", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "KEYWORD_else")
        self.assertEqual(result[0]["value"], "else")

    def test_keyword_while(self):
        """Test while keyword."""
        result = lex("while", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "KEYWORD_while")
        self.assertEqual(result[0]["value"], "while")

    def test_keyword_for(self):
        """Test for keyword."""
        result = lex("for", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "KEYWORD_for")
        self.assertEqual(result[0]["value"], "for")

    def test_keyword_return(self):
        """Test return keyword."""
        result = lex("return", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "KEYWORD_return")
        self.assertEqual(result[0]["value"], "return")

    def test_keyword_break(self):
        """Test break keyword."""
        result = lex("break", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "KEYWORD_break")
        self.assertEqual(result[0]["value"], "break")

    def test_keyword_continue(self):
        """Test continue keyword."""
        result = lex("continue", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "KEYWORD_continue")
        self.assertEqual(result[0]["value"], "continue")

    def test_integer_constant(self):
        """Test integer constant token."""
        result = lex("123", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "INT_CONST")
        self.assertEqual(result[0]["value"], "123")
        self.assertEqual(result[0]["line"], 1)
        self.assertEqual(result[0]["column"], 1)

    def test_char_constant_simple(self):
        """Test simple character constant."""
        result = lex("'a'", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "CHAR_CONST")
        self.assertEqual(result[0]["value"], "'a'")

    def test_char_constant_escape_newline(self):
        """Test character constant with newline escape."""
        result = lex("'\\n'", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "CHAR_CONST")
        self.assertEqual(result[0]["value"], "'\\n'")

    def test_char_constant_escape_tab(self):
        """Test character constant with tab escape."""
        result = lex("'\\t'", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "CHAR_CONST")
        self.assertEqual(result[0]["value"], "'\\t'")

    def test_char_constant_escape_single_quote(self):
        """Test character constant with escaped single quote."""
        result = lex("'\\''", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "CHAR_CONST")
        self.assertEqual(result[0]["value"], "'\\''")

    def test_char_constant_escape_backslash(self):
        """Test character constant with escaped backslash."""
        result = lex("'\\\\'", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "CHAR_CONST")
        self.assertEqual(result[0]["value"], "'\\\\'")

    def test_operator_plus(self):
        """Test plus operator."""
        result = lex("+", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "OP_+")
        self.assertEqual(result[0]["value"], "+")

    def test_operator_minus(self):
        """Test minus operator."""
        result = lex("-", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "OP_-")
        self.assertEqual(result[0]["value"], "-")

    def test_operator_multiply(self):
        """Test multiply operator."""
        result = lex("*", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "OP_*")
        self.assertEqual(result[0]["value"], "*")

    def test_operator_divide(self):
        """Test divide operator."""
        result = lex("/", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "OP_/")
        self.assertEqual(result[0]["value"], "/")

    def test_operator_modulo(self):
        """Test modulo operator."""
        result = lex("%", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "OP_%")
        self.assertEqual(result[0]["value"], "%")

    def test_operator_eq_eq(self):
        """Test equality operator (maximal munch)."""
        result = lex("==", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "OP_==")
        self.assertEqual(result[0]["value"], "==")

    def test_operator_not_eq(self):
        """Test not equal operator."""
        result = lex("!=", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "OP_!=")
        self.assertEqual(result[0]["value"], "!=")

    def test_operator_less(self):
        """Test less than operator."""
        result = lex("<", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "OP_<")
        self.assertEqual(result[0]["value"], "<")

    def test_operator_greater(self):
        """Test greater than operator."""
        result = lex(">", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "OP_>")
        self.assertEqual(result[0]["value"], ">")

    def test_operator_less_eq(self):
        """Test less than or equal operator."""
        result = lex("<=", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "OP_<=")
        self.assertEqual(result[0]["value"], "<=")

    def test_operator_greater_eq(self):
        """Test greater than or equal operator."""
        result = lex(">=", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "OP_>=")
        self.assertEqual(result[0]["value"], ">=")

    def test_operator_and_and(self):
        """Test logical AND operator."""
        result = lex("&&", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "OP_&&")
        self.assertEqual(result[0]["value"], "&&")

    def test_operator_or_or(self):
        """Test logical OR operator."""
        result = lex("||", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "OP_||")
        self.assertEqual(result[0]["value"], "||")

    def test_punctuation_semicolon(self):
        """Test semicolon punctuation."""
        result = lex(";", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "SEP_;")
        self.assertEqual(result[0]["value"], ";")

    def test_punctuation_comma(self):
        """Test comma punctuation."""
        result = lex(",", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "SEP_,")
        self.assertEqual(result[0]["value"], ",")

    def test_punctuation_left_paren(self):
        """Test left parenthesis."""
        result = lex("(", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "SEP_(")
        self.assertEqual(result[0]["value"], "(")

    def test_punctuation_right_paren(self):
        """Test right parenthesis."""
        result = lex(")", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "SEP_)")
        self.assertEqual(result[0]["value"], ")")

    def test_punctuation_left_brace(self):
        """Test left brace."""
        result = lex("{", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "SEP_{")
        self.assertEqual(result[0]["value"], "{")

    def test_punctuation_right_brace(self):
        """Test right brace."""
        result = lex("}", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "SEP_}")
        self.assertEqual(result[0]["value"], "}")

    def test_comment_single_line(self):
        """Test single-line comment is skipped."""
        result = lex("// this is a comment\nx", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "IDENTIFIER")
        self.assertEqual(result[0]["value"], "x")
        self.assertEqual(result[0]["line"], 2)

    def test_whitespace_only(self):
        """Test whitespace-only source returns empty token list."""
        result = lex("   \t\n  ", "test.c")
        self.assertEqual(result, [])

    def test_multiple_tokens(self):
        """Test multiple tokens in sequence."""
        result = lex("int x = 5;", "test.c")
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0]["type"], "KEYWORD_int")
        self.assertEqual(result[0]["value"], "int")
        self.assertEqual(result[1]["type"], "IDENTIFIER")
        self.assertEqual(result[1]["value"], "x")
        self.assertEqual(result[2]["type"], "OP_=")
        self.assertEqual(result[2]["value"], "=")
        self.assertEqual(result[3]["type"], "INT_CONST")
        self.assertEqual(result[3]["value"], "5")

    def test_maximal_munch_plus_plus(self):
        """Test maximal munch: ++ should be one token, not two +."""
        result = lex("++", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "OP_++")
        self.assertEqual(result[0]["value"], "++")

    def test_maximal_munch_plus_then_plus(self):
        """Test two separate + operators with space."""
        result = lex("+ +", "test.c")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["type"], "OP_+")
        self.assertEqual(result[1]["type"], "OP_+")

    def test_complex_expression(self):
        """Test complex C expression."""
        result = lex("x = a + b * (c - d);", "test.c")
        self.assertEqual(len(result), 11)
        # Verify token sequence
        self.assertEqual(result[0]["value"], "x")
        self.assertEqual(result[1]["value"], "=")
        self.assertEqual(result[2]["value"], "a")
        self.assertEqual(result[3]["value"], "+")
        self.assertEqual(result[4]["value"], "b")
        self.assertEqual(result[5]["value"], "*")
        self.assertEqual(result[6]["value"], "(")
        self.assertEqual(result[7]["value"], "c")
        self.assertEqual(result[8]["value"], "-")
        self.assertEqual(result[9]["value"], "d")
        self.assertEqual(result[10]["value"], ")")


class TestLexLineColumnTracking(unittest.TestCase):
    """Test line and column number tracking."""

    def test_column_after_identifier(self):
        """Test column tracking after identifier."""
        result = lex("abc", "test.c")
        self.assertEqual(result[0]["column"], 1)

    def test_line_number_newline(self):
        """Test line number increments on newline."""
        result = lex("x\ny", "test.c")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["line"], 1)
        self.assertEqual(result[0]["column"], 1)
        self.assertEqual(result[1]["line"], 2)
        self.assertEqual(result[1]["column"], 1)

    def test_column_after_newline(self):
        """Test column resets after newline."""
        result = lex("x\n  y", "test.c")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[1]["line"], 2)
        self.assertEqual(result[1]["column"], 3)  # After 2 spaces

    def test_multiple_lines(self):
        """Test token positions across multiple lines."""
        source = "int x;\nchar y;"
        result = lex(source, "test.c")
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0]["line"], 1)  # int
        self.assertEqual(result[1]["line"], 1)  # x
        self.assertEqual(result[2]["line"], 1)  # ;
        self.assertEqual(result[3]["line"], 2)  # char


class TestLexErrorHandling(unittest.TestCase):
    """Test error handling for invalid input."""

    def test_illegal_character(self):
        """Test exception on illegal character."""
        with self.assertRaises(Exception) as context:
            lex("@", "test.c")
        self.assertIn("test.c:1:1: error: unexpected character '@'", str(context.exception))

    def test_illegal_character_with_position(self):
        """Test exception includes correct position for illegal character."""
        with self.assertRaises(Exception) as context:
            lex("  @", "test.c")
        self.assertIn("test.c:1:3: error: unexpected character '@'", str(context.exception))

    def test_unterminated_char_constant(self):
        """Test exception on unterminated character constant."""
        with self.assertRaises(Exception) as context:
            lex("'a", "test.c")
        self.assertIn("error:", str(context.exception).lower())
        self.assertIn("test.c:1:1", str(context.exception))

    def test_unterminated_char_constant_empty(self):
        """Test exception on empty unterminated character constant."""
        with self.assertRaises(Exception) as context:
            lex("'", "test.c")
        self.assertIn("error:", str(context.exception).lower())

    def test_illegal_char_in_escape(self):
        """Test exception on invalid escape sequence."""
        with self.assertRaises(Exception) as context:
            lex("'\\x'", "test.c")
        self.assertIn("error:", str(context.exception).lower())

    def test_illegal_character_after_valid_tokens(self):
        """Test exception position after valid tokens."""
        with self.assertRaises(Exception) as context:
            lex("int x = 1 @", "test.c")
        self.assertIn("test.c:1:11: error: unexpected character '@'", str(context.exception))

    def test_dollar_sign_illegal(self):
        """Test dollar sign is illegal character."""
        with self.assertRaises(Exception) as context:
            lex("$", "test.c")
        self.assertIn("error: unexpected character '$'", str(context.exception))

    def test_question_mark_illegal(self):
        """Test question mark is illegal character."""
        with self.assertRaises(Exception) as context:
            lex("?", "test.c")
        self.assertIn("error: unexpected character '?'", str(context.exception))

    def test_caret_illegal(self):
        """Test caret is illegal character."""
        with self.assertRaises(Exception) as context:
            lex("^", "test.c")
        self.assertIn("error: unexpected character '^'", str(context.exception))

    def test_tilde_illegal(self):
        """Test tilde is illegal character."""
        with self.assertRaises(Exception) as context:
            lex("~", "test.c")
        self.assertIn("error: unexpected character '~'", str(context.exception))

    def test_quote_illegal(self):
        """Test double quote is illegal character (strings not supported)."""
        with self.assertRaises(Exception) as context:
            lex('"', "test.c")
        self.assertIn("error: unexpected character '\"'", str(context.exception))

    def test_backtick_illegal(self):
        """Test backtick is illegal character."""
        with self.assertRaises(Exception) as context:
            lex("`", "test.c")
        self.assertIn("error: unexpected character '`'", str(context.exception))


class TestLexBoundaryCases(unittest.TestCase):
    """Test boundary and edge cases."""

    def test_underscore_identifier(self):
        """Test identifier starting with underscore."""
        result = lex("_var", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "IDENTIFIER")
        self.assertEqual(result[0]["value"], "_var")

    def test_underscore_only_identifier(self):
        """Test identifier that is just underscore."""
        result = lex("_", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "IDENTIFIER")
        self.assertEqual(result[0]["value"], "_")

    def test_identifier_with_digits(self):
        """Test identifier containing digits."""
        result = lex("var123", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "IDENTIFIER")
        self.assertEqual(result[0]["value"], "var123")

    def test_zero_constant(self):
        """Test zero as integer constant."""
        result = lex("0", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "INT_CONST")
        self.assertEqual(result[0]["value"], "0")

    def test_large_number(self):
        """Test large integer constant."""
        result = lex("123456789", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "INT_CONST")
        self.assertEqual(result[0]["value"], "123456789")

    def test_single_char_source(self):
        """Test single character source."""
        result = lex("a", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "IDENTIFIER")

    def test_all_keyword_types(self):
        """Test all keyword types are recognized."""
        keywords = ["int", "char", "if", "else", "while", "for", "return", "break", "continue"]
        for kw in keywords:
            result = lex(kw, "test.c")
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["type"], f"KEYWORD_{kw}")

    def test_mixed_operators(self):
        """Test mixed single and multi-character operators."""
        result = lex("a+b*c-d/e%f", "test.c")
        self.assertEqual(len(result), 11)

    def test_nested_braces(self):
        """Test nested braces."""
        result = lex("{{}}", "test.c")
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0]["type"], "SEP_{")
        self.assertEqual(result[1]["type"], "SEP_{")
        self.assertEqual(result[2]["type"], "SEP_}")
        self.assertEqual(result[3]["type"], "SEP_}")

    def test_comment_at_end_of_file(self):
        """Test comment at end of file with no newline."""
        result = lex("x // comment", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "IDENTIFIER")
        self.assertEqual(result[0]["value"], "x")

    def test_multiple_comments(self):
        """Test multiple comments."""
        result = lex("// first\nx // second\ny", "test.c")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["value"], "x")
        self.assertEqual(result[0]["line"], 2)
        self.assertEqual(result[1]["value"], "y")
        self.assertEqual(result[1]["line"], 3)

    def test_tab_whitespace(self):
        """Test tab character as whitespace."""
        result = lex("\tx", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["column"], 2)  # After tab

    def test_mixed_whitespace(self):
        """Test mixed spaces and tabs."""
        result = lex("  \t  x", "test.c")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["column"], 6)  # After 2 spaces, 1 tab, 2 spaces


class TestLexMaximalMunch(unittest.TestCase):
    """Test maximal munch rule for operators."""

    def test_assign_vs_eq(self):
        """Test = vs == distinction."""
        result1 = lex("=", "test.c")
        self.assertEqual(result1[0]["type"], "OP_=")
        
        result2 = lex("==", "test.c")
        self.assertEqual(result2[0]["type"], "OP_==")

    def test_less_vs_less_eq(self):
        """Test < vs <= distinction."""
        result1 = lex("<", "test.c")
        self.assertEqual(result1[0]["type"], "OP_<")
        
        result2 = lex("<=", "test.c")
        self.assertEqual(result2[0]["type"], "OP_<=")

    def test_greater_vs_greater_eq(self):
        """Test > vs >= distinction."""
        result1 = lex(">", "test.c")
        self.assertEqual(result1[0]["type"], "OP_>")
        
        result2 = lex(">=", "test.c")
        self.assertEqual(result2[0]["type"], "OP_>=")

    def test_not_vs_not_eq(self):
        """Test ! vs != distinction."""
        result1 = lex("!", "test.c")
        self.assertEqual(result1[0]["type"], "OP_!")
        
        result2 = lex("!=", "test.c")
        self.assertEqual(result2[0]["type"], "OP_!=")

    def test_plus_vs_plus_plus(self):
        """Test + vs ++ distinction."""
        result1 = lex("+", "test.c")
        self.assertEqual(result1[0]["type"], "OP_+")
        
        result2 = lex("++", "test.c")
        self.assertEqual(result2[0]["type"], "OP_++")

    def test_minus_vs_minus_minus(self):
        """Test - vs -- distinction."""
        result1 = lex("-", "test.c")
        self.assertEqual(result1[0]["type"], "OP_-")
        
        result2 = lex("--", "test.c")
        self.assertEqual(result2[0]["type"], "OP_--")

    def test_and_vs_and_and(self):
        """Test & vs && distinction."""
        result1 = lex("&", "test.c")
        self.assertEqual(result1[0]["type"], "OP_&")
        
        result2 = lex("&&", "test.c")
        self.assertEqual(result2[0]["type"], "OP_&&")

    def test_or_vs_or_or(self):
        """Test | vs || distinction."""
        result1 = lex("|", "test.c")
        self.assertEqual(result1[0]["type"], "OP_|")
        
        result2 = lex("||", "test.c")
        self.assertEqual(result2[0]["type"], "OP_||")


class TestLexIntegration(unittest.TestCase):
    """Integration tests with realistic C code snippets."""

    def test_simple_function_declaration(self):
        """Test simple function declaration."""
        source = "int main()"
        result = lex(source, "test.c")
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0]["value"], "int")
        self.assertEqual(result[1]["value"], "main")
        self.assertEqual(result[2]["value"], "(")
        self.assertEqual(result[3]["value"], ")")

    def test_variable_declaration(self):
        """Test variable declaration."""
        source = "int x = 10;"
        result = lex(source, "test.c")
        self.assertEqual(len(result), 5)
        values = [t["value"] for t in result]
        self.assertEqual(values, ["int", "x", "=", "10", ";"])

    def test_if_statement(self):
        """Test if statement."""
        source = "if (x > 0) { return x; }"
        result = lex(source, "test.c")
        values = [t["value"] for t in result]
        self.assertIn("if", values)
        self.assertIn(">", values)
        self.assertIn("return", values)

    def test_while_loop(self):
        """Test while loop."""
        source = "while (i < 10) { i = i + 1; }"
        result = lex(source, "test.c")
        values = [t["value"] for t in result]
        self.assertIn("while", values)
        self.assertIn("<", values)
        self.assertEqual(values.count("{"), 1)
        self.assertEqual(values.count("}"), 1)

    def test_for_loop(self):
        """Test for loop."""
        source = "for (i = 0; i < 10; i++) { }"
        result = lex(source, "test.c")
        values = [t["value"] for t in result]
        self.assertIn("for", values)
        self.assertIn("++", values)

    def test_char_declaration(self):
        """Test char variable with character constant."""
        source = "char c = 'a';"
        result = lex(source, "test.c")
        values = [t["value"] for t in result]
        self.assertEqual(values, ["char", "c", "=", "'a'", ";"])

    def test_complex_expression_with_all_operators(self):
        """Test expression with various operators."""
        source = "a == b && c != d || e <= f >= g"
        result = lex(source, "test.c")
        values = [t["value"] for t in result]
        self.assertIn("==", values)
        self.assertIn("&&", values)
        self.assertIn("!=", values)
        self.assertIn("||", values)
        self.assertIn("<=", values)
        self.assertIn(">=", values)

    def test_multiple_statements(self):
        """Test multiple statements."""
        source = """int x;
char y;
x = 1;
y = 'a';"""
        result = lex(source, "test.c")
        # Should have tokens from all 4 lines
        self.assertGreater(len(result), 10)
        lines = set(t["line"] for t in result)
        self.assertEqual(lines, {1, 2, 3, 4})


if __name__ == "__main__":
    unittest.main()
