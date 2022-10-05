#!/usr/bin/env python3

from myhdl import *

from hw.components import mux2way


@block
def ram(dout, din, addr, we, clk, rst, width, depth):
    loads = [Signal(bool(0)) for i in range(depth)]
    outputs = [Signal(modbv(0)[width:]) for i in range(depth)]
    registersList = [None for i in range(depth)]

    @always_comb
    def comb():
        pass

    return instances()


@block
def pc(increment, load, i, output, width, clk, rst):
    regIn = Signal(modbv(0)[width:])
    regOut = Signal(modbv(0)[width:])
    regLoad = Signal(bool(0))

    @always_comb
    def comb():
        pass

    return instances()


@block
def registerN(i, load, output, width, clk, rst):
    binaryDigitList = [None for n in range(width)]
    outputs = [Signal(bool(0)) for n in range(width)]

    @always_comb
    def comb():
        pass

    return instances()


@block
def register8(i, load, output, clk, rst):
    binaryDigitList = [None for n in range(8)]
    output_n = [Signal(bool(0)) for n in range(8)]

    for k in range(8):
        binaryDigitList[k] = binaryDigit(i(k), load, output_n[k], clk, rst)

    @always_comb
    def comb():
        for i in range(8):
            output.next[i] = output_n[i]
    return instances()


@block
def binaryDigit(i, load, output, clk, rst):
    q, d, clear, presset = [Signal(bool(0)) for i in range(4)]
    mux = mux2way(d,q,i,load)
    fl1pfl0p = dff(q,d,clear,presset,clk,rst)
    @always_comb
    def comb():
        output.next = q

    return instances()

@block
def dff(q, d, clear, presset, clk, rst):
    @always_seq(clk.posedge, reset=rst)
    def logic():
        if clear:
            q.next = 0
        elif presset:
            q.next = 1
        else:
            q.next = d

    return instances()