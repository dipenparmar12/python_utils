def flatten(data, prefix=''):
    """
    Flattens a nested dictionary into a single-level dictionary with dot-separated keys for dictionaries and index-based keys for lists.

    Parameters:
    - data (dict): The nested dictionary to be flattened.
    - prefix (str, optional): A string to prepend to the keys. Defaults to ''.

    Returns:
    dict: A flattened dictionary where nested dictionaries are represented with dot-separated keys and lists are indexed.

    Example:
    >>> nested_obj = {
   ...     'a': 1,
   ...     'b': {
   ...         'c': 2,
   ...         'd': [3, 4],
   ...         'e': {
   ...             'f': 5,
   ...             'g': [6, 7]
   ...         }
   ...     }
   ... }
   ...
    >>> flattened_obj = flatten(nested_obj)
    >>> print(flattened_obj)
    {'a': 1, 'b.c': 2, 'b.d[0]': 3, 'b.d[1]': 4, 'b.e.f': 5, 'b.e.g[0]': 6, 'b.e.g[1]': 7}
    """

    result = {}
    for key, value in data.items():
        prop = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            result.update(flatten(value, prop))
        elif isinstance(value, list):
            for i, item in enumerate(value):
                array_prop = f"{prop}[{i}]"
                if isinstance(item, (dict, list)):
                    result.update(flatten(item, array_prop))
                else:
                    result[array_prop] = item
            if not value:  # Handle empty lists
                result[prop] = []
        else:
            result[prop] = value
            
    return result
