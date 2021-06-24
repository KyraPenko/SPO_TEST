from Lexer import Lexer
from SM import SM
from Parser import Parser

if __name__ == '__main__':
    L = Lexer()
    L.term('test.txt')
    print('List of tokens:\n\n', L.list_tkn)
    try:
        P = Parser(L.list_tkn)
        Tree = P.T()
        print('\nOutput tree:\n', Tree)
        StackMachine = SM(Tree.children)
        StackMachine.start()
    except BaseException:
        print('Syntax error')
