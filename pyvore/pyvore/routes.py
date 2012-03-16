def automore(request, elements, kw):
    # this is for adding the more kwargs for backbone urls
    kw.setdefault('more', ())
    return elements, kw

def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.include(session_routes, route_prefix='/api/sessions')

    config.include(pyramid_signup_routes)

    # needs to be last route
    config.add_route('socket_io', 'socket.io/*remaining')

    config.add_route('index', '/*more', pregenerator=automore)

def session_routes(config):
    config.add_route('get_sessions', '', request_method='GET')
    config.add_route('get_chatlog', '/{pk}', request_method='GET')
    config.add_view('pyvore.views.sessions.SessionController', renderer='json',
        attr='get_sessions', route_name='get_sessions')
    config.add_view('pyvore.views.sessions.SessionController', renderer='json',
        attr='get_chatlog', route_name='get_chatlog')

def pyramid_signup_routes(config):
    config.include('pyramid_signup')

    config.add_view('pyramid_signup.views.AuthController', attr='login', route_name='login',
            renderer='pyvore:templates/login.jinja2')

    config.add_view('pyramid_signup.views.ForgotPasswordController', attr='forgot_password', route_name='forgot_password',
            renderer='pyvore:templates/forgot_password.jinja2')

    config.add_view('pyramid_signup.views.ForgotPasswordController', attr='reset_password', route_name='reset_password',
            renderer='pyvore:templates/reset_password.jinja2')

    config.add_view('pyramid_signup.views.RegisterController', attr='register', route_name='register',
            renderer='pyvore:templates/register.jinja2')

    config.add_view('pyramid_signup.views.ProfileController', attr='profile', route_name='profile',
            renderer='pyvore:templates/profile.jinja2')

    config.add_view('pyramid_signup.views.ProfileController', attr='edit_profile', route_name='edit_profile',
            renderer='pyvore:templates/edit_profile.jinja2')
