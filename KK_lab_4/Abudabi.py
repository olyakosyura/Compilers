__author__ = 'admin'


class abudabi():
    def __init__(self):
        self.fo = None
        self.g = None
        self.c_token = ''
        self.c_token_type = ''
        self.delimiters = {' ', '\t', '\n'}
        self.identificators = {}
        self.last_pos = 0
        self.last_char = ' '

    def get_next_token(self):
        s = ''
        self.last_pos = self.fo.tell()
        c = self.fo.read(1)
        while c in self.delimiters:
            c = self.fo.read(1)
        while c not in self.delimiters and c not in self.g.e and c != '':
            s += c
            c = self.fo.read(1)
        if s == '' and c in self.g.e:
            self.c_token = c
            return c
        self.c_token = s
        return s

    def loop_back(self):
        self.fo.seek(self.last_pos)

    def run(self):
        result = self.read_block()
        if result[0] == 'Error':
            print(result)
        return result

    def read_block(self):
        begin_tok = self.get_next_token()
        if begin_tok == 'begin':
            res = self.read_operators()
            if res[0] == 'Error':
                return res
            res = self.read_block_end()
            return res
            # return all the identificators and values
        else:
            return ('Error', 'cant find starting block')

    def read_block_end(self):
        end_block = self.get_next_token()
        if end_block == 'end':
            return ('Result')
        else:
            return ('Error', 'cant find end of the block')

    def read_operators(self):
        id = self.get_next_token()
        if id in self.g.n or id in self.g.e:
            return ('Error', 'You should use unique ID at the start of operator')
        if id not in self.identificators:
            self.identificators[id] = False
        res = self.get_next_token()
        if res != '=':
            return ('Error', 'Expected \'=\' instead of ' + res)
        res = self.read_expression()
        if res[0] == 'Error':
            return res
        else:
            if res[1] == 'true':
                self.identificators[id] = True
            else:
                self.identificators[id] = False
        delim = self.get_next_token()
        if delim == ';':
            res = self.read_operators()
            if res[0] == 'Error':
                return res
        elif delim == 'end':
            self.loop_back()
            return ('Exit', ' end of the program reached')
        else:
            return ('Error', ' cant detect next statment')
        return res

    def read_expression(self):
        res1 = self.read_value()
        if res1[0] == 'Error':
            return res1
        res = self.get_next_token()
        while res != ';' and res != 'end':
            if res == '!':
                res2 = self.read_expression()
                if res2[0] == 'Error':
                    return res2
                res1 = self.log_or(res1, res2)
            elif res == '&':
                res2 = self.read_value()
                if res2[0] == 'Error':
                    return res2
                res1 = self.log_and(res1, res2)
            else:
                return ('Error', 'Unexpected symbol ' + res)
            res = self.get_next_token()
        self.loop_back()
        return res1

    def read_value(self):
        temp = self.get_next_token()
        if temp != '-':
            res = self.is_value(temp)
            if res[0] == 'Error':
                return res
            return ('Value', res[1])
        else:
            val = self.get_next_token()
            resval = self.is_value(val)
            if resval[0] == 'Error':
                return resval
            if resval[1] == 'true':
                return ('Value', 'false')
            return ('Value', 'true')

    def is_value(self, t):
        if t == 'true' or t == 'false':
            return ('Value', t)
        if self.identificators.get(t) is None:
            return ('Error', 'Cant uderstand identificator' + t)
        tt = self.identificators[t]
        if tt:
            return ('Id', 'true')
        return ('Id', 'false')

    def log_or(self, a, b):
        if a[1] == 'true' or b[1] == 'true':
            return ('Value', 'true')
        return ('Value', 'false')

    def log_and(self, a, b):
        if a[1] == 'true' and b[1] == 'true':
            return ('Value', 'true')
        return ('Value', 'false')