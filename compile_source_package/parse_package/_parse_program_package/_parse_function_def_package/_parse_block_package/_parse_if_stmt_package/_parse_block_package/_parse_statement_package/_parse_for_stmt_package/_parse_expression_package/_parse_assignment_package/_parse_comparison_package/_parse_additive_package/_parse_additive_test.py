# === std / third-party imports ===
import unittest
from unittest.mock import patch

# === relative import of UUT ===
from ._parse_additive_src import _parse_additive


class TestParseAdditive(unittest.TestCase):
    """单元测试：_parse_additive 函数"""

    def test_no_additive_operator(self):
        """测试：没有 + 或 - 运算符，直接返回乘法表达式"""
        parser_state = {
            "tokens": [{"type": "NUMBER", "value": "5", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        mock_multiplicative_result = {"type": "multiplicative", "value": "5", "line": 1, "column": 1}
        
        with patch('._parse_multiplicative_package._parse_multiplicative_src._parse_multiplicative', return_value=mock_multiplicative_result) as mock_mult:
            with patch('._get_current_token_package._get_current_token_src._get_current_token') as mock_get_token:
                mock_get_token.return_value = None  # 没有更多 token
                
                result = _parse_additive(parser_state)
                
                self.assertEqual(result, mock_multiplicative_result)
                mock_get_token.assert_called_once()

    def test_single_addition(self):
        """测试：单个加法运算符 a + b"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "3", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        multiplicative_results = [
            {"type": "multiplicative", "value": "3", "line": 1, "column": 1},
            {"type": "multiplicative", "value": "5", "line": 1, "column": 5}
        ]
        call_count = [0]
        
        def mock_multiplicative_side_effect(ps):
            result = multiplicative_results[call_count[0]]
            call_count[0] += 1
            return result
        
        with patch('._parse_multiplicative_package._parse_multiplicative_src._parse_multiplicative', side_effect=mock_multiplicative_side_effect) as mock_mult:
            with patch('._get_current_token_package._get_current_token_src._get_current_token') as mock_get_token:
                with patch('._advance_package._advance_src._advance') as mock_advance:
                    mock_get_token.side_effect = [
                        {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                        None
                    ]
                    
                    result = _parse_additive(parser_state)
                    
                    self.assertEqual(result["type"], "additive")
                    self.assertEqual(result["value"], "+")
                    self.assertEqual(len(result["children"]), 2)
                    self.assertEqual(result["children"][0]["value"], "3")
                    self.assertEqual(result["children"][1]["value"], "5")
                    self.assertEqual(result["line"], 1)
                    self.assertEqual(result["column"], 3)
                    
                    self.assertEqual(mock_advance.call_count, 1)

    def test_single_subtraction(self):
        """测试：单个减法运算符 a - b"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "10", "line": 2, "column": 1},
                {"type": "MINUS", "value": "-", "line": 2, "column": 4},
                {"type": "NUMBER", "value": "4", "line": 2, "column": 6}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        multiplicative_results = [
            {"type": "multiplicative", "value": "10", "line": 2, "column": 1},
            {"type": "multiplicative", "value": "4", "line": 2, "column": 6}
        ]
        call_count = [0]
        
        def mock_multiplicative_side_effect(ps):
            result = multiplicative_results[call_count[0]]
            call_count[0] += 1
            return result
        
        with patch('._parse_multiplicative_package._parse_multiplicative_src._parse_multiplicative', side_effect=mock_multiplicative_side_effect) as mock_mult:
            with patch('._get_current_token_package._get_current_token_src._get_current_token') as mock_get_token:
                with patch('._advance_package._advance_src._advance') as mock_advance:
                    mock_get_token.side_effect = [
                        {"type": "MINUS", "value": "-", "line": 2, "column": 4},
                        None
                    ]
                    
                    result = _parse_additive(parser_state)
                    
                    self.assertEqual(result["type"], "additive")
                    self.assertEqual(result["value"], "-")
                    self.assertEqual(result["children"][0]["value"], "10")
                    self.assertEqual(result["children"][1]["value"], "4")

    def test_left_associative_multiple_operators(self):
        """测试：左结合性 a + b - c 应该解析为 (a + b) - c"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
                {"type": "MINUS", "value": "-", "line": 1, "column": 7},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 9}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        multiplicative_results = [
            {"type": "multiplicative", "value": "1", "line": 1, "column": 1},
            {"type": "multiplicative", "value": "2", "line": 1, "column": 5},
            {"type": "multiplicative", "value": "3", "line": 1, "column": 9}
        ]
        call_count = [0]
        
        def mock_multiplicative_side_effect(ps):
            result = multiplicative_results[call_count[0]]
            call_count[0] += 1
            return result
        
        with patch('._parse_multiplicative_package._parse_multiplicative_src._parse_multiplicative', side_effect=mock_multiplicative_side_effect) as mock_mult:
            with patch('._get_current_token_package._get_current_token_src._get_current_token') as mock_get_token:
                with patch('._advance_package._advance_src._advance') as mock_advance:
                    mock_get_token.side_effect = [
                        {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                        {"type": "MINUS", "value": "-", "line": 1, "column": 7},
                        None
                    ]
                    
                    result = _parse_additive(parser_state)
                    
                    # 验证左结合性：最外层应该是减法，左子节点是加法
                    self.assertEqual(result["type"], "additive")
                    self.assertEqual(result["value"], "-")
                    self.assertEqual(result["line"], 1)
                    self.assertEqual(result["column"], 7)
                    
                    # 左子节点应该是加法节点
                    left_child = result["children"][0]
                    self.assertEqual(left_child["type"], "additive")
                    self.assertEqual(left_child["value"], "+")
                    self.assertEqual(left_child["children"][0]["value"], "1")
                    self.assertEqual(left_child["children"][1]["value"], "2")
                    
                    # 右子节点应该是 3
                    right_child = result["children"][1]
                    self.assertEqual(right_child["value"], "3")
                    
                    # 验证 advance 被调用了 2 次
                    self.assertEqual(mock_advance.call_count, 2)

    def test_non_additive_token_stops_parsing(self):
        """测试：遇到非加法运算符时停止解析"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "5", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 5},
                {"type": "STAR", "value": "*", "line": 1, "column": 7},  # 乘法运算符，应该停止
                {"type": "NUMBER", "value": "2", "line": 1, "column": 9}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        multiplicative_results = [
            {"type": "multiplicative", "value": "5", "line": 1, "column": 1},
            {"type": "multiplicative", "value": "3", "line": 1, "column": 5}
        ]
        call_count = [0]
        
        def mock_multiplicative_side_effect(ps):
            result = multiplicative_results[call_count[0]]
            call_count[0] += 1
            return result
        
        with patch('._parse_multiplicative_package._parse_multiplicative_src._parse_multiplicative', side_effect=mock_multiplicative_side_effect) as mock_mult:
            with patch('._get_current_token_package._get_current_token_src._get_current_token') as mock_get_token:
                with patch('._advance_package._advance_src._advance') as mock_advance:
                    mock_get_token.side_effect = [
                        {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                        {"type": "STAR", "value": "*", "line": 1, "column": 7}  # 非加法运算符
                    ]
                    
                    result = _parse_additive(parser_state)
                    
                    # 只解析了 5 + 3，遇到 * 停止
                    self.assertEqual(result["type"], "additive")
                    self.assertEqual(result["value"], "+")
                    self.assertEqual(mock_advance.call_count, 1)

    def test_empty_token_list(self):
        """测试：空 token 列表"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        mock_multiplicative_result = {"type": "multiplicative", "value": None, "line": 0, "column": 0}
        
        with patch('._parse_multiplicative_package._parse_multiplicative_src._parse_multiplicative', return_value=mock_multiplicative_result) as mock_mult:
            with patch('._get_current_token_package._get_current_token_src._get_current_token') as mock_get_token:
                mock_get_token.return_value = None
                
                result = _parse_additive(parser_state)
                
                self.assertEqual(result, mock_multiplicative_result)
                mock_get_token.assert_called_once()

    def test_parser_state_pos_modified(self):
        """测试：parser_state['pos'] 被正确修改"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        multiplicative_results = [
            {"type": "multiplicative", "value": "1", "line": 1, "column": 1},
            {"type": "multiplicative", "value": "2", "line": 1, "column": 5}
        ]
        call_count = [0]
        
        def mock_multiplicative_side_effect(ps):
            result = multiplicative_results[call_count[0]]
            call_count[0] += 1
            return result
        
        def mock_advance_side_effect(ps):
            ps["pos"] += 1
        
        with patch('._parse_multiplicative_package._parse_multiplicative_src._parse_multiplicative', side_effect=mock_multiplicative_side_effect):
            with patch('._get_current_token_package._get_current_token_src._get_current_token') as mock_get_token:
                with patch('._advance_package._advance_src._advance', side_effect=mock_advance_side_effect) as mock_advance:
                    mock_get_token.side_effect = [
                        {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                        None
                    ]
                    
                    initial_pos = parser_state["pos"]
                    result = _parse_additive(parser_state)
                    final_pos = parser_state["pos"]
                    
                    # pos 应该增加了 1（消耗了 PLUS token）
                    self.assertEqual(final_pos, initial_pos + 1)


if __name__ == "__main__":
    unittest.main()
