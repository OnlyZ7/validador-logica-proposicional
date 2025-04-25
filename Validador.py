# GRUPO RA1 
#Arthur Leme
#André Thiago
#Matheus Reich


# Validador de expressões de lógica proposicional escritas em LaTeX

import sys

TOKENS = {
    '\\neg': 'NOT',
    '\\wedge': 'AND',
    '\\vee': 'OR',
    '\\rightarrow': 'IMPLIES',
    '\\leftrightarrow': 'IFF',
    'true': 'CONST',
    'false': 'CONST',
    '(': 'LPAREN',
    ')': 'RPAREN',
}

class Lexer:
    def __init__(self, linha):
        self.linha = linha.strip().replace('\\\\', '\\').split('#')[0].strip()
        self.pos = 0
        self.tokens = []
        self.estado = 'INICIAL'

    def avancar(self):
        if self.pos < len(self.linha):
            c = self.linha[self.pos]
            self.pos += 1
            return c
        return None

    def retroceder(self):
        self.pos -= 1

    def proximo_token(self):
        buffer = ''
        self.estado = 'INICIAL'

        while self.pos < len(self.linha):
            c = self.avancar()

            if self.estado == 'INICIAL':
                if c.isspace():
                    continue
                elif c == '(': return ('LPAREN', c)
                elif c == ')': return ('RPAREN', c)
                elif c == '\\': self.estado = 'OPERADOR'; buffer += c
                elif c.isdigit(): self.estado = 'PROP'; buffer += c
                elif c.isalpha(): self.estado = 'ID'; buffer += c
                else: return ('ERROR', c)

            elif self.estado == 'OPERADOR':
                buffer += c
                candidatos = [op for op in TOKENS if op.startswith(buffer)]
                if buffer in TOKENS: return (TOKENS[buffer], buffer)
                elif len(candidatos) > 0: continue
                else: return ('ERROR', buffer)

            elif self.estado == 'ID':
                if c.isalnum(): buffer += c
                else:
                    self.retroceder()
                    if buffer in ['true', 'false']: return ('CONST', buffer)
                    elif buffer.startswith('p') and len(buffer) > 1 and buffer[1:].isalnum(): return ('PROP', buffer)
                    else: return ('ERROR', buffer)

            elif self.estado == 'PROP':
                if c.isalnum(): buffer += c
                else:
                    self.retroceder()
                    return ('PROP', buffer)

        if self.estado == 'OPERADOR' and buffer in TOKENS: return (TOKENS[buffer], buffer)
        if self.estado == 'ID':
            if buffer in ['true', 'false']: return ('CONST', buffer)
            elif buffer.startswith('p') and len(buffer) > 1 and buffer[1:].isalnum(): return ('PROP', buffer)
            else: return ('ERROR', buffer)
        if self.estado == 'PROP': return ('PROP', buffer)

        return ('EOF', None)

    def tokenizar(self):
        tokens = []
        while True:
            tok = self.proximo_token()
            tokens.append(tok)
            if tok[0] in ['EOF', 'ERROR']:
                break
        return tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def current(self):
        return self.tokens[self.index][0]

    def eat(self, expected):
        if self.current() == expected:
            self.index += 1
            return True
        return False

    def parse(self):
        valid = self.formula()
        return valid and self.current() == 'EOF'

    def formula(self):
        if self.current() == 'CONST': return self.eat('CONST')
        elif self.current() == 'PROP': return self.eat('PROP')
        elif self.current() == 'LPAREN':
            self.eat('LPAREN')
            if self.current() == 'NOT':
                self.eat('NOT')
                if not self.formula(): return False
                return self.eat('RPAREN')
            elif self.current() in ['AND', 'OR', 'IMPLIES', 'IFF']:
                op = self.current()
                self.eat(op)
                if not self.formula(): return False
                if not self.formula(): return False
                return self.eat('RPAREN')
            else:
                return False
        return False


def validar(expressao):
    lexer = Lexer(expressao)
    tokens = lexer.tokenizar()
    if any(t[0] == 'ERROR' for t in tokens): return False
    parser = Parser(tokens)
    return parser.parse()


def main():
    if len(sys.argv) < 2:
        print("Uso: python validador.py arquivo.txt")
        sys.exit(1)

    try:
        with open(sys.argv[1], encoding='utf-8') as f:
            linhas = [l.strip() for l in f if l.strip()]
            total = int(linhas[0])
            expressoes = linhas[1:total+1]

            for e in expressoes:
                print("valida" if validar(e) else "invalida")

    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
