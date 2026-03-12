# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_package._parse_primary_src import _parse_primary

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
#   "filename": str,
#   "pos": int,
#   "error": str
# }

# === main function ===
def _parse_unary_op(parser_state: ParserState) -> AST:
    """
    解析一元运算符表达式（如 -x, not x, ~x）。
    输入：parser_state（pos 指向当前 token）。
    输出：AST 节点或 None（如果不是一元表达式）。
    副作用：如果成功解析，修改 parser_state["pos"] 到表达式结束位置。
    异常：语法错误时抛出 SyntaxError。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查是否还有 token
    if pos >= len(tokens):
        return None
    
    current_token = tokens[pos]
    token_type = current_token["type"]
    
    # 检查当前 token 是否为一元运算符
    unary_operators = {"MINUS", "NOT", "TILDE"}
    if token_type not in unary_operators:
        return None
    
    # 记录运算符信息
    operator_value = current_token["value"]
    operator_line = current_token["line"]
    operator_column = current_token["column"]
    
    # 前进 pos，跳过运算符 token
    parser_state["pos"] = pos + 1
    
    # 解析右侧操作数
    operand_ast = _parse_primary(parser_state)
    
    # 检查是否成功解析操作数
    if operand_ast is None:
        # 恢复 pos 到运算符位置（可选，但有助于调试）
        parser_state["pos"] = pos
        filename = parser_state.get("filename", "<unknown>")
        raise SyntaxError(f"{filename}:{operator_line}:{operator_column}: Expected expression after unary operator")
    
    # 构建一元运算 AST 节点
    result: AST = {
        "type": "unary_op",
        "operator": operator_value,
        "operand": operand_ast,
        "line": operator_line,
        "column": operator_column
    }
    
    return result

# === helper functions ===
# 无额外 helper 函数，逻辑已在主函数中完成

# === OOP compatibility layer ===
# 本模块为普通函数节点，不需要 OOP wrapper
