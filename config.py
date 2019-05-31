import defaults

from defaults import CSV_FIELDS, FIELD_PATTERNS, password, convert_fields, rel

FIELD_DEFAULTS = { }

def is_note(base, path, data):
    return rel(base, path) == "tokens"

def username(data):
    fields = data['fields']
    return fields.get('login') or fields.get('user') or fields.get('username') or fields.get('email')

def fields(data, is_note):
    fields = data['fields']
    if 'user' in fields or 'username' in fields or 'login' in fields:
        fields.pop('user', None)
        fields.pop('username', None)
        fields.pop('login', None)
    elif not is_note:
        fields.pop('email', None)
    fields.pop('password', None) # left over from bad importer
    fields.pop('otpauth', None)
    fields.pop('url', None)
    return convert_fields(fields)

def note_ok(line):
    return True

def notes(data, is_note):
    notes = []
    if is_note and data['password'] != '':
        notes.append(data['password'])
    notes.extend(filter(lambda line: note_ok(line), data['notes']))
    return '\n'.join(notes)

def parse(data):
    lines = data.split('\n')
    if lines[1:2] == ['---']: # hack around an old importer mess
        return defaults.parse("\n".join([lines[0], *lines[3:]]))
    else:
        return defaults.parse(data)

FIELD_FUNCTIONS = {
    **defaults.FIELD_FUNCTIONS,
    'login_password': lambda base, path, data: password(data) if not is_note(base, path, data) else "",
    'type': lambda base, path, data: "note" if is_note(base, path, data) else "login",
    'fields': lambda base, path, data: fields(parse(data), is_note(base, path, data)),
    'notes': lambda base, path, data: notes(parse(data), is_note(base, path, data)),
    'login_username': lambda base, path, data: username(parse(data)) if not is_note(base, path, data) else "",
}

del FIELD_PATTERNS['login_username']
