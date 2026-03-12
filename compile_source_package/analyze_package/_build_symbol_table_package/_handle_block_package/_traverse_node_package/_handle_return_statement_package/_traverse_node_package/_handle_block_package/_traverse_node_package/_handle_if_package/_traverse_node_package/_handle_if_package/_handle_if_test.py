# === imports ===
from typing import Dict, Any
from unittest.mock import patch

# === relative import for tested module ===
from ._handle_if_src import _handle_if

# === ADT defines ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]

# === test helpers ===
def create_ast_node(
    node_type: str,
    children: list = None,
    value: Any = None,
    data_type: str = None,
    line: int = 0,
    column: int = 0
) -> AST:
    """创建 AST 节点辅助函数"""
    node = {
        "type": node_type,
        "children": children if children is not None else [],
        "line": line,
        "column": column
    }
    if value is not None:
        node["value"] = value
    if data_type is not None:
        node["data_type"] = data_type
    return node


def create_symbol_table(
    current_scope: int = 0,
    scope_stack: list = None,
    errors: list = None,
    variables: Dict = None,
    functions: Dict = None,
    current_function: str = None
) -> SymbolTable:
    """创建符号表辅助函数"""
    table = {
        "current_scope": current_scope,
        "scope_stack": scope_stack if scope_stack is not None else [],
        "errors": errors if errors is not None else [],
        "variables": variables if variables is not None else {},
        "functions": functions if functions is not None else {}
    }
    if current_function is not None:
        table["current_function"] = current_function
    return table


# === test cases ===
@patch("._handle_if_src._traverse_node")
def test_handle_if_happy_path_no_else(mock_traverse_node):
    """测试正常 if 语句（无 else 分支）"""
    # 准备：条件表达式为 int 类型
    condition = create_ast_node("expression", data_type="int", line=10, column=5)
    then_branch = create_ast_node("block", line=11, column=5)
    
    if_node = create_ast_node("if", children=[condition, then_branch], line=10, column=0)
    symbol_table = create_symbol_table(current_scope=0)
    
    # 执行
    _handle_if(if_node, symbol_table)
    
    # 验证：无错误记录
    assert len(symbol_table["errors"]) == 0, "不应记录错误"
    
    # 验证：作用域正确变化（进入+1，退出恢复）
    assert symbol_table["current_scope"] == 0, "作用域应恢复到 0"
    assert len(symbol_table["scope_stack"]) == 0, "作用域栈应为空"
    
    # 验证：_traverse_node 被调用一次（处理 then 分支）
    mock_traverse_node.assert_called_once_with(then_branch, symbol_table)


@patch("._handle_if_src._traverse_node")
def test_handle_if_happy_path_with_else(mock_traverse_node):
    """测试正常 if 语句（有 else 分支）"""
    # 准备：条件表达式为 int 类型
    condition = create_ast_node("expression", data_type="int", line=10, column=5)
    then_branch = create_ast_node("block", line=11, column=5)
    else_branch = create_ast_node("block", line=15, column=5)
    
    if_node = create_ast_node("if", children=[condition, then_branch, else_branch], line=10, column=0)
    symbol_table = create_symbol_table(current_scope=0)
    
    # 执行
    _handle_if(if_node, symbol_table)
    
    # 验证：无错误记录
    assert len(symbol_table["errors"]) == 0, "不应记录错误"
    
    # 验证：作用域正确变化（最终恢复到 0）
    assert symbol_table["current_scope"] == 0, "作用域应恢复到 0"
    assert len(symbol_table["scope_stack"]) == 0, "作用域栈应为空"
    
    # 验证：_traverse_node 被调用两次（then 和 else 分支）
    assert mock_traverse_node.call_count == 2, "应调用 _traverse_node 两次"
    
    # 验证调用顺序：先 then 后 else
    calls = mock_traverse_node.call_args_list
    assert calls[0][0][0] == then_branch, "第一次应处理 then 分支"
    assert calls[1][0][0] == else_branch, "第二次应处理 else 分支"


@patch("._handle_if_src._traverse_node")
def test_handle_if_type_error_condition_not_int(mock_traverse_node):
    """测试条件表达式类型错误（非 int 类型）"""
    # 准备：条件表达式为 char 类型（错误）
    condition = create_ast_node("expression", data_type="char", line=10, column=5)
    then_branch = create_ast_node("block", line=11, column=5)
    
    if_node = create_ast_node("if", children=[condition, then_branch], line=10, column=0)
    symbol_table = create_symbol_table(current_scope=0)
    
    # 执行
    _handle_if(if_node, symbol_table)
    
    # 验证：记录类型错误
    assert len(symbol_table["errors"]) == 1, "应记录一个错误"
    error = symbol_table["errors"][0]
    assert error["type"] == "type_error", "错误类型应为 type_error"
    assert "int" in error["message"], "错误消息应提及 int 类型"
    assert error["line"] == 10, "错误行号应为 10"
    assert error["column"] == 5, "错误列号应为 5"
    
    # 验证：即使有错误，仍然处理 then 分支
    mock_traverse_node.assert_called_once_with(then_branch, symbol_table)
    
    # 验证：作用域正确恢复
    assert symbol_table["current_scope"] == 0, "作用域应恢复到 0"


@patch("._handle_if_src._traverse_node")
def test_handle_if_nested_scope_management(mock_traverse_node):
    """测试嵌套作用域管理（初始作用域不为 0）"""
    # 准备：初始作用域为 2
    condition = create_ast_node("expression", data_type="int", line=10, column=5)
    then_branch = create_ast_node("block", line=11, column=5)
    else_branch = create_ast_node("block", line=15, column=5)
    
    if_node = create_ast_node("if", children=[condition, then_branch, else_branch], line=10, column=0)
    symbol_table = create_symbol_table(current_scope=2, scope_stack=[0, 1])
    
    # 执行
    _handle_if(if_node, symbol_table)
    
    # 验证：作用域正确恢复（回到 2）
    assert symbol_table["current_scope"] == 2, "作用域应恢复到 2"
    assert symbol_table["scope_stack"] == [0, 1], "作用域栈应恢复原状"
    
    # 验证：_traverse_node 被调用两次
    assert mock_traverse_node.call_count == 2


@patch("._handle_if_src._traverse_node")
def test_handle_if_preserves_existing_errors(mock_traverse_node):
    """测试保留已有错误记录"""
    # 准备：符号表中已有错误
    condition = create_ast_node("expression", data_type="int", line=10, column=5)
    then_branch = create_ast_node("block", line=11, column=5)
    
    if_node = create_ast_node("if", children=[condition, then_branch], line=10, column=0)
    existing_error = {"type": "syntax_error", "message": "已有错误", "line": 1, "column": 1}
    symbol_table = create_symbol_table(current_scope=0, errors=[existing_error])
    
    # 执行
    _handle_if(if_node, symbol_table)
    
    # 验证：已有错误保留，无新错误
    assert len(symbol_table["errors"]) == 1, "错误数量应保持为 1"
    assert symbol_table["errors"][0] == existing_error, "已有错误应保留"


@patch("._handle_if_src._traverse_node")
def test_handle_if_multiple_type_errors_accumulate(mock_traverse_node):
    """测试多个类型错误累积"""
    # 准备：条件表达式为 char 类型
    condition = create_ast_node("expression", data_type="char", line=10, column=5)
    then_branch = create_ast_node("block", line=11, column=5)
    
    if_node = create_ast_node("if", children=[condition, then_branch], line=10, column=0)
    existing_error = {"type": "syntax_error", "message": "已有错误", "line": 1, "column": 1}
    symbol_table = create_symbol_table(current_scope=0, errors=[existing_error])
    
    # 执行
    _handle_if(if_node, symbol_table)
    
    # 验证：错误累积
    assert len(symbol_table["errors"]) == 2, "错误数量应为 2"
    assert symbol_table["errors"][0] == existing_error, "已有错误应保留"
    assert symbol_table["errors"][1]["type"] == "type_error", "新错误应为 type_error"


@patch("._handle_if_src._traverse_node")
def test_handle_if_condition_missing_data_type(mock_traverse_node):
    """测试条件表达式缺少 data_type 字段"""
    # 准备：条件表达式无 data_type
    condition = create_ast_node("expression", line=10, column=5)  # 无 data_type
    then_branch = create_ast_node("block", line=11, column=5)
    
    if_node = create_ast_node("if", children=[condition, then_branch], line=10, column=0)
    symbol_table = create_symbol_table(current_scope=0)
    
    # 执行
    _handle_if(if_node, symbol_table)
    
    # 验证：记录类型错误（None != "int"）
    assert len(symbol_table["errors"]) == 1, "应记录一个错误"
    assert symbol_table["errors"][0]["type"] == "type_error"
    
    # 验证：仍然处理 then 分支
    mock_traverse_node.assert_called_once()


@patch("._handle_if_src._traverse_node")
def test_handle_if_scope_stack_operations(mock_traverse_node):
    """测试作用域栈操作细节"""
    condition = create_ast_node("expression", data_type="int", line=10, column=5)
    then_branch = create_ast_node("block", line=11, column=5)
    else_branch = create_ast_node("block", line=15, column=5)
    
    if_node = create_ast_node("if", children=[condition, then_branch, else_branch], line=10, column=0)
    symbol_table = create_symbol_table(current_scope=0)
    
    # 执行
    _handle_if(if_node, symbol_table)
    
    # 验证：栈操作正确（push 两次，pop 两次，最终为空）
    assert len(symbol_table["scope_stack"]) == 0, "作用域栈最终应为空"
    assert symbol_table["current_scope"] == 0, "当前作用域应恢复为 0"


# === test runner ===
if __name__ == "__main__":
    import sys
    
    test_functions = [
        test_handle_if_happy_path_no_else,
        test_handle_if_happy_path_with_else,
        test_handle_if_type_error_condition_not_int,
        test_handle_if_nested_scope_management,
        test_handle_if_preserves_existing_errors,
        test_handle_if_multiple_type_errors_accumulate,
        test_handle_if_condition_missing_data_type,
        test_handle_if_scope_stack_operations,
    ]
    
    passed = 0
    failed = 0
    
    for test_func in test_functions:
        try:
            test_func()
            print(f"✓ {test_func.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"✗ {test_func.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test_func.__name__}: {type(e).__name__}: {e}")
            failed += 1
    
    print(f"\n结果：{passed} 通过，{failed} 失败")
    sys.exit(0 if failed == 0 else 1)
