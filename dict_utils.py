def get_nested_attr(data, keys, default=None, raise_error=False, error_msg=None):
    """
    Retrieve nested attributes from a class object or dictionary.

    Args:
        data: The class object or dictionary from which to retrieve the nested attribute.
        keys: A list of strings representing the nested attribute path.
              Each string corresponds to an attribute name or key in the nested structure.
              Alternatively, if the attribute keys themselves are nested, you can provide
              a list of lists, where each inner list represents a nested path.
        default: The value to return if the item is not found (default is None).
        raise_error (bool): Whether to raise an exception if the item is not found (default is False).
        error_msg (str): The custom error message to raise if an exception is raised.

    Returns:
        The value of the nested attribute if found, otherwise the default value or None if not found,
        depending on the value of the raise_error argument.

    Example:
        >>> data = {'a': {'b': {'c': 123}}}
        >>> _get_nested_attr(data, ['a']) # {'b': {'c': 123}}
        >>> _get_nested_attr(data, ['a', 'b', 'c']) # 123

    Example:
        # Define classes
        class Address:
            def __init__(self, city, some_dict):
                self.city = city
                self.some_dict = some_dict

        class Employee:
            def __init__(self, designation, address):
                self.designation = designation
                self.address = address

        # Create objects
        address = Address(city="New York", some_dict={'a': {'b': {'c': 123}}})
        employee = Employee(designation='developer', address=address)

        # Get nested property
        city = get_nested_attr(employee, ['address', 'city'])
        print(city)  # Output: New York

        address_only = get_nested_attr(employee, 'address')
        print(address_only)  # Output: <__main__.Address>

        some_nested_data = get_nested_attr(employee, [['address', 'some_dict'], ['a', 'b', 'c']])
        print(some_nested_data) # Output: 123

        some_nested_data1 = get_nested_attr(employee, ['address', 'some_dict', 'a', 'b', 'c'])
        print(some_nested_data1) # Output: 123
    """

    # if data is None: return default

    # if data is None: return default

    if isinstance(keys, str):
        keys = [keys]

    def _get_value(data, keys):
        for key in keys:
            if isinstance(data, dict):
                if key in data:
                    data = data[key]
                else:
                    if raise_error:
                        if error_msg:
                            raise KeyError(error_msg)
                        else:
                            raise KeyError(f"Key '{key}' not found in the nested structure.")
                    else:
                        return default  # Return default value if key not found
            else:
                if hasattr(data, key):
                    data = getattr(data, key)
                else:
                    if raise_error:
                        if error_msg:
                            raise AttributeError(error_msg)
                        else:
                            raise AttributeError(f"Attribute '{key}' not found in the object.")
                    else:
                        return default  # Return default value if attribute not found
        return data

    if isinstance(keys[0], list):  # If keys themselves are nested
        for nested_keys in keys:
            result = _get_value(data, nested_keys)
            if result is not None:
                return result
        return default if not raise_error else None
    else:
        return _get_value(data, keys)
