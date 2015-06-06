__author__ = 'admin'
from queue import Queue

class Grammar:
    def __init__(self):
        self.n = set()
        self.e = set()
        self.d = set()  # исчезающие нетерминалы
        self.s = ''
        self.p = {}
        pass

    def input_from_lines(self, lines):
        self.n.update(lines[1])
        # добавляем все нетерминалы
        self.e.update(lines[3])
        # добавляем все терминалы
        for i in lines[5:-1]:
            rule = [i[:i.index('->')], tuple(i[i.index('->')+1:])]
            if self.p.get(rule[0][0]) is None:
                self.p[rule[0][0]] = set()
            self.p[rule[0][0]].add(rule[1])
        self.s = lines[-1][0]

    def out_to_lines(self):
        lines = []
        count = 0
        lines.append(str(len(self.n)))
        lines.append(' '.join(self.n))
        lines.append(str(len(self.e)))
        lines.append(' '.join(self.e))
        lines.append(str(0))  # 4
        for key, rules in self.p.items():
            for rule in rules:
                count += 1
                lines.append(key + " -> " + ' '.join(rule))
        lines[4] = str(count)
        lines.append(self.s)
        return lines

    def normalize(self):
        G1 = Grammar()
        G1.e |= self.e
        G1.n = set()
        transtable = {}
        for state in self.n:
            t = ''
            for st in state:
                t += st
            transtable[state] = t
            G1.n.add(t)
        G1.s = transtable[self.s]
        for rr, rls in self.p.items():
            G1.p[transtable[rr]] = set()
            for rl in rls:
                trl = tuple()
                for lit in rl:
                    if lit in self.n:
                        trl += (transtable[lit],)
                    else:
                        trl += (lit,)
                G1.p[transtable[rr]].add(trl)
        return G1

    def a_in_b(self, a, b):
        arg = False
        for i in range(len(b)-len(a)+1):
            k = b[i:i+len(a)]
            if a == k:
                arg = True
                break
        return arg and self.wo_term(a) and self.wo_term(b)

    def wo_term(self, a):
        t1 = set(a)
        t1 -= self.e
        return len(t1) == len(a)

    def shrink(self, a):
        t1 = [la for la in a if la != '~']
        if len(t1) == 0:
            t1.append('~')
        return tuple(t1)

    def reachable(self, start, finish):
        result = False
        output = set()
        output.add(finish)
        while not result and len(output) > 0:
            if start not in output:
                st = output.pop()
                for rl, rr in self.p.items():
                    for rri in rr:
                        if self.a_in_b(st, rri):
                            output.add((rl,))
            else:
                result = True
        return result

    def reachable_2(self, start, finish):
        result = False
        if start != finish:
            if len(self.e & set(start)) > len(self.e & set(finish)):
                return False
            t1 = list(start)
            t2 = list(finish)
            for i in range(len(t2)):
                if t1[i] in self.e and t2[i] in self.e:
                    if t1[i] != t2[i]:
                        return False
                    else:
                        result = True
                elif t1[i] in self.n and t2[i] in self.n:
                    if t1[i] != t2[i]:
                        ptemp = self.p.get(t1[i], [])
                        for v in ptemp:
                            temp = tuple()
                            for st in start:
                                if st != t1[i]:
                                    temp += (st,)
                                else:
                                    temp += v
                            if self.reachable_2(self.shrink(temp), finish):
                                return True
                            result = False
                    else:
                        result = True
                elif t1[i] in self.n and t2[i] in self.e:
                    ptemp = self.p.get(t1[i], [])
                    for v in ptemp:
                        temp = tuple()
                        for st in start:
                            if st != t1[i]:
                                temp += (st,)
                            else:
                                temp += v
                        if self.reachable_2(self.shrink(temp), finish):
                            return True
                        result = False

                elif t1[i] in self.e and t2[i] in self.n:
                    return False
        else:
            result = True
        return result

    def disapearing(self):
        result = set()
        for non in self.n:
            if self.reachable_2((non,), ('~',)):
                result.add(non)
        self.d = result
        return result

    def alg_81(self):
        G1 = Grammar()
        G1.n.update(self.n)
        N = self.disapearing()
        G1.d |= self.d
        G1.n.update(set(disp+'\"' for disp in N))
        G1.e |= self.e
        G1.s = self.s
        if self.s in N:
            G1.s = self.s + '\"'
            G1.n.add(self.s + '\"')
        sc = -1
        for rl, rr in self.p.items():
            if G1.p.get(rl) is None:
                G1.p[rl] = set()
                G1.p[rl+'\"'] = set()
            for rri in rr:
                if rri != ('~',):
                    for nd in rri:
                        if nd not in N:
                            sc = rri.index(nd)
                            break
                        else:
                            sc = len(rri)
                    for sci in range(sc):
                        trr = (rri[sci]+'\"',)+rri[sci+1:]
                        G1.n.add(rri[sci]+'\"')
                        G1.p[rl].add(trr)
                        if rl in N:
                            G1.p[rl+'\"'].add(trr)
                    if sc < len(rri):
                        G1.p[rl].add(rri[sc:])
                        if rl in N:
                            G1.p[rl+'\"'].add(rri[sc:])
                else:
                    G1.p[rl].add(rri)
        G1.p = {key: val for key, val in G1.p.items() if val != set()}
        return G1

    def g(self, stack, value):
        # VALUE ЭТО ЦЕПОЧКА
        # ТУТ ПРОВЕРЯЕМ УСЛОВИЯ ПРИНАДЛЕЖНОСТИ К N
        if value[0] not in self.d:
            t = set(value[1:])
            if len(t) == len(value)-1:
                stack.add(value)
                return True
        return False

    def g_minus(self, value, stack, g):
        if value == tuple():
            return value
        if value[0] in self.d:
            return tuple()
        t = set(value[1:])
        if len(t) != len(value)-1:
            return tuple()
        if value not in g.n:
            stack.add(value)
            g.n.add(value)
        return value

    def tpl_rplc(self,sub_tuple, in_tuple, on_element):
        res = tuple()
        switch = True
        for t in in_tuple:
            if t != on_element:
                res += (t,)
            else:
                if switch:
                    res += sub_tuple
                    switch = False
        return self.shrink(res)

    def alg_82(self):
        G2 = Grammar()
        stack = set()
        self.g_minus((self.s,), stack, G2)
        G2.s = (self.s,)
        G2.e = self.e.copy()
        while len(stack) > 0:
            state = stack.pop()
            if state not in G2.p:
                G2.p[state] = set()
            if state[0] in self.n:
                # ПУНКТ i ШАГА 3В АЛГ 8.2
                for rr in self.p.get(state[0], set()):
                    temp = self.g_minus(self.tpl_rplc(rr, state, state[0]),stack,G2)
                    if temp != tuple():
                        G2.p[state].add((temp,))
            else:
                # ПУНКТЫ ii, iii ШАГА 3В АЛГ 8.2
                if len(state) > 1:
                    for s in state[1:]:
                        if s in self.n:
                            ind = state.index(s)
                            for rr in self.p.get(s, set()):
                                if rr != ('~',):
                                    temp = self.g_minus(self.tpl_rplc(rr, state[ind:], s),
                                                        stack,
                                                        G2)
                                    if temp!= tuple():
                                        G2.p[state].add((state[0],temp))
                                    else:
                                        G2.p[state].add((state[0],))
                G2.p[state].add((state[0],))
        return G2

    def alg_83(self):
        G1 = Grammar()
        G1.e |= self.e
        G1.s = self.s

        transtable = {}
        counter = 1
        transtable[counter] = self.s
        stack = Queue()
        stack.put(self.s)
        G1.n.add(self.s)
        while stack.qsize() > 0:
            state = stack.get()
            for rule in self.p.get(state,set()):
                lit = rule[0]
                if lit in self.n and lit not in G1.n:
                    counter += 1
                    transtable[counter] = lit
                    stack.put(lit)
                    G1.n.add(lit)
        added = {lit for lit in transtable.values()}
        for nd in self.n:
            if nd not in added:
                counter += 1
                transtable[counter] = nd
                G1.n.add(nd)

        for i in reversed(range(1,counter+1)):
            state = transtable[i]
            if state not in G1.p:
                G1.p[state] = set()
            for rule in self.p.get(state,set()):
                if rule[0] in self.n:
                    for rule2 in G1.p.get(rule[0],set()):
                        G1.p[state].add(self.tpl_rplc(rule2,rule,rule[0]))
                else:
                    G1.p[state].add(rule)
        G1.n |= set('X'+lit for lit in self.e)
        temprules = G1.p.copy()
        G1.p.clear()
        for lit in self.e:
            G1.p['X'+lit] = (lit,)
        for key, rules in temprules.items():
            G1.p[key] = set()
            for rule in rules:
                tprl = rule
                if rule[0] in self.e:
                    for lit in rule[1:]:
                        if lit in self.e:
                            tprl = (tprl[0],) + self.tpl_rplc(('X'+lit,),tprl[1:],lit)
                    G1.p[key].add(tprl)
        return G1
