
def distinct(iterable, keyfunc=None):
    seen = set()
    for item in iterable:
        key = item if keyfunc is None else keyfunc(item)
        if key not in seen:
            seen.add(key)
            yield item