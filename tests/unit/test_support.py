import json
import pytest
from testing_support import browser_session, load_data

def test_browser_closes_when_test_fails():
    class Browser:
        closed = False
        def quit(self):
            self.closed = True
    browser = Browser()
    with pytest.raises(RuntimeError, match='assertion failed'):
        with browser_session(lambda: browser):
            raise RuntimeError('assertion failed')
    assert browser.closed

def test_environment_overrides_example_without_modifying_disk(tmp_path):
    folder = tmp_path / 'shopify'
    folder.mkdir()
    file = folder / 'test_data.example.json'
    file.write_text(json.dumps({'email': '', 'shirts-title': 'Practice shirt'}))
    data = load_data(folder, {'QA_SHOPIFY_EMAIL': 'qa@example.test'}, ['email'])
    assert data['email'] == 'qa@example.test'
    assert json.loads(file.read_text())['email'] == ''

def test_missing_credentials_fail_with_names_only(tmp_path):
    (tmp_path / 'test_data.example.json').write_text('{"password":""}')
    with pytest.raises(ValueError, match='Configure required values'):
        load_data(tmp_path, {}, ['password'])

def test_rejects_invalid_data_shape(tmp_path):
    (tmp_path / 'test_data.example.json').write_text('[]')
    with pytest.raises(ValueError, match='JSON object'):
        load_data(tmp_path, {})
