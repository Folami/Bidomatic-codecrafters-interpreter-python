class AstPrinter:
    def print(self, expr):
        return expr.accept(self)

    def visit_binary_expr(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr):
        return self.parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr):
        if expr.value is None:
            return "nil"
        if isinstance(expr.value, bool):
            return "true" if expr.value else "false"
        if isinstance(expr.value, float):
            # If the float is an integer (e.g. 34.0), format with one decimal place.
            # Otherwise, use the full string representation (preserving extra decimals).
            if expr.value.is_integer():
                return f"{expr.value:.1f}"
            else:
                return str(expr.value)
        if isinstance(expr.value, str):
            # String literals without quotes in AST
            return expr.value
        return str(expr.value)

    def visit_unary_expr(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def visit_variable_expr(self, expr):
        return expr.name.lexeme

    def parenthesize(self, name, *exprs):
        parts = [f"({name}"]
        for expr in exprs:
            parts.append(" ")
            parts.append(expr.accept(self))
        parts.append(")")
        return "".join(parts)



