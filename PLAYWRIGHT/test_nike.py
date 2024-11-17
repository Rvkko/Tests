from playwright.async_api import async_playwright, expect
import asyncio

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Launch browser in headed mode
        page = await browser.new_page()

        # Test check title
        await page.goto("https://www.nike.com/us/en_us/")
        await expect(page).to_have_title("Nike. Just Do It. Nike.com")
        print(await page.title())

        await page.fill('button[aria-label="search"]', 'Air Jordan')
        page.keyboard.press('Enter')

        # Test check title
        await expect(page).to_have_title("Nike. Just Do It. Nike.com")

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())