# === imports ===
import unittest
from unittest.mock import patch
from typing import Dict, Any

# === relative import of target function ===
from ._parse_and_src import _parse_and

# === test helper types ===
ParserState = Dict[str, Any]
AST = Dict[str, Any]
Token = Dict[str, Any]

# === test class ===
class TestParseAnd(unittest.TestCase):
    """单元测试：_parse_and 函数解析逻辑与运算符（&&）表达式"""

    def _make_token(self, value: str, line: int = 1, column: int = 1, token_type: str = "operator") -> Token:
        """辅助函数：创建 token 字典"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _make_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.txt") -> ParserState:
        """辅助函数：创建 parser_state 字典"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def test_no_and_operator_single_expression(self):
        """测试：无 && 运算符，直接返回下层表达式"""
        mock_ast = {"type": "COMPARISON", "value": "a > b", "line": 1, "column": 1}
        
        tokens = [self._make_token("a", 1, 1, "identifier")]
        parser_state = self._make_parser_state(tokens, pos=0)
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_assignment_package._parse_conditional_package._parse_or_package._parse_and_package._parse_comparison_package._parse_comparison_src._parse_comparison") as mock_parse_comparison:
            mock_parse_comparison.return_value = mock_ast
            
            result = _parse_and(parser_state)
            
            # 验证返回 AST
            self.assertEqual(result, mock_ast)
            # 验证 pos 未改变（_parse_comparison 会更新）
            mock_parse_comparison.assert_called_once()

    def test_single_and_operator(self):
        """测试：单个 && 运算符，构建 AND 节点"""
        left_ast = {"type": "COMPARISON", "value": "a", "line": 1, "column": 1}
        right_ast = {"type": "COMPARISON", "value": "b", "line": 1, "column": 5}
        
        tokens = [
            self._make_token("a", 1, 1, "identifier"),
            self._make_token("&&", 1, 3, "operator"),
            self._make_token("b", 1, 6, "identifier")
        ]
        parser_state = self._make_parser_state(tokens, pos=0)
        
        call_count = [0]
        def side_effect(ps):
            result = [left_ast, right_ast][call_count[0]]
            call_count[0] += 1
            ps["pos"] += 1  # 模拟 _parse_comparison 更新 pos
            return result
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_assignment_package._parse_conditional_package._parse_or_package._parse_and_package._parse_comparison_package._parse_comparison_src._parse_comparison") as mock_parse_comparison:
            mock_parse_comparison.side_effect = side_effect
            
            result = _parse_and(parser_state)
            
            # 验证返回 AND 类型 AST
            self.assertEqual(result["type"], "AND")
            self.assertEqual(result["left"], left_ast)
            self.assertEqual(result["right"], right_ast)
            self.assertEqual(result["line"], 1)  # && token 的 line
            self.assertEqual(result["column"], 3)  # && token 的 column
            # 验证调用了两次 _parse_comparison
            self.assertEqual(mock_parse_comparison.call_count, 2)

    def test_multiple_and_operators_left_associative(self):
        """测试：多个 && 运算符，验证左结合性 (a && b) && c"""
        ast_a = {"type": "COMPARISON", "value": "a", "line": 1, "column": 1}
        ast_b = {"type": "COMPARISON", "value": "b", "line": 1, "column": 5}
        ast_c = {"type": "COMPARISON", "value": "c", "line": 1, "column": 9}
        
        tokens = [
            self._make_token("a", 1, 1, "identifier"),
            self._make_token("&&", 1, 3, "operator"),
            self._make_token("b", 1, 6, "operator"),
            self._make_token("&&", 1, 8, "operator"),
            self._make_token("c", 1, 11, "identifier")
        ]
        parser_state = self._make_parser_state(tokens, pos=0)
        
        call_count = [0]
        ast_results = [ast_a, ast_b, ast_c]
        
        def side_effect(ps):
            result = ast_results[call_count[0]]
            call_count[0] += 1
            ps["pos"] += 1
            return result
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_assignment_package._parse_conditional_package._parse_or_package._parse_and_package._parse_comparison_package._parse_comparison_src._parse_comparison") as mock_parse_comparison:
            mock_parse_comparison.side_effect = side_effect
            
            result = _parse_and(parser_state)
            
            # 验证外层 AND 节点
            self.assertEqual(result["type"], "AND")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 8)  # 第二个 && 的位置
            
            # 验证左子节点也是 AND（左结合）
            left_child = result["left"]
            self.assertEqual(left_child["type"], "AND")
            self.assertEqual(left_child["column"], 3)  # 第一个 && 的位置
            self.assertEqual(left_child["left"], ast_a)
            self.assertEqual(left_child["right"], ast_b)
            
            # 验证右子节点
            self.assertEqual(result["right"], ast_c)
            
            # 验证调用了三次 _parse_comparison
            self.assertEqual(mock_parse_comparison.call_count, 3)

    def test_pos_updated_correctly(self):
        """测试：parser_state['pos'] 正确更新到表达式结束位置"""
        ast_a = {"type": "COMPARISON", "value": "a", "line": 1, "column": 1}
        ast_b = {"type": "COMPARISON", "value": "b", "line": 1, "column": 5}
        
        tokens = [
            self._make_token("a", 1, 1, "identifier"),
            self._make_token("&&", 1, 3, "operator"),
            self._make_token("b", 1, 6, "identifier"),
            self._make_token(";", 1, 8, "punctuation")  # 后续 token
        ]
        parser_state = self._make_parser_state(tokens, pos=0)
        
        call_count = [0]
        ast_results = [ast_a, ast_b]
        
        def side_effect(ps):
            result = ast_results[call_count[0]]
            call_count[0] += 1
            ps["pos"] += 1
            return result
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_assignment_package._parse_conditional_package._parse_or_package._parse_and_package._parse_comparison_package._parse_comparison_src._parse_comparison") as mock_parse_comparison:
            mock_parse_comparison.side_effect = side_effect
            
            result = _parse_and(parser_state)
            
            # 验证 pos 更新到 && 和 b 之后（pos=3）
            self.assertEqual(parser_state["pos"], 3)

    def test_empty_tokens(self):
        """测试：空 tokens 列表，直接返回下层结果"""
        mock_ast = {"type": "COMPARISON", "value": "", "line": 1, "column": 1}
        
        parser_state = self._make_parser_state([], pos=0)
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_assignment_package._parse_conditional_package._parse_or_package._parse_and_package._parse_comparison_package._parse_comparison_src._parse_comparison") as mock_parse_comparison:
            mock_parse_comparison.return_value = mock_ast
            
            result = _parse_and(parser_state)
            
            self.assertEqual(result, mock_ast)
            mock_parse_comparison.assert_called_once()

    def test_pos_at_end_no_tokens(self):
        """测试：pos 已在 tokens 末尾，不进入循环"""
        mock_ast = {"type": "COMPARISON", "value": "x", "line": 1, "column": 1}
        
        tokens = [self._make_token("x", 1, 1, "identifier")]
        parser_state = self._make_parser_state(tokens, pos=1)  # pos 已在末尾
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_assignment_package._parse_conditional_package._parse_or_package._parse_and_package._parse_comparison_package._parse_comparison_src._parse_comparison") as mock_parse_comparison:
            mock_parse_comparison.return_value = mock_ast
            
            result = _parse_and(parser_state)
            
            self.assertEqual(result, mock_ast)
            mock_parse_comparison.assert_called_once()

    def test_and_token_line_column_preserved(self):
        """测试：&& token 的 line/column 正确保存到 AST 节点"""
        left_ast = {"type": "COMPARISON", "value": "a", "line": 2, "column": 5}
        right_ast = {"type": "COMPARISON", "value": "b", "line": 2, "column": 10}
        
        tokens = [
            self._make_token("a", 2, 5, "identifier"),
            self._make_token("&&", 2, 7, "operator"),  # line=2, column=7
            self._make_token("b", 2, 10, "identifier")
        ]
        parser_state = self._make_parser_state(tokens, pos=0)
        
        call_count = [0]
        ast_results = [left_ast, right_ast]
        
        def side_effect(ps):
            result = ast_results[call_count[0]]
            call_count[0] += 1
            ps["pos"] += 1
            return result
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_assignment_package._parse_conditional_package._parse_or_package._parse_and_package._parse_comparison_package._parse_comparison_src._parse_comparison") as mock_parse_comparison:
            mock_parse_comparison.side_effect = side_effect
            
            result = _parse_and(parser_state)
            
            self.assertEqual(result["line"], 2)
            self.assertEqual(result["column"], 7)

    def test_non_and_token_stops_loop(self):
        """测试：遇到非 && token 时停止循环"""
        ast_a = {"type": "COMPARISON", "value": "a", "line": 1, "column": 1}
        ast_b = {"type": "COMPARISON", "value": "b", "line": 1, "column": 5}
        
        tokens = [
            self._make_token("a", 1, 1, "identifier"),
            self._make_token("&&", 1, 3, "operator"),
            self._make_token("b", 1, 6, "identifier"),
            self._make_token("||", 1, 8, "operator"),  # 逻辑或，应停止
            self._make_token("c", 1, 11, "identifier")
        ]
        parser_state = self._make_parser_state(tokens, pos=0)
        
        call_count = [0]
        ast_results = [ast_a, ast_b]
        
        def side_effect(ps):
            result = ast_results[call_count[0]]
            call_count[0] += 1
            ps["pos"] += 1
            return result
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_assignment_package._parse_conditional_package._parse_or_package._parse_and_package._parse_comparison_package._parse_comparison_src._parse_comparison") as mock_parse_comparison:
            mock_parse_comparison.side_effect = side_effect
            
            result = _parse_and(parser_state)
            
            # 只解析了 a && b，遇到 || 停止
            self.assertEqual(result["type"], "AND")
            self.assertEqual(result["left"], ast_a)
            self.assertEqual(result["right"], ast_b)
            self.assertEqual(mock_parse_comparison.call_count, 2)


# === run tests ===
if __name__ == "__main__":
    unittest.main()
