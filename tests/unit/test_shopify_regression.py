"""Exercise the actual historical helper without contacting Shopify."""
import ast
from pathlib import Path
from types import SimpleNamespace

def test_product_helper_refreshes_the_injected_browser():
    source = Path('legacy/selenium/shopify/test_login_sell.py').read_text()
    helper = next(n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == 'product_add')
    entered = []
    class Element:
        def click(self):
            pass
        def send_keys(self, value):
            entered.append(value)
    class Browser:
        refreshed = False
        def refresh(self):
            self.refreshed = True
    namespace = {
        'By': SimpleNamespace(XPATH='xpath'),
        'EC': SimpleNamespace(element_to_be_clickable=lambda locator: locator),
    }
    exec(compile(ast.Module(body=[helper], type_ignores=[]), '<actual product_add>', 'exec'), namespace)
    browser = Browser()
    namespace['product_add'](browser, SimpleNamespace(until=lambda condition: Element()), {'shirts-title': 'Synthetic shirt'})
    assert browser.refreshed
    assert entered[0] == 'Synthetic shirt'
