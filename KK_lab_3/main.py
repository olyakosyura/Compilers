# coding=utf-8
__author__ = 'admin'
from Grammar import Grammar

print("Input path to file")
# sss = input()
sss = "F:\\KKKK\\KK_lab_3\\text2.txt"
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
G3 = G0.homsky_form()
t = ('true', '&', '-', 'true')
if G3.CYK(t):
    print(G3.left_output(t))

target = open("F:\\KKKK\\KK_lab_3\\out.txt", 'w')
target.truncate()
for line in G3.out_to_lines():
    target.write(line + "\n")
target.close()