# Trabalho de Compiladores 

> Objetivo: Explorar e aplicar os conceitos de análise léxica, sintática e semântica vistos na disciplina Compiladores ao modificar um gerador de analisador.

# Diferença entre Flex vs Bison vs Yacc

## FLEX

Flex é uma ferramenta usada para criar o **analisador léxico** (lexer).
Ele lê **caracteres da entrada** e transforma em **tokens**, como:

* NUMBER
* PLUS
* MINUS
* IDENTIFIER
* etc.

O Flex pega seu arquivo `.l` e gera um arquivo C chamado `lex.yy.c`, que contém a função `yylex()`.
Essa função é chamada pelo parser (Bison/Yacc) toda vez que ele precisa de um próximo token.


## BISON

Bison é o **sucessor moderno do Yacc**.
Ele cria o **analisador sintático** (parser), que interpreta a sequência de tokens de acordo com uma **gramática**.

Você escreve regras em um arquivo `.y`, e o Bison gera:

* `calc.tab.c` → código do parser
* `calc.tab.h` → definições de tokens

O parser é responsável por entender expressões como:

```
3 + 4 * 2
(10 - 5) / 2
```

Ele sabe a ordem das operações, precedência e associatividade.

## YACC

Yacc é uma ferramenta **mais antiga**, que fazia a mesma coisa que Bison faz hoje.
Ela foi a primeira ferramenta popular de geração de parsers em sistemas Unix.

O Bison foi criado como **substituto compatível**, com muito mais recursos.

O Yacc ainda existe, mas raramente é usado hoje porque:

* não recebe melhorias
* tem menos funcionalidades
* gera código mais limitado

Bison é considerado o padrão moderno.

Resumindo:
* **Flex** lê o texto e descobre “o que é o quê” (números, operadores, etc.).
* **Bison** interpreta esses tokens com base em uma gramática e calcula o resultado.
* **Yacc** é a versão antiga do Bison.

# Mais sobre YACC (Yet Another Compiler-Compiler)
>  É um compilador que implementa uma linguagem que permite criar outros compiladores. Ele facilita a leitura de um programa de computador em uma linguagem e contrói uma árvore sintática para o programa de entreda.
Um gerador de analisadores sintáticos recebe como entrada uma especificação de sintaxe e produz como saída um procedimento para reconhecer essa linguagem. São chamados de compiladores de compiladores.

Características e conceitos do YACC:

* A entrada para YACC é uma gramática livre de contexto, que descreve as regras sintáticas da linguagem que ele analisa.

* O YACC Traduz a gramática em função C que pode realizar uma análise sintática eficiente do texto de entrada de acordo com regras predefinidas/

* Ele faz a análise a partir do LALR(1) (LookAhead, Left-to-right, Rightmost derivation producer with 1 lookahead token), que é um método de análise bottom-up, onde ele utiliza 1 token lookahead para determinar a próxima ação de análise

* Ações semânticas -> são as produções gramaticais associadas a uma ação, isso possibilta que o código execute, geralmente em C, usado na construção de árvores de sintaxe abstrata, na geração de representações intermediárias ou no tratamento de erros.

* Gramáticas de Atributos -> Consistem em símbolos gramaticais não terminais com atributos, que, por meio de ações semânticas, são usados na construção de árvores de análise sintática ou na saída de código.

* É frequentemente usado junto com Flex, ferramenta que gera analisadores léxicos que dividem entrada em tokens que são então processados pelo analisador YACC.

Ações Semânticas e Gramáticas de Atributos em YACC

* "$n" na ação semântica, onde n é um número inteiro, designa o atributo do símbolo não terminal no lado direito da produção.
* "$$" designa o atributo do símbolo não terminal no lado esquerdo da produção. 


Exemplo de arquivo de entrada YACC:

obs: geralmente começam com .y

```yacc
/* definições */
...

%%
/* regras* /
...
%%

/* rotinas auxiliares */
...
```

* Definição: Inclui informações sobre tokens usados na definição da sintaxe. Essa parte pode incluir código C externo, dentro de %{ %}.
* Regra: Contém definições gramaticais em uma forma BNF modificada, são código C em {} e podem ser incorporadas dentro de esquemas de tradução.
* Rotinas Auxiliares: Contém apenas código em C, inclui definiç!Oes de funçÕes para todas as funções necessárias na parte de regras, pode conter a definição da função main se o analisar sintático for executado como um programa e a função main() deve chamar a função yyparse().

### Arquivos .l (lex/flex)

Programa que gera analisadores léxicos. Contém expressões regulares e ações associadas a elas, que são usadas para reconhecer "tokens" em um código-fonte ou fluxo de texto.

Saída de um Lex: arquivo em c (.c), que depois é compilado para criar um programa executável que pode identificar os tokens definidos.

Veja abaixo uma sequência de compilação no momento de uma atribuição:

![compilation-sequence.png](./image/compilation-sequence.png)

* Lex -> Lexical Analyzer
* Yacc -> Syntax Analyzer

| Arquivo      | Você edita? | Por quê?                            |
| ------------ | ----------- | ----------------------------------- |
| `src/calc.y` | ✔️ Sim      | onde fica a **gramática** do parser |
| `src/calc.l` | ✔️ Sim      | onde ficam as **regras do lexer**   |
| `calc.tab.c` | ❌ Não      | gerado automaticamente              |
| `calc.tab.h` | ❌ Não      | gerado automaticamente              |
| `lex.yy.c`   | ❌ Não      | gerado automaticamente              |


# Prática

## Exemplos de comandos com SELECT

```
sql > SELECT * FROM clientes;

sql > SELECT nome, email FROM clientes WHERE idade > 30;
```

## Exemplos de comandos com JOIN

```
sql > SELECT nome, valor FROM clientes JOIN pedidos ON id = cliente_id;
```

## Exemplos de comandos com INSERT

```
sql > INSERT INTO clientes (id, nome, idade, cpf, email) VALUES (6, "Rogério Ramos", 50, "999.888.777-66", "rogerio@example.com");
```
## Exemplos de comandos com UPDATE

```
sql > UPDATE clientes SET idade = 29 WHERE nome = "Ana Souza";

sql > UPDATE clientes SET email = "novoemail@example.com", idade = 45 WHERE id = 5;
```

## Exemplos de comandos com DELETE

```
sql > DELETE FROM clientes WHERE idade < 25;

sql > DELETE FROM pedidos;
```

# Contribuidores

* Gabriela Lacerda (@gabrielasl18)
* Isabele Rocha (@isadpr)
* João Vitor (@joao)

