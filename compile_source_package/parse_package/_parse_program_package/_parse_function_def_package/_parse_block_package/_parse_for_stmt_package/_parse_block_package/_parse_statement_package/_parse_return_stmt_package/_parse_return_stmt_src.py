# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No subfunctions needed

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
#   "type": str,             # 节点类型 (RETURN_STMT, etc.)
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
def _parse_return_stmt(parser_state: ParserState) -> AST:
    """
    Parse return statement: return [expression];
    
    Input: parser_state with pos pointing to RETURN token
    Output: RETURN_STMT AST node with optional return value expression
    Side effect: updates parser_state["pos"] to after semicolon
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Step 1: Consume RETURN token
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input, expected return statement")
    
    return_token = tokens[pos]
    if return_token["type"] != "RETURN":
        raise SyntaxError(f"Expected RETURN token, got {return_token['type']}")
    
    line = return_token.get("line", 0)
    column = return_token.get("column", 0)
    pos += 1
    
    # Step 2: Check if next token is semicolon (return without value)
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input after 'return'")
    
    current_token = tokens[pos]
    
    # Step 3: Build AST node
    ast_node: AST = {
        "type": "RETURN_STMT",
        "children": [],
        "value": None,
        "line": line,
        "column": column
    }
    
    # Step 4: If not semicolon, parse expression
    if current_token["type"] != "SEMICOLON":
        # Parse expression (delegate to expression parser in real implementation)
        # For now, we parse until we find semicolon
        expr_start = pos
        while pos < len(tokens) and tokens[pos]["type"] != "SEMICOLON":
            pos += 1
        
        if pos >= len(tokens):
            raise SyntaxError("Missing semicolon after return expression")
        
        # Store expression tokens as children (simplified)
        # In full implementation, this would call _parse_expression
        ast_node["children"] = tokens[expr_start:pos]
    
    # Step 5: Consume semicolon
    parser_state["pos"] = pos + 1
    
    return ast_node

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function