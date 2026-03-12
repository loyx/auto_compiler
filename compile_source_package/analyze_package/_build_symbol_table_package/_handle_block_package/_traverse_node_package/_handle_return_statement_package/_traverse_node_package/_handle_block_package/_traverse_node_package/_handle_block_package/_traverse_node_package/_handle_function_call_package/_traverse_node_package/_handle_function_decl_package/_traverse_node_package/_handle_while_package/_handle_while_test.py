# === std / third-party imports ===
import unittest
from typing import Any, Dict
from unittest.mock import patch, MagicMock

# === ADT defines ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


# === Test Class ===
class TestHandleWhile(unittest.TestCase):
    """测试 _handle_while 函数处理 while 循环语句节点。"""
    
    def _create_symbol_table(self) -> SymbolTable:
        """创建空的符号表。"""
        return {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "current_function": None,
            "errors": []
        }
    
    def _create_while_node(
        self,
        line: int = 10,
        column: int = 5,
        condition: AST = None,
        body: AST = None
    ) -> AST:
        """创建 while 节点。"""
        node = {
            "type": "while",
            "line": line,
            "column": column
        }
        if condition is not None:
            node["condition"] = condition
        if body is not None:
            node["body"] = body
        return node
    
    def _create_mock_node(self, node_type: str = "mock") -> AST:
        """创建模拟 AST 节点。"""
        return {
            "type": node_type,
            "line": 1,
            "column": 1
        }

    @patch(".._traverse_node_src._traverse_node")
    def test_handle_while_happy_path(self, mock_traverse_node: MagicMock) -> None:
        """测试正常 while 节点，包含 condition 和 body。"""
        from ._handle_while_src import _handle_while
        
        condition_node = self._create_mock_node("binary_op")
        body_node = self._create_mock_node("block")
        while_node = self._create_while_node(
            line=10,
            column=5,
            condition=condition_node,
            body=body_node
        )
        symbol_table = self._create_symbol_table()
        
        _handle_while(while_node, symbol_table)
        
        # 验证 _traverse_node 被调用两次（condition 和 body 各一次）
        self.assertEqual(mock_traverse_node.call_count, 2)
        
        # 验证调用参数
        calls = mock_traverse_node.call_args_list
        self.assertEqual(calls[0][0][0], condition_node)
        self.assertEqual(calls[0][0][1], symbol_table)
        self.assertEqual(calls[1][0][0], body_node)
        self.assertEqual(calls[1][0][1], symbol_table)
        
        # 验证没有记录错误
        self.assertEqual(len(symbol_table["errors"]), 0)

    @patch(".._traverse_node_src._traverse_node")
    def test_handle_while_missing_condition(self, mock_traverse_node: MagicMock) -> None:
        """测试 while 节点缺少 condition 字段。"""
        from ._handle_while_src import _handle_while
        
        body_node = self._create_mock_node("block")
        while_node = self._create_while_node(
            line=15,
            column=8,
            condition=None,
            body=body_node
        )
        symbol_table = self._create_symbol_table()
        
        _handle_while(while_node, symbol_table)
        
        # 验证 _traverse_node 只被调用一次（只处理 body）
        self.assertEqual(mock_traverse_node.call_count, 1)
        self.assertEqual(mock_traverse_node.call_args[0][0], body_node)
        
        # 验证记录了错误
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["error_type"], "missing_condition")
        self.assertEqual(error["message"], "while 语句缺少条件表达式")
        self.assertEqual(error["line"], 15)
        self.assertEqual(error["column"], 8)

    @patch(".._traverse_node_src._traverse_node")
    def test_handle_while_missing_body(self, mock_traverse_node: MagicMock) -> None:
        """测试 while 节点缺少 body 字段。"""
        from ._handle_while_src import _handle_while
        
        condition_node = self._create_mock_node("binary_op")
        while_node = self._create_while_node(
            line=20,
            column=3,
            condition=condition_node,
            body=None
        )
        symbol_table = self._create_symbol_table()
        
        _handle_while(while_node, symbol_table)
        
        # 验证 _traverse_node 只被调用一次（只处理 condition）
        self.assertEqual(mock_traverse_node.call_count, 1)
        self.assertEqual(mock_traverse_node.call_args[0][0], condition_node)
        
        # 验证记录了错误
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["error_type"], "missing_body")
        self.assertEqual(error["message"], "while 语句缺少循环体")
        self.assertEqual(error["line"], 20)
        self.assertEqual(error["column"], 3)

    @patch(".._traverse_node_src._traverse_node")
    def test_handle_while_both_missing(self, mock_traverse_node: MagicMock) -> None:
        """测试 while 节点 condition 和 body 都缺失。"""
        from ._handle_while_src import _handle_while
        
        while_node = self._create_while_node(
            line=25,
            column=10,
            condition=None,
            body=None
        )
        symbol_table = self._create_symbol_table()
        
        _handle_while(while_node, symbol_table)
        
        # 验证 _traverse_node 没有被调用
        self.assertEqual(mock_traverse_node.call_count, 0)
        
        # 验证记录了两条错误
        self.assertEqual(len(symbol_table["errors"]), 2)
        
        # 验证第一条错误（missing_condition）
        error1 = symbol_table["errors"][0]
        self.assertEqual(error1["error_type"], "missing_condition")
        self.assertEqual(error1["message"], "while 语句缺少条件表达式")
        self.assertEqual(error1["line"], 25)
        self.assertEqual(error1["column"], 10)
        
        # 验证第二条错误（missing_body）
        error2 = symbol_table["errors"][1]
        self.assertEqual(error2["error_type"], "missing_body")
        self.assertEqual(error2["message"], "while 语句缺少循环体")
        self.assertEqual(error2["line"], 25)
        self.assertEqual(error2["column"], 10)

    @patch(".._traverse_node_src._traverse_node")
    def test_handle_while_missing_field_in_node(self, mock_traverse_node: MagicMock) -> None:
        """测试 while 节点完全缺失 condition/body 键（而非值为 None）。"""
        from ._handle_while_src import _handle_while
        
        # 创建不包含 condition 和 body 键的节点
        while_node = {
            "type": "while",
            "line": 30,
            "column": 7
        }
        symbol_table = self._create_symbol_table()
        
        _handle_while(while_node, symbol_table)
        
        # 验证 _traverse_node 没有被调用
        self.assertEqual(mock_traverse_node.call_count, 0)
        
        # 验证记录了两条错误
        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertEqual(symbol_table["errors"][0]["error_type"], "missing_condition")
        self.assertEqual(symbol_table["errors"][1]["error_type"], "missing_body")

    @patch(".._traverse_node_src._traverse_node")
    def test_handle_while_errors_list_initialized(self, mock_traverse_node: MagicMock) -> None:
        """测试当 symbol_table 没有 errors 字段时会自动初始化。"""
        from ._handle_while_src import _handle_while
        
        while_node = self._create_while_node(
            line=35,
            column=12,
            condition=None,
            body=None
        )
        # 创建没有 errors 字段的 symbol_table
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }
        
        _handle_while(while_node, symbol_table)
        
        # 验证 errors 字段被创建
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 2)

    @patch(".._traverse_node_src._traverse_node")
    def test_handle_while_preserves_existing_errors(self, mock_traverse_node: MagicMock) -> None:
        """测试处理 while 节点时保留已有的错误。"""
        from ._handle_while_src import _handle_while
        
        while_node = self._create_while_node(
            line=40,
            column=5,
            condition=None,
            body=None
        )
        symbol_table = self._create_symbol_table()
        # 添加已有错误
        symbol_table["errors"].append({
            "error_type": "previous_error",
            "message": "之前的错误",
            "line": 1,
            "column": 1
        })
        
        _handle_while(while_node, symbol_table)
        
        # 验证保留了原有错误并添加了新错误
        self.assertEqual(len(symbol_table["errors"]), 3)
        self.assertEqual(symbol_table["errors"][0]["error_type"], "previous_error")
        self.assertEqual(symbol_table["errors"][1]["error_type"], "missing_condition")
        self.assertEqual(symbol_table["errors"][2]["error_type"], "missing_body")


# === Main ===
if __name__ == "__main__":
    unittest.main()
