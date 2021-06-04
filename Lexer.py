import re


class Lexer(object):
    tkn = {"IF": "^if$", "ELSE": "^else$", "WHILE": "^while$", "OP": "^[-+*/]$", "LOG_OP": r"^==|>|>=|<|<=|!=$",
            "LBreaket": "[(]", "RBreaket": "[)]", 'POINT': r'\.', "END_COM": "^;$", "LFBreaket": "^[{]$",
            'LINKED_LIST_KW': r'LinkedList', "RFBreaket": "^[}]$", "APPOINT_OP": "^=$", "ENDCOM": "^;$",
            "NUMBER": r"^0|([1-9][0-9]*)$", "STR": r"'[^']*'", "VAR": "^[a-zA-Z0-9_]+$", "UNDEFINED": r".*[^.]*"}

    def __init__(self):
        self.list_tokens = []

    def tkn_(self, item):
        for key in self.tkn.keys():
            if re.fullmatch(self.tkn[key], item):
                return key

    def term(self, file):
        with open(file) as file_handler:
            buffer = ''
            last_token = ''
            for line in file_handler:
                for char in line:
                    if not len(buffer) and char == "'":
                        buffer += char
                        continue
                    elif len(buffer) and not buffer.count("'") == 2:
                        if buffer[0] == "'":
                            buffer += char
                            continue

                    if last_token == 'POINT':
                        if not char == '(':
                            buffer += char
                            continue
                        else:
                            self.list_tokens.append({'METHOD': buffer})
                            buffer = ''

                    last_token = self.tkn_(buffer)
                    buffer += char
                    tkn = self.tkn_(buffer)

                    if tkn == "UNDEFINED":
                        if len(buffer) and not last_token == "UNDEFINED":
                            self.list_tokens.append({last_token: buffer[:-1]})
                        if not (buffer[-1] == ' ' or buffer[-1] == '\n'):
                            buffer = buffer[-1]
                        else:
                            buffer = ''

            tkn = self.tkn_(buffer)
            if not tkn == "UNDEFINED":
                self.list_tokens.append({tkn: buffer[0]})
