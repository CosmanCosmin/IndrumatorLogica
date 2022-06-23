# (a<->b) = ((a->b)&(b->a))
def eliminateDoubleImplication(a, b):
    return f"(({a}->{b})&({b}->{a}))"


# (a->b) = (~a|b)
def eliminateImplication(a, b):
    return f"(~{a}|{b})"


# (a|(b&c)) = ((a|b)&(a|c))
def distributeOr1(a, b, c):
    return f"(({a}|{b})&({a}|{c}))"


# ((a&b)|c) = ((a|c)&(b|c))
def distributeOr2(a, b, c):
    return f"(({a}|{c})&({b}|{c}))"


# (a&(b|c)) = ((a&b)|(a&c))
def distributeAnd1(a, b, c):
    return f"(({a}&{b})|({a}&{c}))"


# ((a|b)&c) = ((a&c)|(b&c))
def distributeAnd2(a, b, c):
    return f"(({a}&{c})|({b}&{c}))"


# (a|(b|c)) = ((a|b)|c)
def swapBracketOr(a, b, c):
    return f"(({a}|{b})|{c})"


# (a&(b&c)) = ((a&b)&c)
def swapBracketAnd(a, b, c):
    return f"(({a}&{b})&{c})"


# ~(a|b) = (~a&~b)
def insertNegationOr(a, b):
    return f"(~{a}&~{b})"


# ~(a&b) = (~a|~b)
def insertNegationAnd(a, b):
    return f"(~{a}|~{b})"


# ~~a = a
def eliminateDoubleNegation(a):
    return f"{a}"


