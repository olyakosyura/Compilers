__author__ = 'admin'
import copy
from copy import deepcopy, copy


class Grammar:
    def __init__(self):
        self.n = set()
        self.e = set()
        self.d = set()

        self.s = ''
        self.p = {}
        self.T = []
        self.np = {}

    def input_from_lines(self, lines):
        self.n.update(lines[1])

        self.e.update(lines[3])

        for i in lines[5:-1]:
            rule = [i[:i.index('->')], tuple(i[i.index('->') + 1:])]
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

    def tpl_rplc(self, sub_tuple, in_tuple, on_element):
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

    def shrink(self, a):
        t1 = [la for la in a if la != '~']
        if len(t1) == 0:
            t1.append('~')
        return tuple(t1)

    def long_rules_del(self):
        g1 = Grammar()
        g1.n = self.n
        g1.e = self.e
        g1.s = self.s
        for rr in self.p:
            rulestodel = []
            g1.p[rr] = set()
            for rule in self.p[rr]:
                if len(rule) > 2:
                    for i in range(len(rule) - 2):
                        t = rule[i + 1:]
                        g1.n.add(''.join(t))
                        if i == 0:
                            g1.p[rr].add((rule[i], ''.join(t)))
                        if ''.join(t) not in g1.p.keys():
                            g1.p[''.join(t)] = set()
                        g1.p[''.join(t)].add((rule[i + 1], ''.join(t[1:])))
                    rulestodel.append(rule)
                else:
                    g1.p[rr].add(rule)
            for rule in rulestodel:
                self.p[rr].discard(rule)
        return g1

    def zero_nonterm(self):
        res = set()
        for rr, rl in self.p.items():
            if ('~',) in rl:
                res.add(rr)
        last_len = len(res) - 1
        if last_len >= 0:
            while last_len != len(res):
                last_len = len(res)
                for rr, rlist in self.p.items():
                    for rl in rlist:
                        diff = set(rl) - res
                        if len(diff) == 0:
                            res.add(rr)
        return res

    def zero_rules_del(self):
        g1 = Grammar()
        g1.n = self.n
        g1.e = self.e
        g1.p = deepcopy(self.p)
        g1.s = self.s
        zt = self.zero_nonterm()
        for rr, rlist in self.p.items():
            for rule in rlist:
                if len(set(rule) - zt) > 0:
                    g1.brute((rr, rule), 0, zt)

        p = deepcopy(g1.p)
        for rr, rlist in p.items():
            for rule in rlist:
                if rule == ('~',):
                    g1.p[rr].discard(rule)
        return g1

    def brute(self, rule, k, zr):
        s = rule[0]
        a = rule[1]
        ii = k
        if k < len(a):
            if a[ii] in zr:
                if a[ii] not in self.p.keys():
                    self.p[s] = set()

                t = a[0:ii] + a[ii + 1:]
                self.p[s].add(t)
                self.brute((s, t), k, zr)
            self.brute(rule, k + 1, zr)

    def unit_pair_del(self):
        unit_pair = set()
        for lit in self.n:
            unit_pair.add((lit, lit))
        lu = len(unit_pair) - 1
        while lu != len(unit_pair):
            lu = len(unit_pair)
            for pair in unit_pair.copy():
                for p in self.p.get(pair[1], set()):
                    if len(p) == 1 and p[0] in self.n:
                        unit_pair.add((pair[0], p[0]))
        for pair in unit_pair:
            for rl in self.p.get(pair[1], set()):
                if pair[0] not in self.p.keys():
                    self.p[pair[0]] = set()
                self.p[pair[0]].add(rl)
        for pair in unit_pair:
            self.p[pair[0]].discard((pair[1],))

    def useless_n_del(self):
        usefull = set()
        ll = -1
        while ll != len(usefull):
            ll = len(usefull)
            for rr, rl in self.p.items():
                for rule in rl:
                    if len(set(rule) - usefull - self.e) == 0:
                        usefull.add(rr)
        reashable = set(self.s)
        ll = -1
        while ll != len(reashable):
            ll = len(reashable)
            for rr, rl in self.p.items():
                for rule in rl:
                    if len(set(rule) - reashable - self.e) > 0:
                        reashable.update(set(rule) - reashable - self.e)

        for rr, rl in self.p.copy().items():
            for rule in rl.copy():
                if len(set(rule) - usefull - self.e) > 0:
                    self.p[rr].discard(rule)

        for rr, rl in self.p.copy().items():
            for rule in rl.copy():
                if len(set(rule) - reashable - self.e) > 0:
                    self.p[rr].discard(rule)
        pass

    def double_n(self):
        g1 = Grammar()
        g1.s = self.s
        g1.e = self.e
        g1.n = self.n
        g1.p = deepcopy(self.p)
        for rr, rl in self.p.items():
            for rule in rl:
                trule = rule
                if len(rule) > 1:
                    if rule[0] in self.e:
                        g1.n.add(rule[0] + '\'')
                        if g1.p.get(rule[0] + '\'') is None:
                            g1.p[rule[0] + '\''] = set()
                        g1.p[rule[0] + '\''].add((rule[0],))
                        trule = (rule[0] + '\'', trule[1])

                    if rule[1] in self.e:
                        g1.n.add(rule[1] + '\'')
                        if g1.p.get(rule[1] + '\'') is None:
                            g1.p[rule[1] + '\''] = set()
                        g1.p[rule[1] + '\''] = {(rule[1],)}
                        trule = (trule[0], rule[1] + '\'')
                    if trule != rule:
                        g1.p[rr].add(trule)
                        g1.p[rr].discard(rule)
        return g1

    def homsky_form(self):
        G3 = self.long_rules_del()
        G3 = G3.zero_rules_del()
        G3.unit_pair_del()
        G3.useless_n_del()
        G3 = G3.double_n()
        return G3

    def CYK(self, n):

        T = []
        i = 0
        for p in range(len(n) + 1):
            T.append(list())
            i += 1
            for v in range(len(n) + 1):
                T[i - 1].append(set())
        for p in range(1, len(n) + 1):
            self.fill_diagonal(p, T, n)
        self.T = deepcopy(T)
        if self.s in T[len(n)][1]:
            return True
        return False

    def fill_diagonal(self, p, T, n):
        for k in range(1, p + 1):
            self.fill_element(T, n, k, p - k + 1)

    def fill_element(self, T, n, i, j):
        if i == 1:
            for rr, rl in self.p.items():
                for rule in rl:
                    if rule == (n[j - 1],):
                        T[i][j].add(rr)
        else:
            for k in range(1, i):
                for B in T[i - k][j]:
                    for C in T[k][j + i - k]:
                        t = (B, C)
                        for rr, rl in self.p.items():
                            for rule in rl:
                                if rule == t:
                                    T[i][j].add(rr)
        pass


    def left_output(self, a):
        count = 0
        for rr, rl in self.p.items():
            for rule in rl:
                self.np[(rr,) + rule] = count
                count += 1
        s = self.gen(a,  len(a), 1, self.s)
        return s

    def gen(self, a, i, j, s):
        if i == 1 and s in self.T[i][j]:
            return (self.np[(s, a[j - 1])],)
        else:
            k, B, C, put = self.Min(i, j, s)
            return (put,) + self.gen(a, i - k, j, B) + self.gen(a, k, j + i - k, C)


    def Min(self, i, j, a):
        for k in range(1, i):
            for B in self.T[i - k][j]:
                for C in self.T[k][j + i - k]:
                    if (B, C) in self.p.get(a):
                        return (k, B, C, self.np[(a, B, C)])