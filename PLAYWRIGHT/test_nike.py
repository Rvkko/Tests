from playwright.async_api import async_playwright, expect
import pytest

@pytest.fixture
async def browser_page():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Launch browser in headed mode
        page = await browser.new_page()
        yield page
        await browser.close()

@pytest.mark.asyncio
async def test_check_title(browser_page):
    await browser_page.goto("https://www.nike.com/us/en_us/")
    await expect(browser_page).to_have_title("Nike. Just Do It. Nike.com")
    print(await browser_page.title())

@pytest.mark.asyncio
async def test_search_shoe(browser_page):
    await browser_page.goto("https://www.nike.com/us/en_us/")
    await browser_page.fill("input[aria-label='Search']", "Air Max 95")
    await browser_page.keyboard.press("Enter")
    await browser_page.wait_for_selector("text=Air Max 95")
    print(await browser_page.title())

@pytest.mark.asyncio
async def test_select_gender(browser_page):
    await browser_page.goto("https://www.nike.com/us/en_us/")
    await browser_page.fill("input[aria-label='Search']", "Air Max 95")
    await browser_page.keyboard.press("Enter")
    await browser_page.wait_for_selector("text=Gender")
    await browser_page.click("text=Gender")
    await browser_page.wait_for_selector("text=Men")
    await browser_page.click("text=Men")
    await browser_page.wait_for_selector("text=Nike Air Max 95 By You")
    await browser_page.click("text=Nike Air Max 95 By You")
    print(await browser_page.title())