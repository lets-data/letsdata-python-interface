def letsdata_assert(result : bool, message : str):
    if not result:
        raise(Exception("letsdata assert - "+message))
    else:
        pass