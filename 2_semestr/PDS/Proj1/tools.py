import sys

def err_print(*args, **kwargs):
    """
    method for printing to stderr
    """
    print(*args, file=sys.stderr, **kwargs)


def get_pipe_name(type_, id_):
    """
    return path for named pipe
    """
    return "/tmp/pds_"+type_+"_"+str(id_)
