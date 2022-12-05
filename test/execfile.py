# In Python3 the function 'execfile' has been deprecated. The alternative is 'exec'.
# While the package 'past.builtins' provide a python2 / python3 compatible version of 'execfile', 
# the import of 'past.builtins' keeps on throwing a deprecation warning about 'imp'.
# Therefore the version of 'execfile' from 'past/builtins' has been replaced by this alternative
# version, found on: https://stackoverflow.com/a/41658338/2292376

# When support of Python2 is finally dropped, this function can be removed

def execfile(filepath, globals=None, locals=None):
    if globals is None:
        globals = {}
    globals.update({
        "__file__": filepath,
        "__name__": "__main__",
    })
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), globals, locals)