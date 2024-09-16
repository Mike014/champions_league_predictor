from playwright.sync_api import sync_playwright, TimeoutError
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
        '#M\\.': '10',  # Escape the dot in the selector
        '#W': '6',
        '#D': '2',
        '#L': '2',
        '#Dif': '15',
        '#Pt\\.': '20'  # Escape the dot in the selector
    }

    for selector, value in form_data.items():
        page.fill(selector, value)

    # Submit the form
    page.click('input[type="submit"]')

    # Wait for the page to load and verify the result
    time.sleep(5)  # Increase wait time to 5 seconds

    try:
        # Verify the expected result
        predicted_goals = page.text_content('.predicted-goals', timeout=10000)  # Increase timeout to 10 seconds
        print(f"Predicted Goals: {predicted_goals}")
    except TimeoutError:
        print("Error: The element '.predicted-goals' was not found on the page.")

    # Close the browser
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
