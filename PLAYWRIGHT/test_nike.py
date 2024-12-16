from playwright.sync_api import sync_playwright
import time

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.nike.com/")
        page.get_by_placeholder("Search").fill("Air Jordan 11")
        time.sleep(3)
        page.locator("img[src='https://static.nike.com/a/images/t_default/u_126ab356-44d8-4a06-89b4-fcdcc8df0245,c_scale,fl_relative,w_1.0,h_1.0,fl_layer_apply/31236ecd-a774-4bf4-bf08-0f5ea28e5aaa/air-jordan-11-retro-low-diffused-blue-mens-shoes-FHNp6G.png']").click()
        time.sleep(3)
        page.locator("label.u-full-width u-full-height d-sm-flx flx-jc-sm-c flx-ai-sm-c").click()
        time.sleep()
        browser.close()

if __name__ == "__main__":
    main()