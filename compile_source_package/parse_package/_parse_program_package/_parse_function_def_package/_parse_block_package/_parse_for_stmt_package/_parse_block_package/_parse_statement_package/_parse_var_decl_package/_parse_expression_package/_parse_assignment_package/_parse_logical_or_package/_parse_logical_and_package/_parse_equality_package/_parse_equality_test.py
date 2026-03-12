# === test file for _parse_equality ===
from unittest.mock import patch

# === import UUT ===
from ._parse_equality_src import _parse_equality

# === Define the module path for patching ===
# This is the absolute path to the UUT module
_UUT_MODULE = "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_var_decl_package._parse_expression_package._parse_assignment_package._parse_logical_or_package._parse_logical_and_package._parse_equality_package._parse_equality_src"


class TestParseEquality:
    """测试相等性表达式解析函数"""

    def test_single_relational_no_equality_op(self):
        """测试单个关系表达式，无相等性运算符"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        mock_relational_node = {
            "type": "IDENTIFIER",
            "children": [],
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_relational_package._parse_relational_src._parse_relational") as mock_parse_relational, \
             patch("._current_token_package._current_token_src._current_token") as mock_current_token:
            
            mock_parse_relational.return_value = mock_relational_node
            mock_current_token.return_value = None  # 无更多 token
            
            result = _parse_equality(parser_state)
            
            assert result == mock_relational_node
            mock_parse_relational.assert_called_once_with(parser_state)
            mock_current_token.assert_called_once_with(parser_state)

    def test_equality_with_eq_operator(self):
        """测试 == 运算符的相等性表达式"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "EQ", "value": "==", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 6}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        left_node = {
            "type": "IDENTIFIER",
            "children": [],
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        right_node = {
            "type": "IDENTIFIER",
            "children": [],
            "value": "y",
            "line": 1,
            "column": 6
        }
        
        with patch("._parse_relational_package._parse_relational_src._parse_relational") as mock_parse_relational, \
             patch("._current_token_package._current_token_src._current_token") as mock_current_token, \
             patch("._consume_package._consume_src._consume") as mock_consume:
            
            mock_parse_relational.side_effect = [left_node, right_node]
            mock_current_token.side_effect = [
                {"type": "EQ", "value": "==", "line": 1, "column": 3},
                None
            ]
            mock_consume.return_value = {"type": "EQ", "value": "==", "line": 1, "column": 3}
            
            result = _parse_equality(parser_state)
            
            assert result["type"] == "BINARY_OP"
            assert result["value"] == "=="
            assert result["line"] == 1
            assert result["column"] == 3
            assert len(result["children"]) == 2
            assert result["children"][0] == left_node
            assert result["children"][1] == right_node
            
            assert mock_parse_relational.call_count == 2
            assert mock_consume.call_count == 1
            mock_consume.assert_called_with(parser_state, "EQ")

    def test_equality_with_ne_operator(self):
        """测试 != 运算符的相等性表达式"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 2, "column": 1},
                {"type": "NE", "value": "!=", "line": 2, "column": 3},
                {"type": "LITERAL", "value": "5", "line": 2, "column": 6}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        left_node = {
            "type": "IDENTIFIER",
            "children": [],
            "value": "a",
            "line": 2,
            "column": 1
        }
        
        right_node = {
            "type": "LITERAL",
            "children": [],
            "value": "5",
            "line": 2,
            "column": 6
        }
        
        with patch("._parse_relational_package._parse_relational_src._parse_relational") as mock_parse_relational, \
             patch("._current_token_package._current_token_src._current_token") as mock_current_token, \
             patch("._consume_package._consume_src._consume") as mock_consume:
            
            mock_parse_relational.side_effect = [left_node, right_node]
            mock_current_token.side_effect = [
                {"type": "NE", "value": "!=", "line": 2, "column": 3},
                None
            ]
            mock_consume.return_value = {"type": "NE", "value": "!=", "line": 2, "column": 3}
            
            result = _parse_equality(parser_state)
            
            assert result["type"] == "BINARY_OP"
            assert result["value"] == "!="
            assert result["line"] == 2
            assert result["column"] == 3
            assert len(result["children"]) == 2
            assert result["children"][0] == left_node
            assert result["children"][1] == right_node

    def test_chained_equality_left_associative(self):
        """测试链式相等性表达式（左结合）"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "EQ", "value": "==", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 6},
                {"type": "EQ", "value": "==", "line": 1, "column": 8},
                {"type": "IDENTIFIER", "value": "z", "line": 1, "column": 11}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        node_x = {"type": "IDENTIFIER", "children": [], "value": "x", "line": 1, "column": 1}
        node_y = {"type": "IDENTIFIER", "children": [], "value": "y", "line": 1, "column": 6}
        node_z = {"type": "IDENTIFIER", "children": [], "value": "z", "line": 1, "column": 11}
        
        with patch("._parse_relational_package._parse_relational_src._parse_relational") as mock_parse_relational, \
             patch("._current_token_package._current_token_src._current_token") as mock_current_token, \
             patch("._consume_package._consume_src._consume") as mock_consume:
            
            mock_parse_relational.side_effect = [node_x, node_y, node_z]
            mock_current_token.side_effect = [
                {"type": "EQ", "value": "==", "line": 1, "column": 3},
                {"type": "EQ", "value": "==", "line": 1, "column": 8},
                None
            ]
            mock_consume.side_effect = [
                {"type": "EQ", "value": "==", "line": 1, "column": 3},
                {"type": "EQ", "value": "==", "line": 1, "column": 8}
            ]
            
            result = _parse_equality(parser_state)
            
            # 左结合：(x == y) == z
            assert result["type"] == "BINARY_OP"
            assert result["value"] == "=="
            assert result["line"] == 1
            assert result["column"] == 8
            
            # 左子节点应该是第一个 BINARY_OP (x == y)
            left_child = result["children"][0]
            assert left_child["type"] == "BINARY_OP"
            assert left_child["value"] == "=="
            assert left_child["line"] == 1
            assert left_child["column"] == 3
            assert left_child["children"][0] == node_x
            assert left_child["children"][1] == node_y
            
            # 右子节点应该是 z
            assert result["children"][1] == node_z
            
            assert mock_parse_relational.call_count == 3
            assert mock_consume.call_count == 2

    def test_mixed_eq_and_ne_operators(self):
        """测试混合 == 和 != 运算符"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "EQ", "value": "==", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6},
                {"type": "NE", "value": "!=", "line": 1, "column": 8},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 11}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        node_a = {"type": "IDENTIFIER", "children": [], "value": "a", "line": 1, "column": 1}
        node_b = {"type": "IDENTIFIER", "children": [], "value": "b", "line": 1, "column": 6}
        node_c = {"type": "IDENTIFIER", "children": [], "value": "c", "line": 1, "column": 11}
        
        with patch("._parse_relational_package._parse_relational_src._parse_relational") as mock_parse_relational, \
             patch("._current_token_package._current_token_src._current_token") as mock_current_token, \
             patch("._consume_package._consume_src._consume") as mock_consume:
            
            mock_parse_relational.side_effect = [node_a, node_b, node_c]
            mock_current_token.side_effect = [
                {"type": "EQ", "value": "==", "line": 1, "column": 3},
                {"type": "NE", "value": "!=", "line": 1, "column": 8},
                None
            ]
            mock_consume.side_effect = [
                {"type": "EQ", "value": "==", "line": 1, "column": 3},
                {"type": "NE", "value": "!=", "line": 1, "column": 8}
            ]
            
            result = _parse_equality(parser_state)
            
            # 左结合：(a == b) != c
            assert result["type"] == "BINARY_OP"
            assert result["value"] == "!="
            assert result["column"] == 8
            
            left_child = result["children"][0]
            assert left_child["type"] == "BINARY_OP"
            assert left_child["value"] == "=="
            assert left_child["children"][0] == node_a
            assert left_child["children"][1] == node_b
            
            assert result["children"][1] == node_c

    def test_non_equality_token_stops_parsing(self):
        """测试非相等性运算符停止解析"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        left_node = {"type": "IDENTIFIER", "children": [], "value": "x", "line": 1, "column": 1}
        
        with patch("._parse_relational_package._parse_relational_src._parse_relational") as mock_parse_relational, \
             patch("._current_token_package._current_token_src._current_token") as mock_current_token:
            
            mock_parse_relational.return_value = left_node
            mock_current_token.return_value = {"type": "PLUS", "value": "+", "line": 1, "column": 3}
            
            result = _parse_equality(parser_state)
            
            # 应该只返回左侧节点，不构建 BINARY_OP
            assert result == left_node
            mock_parse_relational.assert_called_once()
            mock_current_token.assert_called_once()

    def test_empty_tokens_list(self):
        """测试空 token 列表"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        empty_node = {"type": "IDENTIFIER", "children": [], "value": "", "line": 0, "column": 0}
        
        with patch("._parse_relational_package._parse_relational_src._parse_relational") as mock_parse_relational, \
             patch("._current_token_package._current_token_src._current_token") as mock_current_token:
            
            mock_parse_relational.return_value = empty_node
            mock_current_token.return_value = None
            
            result = _parse_equality(parser_state)
            
            assert result == empty_node
            mock_parse_relational.assert_called_once()

    def test_pos_at_end_of_tokens(self):
        """测试 pos 已在 token 列表末尾"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 1,  # 已在末尾
            "filename": "test.py",
            "error": None
        }
        
        left_node = {"type": "IDENTIFIER", "children": [], "value": "x", "line": 1, "column": 1}
        
        with patch("._parse_relational_package._parse_relational_src._parse_relational") as mock_parse_relational, \
             patch("._current_token_package._current_token_src._current_token") as mock_current_token:
            
            mock_parse_relational.return_value = left_node
            mock_current_token.return_value = None
            
            result = _parse_equality(parser_state)
            
            assert result == left_node
