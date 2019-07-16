def split_list(l, n):
    for idx in range(0, len(l), n):
        yield l[idx:idx + n]
