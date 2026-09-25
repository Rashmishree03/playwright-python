class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username = "Username"
        self.password = "Password"
        self.login_button = "[type='submit']"
        self.dashboard_title = "//h6[text() = 'Dashboard']"

    def open(self):
        self.page.goto("/web/index.php/auth/login")

    def enter_username(self, username):
        self.page.get_by_placeholder(self.username).fill(username)

    def enter_password(self, password):
        self.page.get_by_placeholder(self.password).fill(password)

    def click_login(self):
        self.page.locator(self.login_button).click()

    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def is_dashboard_displayed(self):
        return self.page.locator(self.dashboard_title).is_visible()