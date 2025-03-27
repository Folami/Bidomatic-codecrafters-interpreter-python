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
        return str(expr.value)
    
    def visit_unary_expr(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.right)
    
    def visit_comma_expr(self, expr):
        # You might want to print as: (,<left> <right>)
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)
    
    def visit_conditional_expr(self, expr):
        return self.parenthesize("?:", expr.condition, expr.then_branch, expr.else_branch)
    
    def parenthesize(self, name, *exprs):
        builder = []
        builder.append(f"({name}")
        for expr in exprs:
            builder.append(" ")
            builder.append(expr.accept(self))
        builder.append(")")
        return "".join(builder)