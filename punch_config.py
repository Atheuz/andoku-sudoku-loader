"""Defines the behaviour for punch.py, the version updater."""

__config_version__ = 1

GLOBALS = {
    'serializer': '{{ year }}.{{ month }}.{{ build }}',
}


FILES = ['VERSION', 'pyproject.toml', 'README.rst']

ACTIONS = {
    'mbuild': {
        'type': 'conditional_reset',
        'field': 'build',
        'update_fields': ['year', 'month']
    }
}

VERSION = [
    {"name": "year", "type": "date", "fmt": "%Y"},
    {"name": "month", "type": "date", "fmt": "%m"},
    {"name": "build", "type": "integer", "start_value": 1},
]
