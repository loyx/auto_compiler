# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_function_def_package._parse_function_def_src import _parse_function_def
from ._is_at_end_package._is_at_end_src import _is_at_end

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型
#   "value": str,            # token 值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (PROGRAM, FUNCTION_DEF, etc.)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,          # token 列表
#   "pos": int,              # 当前位置
#   "filename": str,         # 源文件名
#   "error": str             # 错误信息（可选）
# }


# === main function ===
def _parse_program(parser_state: dict) -> dict:
    """解析整个程序：零个或多个函数定义。"""
    function_defs = []
    
    # 循环解析函数定义，直到 token 流结束
    while not _is_at_end(parser_state):
        func_def = _parse_function_def(parser_state)
        function_defs.append(func_def)
    
    # 返回 PROGRAM 根节点
    return {
        "type": "PROGRAM",
        "children": function_defs,
        "value": None,
        "line": 0,
        "column": 0
    }


# === helper functions ===


# === OOP compatibility layer ===
