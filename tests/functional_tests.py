import pytest
import os
from playwright.sync_api import Page, expect

BASE_URL = os.environ.get("BASE_URL", "https://shrimp.tips/").rstrip("/") + "/"

def test_homepage_loads(page: Page):
    page.goto(BASE_URL)
    expect(page).to_have_title("ShrimpTips - Ocean Safety for Wild Shrimp")
    expect(page.locator("h1")).to_contain_text("🦐 ShrimpTips")
    expect(page.locator("body")).to_contain_text("Ocean Safety & Health Guidance for Wild Shrimp")

def test_initial_poster_generates(page: Page):
    page.goto(BASE_URL)
    # Wait for the initial poster to generate (it has a 1s timeout in the code)
    poster_image = page.locator(".poster-image")
    safety_tip = page.locator(".safety-tip")
    
    expect(poster_image).to_be_visible(timeout=30000)
    expect(safety_tip).to_be_visible(timeout=30000)
    expect(safety_tip).not_to_be_empty()

def test_generate_button_works(page: Page):
    page.goto(BASE_URL)
    # Wait for initial poster
    expect(page.locator(".poster-image")).to_be_visible(timeout=15000)
    
    # Click generate button
    btn = page.locator("#generate-btn")
    btn.click()
    
    # Check that it enters loading state
    expect(btn).to_be_disabled()
    expect(btn).to_contain_text("Generating...")
    
    # Wait for new poster
    expect(btn).to_be_enabled(timeout=30000)
    
    # Check for image or error
    poster_image = page.locator(".poster-image")
    error_msg = page.locator(".error")
    
    if error_msg.is_visible():
        print(f"Poster generation failed with error: {error_msg.inner_text()}")
        pytest.fail("Poster generation failed on the server")
    
    expect(poster_image).to_be_visible()
    expect(page.locator(".safety-tip")).to_be_visible()

def test_button_disabled_during_load(page: Page):
    page.goto(BASE_URL)
    # The page starts generating immediately
    btn = page.locator("#generate-btn")
    
    # It should be disabled initially until the first poster loads
    # Note: the HTML says <button id="generate-btn" ... disabled>
    expect(btn).to_be_disabled()
    
    # Wait until it becomes enabled
    expect(btn).to_be_enabled(timeout=15000)
