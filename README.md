# Capture

Capture stdout and/or stderr conveniently.


## Examples

### Capturing in Python

To capture both outputs:

    >>> import sys
    >>> from capture import capture
    >>> with capture as output:
    ...     print 'Hello world!'
    ...     print >>sys.stdout, 'They see me testing!'
    ...
    >>> print output
    Hello world!
    They see me testing!
    >>> print output.stdout
    Hello world!
    >>> print output.stderr
    They see me testing!

Or if you are only interested in stdout:

    >>> from capture import stdout
    >>> with stdout as output:
    ...     print 'Hello world!'
    ...
    >>> print output
    Hello world!


###  Capturing to a file

You can also capture the output to a file:

    >>> from capture import tee
    >>> with tee('/tmp/output.log'):
    ...     print 'Hello world!'
    ...

Et voila:

    user@shell ~$ cat /tmp/output.log
    Hello world!


## Bugs/Features

You can use the [issue tracker](https://github.com/tehmaze/capture/issues)
at GitHub.
