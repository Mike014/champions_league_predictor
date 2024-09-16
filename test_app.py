from playwright.sync_api import sync_playwright
import time

def run(playwright):
    # Launch Microsoft Edge browser
    browser = playwright.chromium.launch(channel="msedge", headless=True)
    context = browser.new_context()
    page = context.new_page()

    # Open the web page
    page.goto('http://127.0.0.1:5000/')

    # Find the form elements and fill them
    form_data = {
        '#M': '10',
        '#W': '6',
        '#D': '2',
        '#L': '2',
        '#Dif': '15',
        '#Pt': '20'
    }

    for selector, value in form_data.items():
        page.fill(selector, value)

    # Submit the form
    page.click('input[type="submit"]')

    # Wait for the page to load and verify the result
    time.sleep(2)  # Wait 2 seconds for the page to load

    # Verify the expected result
    predicted_goals = page.text_content('.predicted-goals')
    print(f"Predicted Goals: {predicted_goals}")

    # Close the browser
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
