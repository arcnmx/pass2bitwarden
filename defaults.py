import os
import re

# https://help.bitwarden.com/article/import-data/#generic-csv-format-individual-account
CSV_FIELDS = [
    'name',
    'folder',
    'type',
    'favorite',
    'notes',
    'fields',
    'login_totp',
    'login_uri',
    'login_username',
    'login_password'
]

FIELD_DEFAULTS = {
    'type': 'login'
}

def rel(base, path):
    return os.path.dirname(path).replace(base, '').lstrip('/')

def password(data):
    return data.split('\n')[0]

# export fields one per line in "key: value" format
def convert_fields(fields):
    return '\n'.join(['{}: {}'.format(k, v) for k, v in fields.items()])

def data_lines(data):
    lines = data.split('\n')
    if len(lines) > 1 and lines[-1] == '':
        del lines[-1]
    return lines

def parse(data):
    lines = data_lines(data)

    fields = {}
    notes = []
    field_pattern = re.compile('^([a-zA-Z0-9_-]+): *(.*)$')
    for line in lines[1:]:
        res = field_pattern.match(line)
        if res is None:
            notes.append(line)
        else:
            fields[res.group(1)] = res.group(2)

    return {
        'data': data,
        'password': lines[0],
        'fields': fields,
        'notes': notes,
    }

FIELD_FUNCTIONS = {
    'name': lambda base, path, data: os.path.basename(path),
    'folder': lambda base, path, data: rel(base, path),
    'login_password': lambda base, path, data: password(data),
}

FIELD_PATTERNS = {
    'login_uri': '^url ?: ?(.*)$',
    'login_username': '^user.* ?: ?(.*)$',
    'login_totp': '^otpauth://totp/.*secret=([a-zA-Z0-9]+).*$',
}
