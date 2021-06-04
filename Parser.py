class Parser:
    def __init__(self, lexer):
        self.h = 0
        self.i = 0
        self.start = lexer
        self.LB = 0

    def ST(self):
        ST = Node('ST')
        while self.i < len(self.start) - 1:
            self.h = 1
            expr = self.expr()
            if expr is not None:
                ST.children.append(expr)
            self.i += 1

        return ST

    def expr(self):
        try:
            expr = Node('expr', height=self.h)
            self.h += 1

            tkn = list(self.start[self.i].keys())[0]

            if tkn == "VAR":
                try:
                    appoint_expr = self.appoint_expr()
                    expr.children.append(appoint_expr)
                    self.h -= 1
                    return expr

                except BaseException:
                    expr.children.append(Leaf(list(self.start[self.i].keys())[0], list(self.start[self.i].values())[0],
                                              self.h))
                    self.check_next('POINT')
                    self.i += 1
                    method = self.method()
                    expr.children.append(method)
                    return expr

            elif tkn == 'WHILE':
                while_expr = self.while_expr()
                expr.children.append(while_expr)
                self.h -= 1
                return expr

            elif tkn == 'IF':
                if_expr = self.if_expr()
                expr.children.append(if_expr)
                self.h -= 1
                return expr

            else:
                return None
        except BaseException:
            raise BaseException

    def method(self):
        method = Node('method', height=self.h)
        self.h += 1
        self.check_next('METHOD')
        self.i += 1
        method.children.append(Leaf(name=list(self.start[self.i].keys())[0], value=list(self.start[self.i].values())[0],
                                    height=self.h))
        self.h += 1
        self.check_next('LBreaket')
        self.i += 1
        method.children.append(Leaf(name=list(self.start[self.i].keys())[0], value=list(self.start[self.i].values())[0],
                                    height=self.h))
        math_expr = self.math_expr()
        method.children.append(math_expr)

        if not list(self.start[self.i].keys())[0] == 'END_COM':
            raise BaseException

        return method

    def if_expr(self):
        h = self.h
        if_expr = Node('if_expr', height=self.h)
        self.h += 1
        start_height = self.h
        self.check_next('LBreaket')
        if_expr.children.append(Leaf('LBreaket', '(', height=self.h))
        self.i += 2
        self.h += 1
        tkn = list(self.start[self.i].keys())[0]

        if tkn == 'VAR' or tkn == 'NUMBER' or tkn == 'LBreaket':
            logic = self.logic(ht=[start_height])
            if_expr.children.append(logic)

            self.h = start_height
            self.check_next('LFBreaket')
            if_expr.children.append(Node('LFBreaket', height=start_height))
            self.i += 1
            num_L = 1
            while num_L:
                if list(self.start[self.i].keys())[0] == 'RFBreaket':
                    num_L -= 1
                if list(self.start[self.i].keys())[0] == 'LFBreaket':
                    num_L += 1
                if num_L:
                    self.i += 1
                    self.h = start_height
                    self.h += 1
                    if list(self.start[self.i].keys())[0] == 'LFBreaket':
                        num_L += 1
                    if list(self.start[self.i].keys())[0] == 'RFBreaket':
                        num_L -= 1
                        break
                    expr = self.expr()
                    if expr is not None:
                        if_expr.children.append(expr)

            if_expr.children.append(Node('RFBreaket', height=start_height))

            if self.i < len(self.start) - 1:
                self.check_next('ELSE')
                self.i += 1
                self.check_next('LFBreaket')
                self.h = h
                if_expr.children.append(Node('ELSE', height=self.h))
                self.h += 1
                start_height = self.h
                if_expr.children.append(Node('LFBreaket', height=self.h))
                num_L = 1

                while num_L:

                    if list(self.start[self.i].keys())[0] == 'RFBreaket':
                        num_L -= 1
                    if list(self.start[self.i].keys())[0] == 'LFBreaket':
                        num_L += 1
                    if num_L:
                        self.i += 1
                        self.h = start_height
                        self.h += 1
                        if list(self.start[self.i].keys())[0] == 'LFBreaket':
                            num_L += 1
                        if list(self.start[self.i].keys())[0] == 'RFBreaket':
                            num_L -= 1
                            break
                        expr = self.expr()
                        if expr is not None:
                            if_expr.children.append(expr)

                if_expr.children.append(Node('RFBreaket', height=start_height))
            return if_expr

    def while_expr(self):
        while_expr = Node('while_expr', height=self.h)
        self.h += 1
        start_height = self.h
        self.check_next('LBreaket')
        while_expr.children.append(Leaf('LBreaket', '(', height=self.h))
        self.i += 2
        self.h += 1
        tkn = list(self.start[self.i].keys())[0]
        if tkn == 'VAR' or tkn == 'NUMBER' or tkn == 'LBreaket':
            math_logic = self.logic(ht=[start_height])
            while_expr.children.append(math_logic)

            self.h = start_height
            self.check_next('LFBreaket')
            self.i += 1
            while_expr.children.append(Node('LFBreaket', height=self.h))
            num_L = 1

            while num_L:
                if list(self.start[self.i].keys())[0] == 'RFBreaket':
                    num_L -= 1
                if list(self.start[self.i].keys())[0] == 'LFBreaket':
                    num_L += 1

                if num_L:
                    self.i += 1
                    self.h = start_height
                    self.h += 1
                    if list(self.start[self.i].keys())[0] == 'LFBreaket':
                        num_L += 1
                    if list(self.start[self.i].keys())[0] == 'RFBreaket':
                        num_L -= 1
                        break
                    expr = self.expr()
                    if expr is not None:
                        while_expr.children.append(expr)

            while_expr.children.append(Node('RFBreaket', height=start_height))
            return while_expr
        else:
            raise BaseException

    def logic(self, ht=[]):
        tkn = list(self.start[self.i].keys())[0]

        if not tkn == 'RBreaket' or not tkn == 'LOGICAL_OP' \
                or not tkn == 'OP':
            logic = Node('logic', height=self.h)
        else:
            logic = ''
        self.h += 1

        if tkn == 'LBreaket':
            ht.append(self.h)
            LBreaket = self.LBreaket()
            logic.children.append(LBreaket)

        elif tkn == 'RBreaket':
            self.h = ht.pop(-1)
            logic = Node('RBreaket', height=self.h)

        elif tkn == 'NUMBER':
            logic.children.append(Leaf(list(self.start[self.i].keys())[0],
                                            list(self.start[self.i].
                                                 values())[0],
                                            self.h))

            if self.i + 1 < len(self.start):
                if list(self.start[self.i + 1].keys())[0] == 'LOG_OP':
                    self.i += 1
                    logic.children.append(Leaf(list(self.start[self.i].
                                                         keys())[0],
                                                    list(self.start[self.i].
                                                         values())[0],
                                                    self.h))

                elif list(self.start[self.i + 1].keys())[0] == 'OP':
                    self.i += 1
                    logic.children.append(Leaf(list(self.start[self.i].
                                                         keys())[0],
                                                    list(self.start[self.i].
                                                         values())[0],
                                                    self.h))

        elif tkn == 'VAR':
            logic.children.append(Leaf(list(self.start[self.i].keys())[0],
                                            list(self.start[self.i].
                                                 values())[0],
                                            self.h))

            if self.i + 1 < len(self.start):
                if list(self.start[self.i + 1].keys())[0] == 'LOG_OP':
                    self.i += 1
                    logic.children.append(Leaf(list(self.start[self.i].
                                                         keys())[0],
                                                    list(self.start[self.i].
                                                         values())[0],
                                                    self.h))

                elif list(self.start[self.i + 1].keys())[0] == 'OP':
                    self.i += 1
                    logic.children.append(Leaf(list(self.start[self.i].
                                                         keys())[0],
                                                    list(self.start[self.i].
                                                         values())[0],
                                                    self.h))

        elif tkn == 'LOG_OP':
            self.h -= 1
            logic = Node('LOG_OP' +
                              list(self.start[self.i].values())[0],
                              height=self.h)

        elif tkn == 'OP':
            self.h -= 1
            logic = Node('OP' + list(self.start[self.i].values())[0],
                              height=self.h)

        elif not tkn == 'END_COM':
            raise BaseException

        if len(ht):
            self.i += 1
            me = self.logic(ht)
            logic.children.append(me)

        return logic

    def check_next(self, values):
        tkn = list(self.start[self.i + 1].keys())[0]
        if not tkn == values:
            raise BaseException

    def appoint_expr(self):
        appoint_expr = Node('appoint_expr', '=', self.h)
        self.check_next("APPOINT_OP")
        self.h += 1
        appoint_expr.children.append(Leaf(list(self.start[self.i].keys())[0],
                                          list(self.start[self.i].
                                              values())[0], self.h))
        self.i += 1
        appoint_expr.children.append(Leaf(list(self.start[self.i].keys())[0],
                                          list(self.start[self.i].
                                              values())[0], self.h))
        self.h -= 1
        self.i += 1
        tkn = list(self.start[self.i].keys())[0]
        if tkn == 'STR':
            self.h += 1
            appoint_expr.children.append(Leaf('STR', list(self.start[self.i].
                                                         values())[0],
                                              self.h))
            self.check_next('END_COM')
            self.i += 1

        elif tkn == 'NUMBER' or tkn == 'LBreaket' or tkn == 'VAR':
            self.h += 1
            math_expr = self.math_expr()
            appoint_expr.children.append(math_expr)

        elif tkn == 'LINKED_LIST_KW':
            self.h += 1
            appoint_expr.children.append(Leaf('LINKED_LIST_KW', list(self.start[self.i].values())[0], self.h))

        return appoint_expr

    def math_expr(self, ht=[]):
        tkn = list(self.start[self.i].keys())[0]
        if not tkn == 'RBreaket' or not tkn == 'OP' or not tkn == 'POINT':
            math_expr = Node('math_expr', height=self.h)
        else:
            math_expr = ''
        self.h += 1

        if tkn == 'LBreaket':
            ht.append(self.h)
            LBreaket = self.LBreaket()
            math_expr.children.append(LBreaket)

        elif tkn == 'RBreaket':
            self.LB -= 1
            self.h = ht.pop(-1)
            if self.LB < 0:
                raise BaseException
            math_expr = Node('RBreaket', value=')', height=self.h)

        elif tkn == 'NUMBER':
            math_expr.children.append(Leaf(list(self.start[self.i].keys())[0],
                                           list(self.start[self.i].
                                                values())[0],
                                           self.h))

            if self.i + 1 < len(self.start):
                if list(self.start[self.i + 1].keys())[0] == 'OP':
                    self.i += 1
                    math_expr.children.append(Leaf(list(self.start[self.i].
                                                        keys())[0],
                                                   list(self.start[self.i].
                                                        values())[0],
                                                   self.h))

        elif tkn == 'OP':
            self.h -= 1
            math_expr = Node('OP' + list(self.start[self.i].values())[0],
                             height=self.h)

        elif tkn == 'VAR':
            math_expr.children.append(Leaf(list(self.start[self.i].keys())[0],
                                           list(self.start[self.i].
                                                values())[0],
                                           self.h))

            if self.i + 1 < len(self.start):
                if list(self.start[self.i + 1].keys())[0] == 'OP':
                    self.i += 1
                    math_expr.children.append(Leaf(list(self.start[self.i].
                                                        keys())[0],
                                                   list(self.start[self.i].
                                                        values())[0],
                                                   self.h))

        elif tkn == 'POINT':
            math_expr = self.method()
            self.i -= 1
        elif not tkn == 'END_COM':
            raise BaseException

        self.i += 1
        if not list(self.start[self.i].keys())[0] == 'END_COM':
            me = self.math_expr(ht)
            math_expr.children.append(me)

        return math_expr

    def LBreaket(self):
        self.LB += 1
        LBreaket = Leaf('LBreaket', '(', height=self.h)

        return LBreaket


class Node:
    def __init__(self, name='', value='', height=0):
        self.children = []
        self.name = name
        self.value = value
        self.height = height
        self.buffer = []

    def __repr__(self):
        str_end = ''
        for child in self.children:
            str_end += "\t" * child.height + f'{child}'
        return f'{self.name}\n{str_end}'


class Leaf:
    def __init__(self, name='', value='', height=0):
        self.name = name
        self.value = value
        self.height = height

    def __repr__(self):
        return f'{self.name} {self.value}\n'
