# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No subfunctions needed for this parser

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
def _parse_param_list(parser_state: ParserState) -> list:
    """
    解析参数列表（LPAREN 之后，RPAREN 之前）。
    
    param_list 语法：
    param_list := IDENTIFIER (COMMA IDENTIFIER)*
    
    输入：parser_state（pos 指向第一个参数或 RPAREN）
    输出：参数 AST 节点列表
    副作用：消费参数相关 token，更新 pos 到 RPAREN 之前
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    params = []
    
    while pos < len(tokens):
        token = tokens[pos]
        
        # 遇到 RPAREN，参数列表结束
        if token["type"] == "RPAREN":
            break
        
        # 期待标识符
        if token["type"] == "IDENTIFIER":
            param_node = {
                "type": "PARAM",
                "value": token["value"],
                "line": token["line"],
                "column": token["column"]
            }
            params.append(param_node)
            pos += 1
            
            # 检查是否有逗号
            if pos < len(tokens):
                next_token = tokens[pos]
                if next_token["type"] == "COMMA":
                    pos += 1
                    # 逗号后必须跟标识符
                    if pos >= len(tokens) or tokens[pos]["type"] != "IDENTIFIER":
                        raise SyntaxError(
                            f"Expected IDENTIFIER after COMMA in {parser_state.get('filename', 'unknown')}"
                        )
                elif next_token["type"] != "RPAREN":
                    # 非逗号非右括号，停止解析
                    break
        else:
            # 非标识符，停止解析
            break
    
    # 更新 parser_state 位置
    parser_state["pos"] = pos
    
    return params

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function