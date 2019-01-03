def calc_result(inst):
    inst.f = 0
    dd = int(inst.d * inst.h)
    t = inst.r
    for j in inst.jobs:
        t += j.p
        if t < dd:
            inst.f += (dd - t) * j.a
        elif t > dd:
            inst.f += (t - dd) * j.b
    inst.f = int(inst.f)