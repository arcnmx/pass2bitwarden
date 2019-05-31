import os

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
    return data.split("\n")[0]

# export fields one per line in "key: value" format
def convert_fields(fields):
    return '\n'.join(['{}: {}'.format(k, v) for k, v in fields.items()])

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
