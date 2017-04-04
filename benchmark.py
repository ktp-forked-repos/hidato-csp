from timeit import default_timer as timer

class benchmark(object):

    def __init__(self, fmt="%0.3g"):
        self.fmt = fmt

    def __enter__(self):
        self.start = timer()
        return self

    def __exit__(self, *args):
        t = timer() - self.start
        self.time = t
