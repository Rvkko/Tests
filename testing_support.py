"""Configuration and cleanup shared by opt-in historical Selenium examples."""
from contextlib import contextmanager
import json
import re
from pathlib import Path

def load_data(directory, environment, required=()):
    directory = Path(directory)
    files = [directory / name for name in ('test_data.json', 'nike_data.json', 'test_data.example.json', 'nike_data.example.json')]
    source = next((p for p in files if p.exists()), None)
    if source is None:
        raise ValueError('No example data file exists for this sample')
    data = json.loads(source.read_text(encoding='utf-8'))
    if not isinstance(data, dict):
        raise ValueError('Test data must be a JSON object')
    prefix = 'QA_' + directory.name.upper().replace('-', '_') + '_'
    for key in set(data) | set(required):
        name = prefix + re.sub(r'[^A-Z0-9]', '_', key.upper())
        if name in environment:
            data[key] = environment[name]
    missing = [key for key in required if data.get(key) in (None, '')]
    if missing:
        raise ValueError('Configure required values: ' + ', '.join(prefix + re.sub(r'[^A-Z0-9]', '_', key.upper()) for key in sorted(missing)))
    return data

@contextmanager
def browser_session(factory):
    browser = factory()
    try:
        yield browser
    finally:
        browser.quit()
