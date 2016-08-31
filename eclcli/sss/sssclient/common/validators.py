import netaddr

from . import exceptions
from ..i18n import _


def validate_int_range(parsed_args, attr_name, min_value=None, max_value=None):
    val = getattr(parsed_args, attr_name, None)
    if val is None:
        return
    try:
        if not isinstance(val, int):
            int_val = int(val, 0)
        else:
            int_val = val
        if ((min_value is None or min_value <= int_val) and
                (max_value is None or int_val <= max_value)):
            return
    except (ValueError, TypeError):
        pass

    if min_value is not None and max_value is not None:
        msg = (_('%(attr_name)s "%(val)s" should be an integer '
                 '[%(min)i:%(max)i].') %
               {'attr_name': attr_name.replace('_', '-'),
                'val': val, 'min': min_value, 'max': max_value})
    elif min_value is not None:
        msg = (_('%(attr_name)s "%(val)s" should be an integer '
                 'greater than or equal to %(min)i.') %
               {'attr_name': attr_name.replace('_', '-'),
                'val': val, 'min': min_value})
    elif max_value is not None:
        msg = (_('%(attr_name)s "%(val)s" should be an integer '
                 'smaller than or equal to %(max)i.') %
               {'attr_name': attr_name.replace('_', '-'),
                'val': val, 'max': max_value})
    else:
        msg = (_('%(attr_name)s "%(val)s" should be an integer.') %
               {'attr_name': attr_name.replace('_', '-'),
                'val': val})

    raise exceptions.CommandError(msg)


def validate_ip_subnet(parsed_args, attr_name):
    val = getattr(parsed_args, attr_name)
    if not val:
        return
    try:
        netaddr.IPNetwork(val)
    except (netaddr.AddrFormatError, ValueError):
        raise exceptions.CommandError(
            (_('%(attr_name)s "%(val)s" is not a valid CIDR.') %
             {'attr_name': attr_name.replace('_', '-'), 'val': val}))
