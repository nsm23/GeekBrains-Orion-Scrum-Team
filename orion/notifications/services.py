from django.utils import dateformat, timezone


def format_datetime_with_system_timezone(datetime, format):
    return dateformat.format(
        value=timezone.localtime(datetime, timezone.get_current_timezone()),
        format_string=format,
    )
