import re

ISO_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"

URL_REGEX = re.compile(
    r'^(?:http|ftp)s?://'
    , re.IGNORECASE)

