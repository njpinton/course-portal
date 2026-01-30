from playwright.sync_api import sync_playwright
import time

time.sleep(2)  # Give server time to start

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    
    # Navigate to CMSC 178DA course page
    page.goto('http://localhost:5001/course/cmsc178da')
    page.wait_for_load_state('networkidle')
    
    # Take full page screenshot
    page.screenshot(path='course_page.png', full_page=True)
    
    # Check if Labs tab exists
    labs_tab = page.query_selector('button.course-tab:has-text("Labs")')
    
    if labs_tab:
        print("✓ Labs tab found on the page!")
        print(f"  Tab text: {labs_tab.inner_text()}")
        
        # Click it
        labs_tab.click()
        page.wait_for_timeout(500)
        
        # Take screenshot of Labs tab content
        page.screenshot(path='labs_tab_view.png', full_page=True)
        print("✓ Clicked Labs tab, took screenshot")
        
        # Count lab cards
        lab_cards = page.query_selector_all('.lab-card')
        print(f"✓ Found {len(lab_cards)} lab cards")
    else:
        print("✗ Labs tab NOT found on page")
        # Print all tab buttons for debugging
        all_tabs = page.query_selector_all('button.course-tab')
        print(f"Found {len(all_tabs)} tabs:")
        for tab in all_tabs:
            print(f"  - {tab.inner_text()}")
    
    browser.close()
