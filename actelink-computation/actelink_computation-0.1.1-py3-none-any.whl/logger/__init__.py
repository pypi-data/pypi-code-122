import coloredlogs, logging

log = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=log, fmt='%(asctime)s %(levelname)s %(filename)s %(funcName)s %(message)s')