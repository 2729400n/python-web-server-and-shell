def append(self: tuple, *values):
    backer = list()
    for i in self:
        backer += [i]
        for i in values:
            backer += [i]
    return tuple(backer)


def preppend(self: tuple, *values):
    backer = list()
    for i in values:
        backer += [i]
    for i in self:
        backer += [i]
    return tuple(backer)
