from functools import partial
import StringIO
import os
import sys


DEVNULL = open(os.devnull, 'w')


class Record(object):
    def __init__(self, *fds):
        self.dupe = StringIO.StringIO()
        self.them = fds

        self.fileno     = partial(self._dupe, 'fileno')
        self.flush      = partial(self._both, 'flush')
        self.isatty     = partial(self._them, 'isatty')
        self.name       = partial(self._them, 'name')
        self.write      = partial(self._both, 'write')
        self.writelines = partial(self._both, 'writelines')

    def __str__(self):
        return self.getvalue()

    def _both(self, operation, *args, **kwargs):
        self._dupe(operation, *args, **kwargs)
        self._them(operation, *args, **kwargs)

    def _dupe(self, operation, *args, **kwargs):
        getattr(self.dupe, operation)(*args, **kwargs)

    def _them(self, operation, *args, **kwargs):
        for fd in self.them:
            getattr(fd, operation)(*args, **kwargs)

    def getvalue(self):
        return self.dupe.getvalue()


class Recorder(object):
    def __init__(self, merged=False, *fds):
        self.fds = list(fds)
        self.output = {}
        self.merged = StringIO.StringIO() if merged else None

    def add(self, name):
        out = getattr(sys, name)
        if self.merged:
            fds = self.fds + [out, self.merged]
        else:
            fds = self.fds + [out]

        # Store original file descriptor
        self.output[name] = (out, Record(*fds))

        # Proxy original file descriptor
        setattr(sys, name, self.output[name][1])

        # Inject convenience method
        setattr(self, name, self.output[name][1])

    def restore(self):
        # Restore original file descriptors
        for name in self.output:
            setattr(sys, name, self.output[name][0])

    def __str__(self):
        if self.merged:
            return self.merged.getvalue()

        elif hasattr(self, 'stdout'):
            return self.stdout.getvalue()

        elif hasattr(self, 'stderr'):
            return self.stderr.getvalue()

        else:
            raise ValueError('Recorder inactive')


class Proxy(object):
    def __init__(self, stdout, stderr, merged, *fds):
        self.proxy_stdout = bool(stdout)
        self.proxy_stderr = bool(stderr)
        self.proxy_merged = bool(merged)
        self.fds = fds

    def __enter__(self):
        self.recorder = Recorder(self.proxy_merged, *self.fds)

        if self.proxy_stdout:
            self.recorder.add('stdout')
        if self.proxy_stderr:
            self.recorder.add('stderr')

        return self.recorder

    def __exit__(self, *args, **kwargs):
        self.recorder.restore()


capture = Proxy(1, 1, 1)
stdout  = Proxy(1, 0, 0)
stderr  = Proxy(0, 1, 0)


def tee(filename, stdout=True, stderr=True, append=False):
    if append:
        fd = open(filename, 'a')
    else:
        fd = open(filename, 'w')

    return Proxy(stdout, stderr, 1, fd)
