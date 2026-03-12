# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression
from ._parse_block_package._parse_block_src import _parse_block

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

ElseIfBranch = Dict[str, Any]
# ElseIfBranch possible fields:
# {
#   "condition": AST,
#   "branch": AST,
#   "line": int,
#   "column": int
# }

# === main function ===
def _parse_if_stmt(parser_state: dict) -> dict:
    """解析 IF 语句，返回 IF AST 节点。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]
    
    # 1. 验证当前 token 是 IF
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: 期望 IF token")
    
    current_token = tokens[pos]
    if current_token["type"] != "IF":
        raise SyntaxError(
            f"{filename}:{current_token['line']}:{current_token['column']}: "
            f"期望 IF token，实际为 {current_token['type']}"
        )
    
    # 记录 IF token 的位置
    if_line = current_token["line"]
    if_column = current_token["column"]
    
    # 2. 消费 IF token
    parser_state["pos"] += 1
    
    # 3. 解析条件表达式
    condition_ast = _parse_expression(parser_state)
    
    # 4. 消费 RPAREN (由 _parse_expression 消费到 RPAREN 之后)
    # _parse_expression 应该已经消费了 RPAREN
    
    # 5. 解析 then 块（当前 token 应该是 LBRACE）
    then_branch = _parse_block(parser_state)
    
    # 6. 处理 ELSE IF 和 ELSE
    else_if_branches = []
    else_branch = None
    
    while parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        
        if current_token["type"] != "ELSE":
            break
        
        # 消费 ELSE token
        else_line = current_token["line"]
        else_column = current_token["column"]
        parser_state["pos"] += 1
        
        # 检查下一个 token
        if parser_state["pos"] >= len(tokens):
            raise SyntaxError(
                f"{filename}:{else_line}:{else_column}: "
                f"ELSE 后期望 IF 或 LBRACE"
            )
        
        next_token = tokens[parser_state["pos"]]
        
        if next_token["type"] == "IF":
            # ELSE IF 分支
            parser_state["pos"] += 1  # 消费 IF token
            
            # 解析条件表达式
            elif_condition = _parse_expression(parser_state)
            
            # 解析 then 块
            elif_branch = _parse_block(parser_state)
            
            else_if_branches.append({
                "condition": elif_condition,
                "branch": elif_branch,
                "line": else_line,
                "column": else_column
            })
        elif next_token["type"] == "LBRACE":
            # ELSE 分支
            else_branch = _parse_block(parser_state)
            break
        else:
            raise SyntaxError(
                f"{filename}:{else_line}:{else_column}: "
                f"ELSE 后期望 IF 或 LBRACE，实际为 {next_token['type']}"
            )
    
    # 7. 构建并返回 IF AST 节点
    return {
        "type": "IF",
        "condition": condition_ast,
        "then_branch": then_branch,
        "else_if_branches": else_if_branches,
        "else_branch": else_branch,
        "line": if_line,
        "column": if_column
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function
