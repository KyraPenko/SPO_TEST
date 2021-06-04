from Lexer import Lexer
from SM import SM
from Parser import Parser

if __name__ == '__main__':
    L = Lexer()
    L.term('test.txt')
    print('Tokens:', L.list_tokens)
    try:
        P = Parser(L.list_tokens)
        Tree = P.ST()
        print('Tree:\n', Tree)
        StackMachine = SM(Tree.children)
        StackMachine.start()
    except BaseException:
        print('Syntax error')
