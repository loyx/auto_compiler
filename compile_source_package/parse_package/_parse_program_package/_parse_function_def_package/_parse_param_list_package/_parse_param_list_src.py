# === std / third-party imports ===
from typing import Any, Dict, List

# === sub function imports ===
# No sub functions - this is a leaf node in the function dependency tree

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型 (e.g., "TYPE", "IDENTIFIER", "COMMA", "RPAREN")
#   "value": str,            # token 值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型
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

ParamNode = Dict[str, Any]
# ParamNode possible fields:
# {
#   "type": "PARAM",
#   "value": str,            # 参数名
#   "param_type": str,       # 参数类型
#   "line": int,             # 行号
#   "column": int            # 列号
# }

# === main function ===
def _parse_param_list(parser_state: dict, pos: int) -> tuple:
    """
    解析参数列表。
    
    输入：parser_state, pos（当前位置指向第一个参数类型）
    输出：(params, new_pos) 元组
    - params: PARAM 节点列表
    - new_pos: 解析后的位置（指向参数列表后的下一个 token）
    """
    tokens: List[Token] = parser_state["tokens"]
    filename: str = parser_state["filename"]
    params: List[ParamNode] = []
    current_pos: int = pos
    
    while current_pos < len(tokens):
        token = tokens[current_pos]
        
        # 遇到右括号或结束，参数列表解析完成
        if token["type"] == "RPAREN":
            break
        
        # 解析参数类型
        if token["type"] != "TYPE":
            # 不是类型也不是右括号，可能是空参数列表或其他情况
            break
        
        type_token = token
        current_pos += 1
        
        # 检查是否有标识符
        if current_pos >= len(tokens):
            raise SyntaxError(
                f"Syntax error at {filename}:{type_token['line']}:{type_token['column']} - "
                f"Expected identifier after type '{type_token['value']}'"
            )
        
        ident_token = tokens[current_pos]
        if ident_token["type"] != "IDENTIFIER":
            raise SyntaxError(
                f"Syntax error at {filename}:{type_token['line']}:{type_token['column']} - "
                f"Expected identifier after type '{type_token['value']}', got '{ident_token['value']}'"
            )
        
        # 创建 PARAM 节点
        param_node: ParamNode = {
            "type": "PARAM",
            "value": ident_token["value"],
            "param_type": type_token["value"],
            "line": type_token["line"],
            "column": type_token["column"]
        }
        params.append(param_node)
        current_pos += 1
        
        # 检查是否有逗号分隔符
        if current_pos < len(tokens):
            next_token = tokens[current_pos]
            if next_token["type"] == "COMMA":
                # 有逗号，继续解析下一个参数
                current_pos += 1
            elif next_token["type"] == "RPAREN":
                # 右括号，参数列表结束
                break
            else:
                # 既不是逗号也不是右括号，参数列表结束
                break
    
    return (params, current_pos)

# === helper functions ===
# No helper functions needed - logic is contained in main function

# === OOP compatibility layer ===
# Not needed - this is a parser helper function, not a framework entry point
