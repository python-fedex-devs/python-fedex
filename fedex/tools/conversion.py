"""Response output conversion tools to help parse suds
response object output.
"""


# This is the suds way of doing this, but its slower.
# For reference only.
# from suds.sudsobject import asdict
# from suds.sax.text import Text
#
# def response_to_dict(obj):
#     """ Converts a suds object to a dictionary.
#     :param obj: object
#     :return: dictionary
#     """
#     out = {}
#     for k, v in asdict(obj).items():  # k = k.lower()
#         if hasattr(v, '__keylist__'):
#             out[k] = response_to_dict(v)
#         elif isinstance(v, list):  # tuple not used
#             out[k] = []
#             for item in v:
#                 if hasattr(item, '__keylist__'):
#                     out[k].append(response_to_dict(item))
#                 else:
#                     out[k].append(
#                         item.title() if isinstance(item, Text) else item)
#         else:
#             out[k] = v.title() if isinstance(v, Text) else v
#     return out


def basic_sobject_to_dict(obj):
    """Converts suds object to dict very quickly.
    Does not serialize date time or normalize key case.
    :param obj: suds object
    :return: dict object
    """
    if not hasattr(obj, '__keylist__'):
        return obj
    data = {}
    fields = obj.__keylist__
    for field in fields:
        val = getattr(obj, field)
        if isinstance(val, list):
            data[field] = []
            for item in val:
                data[field].append(basic_sobject_to_dict(item))
        else:
            data[field] = basic_sobject_to_dict(val)
    return data


def sobject_to_dict(obj, key_to_lower=False, json_serialize=False):
    """
    Converts a suds object to a dict. Includes advanced features.
    :param json_serialize: If set, changes date and time types to iso string.
    :param key_to_lower: If set, changes index key name to lower case.
    :param obj: suds object
    :return: dict object
    """
    import datetime

    if not hasattr(obj, '__keylist__'):
        if json_serialize and isinstance(obj, (datetime.datetime, datetime.time, datetime.date)):
            return obj.isoformat()
        else:
            return obj
    data = {}
    fields = obj.__keylist__
    for field in fields:
        val = getattr(obj, field)
        if key_to_lower:
            field = field.lower()
        if isinstance(val, list):
            data[field] = []
            for item in val:
                data[field].append(sobject_to_dict(item, json_serialize=json_serialize))
        else:
            data[field] = sobject_to_dict(val, json_serialize=json_serialize)
    return data


def sobject_to_json(obj, key_to_lower=False):
    """
    Converts a suds object to a JSON string.
    :param obj: suds object
    :param key_to_lower: If set, changes index key name to lower case.
    :return: json object
    """
    import json
    data = sobject_to_dict(obj, key_to_lower=key_to_lower, json_serialize=True)
    return json.dumps(data)
