# -*- coding: utf-8 -*-

import optimization
import sys

def test_printschedule(s):
    sys.stderr.write("testing printschedule...\n")
    optimization.printschedule(s)

def test_schedulecost(s):
    sys.stderr.write("testing schedulecost...\n")
    print optimization.schedulecost(s)
    sys.stderr.write("??? expecting 5285 according to textbook???...\n")

def test_randomoptimize(domain):
    sys.stderr.write("testing random optimization...\n")
    s = optimization.randomoptimize(domain, optimization.schedulecost)
    print optimization.schedulecost(s)
    optimization.printschedule(s)

def test_hillclimb(domain):
    sys.stderr.write("testing hillclimb optimization...\n")
    s = optimization.hillclimb(domain, optimization.schedulecost)
    print optimization.schedulecost(s)
    optimization.printschedule(s)

def test_annealing(domain):
    sys.stderr.write("testing annealing optimization...\n")
    s = optimization.annealingoptimize(domain, optimization.schedulecost)
    print optimization.schedulecost(s)
    optimization.printschedule(s)

def test_genetic(domain):
    sys.stderr.write("testing genetic optimization...\n")
    s = optimization.geneticoptimize(domain, optimization.schedulecost)
    optimization.printschedule(s)

def main():
    s=[4,4,4,2,2,6,6,5,5,6,6,0]
    test_printschedule(s)
    test_schedulecost(s)
    # test optimization
    domain=[(0,8)] * (len(optimization.people)*2)
    test_randomoptimize(domain)
    test_hillclimb(domain)
    test_annealing(domain)
    test_genetic(domain)
    return

if __name__ == '__main__':
    main()
