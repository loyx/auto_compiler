# === std / third-party imports ===
from typing import Any, Dict, List

# === sub function imports ===
# Deferred imports to allow mocking in tests without triggering dependency chain
# from ._parse_program_package._parse_program_src import _parse_program
# from ._init_parser_state_package._init_parser_state_src import _init_parser_state

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
#   "type": str,             # 节点类型 (PROGRAM, FUNCTION_DEF, PARAM, VAR_DECL, IF_STMT, WHILE_STMT, FOR_STMT, RETURN_STMT, BREAK_STMT, CONTINUE_STMT, EXPR_STMT, BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, BLOCK)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值（如变量名、字面量值）
#   "line": int,             # 行号（用于错误报告）
#   "column": int            # 列号（用于错误报告）
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
def parse(tokens: List[Token], filename: str) -> AST:
    """
    语法分析器：将 token 流构建为抽象语法树 (AST)。
    
    支持函数定义、变量声明、表达式、控制结构（if/else/while/for/return/break/continue）。
    遇到语法错误时抛出带行列号的异常。
    """
    # Deferred imports to allow mocking in tests
    from ._parse_program_package._parse_program_src import _parse_program
    from ._init_parser_state_package._init_parser_state_src import _init_parser_state
    
    parser_state = _init_parser_state(tokens, filename)
    ast = _parse_program(parser_state)
    return ast

# === helper functions ===
# No helper functions in this file

# === OOP compatibility layer ===
# Not required for this function node (parser utility)