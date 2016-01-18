"""Response output conversion tools to help parse suds
response object output.
"""
from suds.sudsobject import asdict
from suds.sax.text import Text


def object_to_dict(obj):
    """ Converts a suds object to a dictionary.
    :param o: object
    :return: dictionary
    """
    out = {}
    for k, v in asdict(obj).items():
        k = k.lower()
        if hasattr(v, '__keylist__'):
            out[k] = object_to_dict(v)
        elif isinstance(v, list):
            out[k] = []
            for item in v:
                if hasattr(item, '__keylist__'):
                    out[k].append(object_to_dict(item))
                else:
                    out[k].append(
                        item.title() if isinstance(item, Text) else item)
        else:
            out[k] = v.title() if isinstance(v, Text) else v
    return out
#
# import datetime
#
# def object_to_dict(obj):
#     """ Converts an object to a dictionary.
#     :param o: object
#     :return: dictionary
#     """
#     if isinstance(obj, (str, unicode, bool, int, long, float, datetime.datetime, datetime.date, datetime.time)):
#         return obj
#     data_dict = {}
#     try:
#         all_keys = obj.__dict__.keys()  # vars(obj).keys()
#     except AttributeError:
#         return obj
#     fields = [k for k in all_keys if not k.startswith('_')]
#     for field in fields:
#         val = getattr(obj, field)
#         if isinstance(val, (list, tuple)):
#             data_dict[field] = []
#             for item in val:
#                 data_dict[field].append(object_to_dict(item))
#         else:
#             data_dict[field] = object_to_dict(val)
#     return data_dict