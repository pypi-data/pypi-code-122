import os
import yaml


def load_file_data(pth):
    with open(pth, mode='r', encoding='utf-8') as f:
        for line in f:
            yield line.strip()


def read_file_(pth):
    gen_object = load_file_data(pth)

    for line in gen_object:
        # TODO do something else
        pass


def read_file(pth, encoding='utf8'):
    try:
        with open(pth, encoding=encoding) as fp:
            cont = fp.read().strip()
        return cont
    except Exception as err:
        print(err)


def write_file(path, data, append_mode=False, encoding='utf8'):
    catalog, file_name = os.path.split(path)
    if catalog and not os.path.exists(catalog):
        os.makedirs(catalog)

    try:
        mode = 'a' if append_mode else 'w'
        with open(path, mode, encoding=encoding) as f:
            f.write(data)
    except Exception as e:
        pass


def yaml_loader(file_pth):
    try:
        with open(file_pth, 'rb') as f:
            cfg = yaml.load(f, Loader=yaml.FullLoader)

        return cfg
    except Exception as e:
        return


def mkdir_p(dst_dir, is_dir=False):
    h, _ = os.path.split(dst_dir)
    if is_dir:
        h = dst_dir
    try:
        if not os.path.exists(h):
            os.makedirs(h)
    except FileExistsError as _:
        pass
    except Exception as err:
        raise err


def walk_dir_with_filter(pth, prefix=None, suffix=None):

    if suffix is None or type(suffix) != list:
        suffix = []
    if prefix is None or type(prefix) != list:
        prefix = []

    r = []
    for root_, dirs, files in os.walk(pth):
        for file_ in files:
            full_pth = os.path.join(root_, file_)

            c = False
            for x in prefix:
                if file_.startswith(x):
                    c = True
                    break
            if c:
                continue
            # if runs here , c is False
            for x in suffix:
                if file_.endswith(x):
                    c = True
                    break
            if c:
                continue
            r.append(full_pth)
    return r


def encode_html(source, obj):
    try:
        source = source.encode(obj.charset)
    except:
        try:
            source = source.encode(obj.charset, 'ignore')
        except:
            source = source.encode('utf-8')
    finally:
        return source
