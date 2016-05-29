"""Pylons environment configuration"""
import os
import hanabira.lib.app_globals as app_globals
import hanabira.lib.helpers as helpers_lib
from hanabira.config.routing import make_map
from hanabira.model import init_model
from mako.lookup import TemplateLookup
from pylons.configuration import PylonsConfig
from pylons.error import handle_mako_error
from sqlalchemy import engine_from_config

def gen_load_environment(cfile, pkgname, app_globals, helpers_lib, make_map, init_model):
    def load_environment(global_conf, app_conf, setup_mode=False):
        """Configure the Pylons environment via the ``pylons.config``
        object
        """
        config = PylonsConfig()
        
        # Pylons paths
        root = os.path.dirname(os.path.dirname(os.path.abspath(cfile)))
        paths = dict(root=root,
                     controllers=os.path.join(root, 'controllers'),
                     static_files=os.path.join(root, 'public'),
                     templates=[os.path.join(root, 'templates')])
    
        # Initialize config with the basic options
        config.init_app(global_conf, app_conf, package=pkgname, paths=paths)
    
        config['routes.map'] = make_map(config)
        config['pylons.app_globals'] = app_globals.Globals(config, paths)
        config['pylons.h'] = helpers_lib
        config['pylons.strict_tmpl_context'] = config.get('pylons.strict_tmpl_context', 'true') == 'true'
        
        # Setup cache object as early as possible
        import pylons
        pylons.cache._push_object(config['pylons.app_globals'].cache)
        
        # Create the Mako TemplateLookup, with the default auto-escaping
        config['pylons.app_globals'].mako_lookup = TemplateLookup(
            directories=paths['templates'],
            error_handler=handle_mako_error,
            module_directory=os.path.join(app_conf['cache_dir'], 'templates'),
            input_encoding='utf-8', default_filters=['escape'],
            imports=['from webhelpers.html import escape'])
        
        # Make app_globals be avaiable out of request context
        
        pylons.app_globals._push_object(config['pylons.app_globals'])
    
        # Setup the SQLAlchemy database engine
        engine = engine_from_config(config, 'sqlalchemy.')
        init_model(engine)
        
        config['pylons.app_globals'].init_model(config, setup_mode)
        
        return config
    return load_environment

load_environment = gen_load_environment(__file__, 'hanabira', app_globals, helpers_lib, make_map, init_model)
