__author__ = 'Roman'
from FSMachine import FSMachine, new_state
import sys
import os
import DisplayMachine

os.environ['TCL_LIBRARY'] = 'C:\Python34\\tcl\\tcl8.6'
os.environ['TK_LIBRARY'] = 'C:\Python34\\tcl\\tcl8.6'

print(sys.platform)
# print(os.environ['TCL_LIBRARY'])
# print(os.environ['TK_LIBRARY'])

prior = {'*': 5, '+': 5, '_': 4, '|': 3, '(': 2, ')': 2}

print("input your regular expression:")
sss = str(input())
stack = []
output = ""
for c in sss:
    if c in prior:
        if c == '(':
            stack.append(c)
        elif c == ')':
            k = stack.pop()
            while k != '(':
                output += k
                k = stack.pop()
        else:
            while (len(stack) > 0) and (prior[c] < prior[stack[-1]]):
                output += stack.pop()
            stack.append(c)
            if stack[-1] in ['+', '*']:
                output += stack.pop()
    else:
        output += c
    pass
while len(stack) > 0:
    if stack[-1] == '(' or stack[-1] == ')':
        print("wrong expression")
        quit()
    else:
        output += stack.pop()

print(output)

machines = []
machine_num = 0
print("Enter any key to proceed:")


for c in output:
    if c in prior:
        # проделываем операции с автоматами по верхушке стека
        if c == '|':
            m1 = machines.pop()
            m2 = machines.pop()
            machines.append(m2.addition(m1))
        elif c == '_':
            m1 = machines.pop()
            m2 = machines.pop()
            machines.append(m2.multiplication(m1))
        elif c == '*':
            m1 = machines.pop()
            machines.append(m1.power())
        elif c == '+':
            m1 = machines.pop()
            machines.append(m1.powerplus())
    else:
        m = FSMachine()
        m.from_literal(c)
        machines.append(m)
        # создаем автомат из одного литерала
if len(machines) != 1:
    print("Something wrong with expression")
    input()
    quit()

m1 = machines.pop()

dd = DisplayMachine.DisplayMachine()
dd.display(m1)
# Далле НКА В ДКА
m1 = m1.determinize()

# Далее преобразование ДКА В КА
m1.del_unreachable_det()
dd = DisplayMachine.DisplayMachine()
dd.display(m1)


backrules = {}
for state in m1.states:
    for a in m1.alph:
        k = state, a
        sc = set()
        for r, v in m1.rules.items():
            rk, rl = r
            if v == state and rl == a:
                sc.add(rk)
        if sc == set():
            continue
        if backrules.get((state, a)) is None:
            backrules[(state, a)] = set()
        backrules[(state, a)].update(sc)

L = []
p1 = m1.finalStates.copy()
p2 = m1.states - m1.finalStates


L.append(p1)
L.append(p2)

KL = {}
c1 = c2 = 0


def count_st_per_lit(l, backr, alph):
    count = 0
    for sg in l:
        if backr.get((sg, alph)) is not None:
            count += 1
    return count


for c in m1.alph:
    c1 = count_st_per_lit(L[0], backrules, c)
    c2 = count_st_per_lit(L[1], backrules, c)

    if c1 <= c2:
        KL[c] = set()
        KL[c].add(0)
    else:
        KL[c] = set()
        KL[c].add(1)

K = 2
for a in m1.alph:
    while KL.get(a) is not None and KL.get(a) != set():
        i = KL[a].pop()
        j = 0
        while j < K:
            PJ1 = set()
            for q in L[j]:
                qwer = m1.rules.get((q, a))
                if qwer is not None:
                    if qwer in L[i]:
                        PJ1.add(q)
            if PJ1 != set():
                PJ2 = L[j] - PJ1
                L[j] = PJ1
                L.append(PJ2)
                for c in m1.alph:
                    c1 = count_st_per_lit(L[j], backrules, c)
                    c2 = count_st_per_lit(L[K], backrules, c)
                    if c not in KL:
                            KL[c] = set()
                    if c1 <= c2:
                        KL[c].add(j)
                    else:
                        KL[c].add(K)
                K += 1
            j += 1

# L меноджество классов эквивалентрости
L = [states for states in L if states != set()]
KA = FSMachine()
transtable = {}
KA.alph |= m1.alph
for i in L:
    tt = new_state()
    KA.states.add(tt)
    transtable[tt] = i
    if m1.startstate in i:
        KA.startstate = tt
    if (m1.finalStates & i) != set():
        KA.finalStates.add(tt)
for i in L:
    key = 0
    for qk in transtable:
        if transtable[qk] == i:
            key = qk
            break
    for s in i:
        for a in m1.alph:
            if m1.rules.get((s, a)) is not None:
                key2 = 0
                for qk in transtable:
                    if m1.rules.get((s, a)) in transtable[qk]:
                        key2 = qk
                KA.rules[(key, a)] = key2

dd = DisplayMachine.DisplayMachine()
dd.display(KA)

print("input your expression:")
sss = str(input())
st = set()
st.add(KA.startstate)
for c in sss:
    st = KA.move_det(st, c)
    if st is None:
        print("No!")
        quit()

if (st & KA.finalStates) != set():
    print("Yes!!!")
else:
    print("No!")