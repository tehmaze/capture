from distutils.core import setup, Extension

setup(
    name         = 'capture',
    version      = '0.1',
    author       = 'Wijnand Modderman',
    author_email = 'maze@pyth0n.org',
    description  = 'Capture stdout and/or stderr',
    license      = 'MIT',
    keywords     = 'capture stdout stderr write read',
    packages     = [
        'capture',
    ],
)

