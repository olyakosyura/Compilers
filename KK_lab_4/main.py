__author__ = 'admin'
import Abudabi
import Grammar


print("Input path to file")
# sss = input()
sss = "F:\\KKKK\\KK_lab_4\\text2.txt"
sss1 = "F:\\KKKK\\KK_lab_4\\program.rulog"
fo = open(sss)
lines = []
G0 = Grammar.Grammar()
while sss != '':
    sss = fo.readline()
    lines.append(sss)
    print(sss)
fo.close()

lines = [ls.replace('\n', '') for ls in lines]
lines = [ls for ls in lines if ls != '']
lines = [ls.split(' ') for ls in lines]
G0.input_from_lines(lines)
P = Abudabi.abudabi()
P.fo = open(sss1, 'r')
P.g = G0
res = P.run()
if res == 'Result':
    for d, v in P.identificators.items():
        print('KEY: ', d, ' VAL: ', v)

pass