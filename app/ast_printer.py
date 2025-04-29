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
        if isinstance(expr.value, float):
            # Match Java's String.format("%.1f", value) behavior
            return f"{expr.value:.1f}"
        if isinstance(expr.value, str):
            # String literals without quotes in AST
            return expr.value
        return str(expr.value)

    def visit_unary_expr(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def visit_variable_expr(self, expr):
        return expr.name.lexeme

    def visit_assign_expr(self, expr):
        from .expr import Variable  # Import at function level to avoid circular imports
        return self.parenthesize("=", Variable(expr.name), expr.value)

    def visit_logical_expr(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_call_expr(self, expr):
        return self.parenthesize("call", expr.callee)

    def visit_get_expr(self, expr):
        return self.parenthesize(".", expr.object)

    def visit_set_expr(self, expr):
        return self.parenthesize("=", expr.object, expr.value)

    def visit_this_expr(self, expr):
        return "this"

    # Uncomment when implementing inheritance
    # def visit_super_expr(self, expr):
    #     return "super." + expr.method.lexeme

    def parenthesize(self, name, *exprs):
        parts = [f"({name}"]
        for expr in exprs:
            parts.append(" ")
            parts.append(expr.accept(self))
        parts.append(")")
        return "".join(parts)



