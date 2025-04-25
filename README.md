# Validador de Expressões de Lógica Proposicional em LaTeX

Este projeto implementa um **analisador léxico e sintático** para verificar se expressões de **lógica proposicional escritas em LaTeX** estão bem formadas, utilizando uma abordagem simples de máquina de estados e um **parser recursivo LL(1)**.

---

## Grupo RA1

- Arthur Leme  
- André Thiago  
- Matheus Reich  

---

## Gramática Utilizada

A gramática aceita as seguintes formas:

```
FORMULA         = CONST | PROP | FORMULAUNARIA | FORMULABINARIA  
CONST           = true | false  
PROP            = [0-9][0-9a-z]* | p[0-9a-z]+  
FORMULAUNARIA   = ( NOT FORMULA )  
FORMULABINARIA  = ( OPBIN FORMULA FORMULA )  
OPBIN           = \wedge | \vee | \rightarrow | \leftrightarrow  
NOT             = \neg  
```

---

## Como Executar

### Com Arquivo de Entrada

```bash
python validador.py arquivo.txt
```

O arquivo deve seguir este formato:
- A **primeira linha** contém um número inteiro `N` indicando quantas expressões serão validadas.
- As **próximas N linhas** devem conter as expressões LaTeX a serem verificadas.

### Exemplo de Arquivo `entrada.txt`

```
3
true
(\neg p0)
(\wedge p1 p2)
```

**Saída esperada:**
```
valida
valida
valida
```

---

## Tokens Reconhecidos

| Token  | Exemplo              |
|--------|----------------------|
| CONST  | `true`, `false`      |
| PROP   | `p0`, `123abc`       |
| LPAREN | `(`                  |
| RPAREN | `)`                  |
| NOT    | `\neg`              |
| AND    | `\wedge`            |
| OR     | `\vee`              |
| IMPLIES| `\rightarrow`       |
| IFF    | `\leftrightarrow`   |
| ERROR  | Token inválido       |

---

## Tratamento de Erros

- Se um token for inválido, o analisador retorna `invalida`.
- Se a expressão não seguir a estrutura esperada da gramática, também será considerada `invalida`.

---

## Estrutura do Código

- `Lexer`: Realiza a análise léxica com base em estados (`INICIAL`, `OPERADOR`, `ID`, `PROP`).
- `Parser`: Implementa recursivamente a verificação LL(1) com as regras da gramática.
- `main()`: Gerencia a entrada de expressões a partir de arquivo `.txt`.

