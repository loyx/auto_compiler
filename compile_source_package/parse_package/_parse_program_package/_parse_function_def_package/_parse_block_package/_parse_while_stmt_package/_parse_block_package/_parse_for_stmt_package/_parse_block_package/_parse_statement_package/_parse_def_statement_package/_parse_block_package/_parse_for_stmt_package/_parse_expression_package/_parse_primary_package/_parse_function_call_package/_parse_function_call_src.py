# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,
#   "value": str,
#   "line": int,
#   "column": int
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "children": list,
#   "value": Any,
#   "line": int,
#   "column": int
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# === main function ===
def _parse_function_call(parser_state: ParserState, func_name: str, start_line: int, start_column: int) -> AST:
    """
    解析函数调用的参数列表并构建 function_call AST 节点。
    
    输入：parser_state（pos 已指向 '(' 之后的第一个 token）、func_name、start_line/column
    输出：function_call AST 节点
    副作用：消费参数列表和 ')'，更新 parser_state['pos']
    """
    args = []
    tokens = parser_state["tokens"]
    
    # 检查是否为空参数列表
    if tokens[parser_state["pos"]]["type"] == "RPAREN":
        parser_state["pos"] += 1
    else:
        # 解析第一个参数
        arg_ast = _parse_expression(parser_state)
        args.append(arg_ast)
        
        # 循环解析后续参数（以逗号分隔）
        while tokens[parser_state["pos"]]["type"] == "COMMA":
            parser_state["pos"] += 1  # 消费逗号
            arg_ast = _parse_expression(parser_state)
            args.append(arg_ast)
        
        # 检查并消费 RPAREN
        if tokens[parser_state["pos"]]["type"] != "RPAREN":
            current_token = tokens[parser_state["pos"]]
            error_msg = (
                f"SyntaxError: Missing ')' in function call at "
                f"{parser_state['filename']}:{current_token['line']}:{current_token['column']}"
            )
            raise SyntaxError(error_msg)
        
        parser_state["pos"] += 1  # 消费 ')'
    
    # 构建 function_call AST 节点
    return {
        "type": "function_call",
        "value": func_name,
        "children": args,
        "line": start_line,
        "column": start_column
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this parser function