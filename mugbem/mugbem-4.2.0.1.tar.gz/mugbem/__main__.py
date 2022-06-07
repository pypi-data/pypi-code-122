import argparse


def main():
    parser = argparse.ArgumentParser(description='Mugbem OSAS')
    parser.add_argument('--gui', default=False, help='Run GUI .osas file reader', action=argparse.BooleanOptionalAction)
    config = parser.parse_args().__dict__

    if config['gui']:
        from .gui import GUI
        return GUI().show()

    from . import bitfinex
    processor = bitfinex.watcher.processor.BookProcessor(
        output_file_path='data/book',
        pack_format='<qfd'
    )

    watcher = bitfinex.watcher.BookWatcher(processor)
    watcher.subscribe(bitfinex.watcher.requests.BookSubscribe(
        symbol='tBTCUSD', precision='R0'
    ))


if __name__ == '__main__':
    main()
