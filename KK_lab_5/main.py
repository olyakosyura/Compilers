from Grammar import Grammar

__author__ = 'admin'


def tokenizate(fo, g):
    token_list = []
    ch = fo.read(1)
    res = ''
    while ch != '':
        if ch in g.e:
            if res in g.e:
                token_list.append((res, symbol[res]))
            else:
                if res != '':
                    token_list.append((res, symbol['atom']))
            res = ''
            token_list.append((ch, symbol[ch]))
        else:
            if ch in [' ', '\n', '$']:
                if res in g.e:
                    token_list.append((res, symbol[res]))
                else:
                    if res != '':
                        token_list.append((res, symbol['atom']))
                res = ''
            else:
                res += ch
        ch = fo.read(1)
    token_list.append(('$', symbol['$']))
    return token_list


marker = '$'
blank = ' '
max = 1000
error_msg = (
    'отсутствует операнд.',
    'несбалансированная правая скобка.',
    'отсутствует оператор.',
    'отсутствует правая скобка.'
)
symbol = {"true": 0, "false": 1, "-": 2, "&": 3, "!": 4, "atom": 5,
          ";": 6, "=": 7, "begin": 8, "end": 9, "$": 10}

matrix = (
    # tr, fal, not, and, orr, atm, col, equ, beg, end, dol
    ('1', '1', '1', '>', '>', '1', '>', '1', '1', '>', '1'),  # true
    ('2', '2', '2', '>', '>', '2', '>', '2', '2', '>', '2'),  # false
    ('<', '<', '3', '>', '>', '<', '>', '3', '3', '>', '3'),  # not
    ('<', '<', '<', '>', '>', '<', '>', '4', '4', '>', '4'),  # and
    ('<', '<', '<', '<', '>', '<', '>', '5', '5', '>', '5'),  # or
    ('6', '6', '6', '>', '>', '6', '>', '=', '6', '>', '6'),  # atom
    ('7', '7', '7', '7', '7', '<', '>', '7', '7', '>', '7'),  # colon
    ('<', '<', '<', '<', '<', '<', '>', '8', '8', '>', '8'),  # equtation
    ('9', '9', '9', '9', '9', '<', '<', '<', '9', '=', '9'),  # begin
    ('0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '>'),  # end
    ('10', '10', '10', '10', '10', '10', '10', '10', '<', '10', '10')  # $$
)

s = list()

token_stream = list()
rp_notation = list()

flag = False
done = False

lines = []
# fileObject = open('C:\\Users\\Roman\\PycharmProjects\\KK5\\text2.txt', 'r')
# fileObject = open('C:\\Users\\admin\\PycharmProjects\\KK_lab_5\\text2.txt', 'r')
fileObject = open('F:\\KKKK\\KK_lab_5\\text2.txt', 'r')
ln = fileObject.readline()
while ln != '':
    lines.append(ln)
    ln = fileObject.readline()
fileObject.close()

lines = [x.replace('\n', '').split(' ') for x in lines]
g = Grammar()
g.input_from_lines(lines)

# fileObject = open('C:\\Users\\Roman\\PycharmProjects\\KK5\\program.rulog', 'r')
# fileObject = open('C:\\Users\\admin\\PycharmProjects\\KK_lab_5\\program.rulog', 'r')
fileObject = open('F:\\KKKK\\KK_lab_5\\program.rulog', 'r')
token_stream = tokenizate(fileObject, g)
fileObject.close()

while True:
    if len(token_stream) > 0:
        ch = token_stream[0]
        token_stream = token_stream[1:]
    if ch[0] == '$':
        done = True
    else:
        s.append(('$', 10))
        t = 0
        while t > 0 or ch != ('$', 10):
            if matrix[s[t][1]][ch[1]] in ['<', '=']:
                s.append(ch)
                t += 1
                ch = token_stream[0]
                token_stream = token_stream[1:]
            elif matrix[s[t][1]][ch[1]] in ['>']:
                while True:
                    rp_notation.append(s[t])
                    t -= 1
                    if matrix[s[t][1]][s[t + 1][1]] == '<':
                        s.pop()
                        break
                    s.pop()
            else:
                print('ERROR: ', error_msg[int(matrix[s[t][1]][ch[1]]) % len(error_msg)])
                flag = True
                break
        if flag:
            flag = False
        else:
            print('\nPOSTFIX NOTATION: \n')
            for p in rp_notation:
                print(p[0])
            pass
    if done: break

print(rp_notation)

