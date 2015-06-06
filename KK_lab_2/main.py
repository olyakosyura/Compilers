__author__ = 'admin'
from Grammar import Grammar

print("Input path to file")
# sss = input()
sss = "F:\\KKKK\\KK_lab_2\\test.txt"
fo = open(sss)
lines = []
G0 = Grammar()
while sss != '':
    sss = fo.readline()
    lines.append(sss)
    print(sss)
fo.close()

lines = [ls.replace('\n', '') for ls in lines]
lines = [ls for ls in lines if ls != '']
lines = [ls.split(' ') for ls in lines]
G0.input_from_lines(lines)
G1 = G0.alg_81()
G2 = G1.alg_82()
G2 = G2.normalize()
G3 = G2.alg_83()

target = open("F:\\KKKK\\KK_lab_2\\out.txt", 'w')
target.truncate()
for line in G3.out_to_lines():
    target.write(line+"\n")
target.close()