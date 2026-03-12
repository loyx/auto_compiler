# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,          # e.g., "LPAREN", "RPAREN", "COMMA", "IDENTIFIER"
#   "value": str,         # token 的文本值
#   "line": int,          # 行号（从 1 开始）
#   "column": int         # 列号（从 1 开始）
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,          # 节点类型，如 "CALL", "IDENTIFIER", "BINARY_OP"
#   "children": list,     # 子节点列表（可选）
#   "value": Any,         # 节点值（可选）
#   "line": int,          # 行号
#   "column": int         # 列号
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,       # Token 列表
#   "filename": str,      # 源文件名
#   "pos": int,           # 当前位置（tokens 列表索引）
#   "error": str          # 错误信息（可选）
# }


# === main function ===
def _parse_function_call(parser_state: dict, callee: dict) -> dict:
    """
    解析函数调用表达式。
    
    输入：parser_state（pos 指向 LPAREN token）、callee（被调用的表达式 AST）
    输出：CALL 类型 AST 节点，包含 callee 和 arguments
    副作用：修改 parser_state["pos"] 到 RPAREN 之后的位置
    异常：缺少 RPAREN 或参数解析失败时抛出 SyntaxError
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # 验证当前 token 是 LPAREN
    if pos >= len(tokens) or tokens[pos]["type"] != "LPAREN":
        raise SyntaxError(f"{filename}:???:???: Expected '(' before function arguments")
    
    # 获取 callee 的位置信息用于返回 AST
    callee_line = callee.get("line", tokens[pos]["line"])
    callee_column = callee.get("column", tokens[pos]["column"])
    
    # 消费 LPAREN token
    parser_state["pos"] += 1
    pos = parser_state["pos"]
    
    # 解析参数列表
    arguments = []
    
    while pos < len(tokens):
        current_token = tokens[pos]
        
        # 遇到 RPAREN，参数列表结束
        if current_token["type"] == "RPAREN":
            break
        
        # 解析一个参数表达式
        arg_ast = _parse_expression(parser_state)
        arguments.append(arg_ast)
        
        # 更新位置
        pos = parser_state["pos"]
        
        # 检查下一个 token
        if pos < len(tokens):
            next_token = tokens[pos]
            if next_token["type"] == "COMMA":
                # 跳过 COMMA，继续解析下一个参数
                parser_state["pos"] += 1
                pos = parser_state["pos"]
            elif next_token["type"] == "RPAREN":
                # 正常结束
                break
            else:
                # 意外的 token
                raise SyntaxError(
                    f"{filename}:{next_token['line']}:{next_token['column']}: "
                    f"Expected ',' or ')' after function argument"
                )
        else:
            # tokens 耗尽，缺少 RPAREN
            raise SyntaxError(
                f"{filename}:???:???: Unexpected end of input, expected ')'"
            )
    
    # 消费 RPAREN token
    if pos >= len(tokens) or tokens[pos]["type"] != "RPAREN":
        raise SyntaxError(
            f"{filename}:???:???: Expected ')' after function arguments"
        )
    
    parser_state["pos"] += 1
    
    # 构建并返回 CALL AST 节点
    return {
        "type": "CALL",
        "callee": callee,
        "arguments": arguments,
        "line": callee_line,
        "column": callee_column
    }


# === helper functions ===
# No helper functions needed; logic is straightforward.

# === OOP compatibility layer ===
# No OOP wrapper needed for this parser function node.
