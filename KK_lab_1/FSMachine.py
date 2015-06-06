__author__ = 'Roman'
import uuid


class State_____Node():
    def __init__(self):
        self.stateid = uuid.uuid4()
        self.caption = str(self.stateid)
        self.marked = False

def new_state():
    return uuid.uuid4()

class FSMachine():
    def __init__(self):
        self.states = set()
        self.finalStates = set()
        self.rules = {}
        self.alph = set()
        self.startstate = new_state()

    def from_literal(self, c):
        tt1 = new_state()
        self.states.add(tt1)
        tt2 = new_state()
        self.states.add(tt2)
        self.finalStates.add(tt2)
        self.startstate = tt1
        self.rules[(tt1, c)] = set()
        self.rules[(tt1, c)].add(tt2)
        self.alph.add(c)

    def addition(self, m):
        t = FSMachine()
        t.alph |= self.alph
        t.alph |= m.alph

        t.states |= self.states
        t.states |= m.states

        tt0 = new_state()
        t.states.add(tt0)
        t.startstate = tt0

        for k, v in self.rules.items():
            if k not in t.rules:
                t.rules[k] = set()
            t.rules[k] |= v
        for k, v in m.rules.items():
            if k not in t.rules:
                t.rules[k] = set()
            t.rules[k] |= v

        for c in t.alph:
            if (tt0,c) not in t.rules:
                t.rules[(tt0,c)] = set()
            t.rules[(tt0,c)] |= self.rules.get((self.startstate,c),set())
            t.rules[(tt0,c)] |= (m.rules.get((m.startstate,c),set()))

        t.finalStates.update(self.finalStates)
        t.finalStates.update(m.finalStates)

        if (self.startstate in self.finalStates)and(m.startstate in m.finalStates):
            t.finalStates.add(tt0)
        return t

    def multiplication(self, m):
        t = FSMachine()
        t.alph |= self.alph
        t.alph |= m.alph

        t.startstate = self.startstate

        t.states |= self.states
        t.states |= m.states

        for k, v in m.rules.items():
            if k in t.rules.keys():
                t.rules[k].update(v)
            else:
                t.rules[k] = v

        for kstat in t.states:
            for klit in t.alph:
                k = kstat, klit
                v = self.rules.get(k,set())
                if k in t.rules.keys():
                    t.rules[k].update(v)
                else:
                    t.rules[k] = v
                if kstat in self.finalStates:
                    t.rules[k].update(m.rules.get((m.startstate, klit),set()))

        if m.startstate in m.finalStates:
            t.finalStates |= self.finalStates
        t.finalStates |= m.finalStates
        return t

    def power(self):
        t = FSMachine()
        t.alph |= self.alph

        t.states |= self.states
        tt0 = new_state()
        t.states.add(tt0)
        t.startstate = tt0

        t.finalStates |= self.finalStates
        t.finalStates.add(tt0)

        for c in self.alph:
            t.rules[(tt0,c)] = self.rules[(self.startstate,c)]

        for kstat in self.states:
            for klit in self.alph:
                k = kstat, klit
                v = self.rules.get(k,set())
                if k in t.rules.keys():
                    t.rules[k].update(v)
                else:
                    t.rules[k] = v

                if kstat in self.finalStates :
                    tempt = self.rules.get((self.startstate,klit),set())
                    t.rules[k].update(tempt)

        return t

    def powerplus(self):
        t = FSMachine()
        t.alph |= self.alph

        t.states |= self.states
        t.startstate = self.startstate
        t.finalStates |= self.finalStates

        for kstat in self.states:
            for klit in self.alph:
                k = kstat, klit
                v = self.rules.get(k,set())
                if k in t.rules.keys():
                    t.rules[k].update(v)
                else:
                    t.rules[k] = v
                if kstat in self.finalStates :
                    t.rules[k].update(self.rules.get((self.startstate,klit),set()))
        return t

    def null_closure_state(self,st):
        result = set()
        temp = self.rules.get((st,''))
        if temp is not None:
            result.add(temp)
        result.add(st)
        return result

    def null_closure_set(self,sts):
        results = None
        stack = []
        if sts is not None:
            results = set()
            results.update(sts)
            stack = sts.copy()
        while len(stack)>0:
            t = stack.pop()
            temp = self.rules.get((t,''))
            if temp is not None:
                for s in temp:
                    if s not in results:
                        results.add(s)
                        stack.append(s)
        return results

    def move(self, sts, a):
        result = None
        for s in sts:
            temp = self.rules.get((s,a))
            if temp is not None:
                if result is None:
                    result = set()
                result.update(temp)
        return result

    def move_det(self, sts, a):
        result = None
        for s in sts:
            temp = self.rules.get((s,a))
            if temp is not None:
                if result is None:
                    result = set()
                result.add(temp)
        return result

    def determinize(self):
        tm = FSMachine()
        tm.alph |= self.alph

        Dstates = []
        Dtran = {}
        transtable = {}
        notmarked = []
        t = self.null_closure_state(self.startstate)
        Dstates.append(t)
        notmarked.append(t)
        while len(notmarked)>0:
            tt = notmarked.pop()
            temp = new_state()
            transtable[temp]=tt
            for a in self.alph:
                U = self.null_closure_set(self.move(tt,a))
                if U is not None:
                    if U not in Dstates:
                        Dstates.append(U)
                        notmarked.append(U)
                    Dtran[(temp, a)] = U

        for TT in Dstates:
            dk = None
            dv = None
            for k, v in transtable.items():
                if v == TT:
                    dk = k

            tm.states.add(dk)
            if self.startstate in TT:
                tm.startstate = dk

            for a in self.alph:
                U = Dtran.get((dk,a))
                if U is not None:
                    tk = None
                    for k, v in transtable.items():
                        if v == U:
                            tk = k
                    if tk is not None:
                        tm.rules[(dk,a)]=tk
            for sss in self.finalStates:
                if sss in TT:
                    tm.finalStates.add(dk)
        return tm

    def del_unreachable_det(self):
        qv = self.startstate
        # m1.states[qk] = qv
        L = set()

        L.add(qv)

        marked = {k: False for k in self.states}

        while len(L) > 0:
            qv = L.pop()
            marked[qv] = True
            for r in self.rules:
                if not marked[self.rules[r]]:
                    L.add(self.rules[r])

        # удалить непомеченные правила и состояния
        tempstates = self.states.copy()
        for sc in tempstates:
            if not marked[sc]:
                for c in self.alph:
                    if self.rules.get((sc, c)) is not None:
                        del self.rules[(sc, c)]
                self.states.remove(sc)


