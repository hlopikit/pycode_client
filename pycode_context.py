class PycodeContext:
    def __init__(self):
        self.domain = None
        self.secret = None
        self.auth_token = None

    def set(self, secret, domain, auth_token):
        self.domain = domain
        self.secret = secret
        self.auth_token = auth_token
        return self


pycode_context = PycodeContext()
