def get_first_item(lst, default=None):
    return next(iter(lst), default) if lst is not None else default
