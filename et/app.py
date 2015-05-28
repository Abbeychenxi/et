import tornado.web


__author__ = 'xuemingli'


class Blueprint(object):
    _first_register = True

    def __init__(self, name, import_name, handlers=None, **settings):
        self.name = name
        self.import_name = import_name
        self.settings = settings
        self.handlers = handlers

    def add_handler(self, pattern, handler):
        if self.handlers is None:
            self.handlers = [(pattern, handler)]
        else:
            self.handlers.append((pattern, handler))

    @property
    def first_register(self):
        if not self._first_register:
            return False
        self._first_register = False
        return True

    def route(self, pattern):
        def warp(cls):
            self.add_handler(pattern, cls)
            return cls
        return warp


class Application(object):
    def __init__(self, handlers=None, default_host="", transforms=None, **settings):
        self.handlers = handlers
        self.default_host = default_host
        self.transforms = transforms
        self.settings = settings
        self.context = {}

    def add_handler(self, handler):
        if not self.handlers:
            self.handlers = []
        self.handlers.append(handler)

    def register_blueprint(self, blueprint, url_prefix=''):
        if isinstance(blueprint, Blueprint):
            if blueprint.first_register:
                self._register_blueprint_handlers(blueprint, url_prefix)
        else:
            raise TypeError("not Blueprint instance")

    def _register_blueprint_handlers(self, blueprint, url_prefix):
        if not blueprint.handlers:
            return
        for spec in blueprint.handlers:
            if isinstance(spec, tuple):
                assert len(spec) in (2, 3)
                pattern = spec[0]
                handler = spec[1]
                if len(spec) == 3:
                    kwargs = spec[2]
                else:
                    kwargs = {}
                pattern = '{0}{1}'.format(url_prefix, pattern)
                _spec = tornado.web.URLSpec(pattern, handler, kwargs)
                self.add_handler(_spec)

    def register_context(self, key, value):
        if isinstance(key, str) and not key.startswith('_'):
            self.context[key] = value

    def __call__(self):
        app = tornado.web.Application(
            self.handlers, self.default_host, self.transforms, **self.settings
        )
        for k, v in self.context.items():
            if isinstance(k, str) and not k.startswith('_'):
                setattr(app, k, v)
        return app


def create(app, blueprints, **context):
    for blueprint, prefix in blueprints:
        app.register_blueprint(blueprint, prefix)
    for k, v in context.items():
        app.register_context(k, v)
    return app()
