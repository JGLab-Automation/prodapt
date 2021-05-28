__author__ = 'JG'

import socket
import traceback
import urllib3
import requests
from json import loads, dumps, JSONDecodeError
import logging
from logging import handlers
from config import environment as env


class Log:

    def __init__(self, filename='exec.log', log_name=__name__):
        self.filename = filename
        self.log_name = log_name

    def critical(self, text):
        self.log(text, 'critical')

    def error(self, text):
        self.log(text, 'error')

    def warning(self, text):
        self.log(text, 'warning')

    def info(self, text):
        self.log(text, 'info')

    def debug(self, text):
        self.log(text, 'debug')

    def log(self, text, level):

        log_format = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')

        log_handler = handlers.RotatingFileHandler(f"{env.suite['workspace']}/artefacts/{self.filename}",
                                                   maxBytes=102400000, backupCount=10)
        log_handler.setFormatter(log_format)

        logger = logging.getLogger(self.log_name)

        if env.suite['log_level'].upper() == 'CRITICAL':
            logger.setLevel(level=logging.CRITICAL)
        elif env.suite['log_level'].upper() == 'ERROR':
            logger.setLevel(level=logging.ERROR)
        elif env.suite['log_level'].upper() == 'WARNING':
            logger.setLevel(level=logging.WARNING)
        elif env.suite['log_level'].upper() == 'INFO':
            logger.setLevel(level=logging.INFO)
        elif env.suite['log_level'].upper() == 'DEBUG':
            logger.setLevel(level=logging.DEBUG)
        elif env.suite['log_level'].upper() == 'NOTSET':
            logger.setLevel(level=logging.NOTSET)

        logger.addHandler(log_handler)

        if level.lower() == 'critical':
            logger.critical(text, exc_info=True)
        elif level.lower() == 'error':
            logger.error(text, exc_info=True)
        elif level.lower == 'warning':
            logger.warning(text, exc_info=True)
        elif level.lower() == 'info':
            logger.info(text)
        elif level.lower() == 'debug':
            logger.debug(text)


class Network:

    def __init__(self):
        self.log = Log()

    def get_ipv4(self, dns='4.2.2.2', port=80):
        try:
            conx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            conx.connect((dns, port))
            ipv4 = conx.getsockname()[0]
            self.log.info(f"Host IPv4 address- {ipv4}")
            return ipv4
        except socket.error as err:
            self.log.error(err)
            traceback.print_exc(err)
            return 'socket_error'
        finally:
            if conx:
                conx.close()


class HTTP:

    def __init__(self, url, header='', payload='', session=None):
        self.url = url
        self.header = header
        self.payload = payload
        self.session = session
        self.log = Log()

    def request(self, operation):

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        try:
            if self.session is None:
                self.log.debug(f"Creating new HTTP session")
                with requests.Session() as session:
                    self.log.debug(f"Sending HTTP request")
                    self.log.debug(f"URL: {self.url} | Header: {self.header} | Payload: {self.payload}")
                    response = session.request(operation, url=self.url, headers=self.header, data=self.payload,
                                               verify=False)
                    self.log.debug(f"{response.status_code} | {response.text}")
            elif self.session is not None:
                self.log.debug(f"Using HTTP session {self.session}")
                self.log.debug(f"Sending HTTP request")
                response = self.session.request(operation, url=self.url, headers=self.header, data=self.payload,
                                                verify=False)
                self.log.debug(f"{response.status_code} | {response.text}")
        except requests.exceptions.ConnectionError as err:
            self.log.error(err)
            traceback.print_stack()
            return 'http_connection_error'
        except requests.exceptions.HTTPError as err:
            self.log.error(err)
            traceback.print_stack()
            return 'http_error'
        except BaseException as err:
            self.log.error(err)
            traceback.print_stack()
            return 'base_exception'

        if operation.upper() == 'GET' or 'POST' or 'PUT' or 'DELETE':
            if response.status_code == 204:
                return 'no_content'
            else:
                try:
                    value = loads(response.text)
                    return value
                except JSONDecodeError as err:
                    self.log.critical(err)
                    return 'decode_error'

    def get(self):
        response = self.request("GET")
        return response

    def add(self):
        response = self.request("POST")
        return response

    def edit(self):
        response = self.request("PUT")
        return response

    def delete(self):
        response = self.request("DELETE")
        return response
