from src.pages.login_page import LoginPage

def test_login(page, config):
    login_page = LoginPage(page)

    login_page.open()
    login_page.login(
        config.get_secret("APP_USERNAME"),
        config.get_secret("APP_PASSWORD")
    )
    page.wait_for_timeout(5000)
    assert login_page.is_dashboard_displayed()

def test_google_search(page):
    login_page = LoginPage(page)
    
    login_page.open()
    assert page.title()

