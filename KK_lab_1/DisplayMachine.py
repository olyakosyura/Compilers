__author__ = 'admin'
from FSMachine import *
from tkinter import *
import math


class DisplayMachine():
    def __init__(self):
        self.m = FSMachine()
        self.stateR = 100
        self.stateRmin = 7
        self.root = Tk()
        self.widx = {}

    def display(self, m1):
        dA = 360.0/(len(m1.states))
        cA = 0
        R = self.stateR
        Rmin = self.stateRmin

        w = Canvas(self.root, height=500, width=500)
        for s in m1.states:
            x0 = 250
            y0 = 250
            x1 = x0 - math.cos((cA/180.0)*math.pi)*R
            y1 = y0 - math.sin((cA/180.0)*math.pi)*R
            if s == m1.startstate:
                self.widx[s] = w.create_oval(x1-Rmin, y1-Rmin, x1+Rmin, y1+Rmin, width=2, outline="red", fill="#999999")
            else:
                self.widx[s] = w.create_oval(x1-Rmin, y1-Rmin, x1+Rmin, y1+Rmin, width=2, fill="#999999")
            if s in m1.finalStates:
                t = Rmin+3
                self.widx[s] = w.create_oval(x1-t, y1-t, x1+t, y1+t, width=1)
            cA += dA
        for k, v in m1.rules.items():
            kstate, klit = k
            vv = set()
            if type(vv) == type(v):
                vv = v
            else:
                vv.add(v)
            for s in vv:
                c1 = w.coords(self.widx[kstate])
                c2 = w.coords(self.widx[s])
                if c1[0] == c2[0] and c1[1] == c2[1]:
                    w.create_oval(c1[0]-Rmin,
                                  c1[1]-Rmin,
                                  c1[0]+Rmin,
                                  c1[1]+Rmin, width=1)
                else:
                    w.create_line(c1[0]+Rmin,
                                  c1[1]+Rmin,
                                  c2[0]+Rmin,
                                  c2[1]+Rmin,
                                  width=2, fill="#567889")
                    c2[0] = c2[0] - c1[0]
                    c2[1] = c2[1] - c1[1]
                    c2[0] /= 2.0
                    c2[1] /= 2.0

                    c2[0] = c2[0] + c1[0] + Rmin
                    c2[1] = c2[1] + c1[1] + Rmin

                    w.create_line(c2[0],
                                  c2[1],
                                  c1[0]+Rmin,
                                  c1[1]+Rmin,
                                  width=2, fill="cyan")
                w.create_text(c2[0],
                              c2[1]-Rmin, text=klit)
        w.pack(fill=BOTH)
        self.root.mainloop()
    pass


