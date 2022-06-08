# -*- coding : utf-8 -*-
# @Time   : 2021/9/29 22:23
# @Author : goodli
# @File   : config.py
# @Project: Valley 山谷

import os
import functools
import inspect
import argparse
from yacs.config import CfgNode as CN

_C = CN(new_allowed=True)


def get_cfg():
    return _C.clone()


def freeze():
    cfg = get_cfg()
    cfg.freeze()

def load_default_cfg():
    cur_path = os.path.abspath(__file__)
    cur_dir  = os.path.split(cur_path)[0]
    _C.merge_from_file(os.path.join(cur_dir, 'defaults.yaml'))
    _C.set_new_allowed(True)
    return _C

def setup_cfg(args):
    """
    Create configs and perform basic setups.
    """

    # load default cfg
    cfg = load_default_cfg()

    # load task specific config
    config_file = os.path.join(args.exp_root, "config", args.config if args.config != "" else "config.yaml")

    if os.path.exists(config_file) is False:
        config_file = os.path.join(os.getcwd(), "config", args.config)

    cfg.merge_from_file(config_file)
    cfg.set_new_allowed(True)

    # override params
    opts = sum([e.split("=") for e in args.opts], [])
    cfg.merge_from_list(opts)
    cfg.set_new_allowed(True)

    # generate misc cfg
    dist_url = 'tcp://{}:{}'.format(args.master_addr, args.master_port)
    cfg.merge_from_list(['LAUNCH.HOST_NUM', args.nnodes,
                         'LAUNCH.GPU_PER_HOST', args.nproc_per_node,
                         'LAUNCH.HOST_RANK', args.node_rank,
                         'LAUNCH.DIST_URL', dist_url,
                         'EXPERIMENT.ROOT_DIR', args.exp_root,
                         'EXPERIMENT.EVAL_ONLY', args.eval_only,
                         'EXPERIMENT.RESUME', args.resume,
                         'EXPERIMENT.CFG_FILE', args.config])

    cfg.freeze()
    
    return cfg
    
def build_config():
    
    # load task specific cfg
    parser = argparse.ArgumentParser()
    parser.add_argument('--nnodes',         type=int, default=1, help="num of host")
    parser.add_argument('--nproc_per_node', type=int, default=1, help="GPU per host")
    parser.add_argument('--node_rank',      type=int, default=0, help="rank of the host")
    parser.add_argument('--master_addr',    type=str, default='127.0.0.1', help="ip addr of the master server")
    parser.add_argument('--master_port',    type=str, default='23456', help="port ofthe master server")

    parser.add_argument('--exp_root', type=str)
    parser.add_argument('--config', type=str, default='config.yaml')

    #parser.add_argument('--local_rank', type=int)
    parser.add_argument(
        "opts",
        help="Modify config options by adding 'KEY VALUE' pairs at the end of the command. "
             "See config references at "
             "https://detectron2.readthedocs.io/modules/config.html#config-references",
        default=None,
        nargs=argparse.REMAINDER,
    )

    args = parser.parse_args()

    if args.config == '':
        config_file = os.path.join(args.exp_root, "config", "config.yaml")
    else:
        config_file = os.path.join(args.exp_root, "config", args.config)

        if os.path.exists(config_file) is False:
            config_file = os.path.join(os.getcwd(), "config", args.config)


    # load default cfg
    load_default_cfg()

    # load task specific config
    _C.merge_from_file(config_file)
    _C.set_new_allowed(True)

    opts = sum([e.split("=") for e in args.opts], [])
    # override params
    _C.merge_from_list(opts)
    _C.set_new_allowed(True)

    dist_url = 'tcp://{}:{}'.format(args.master_addr, args.master_port)
    _C.merge_from_list(['LAUNCH.HOST_NUM', args.nnodes,
                        'LAUNCH.GPU_PER_HOST', args.nproc_per_node,
                        'LAUNCH.HOST_RANK', args.node_rank,
                        'LAUNCH.DIST_URL', dist_url,
                        'EXPERIMENT.ROOT_DIR', args.exp_root])

    #_C.freeze()

    return get_cfg()


def configurable(init_func=None, *, from_config=None):
    """
    Decorate a function or a class's __init__ method so that it can be called
    with a :class:`CfgNode` object using a :func:`from_config` function that translates
    :class:`CfgNode` to arguments.

    Examples:
    ::
        # Usage 1: Decorator on __init__:
        class A:
            @configurable
            def __init__(self, a, b=2, c=3):
                pass

            @classmethod
            def from_config(cls, cfg):   # 'cfg' must be the first argument
                # Returns kwargs to be passed to __init__
                return {"a": cfg.A, "b": cfg.B}

        a1 = A(a=1, b=2)  # regular construction
        a2 = A(cfg)       # construct with a cfg
        a3 = A(cfg, b=3, c=4)  # construct with extra overwrite

        # Usage 2: Decorator on any function. Needs an extra from_config argument:
        @configurable(from_config=lambda cfg: {"a: cfg.A, "b": cfg.B})
        def a_func(a, b=2, c=3):
            pass

        a1 = a_func(a=1, b=2)  # regular call
        a2 = a_func(cfg)       # call with a cfg
        a3 = a_func(cfg, b=3, c=4)  # call with extra overwrite

    Args:
        init_func (callable): a class's ``__init__`` method in usage 1. The
            class must have a ``from_config`` classmethod which takes `cfg` as
            the first argument.
        from_config (callable): the from_config function in usage 2. It must take `cfg`
            as its first argument.
    """

    if init_func is not None:
        assert (
            inspect.isfunction(init_func)
            and from_config is None
            and init_func.__name__ == "__init__"
        ), "Incorrect use of @configurable. Check API documentation for examples."

        @functools.wraps(init_func)
        def wrapped(self, *args, **kwargs):
            try:
                from_config_func = type(self).from_config
            except AttributeError as e:
                raise AttributeError(
                    "Class with @configurable must have a 'from_config' classmethod."
                ) from e
            if not inspect.ismethod(from_config_func):
                raise TypeError("Class with @configurable must have a 'from_config' classmethod.")

            if _called_with_cfg(*args, **kwargs):
                explicit_args = _get_args_from_config(from_config_func, *args, **kwargs)
                init_func(self, **explicit_args)
            else:
                init_func(self, *args, **kwargs)

        return wrapped

    else:
        if from_config is None:
            return configurable  # @configurable() is made equivalent to @configurable
        assert inspect.isfunction(
            from_config
        ), "from_config argument of configurable must be a function!"

        def wrapper(orig_func):
            @functools.wraps(orig_func)
            def wrapped(*args, **kwargs):
                if _called_with_cfg(*args, **kwargs):
                    explicit_args = _get_args_from_config(from_config, *args, **kwargs)
                    return orig_func(**explicit_args)
                else:
                    return orig_func(*args, **kwargs)

            return wrapped

        return wrapper


def _get_args_from_config(from_config_func, *args, **kwargs):
    """
    Use `from_config` to obtain explicit arguments.

    Returns:
        dict: arguments to be used for cls.__init__
    """
    signature = inspect.signature(from_config_func)
    if list(signature.parameters.keys())[0] != "cfg":
        if inspect.isfunction(from_config_func):
            name = from_config_func.__name__
        else:
            name = f"{from_config_func.__self__}.from_config"
        raise TypeError(f"{name} must take 'cfg' as the first argument!")
    support_var_arg = any(
        param.kind in [param.VAR_POSITIONAL, param.VAR_KEYWORD]
        for param in signature.parameters.values()
    )
    if support_var_arg:  # forward all arguments to from_config, if from_config accepts them
        ret = from_config_func(*args, **kwargs)
    else:
        # forward supported arguments to from_config
        supported_arg_names = set(signature.parameters.keys())
        extra_kwargs = {}
        for name in list(kwargs.keys()):
            if name not in supported_arg_names:
                extra_kwargs[name] = kwargs.pop(name)
        ret = from_config_func(*args, **kwargs)
        # forward the other arguments to __init__
        ret.update(extra_kwargs)
    return ret


def _called_with_cfg(*args, **kwargs):
    """
    Returns:
        bool: whether the arguments contain CfgNode and should be considered
            forwarded to from_config.
    """
    from omegaconf import DictConfig

    if len(args) and isinstance(args[0], (CN, DictConfig)):
        return True
    if isinstance(kwargs.pop("cfg", None), (CN, DictConfig)):
        return True
    # `from_config`'s first argument is forced to be "cfg".
    # So the above check covers all cases.
    return False