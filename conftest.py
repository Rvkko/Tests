"""No live account automation is collected unless --live is explicitly requested."""
import ast
import os
from pathlib import Path
import pytest
from testing_support import browser_session, load_data

def pytest_addoption(parser):
    parser.addoption('--live', action='store_true', default=False, help='Collect historical live-site samples (can modify real accounts)')

def pytest_ignore_collect(collection_path, config):
    return 'legacy' in Path(collection_path).parts and not config.getoption('--live')

@pytest.fixture
def driver(request):
    if not request.config.getoption('--live'):
        pytest.skip('Live-site samples require --live')
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    factory = webdriver.Firefox if os.environ.get('QA_BROWSER') == 'firefox' else webdriver.Chrome
    with browser_session(factory) as browser:
        browser.maximize_window()
        yield browser, WebDriverWait(browser, 15)

@pytest.fixture
def test_data(request):
    tree = ast.parse(Path(request.module.__file__).read_text(encoding='utf-8'))
    required = {n.slice.value for n in ast.walk(tree) if isinstance(n, ast.Subscript) and isinstance(n.value, ast.Name) and n.value.id == 'test_data' and isinstance(n.slice, ast.Constant) and isinstance(n.slice.value, str)}
    try:
        return load_data(Path(request.module.__file__).parent, os.environ, required)
    except ValueError as error:
        pytest.skip(str(error))

@pytest.fixture
def nike_data(request):
    return load_data(Path(request.module.__file__).parent, os.environ, ['shoe'])
