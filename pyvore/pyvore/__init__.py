from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from webassets import Bundle

from sqlalchemy import engine_from_config

from pyramid_beaker import session_factory_from_settings

from pyramid_signup.interfaces import ISUSession

from deform_jinja2 import jinja2_renderer_factory
from deform_jinja2.translator import PyramidTranslator

from pyramid_signup.interfaces import ISULoginForm
from pyramid_signup.interfaces import ISURegisterForm
from pyramid_signup.interfaces import ISUForgotPasswordForm
from pyramid_signup.interfaces import ISUResetPasswordForm
from pyramid_signup.interfaces import ISUProfileForm
from pyramid_signup.events import PasswordResetEvent
from pyramid_signup.events import NewRegistrationEvent
from pyramid_signup.events import RegistrationActivatedEvent
from pyramid_signup.events import ProfileUpdatedEvent
from pyramid_signup import groupfinder

import os
import deform

from pyvore.models import DBSession
from pyvore.forms import PyvoreForm
from pyvore.interfaces import ISession

here = os.path.dirname(__file__)

def handle_request(event):
  request = event.request
  session = request.registry.getUtility(ISUSession)
  session.commit()

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    session_factory = session_factory_from_settings(settings)
    authn_policy = AuthTktAuthenticationPolicy('pyvor3',
                 callback=groupfinder)

    authz_policy = ACLAuthorizationPolicy()

    config = Configurator(
        settings=settings,
        session_factory=session_factory,
        authorization_policy=authz_policy,
        authentication_policy=authn_policy
    )

    config.add_subscriber(handle_request, PasswordResetEvent)
    config.add_subscriber(handle_request, NewRegistrationEvent)
    config.add_subscriber(handle_request, RegistrationActivatedEvent)
    config.add_subscriber(handle_request, ProfileUpdatedEvent)

    config.registry.registerUtility(DBSession, ISession)

    jst = Bundle('templates/*.html',
            filters='jst',
            output='jst.js', debug=False)

    config.add_webasset('jst', jst)


    # jinja2 configuration
    config.add_jinja2_extension('jinja2.ext.i18n')
    config.add_jinja2_extension('webassets.ext.jinja2.AssetsExtension')
    config.add_jinja2_search_path(os.path.join(here, 'templates'))
    config.add_jinja2_search_path("pyvore:templates")

    jinja2_env = config.get_jinja2_environment()

    assets_env = config.get_webassets_env()
    jinja2_env.assets_environment = assets_env

    renderer = jinja2_renderer_factory(
        search_paths=(
            'pyvore:templates/',
        ),
        default_templates='deform_jinja2:bootstrap_templates',
        translator=PyramidTranslator()
    )

    deform.Form.set_default_renderer(renderer)

    # The are from pyramid_signup, we are overriding them to use CouchForm
    # for rendering
    override_forms = [
        ISULoginForm, ISURegisterForm, ISUForgotPasswordForm,
        ISUResetPasswordForm, ISUProfileForm
    ]

    for form in override_forms:
        config.registry.registerUtility(PyvoreForm, form)

    config.registry.registerUtility(DBSession, ISUSession)

    config.include('pyvore.routes')

    config.scan()

    return config.make_wsgi_app()
