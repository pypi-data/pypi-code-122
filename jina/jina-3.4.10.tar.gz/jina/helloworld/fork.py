import os
import shutil

from jina.logging.predefined import default_logger


def fork_hello(args) -> None:
    """Fork the hello world demos into a new directory

    :param args: the arg from cli

    """
    from_path = os.path.join(os.path.dirname(__file__), args.project)
    shutil.copytree(from_path, args.destination)
    full_path = os.path.abspath(args.destination)
    default_logger.info(f'{args.project} project is forked to {full_path}')
    default_logger.info(
        f'''
    To run the project:
    ~$ cd {full_path}
    ~$ python app.py
    '''
    )
