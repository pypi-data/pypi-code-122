import atexit
import os
import sys
import uuid
from types import FunctionType
from typing import Union

from werkzeug.exceptions import NotFound as SuperNotFound
from werkzeug.routing import Map, Rule

from restfx.globs import _app_ctx_stack
from restfx.util import ContextStore, utils
from . import __meta__
from .http import HttpRequest, NotFound, ServerError
from .middleware import MiddlewareManager
from .routes import Collector


class AppContext:
    def __init__(self, app):
        self.app = app
        self.store = ContextStore(_app_ctx_stack)
        self.ref_count = 0

    def push(self):
        top = _app_ctx_stack.top
        if not top or top != self:
            _app_ctx_stack.push(self)
        self.ref_count += 1

    def pop(self):
        if _app_ctx_stack.top != self:
            return
        self.ref_count -= 1
        if self.ref_count > 0:
            return
        _app_ctx_stack.pop()
        del self.store

    def __enter__(self):
        self.push()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pop()


def print_meta():
    print(__meta__.text_img)


class App:
    # APP 实例集合
    _APPS = {}

    def __init__(self,
                 app_root: str,
                 app_id: str = None,
                 api_prefix='api',
                 debug=True,
                 append_slash=False,
                 strict_mode=False,
                 api_page_enabled=None,
                 api_page_name: str = None,
                 api_page_expanded=False,
                 api_page_cache=None,
                 api_page_addition=None,
                 api_page_header=None,
                 api_page_footer=None,
                 api_page_assets: tuple = None,
                 allowed_route_meta: dict = None,
                 favicon: str = None
                 ):
        """

        :param app_root: 应用的根目录
        :param app_id: 全局的唯一 id, 用于标识一个APP。
        :param api_prefix: API接口URL前缀
        :param debug: 是否启用调试模式
        :param append_slash: 是否在URL末尾使用 / 符号
        :param strict_mode: 是否启用严格模式。在严格模式下，不允许在请求时携带未声明的参数
        :param api_page_enabled: 只否启用接口页面
        :param api_page_name: 接口页面名称
        :param api_page_expanded: 是否在页面加载后自动展开接口列表
        :param api_page_cache: 是否缓存接口数据
        :param api_page_addition: 接口页面上要展示的接口的附加信息函数，其接收一个 dict 类型的参数 route_info
        :param api_page_header: 接口页面上，需要自定义展示在页面顶部的信息
        :param api_page_footer: 接口页面上，需要自定义展示在页面底部的信息
        :param api_page_assets: 接口页面上，需要自定义的JS和CSS以及其它资源 (通过 static 托管，此接口仅填写地址)
        :param allowed_route_meta: 路由装饰器上，指定允许使用的自定义元数据参数。当此值为 None 时，不限制。
        """
        print_meta()

        # 更新系统路径
        if app_root not in sys.path:
            sys.path.insert(0, app_root)

        from .config import AppConfig
        from .routes import ApiPage
        from .routes import Router
        from .util import Logger

        # 上下文需要先创建，以便后续的模块能直接使用
        self.context = AppContext(self)
        self.context.push()

        self.id = app_id or str(uuid.uuid4())
        self._logger = Logger(app_id)

        self._APPS[self.id] = self

        self.config = AppConfig(self.id, app_root, debug, api_prefix, append_slash,
                                strict_mode, api_page_enabled, api_page_name,
                                api_page_expanded, api_page_cache, api_page_addition,
                                api_page_header, api_page_footer, api_page_assets,
                                allowed_route_meta)
        self.config.middleware_manager = MiddlewareManager(self.config)
        self._api_prefix = api_prefix
        self._router = Router(self.config)
        self._api_page = ApiPage(self.config)

        self._custom_url_map = {}

        self._favicon = favicon

        self._url_map = Map([
            Rule('/favicon.ico', endpoint='favicon'),
            Rule('/%s%s' % (api_prefix, '/' if append_slash else ''), endpoint='_api_page'),
            Rule('/%s/api.json' % api_prefix, endpoint='_api_page'),
            Rule('/%s/export' % api_prefix, endpoint='_api_page'),
            Rule('/%s/<path:entry>%s' % (api_prefix, '/' if append_slash else ''), endpoint='entry_only')
        ])

        Collector.create(app_id, app_root, append_slash)

        from restfx import commands
        commands.register('persist', self.persist, 'Persist routes info into file', '[filename] [encoding]')

    def dispose(self):
        self.config.middleware_manager.handle_shutdown()

        del self.config.middleware_manager

        for plugin in self.config.plugins:
            try:
                plugin.destroy()
            except Exception as e:
                self._logger.error('Failed to destroy plugin %r' % plugin.__name__, e)

        self._logger.info('App "%s" is shutting down' % self.id)
        Collector.destroy(self.id)
        self.context.pop()
        if self.id in self._APPS:
            del self._APPS[self.id]

    def handle_wsgi_request(self, environ, start_response):
        """
        接收并处理来自 wsgi 的请求
        :param environ:
        :param start_response:
        :return:
        """

        request = None
        response = None
        try:
            request = HttpRequest(environ, self)
            request.context().push()

            response = self.config.middleware_manager.handle_coming(request)
            if not response:
                adapter = self._url_map.bind_to_environ(environ)

                endpoint, values = adapter.match()
                if endpoint == '_api_page':
                    response = self._api_page.dispatch(request)
                elif endpoint == 'entry_only':
                    response = self._router.dispatch(request, values['entry'])
                elif endpoint in self._custom_url_map:
                    response = self._custom_url_map[endpoint](request, **values)
                elif endpoint == 'favicon':
                    if self._favicon is None:
                        response = NotFound()
                    else:
                        from .http import FileResponse
                        response = FileResponse(os.path.join(self.config.ROOT, self._favicon))
                else:
                    response = NotFound()
        except Exception as e:
            # 忽略静态资源请求的 .js.map/.css.map 文件
            if request and (request.path.lower().endswith('.js.map') or request.path.lower().endswith('.css.map')):
                response = NotFound()
            else:
                msg = utils.get_exception_info(e)
                if request:
                    msg = 'Error occurred during handling request %r:\n\t%s' % (request.path, msg)

                self._logger.error(msg)

                if isinstance(e, SuperNotFound):
                    response = NotFound()
                elif self.config.debug:
                    response = ServerError(msg.replace('<', '&lt;').replace('>', '&gt;'))
                else:
                    response = ServerError()
        finally:
            result = self.config.middleware_manager.handle_leaving(request, response)
            if result:
                response = result
            request.context().pop()
            import werkzeug
            sv = sys.version_info
            response.headers['server'] = '%s/%s werkzeug/%s Python/%s' % (
                __meta__.name, __meta__.version, werkzeug.__version__, '%s.%s.%s' % (sv[0], sv[1], sv[2])
            )
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        """
        wsgi 入口
        :param environ:
        :param start_response:
        :return:
        """
        if not self.config.static_map:
            return self.handle_wsgi_request(environ, start_response)

        from werkzeug.middleware.shared_data import SharedDataMiddleware
        return SharedDataMiddleware(self.handle_wsgi_request, self.config.static_map)(
            environ, start_response)

    def startup(self, host=None, port=9127, threaded=True, **kwargs):
        """
        开发时使用的服务器，一般来说，应仅用于开发
        :param host:
        :param port:
        :param threaded:
        :param kwargs: 适用于 werkzeug 的 run_simple 函数的其它参数
        :return:
        """
        from restfx.util import helper
        from werkzeug.serving import run_simple

        debug = self.config.debug

        if debug:
            helper.print_meta('dev-server *DEBUG MODE*')
        else:
            helper.print_meta('dev-server')

        # 检查启动参数
        cmd_host = None
        cmd_port = None
        argv = sys.argv
        if len(argv) > 1:
            server_arg = argv[1].split(':')
            if len(server_arg) == 1:
                self._logger.warning('Invalid startup argument "%s" (ignored):' % argv[1])
            else:
                cmd_host = server_arg[0]
                cmd_port = int(server_arg[1])

        # 检查环境变量
        env_host = os.environ.get('RESTFX_HOST')
        env_port = os.environ.get('RESTFX_PORT')

        if env_host is not None:
            host = env_host
            self._logger.info('Using host from environment variable RESTFX_HOST: %s' % host)
        elif cmd_host:
            host = cmd_host
            self._logger.info('Using host from command line host: %s' % host)
        else:
            self._logger.info('Using host in code: %s' % host)
        if env_port is not None:
            port = int(env_port)
            self._logger.info('Using port from environment variable RESTFX_PORT: %s' % port)
        elif cmd_host:
            port = cmd_port
            self._logger.info('Using port from command line port: %s' % port)
        else:
            self._logger.info('Using port in code: %s' % port)

        # 检查端口是否被占用
        # if utils.is_port_used(port):
        #     self._logger.warning('The port "%s" is not available, pick another one instead.' % port)
        #     exit(1)

        # 支持 空串和 * 标志
        if host in [None, '', '*']:
            host = '0.0.0.0'

        if self.config.api_page_enabled:
            if host == '0.0.0.0':
                ips = utils.get_ip_list()
            else:
                ips = [host]

            protocol = 'https' if kwargs.get('ssl_context') else 'http'

            print(' * Table of APIs:')
            for ip in ips:
                print('\t- %s://%s:%s/%s%s' % (
                    protocol, ip, port, self._api_prefix, '/' if self.config.append_slash else ''
                ))

        run_simple(host, port, self, use_debugger=debug, use_reloader=debug, threaded=threaded, **kwargs)

    def register_types(self, *types):
        """
        注册路由参数上使用的类型，目前仅支持枚举类型
        :param types:
        :return:
        """
        collector = Collector.get(self.id)
        for type_item in types:
            collector.global_types[type_item.__name__] = type_item

    def collect(self):
        """
        收集路由
        :return:
        """
        return Collector.get(self.id).collect(self.config.routes_map)

    def persist(self, filename: str = 'dist/routes_map.py', encoding='utf8'):
        """
        持久化路由信息到文件
        :param encoding: 文件编码
        :param filename: 输出的路由文件名称
        :return:
        """
        routes_file = os.path.basename(filename)
        routes_dir = os.path.dirname(filename)
        return Collector.get(self.id).persist(self.config.routes_map, routes_file, routes_dir, encoding)

    def set_logger(self, logger):
        """
        设置自定义的 logger
        :param logger:
        :return:
        """
        self._logger.custom_logger = logger
        return self

    def map_urls(self, urls_map: dict):
        """
        自定义的 url 映射，这些映射不会经过路由处理，而是直接来自 werkzeug
        :param urls_map:
        :return:
        """
        for url in urls_map:
            self._custom_url_map[url] = urls_map[url]
            self._url_map.add(Rule(url, endpoint=url))
        return self

    def map_routes(self, routes_map: dict):
        """
        注册路由映射表
        :param routes_map:
        :return:
        """
        for path in routes_map:
            if not path:
                raise Exception('Empty route map prefix value')
            pkg = routes_map[path]
            pkg_path = os.path.join(self.config.ROOT, pkg.replace('.', '/'))
            if not os.path.exists(pkg_path):
                self._logger.warning('Route map "%s" does not exist, path=%s' % (pkg, pkg_path))
            self.config.routes_map[path] = pkg
        return self

    def map_static(self, static_map: dict):
        """
        设置静态资源目录映射
        :param static_map:
        :return:
        """
        for prefix in static_map:
            # 静态资源的前缀，必须以 / 开头
            if prefix[0] != '/':
                self._logger.warning(
                    'Invalid prefix of static map, it should start with "/": %s' % prefix)
                continue
            if prefix.lower() == '/internal_assets':
                self._logger.warning(
                    'The prefix of static map is reserved, pick another one please: %s' % prefix)
                continue
            target_path = static_map[prefix]
            abs_target_path = os.path.abspath(os.path.join(self.config.ROOT, target_path))
            # 无论目录是否存在都注册，因为静态目录可能是动态生成的
            self.config.static_map[prefix] = abs_target_path
            if os.path.exists(abs_target_path):
                self._logger.debug('Map static url %s to path %s' % (prefix, abs_target_path))
            else:
                self._logger.warning(
                    'The target path of static url %s not found: %s' % (prefix, abs_target_path))
        return self

    def register_routes(self, routes: list):
        """
        注册路由列表。一般来说，应当通过以下方法调用：

        from dist import routes_map

        app.register_routes(routes_map.routes)

        :param routes: 其每一项都应该是一个 list, 元素依次为 method: str, path: str, handler: FunctionType
        :return:
        """
        for handler, api_info in routes:
            from .util.func_util import FunctionDescription

            method = api_info['method']
            path = api_info['path']

            rid = '%s#%s' % (path, method.lower())
            if rid in self._router.production_routes:
                self._logger.warning('Duplicated route %s %s' % (method, path))

            desc = FunctionDescription(handler)
            self._router.production_routes[rid] = {
                'func': handler,
                'args': desc.arguments
            }
            self.config.docs.append(api_info)

        return self

    def register_middleware(self, *middlewares, index: int = -1):
        """
        注册中间件，注册的中间件将按顺序执行
        :param middlewares: 中间件实例列表
        :param index: 要将包插入的位置，指定为 -1 表示放到最后
        :return:
        """
        from restfx.middleware import MiddlewareBase

        for middleware in middlewares:
            assert isinstance(middleware, MiddlewareBase)
            if index == -1:
                self.config.middlewares.append(middleware)
                self.config.reversed_middlewares.insert(0, middleware)
            else:
                self.config.middlewares.insert(index, middleware)
                if index == 0:
                    self.config.reversed_middlewares.append(middleware)
                else:
                    self.config.reversed_middlewares.insert(-index, middleware)
                # 每添加一个，将 index 后移动一个位置
                index += 1
            # 调用中间件，标记中间件的启动
            middleware.on_startup(self)

        return self

    def inject(self, **kwargs):
        """
        全局注入接口
        :param kwargs:
        :return:
        """
        self.config.injections.update(**kwargs)
        return self

    def register_plugins(self, *plugins):
        """
        注册插件，插件没有顺序之分
        :param plugins: 插件实例列表
        :return:
        """
        from restfx.plugin import PluginBase

        for plugin in plugins:
            assert isinstance(plugin, PluginBase)
            self.config.plugins.append(plugin)
            # 调用插件，标记中间件的启动
            plugin.setup(self)

        return self

    def register_enums(self, enum_types: Union[list, tuple], ignore_non_enum=True):
        """
        注册枚举类型
        :param enum_types: 要注册的枚举类型
        :param ignore_non_enum: 是否忽略慧枚举类型
        :return:
        """
        from enum import Enum

        for enum_type in enum_types:
            if not ignore_non_enum:
                assert issubclass(enum_type, Enum)
            if enum_type in self.config.enum_types:
                continue
            self.config.enum_types.append(enum_type)

        return self

    @classmethod
    def register_command(cls, command: str, handler: FunctionType, description: str):
        from restfx import commands
        commands.register(command, handler, description)

    def test_command(self):
        from restfx import commands
        return commands.execute(*sys.argv, working_dir=self.config.ROOT)

    @classmethod
    def get(cls, app_id: str):
        """
        获取指定的应用
        :param app_id:
        :return:
        :rtype: App
        """
        return cls._APPS.get(app_id)

    @staticmethod
    def current():
        """
        获取当前的应用
        :return:
        """
        from restfx import globs
        return globs.current_app

    @staticmethod
    def store():
        """
        获取当前应用的存储对象
        :return:
        """
        from restfx import globs
        return globs.app_store


@atexit.register
def _destroy_apps():
    # Parse the ids into list to avoid the error "RuntimeError: dictionary changed size during iteration"
    app_ids = list(App._APPS.keys())
    for app_id in app_ids:
        app = App.get(app_id)
        app.dispose()
