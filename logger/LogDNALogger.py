import logging

from logdna import LogDNAHandler


class LogDNALogger:

    def __init__(self, logdna_key):
        self.log = logging.getLogger('logdna')
        self.log.addHandler(LogDNAHandler(logdna_key))
        self.log.info("LogDNA up and running....")

    def get_logger(self):
        return logging.getLogger(__name__)