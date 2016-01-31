"""
Routing configuration.
"""
# Tornado pro-tip: regex routing is optimized by putting more frequently
# accessed routes and simpler regexes before other routes.
routes = [
    (r"/", IndexHandler),
    (r"/login", LoginHandler),
    (r"/logout", LogoutHandler),
    (r"/register/culdap", CuLdapRegisterHandler),
    (r"/register", RegisterHandler),
    (r"/dashboard", DashboardHandler),
    (r"/api/surveys", SurveyHandler),
    (r"/api/response", ResponseHandler),
    (r"/userinfo", UserInfoHandler),
    (r"/userinfo/update", UserInfoUpdateHandler)
]
