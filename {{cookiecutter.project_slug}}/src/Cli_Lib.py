import telnetlib
import paramiko
from cloudshell.core.logger import qs_logger
import time
import re
re.match

class Cli:
    handler = None

    def __init__(self, address, port, username='', password='', timeout=60, protocol='Auto', logger=None):
        """

        :param address:
        :param port:
        :param username:
        :param password:
        :param timeout:
        :param protocol: Auto, Telnet, SSH
        :param logger:
        :return:
        """

        if protocol.lower() == 'telnet':
            try:
                self.handler = TelnetHandler(address, port, username, password, timeout, logger)
            except:
                raise IOError('Unable to connect to device')

        elif protocol.lower() == 'ssh':
            try:
                self.handler = SSHHandler(address, port, username, password, timeout, logger)
            except:
                raise IOError('Unable to connect to device')

        elif protocol.lower() == 'auto':
            try:
                self.handler = SSHHandler(address, port, username, password, timeout, logger)
            except:
                try:
                    self.handler = TelnetHandler(address, port, username, password, timeout, logger)
                except:
                    raise IOError('Unable to connect to device')
        else:
            raise AttributeError('invalid protocol')


class SSHHandler(paramiko.SSHClient):
    def __init__(self, address, port=22, username='', password='', timeout=60, logger=None):

            if logger is None:
                logger = qs_logger.get_qs_logger('Provision Telnet')
            self.logger = logger

            logger.info('Initialize SSHHandler: {address=' + address + ' port=' + str(port) + ' timeout=' +
                        str(timeout))

            paramiko.SSHClient.__init__(self)

            self.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            self.address = address
            self.username = username
            self.password = password
            self.timeout = timeout
            self.port = port

            self.login()

    def login(self):
        self.logger.info('Logging in ssh handler')
        self.connect(self.address, username=self.username, password=self.password, timeout=self.timeout,
                     port=self.port)

    def send_and_receive(self, line):
        return self.exec_command(line)


class TelnetHandler(telnetlib.Telnet):

    login_prompt = '[Ll]ogin:'
    password_prompt = '[Pp]assword:'
    default_prompt_set = ['.*?#', '.*?>', '.*?%', login_prompt, password_prompt]
    last_result = ''
    last_result_stripped = ''
    last_pattern_index = -1

    def __init__(self, address, port=23, username='', password='', timeout=60, logger=None):

            if logger is None:
                logger = qs_logger.get_qs_logger('TelnetHandler')

            self.logger = logger

            self.logger.info('Initialize TelnetHandler: {address=' + address + ' port=' + str(port) + ' timeout=' +
                        str(timeout))
            if timeout is 0:
                telnetlib.Telnet.__init__(self, address, port)
            else:
                telnetlib.Telnet.__init__(self, address, port, timeout)

            self.address = address
            self.port = port
            self.timeout=timeout
            self.username = username
            self.password = password

            #TODO Move login to wrapper init
            self.login()

    def login(self):

        self.logger.info('Logging in telnet handler')
        self.send_and_receive('\r\n', use_pattern=True)
        #TODO clarify pattern matching without using indexes
        if self.last_pattern_index == self.default_prompt_set.index(self.login_prompt):  # Matched Login pattern
            if self._from_login_prompt() == -1:
                return -1

        elif self.last_pattern_index == 4: # Started at password prompt
            self.send_and_receive('\r\n')
            if self.last_pattern_index == 3: # Matched Login pattern
                if self._from_login_prompt() == -1:
                    return -1

        elif self.last_pattern_index in [0,1,2]: # Already logged in
            while self.last_pattern_index not in [-1,3]:
                self.send_and_receive('exit')

            if self.last_pattern_index == 3:
                self._from_login_prompt()

            else:
                self.open(self.address, self.port, self.timeout)
                self.send_and_receive('\r\n')
                if self.last_pattern_index == 3:
                    self._from_login_prompt()
                elif self.last_pattern_index == -1:
                    self.logger.error('Incorrect login result, unable get prompt')
                    self.logger.debug(self.last_result_stripped)

        self.logger.info('Successful login')
        return 1


    def _from_login_prompt(self):
        self.send_and_receive(self.username)
        if self.last_pattern_index == 4: # Matched Password pattern
            self.send_and_receive(self.password)
            if self.last_pattern_index not in [0,1,2]: # Did not receive prompt
                self.logger.error('Incorrect login result, no matching prompt')
                self.logger.debug(self.last_result_stripped)
                return -1
        else: # Did not get password prompt
            self.logger.error('Incorrect login result, did not receive password prompt')
            self.logger.debug(self.last_result_stripped)
            return -1

        return 1

    def strip_last_line(self, content):
        try:
            return content.rsplit('\r\n', 1)[0]
        except IndexError:
            return content

    def strip_first_line(self, content):
        try:
            return content.split('\r\n', 1)[1]
        except IndexError:
            return content

    def clear_read_buffer(self):
        result = None

        while result != '':
            result = self.read_very_eager()

    def send_and_receive(self, line, use_pattern=True, patterns=[]):
        #TODO return the objects instead of setting internal members
        self.logger.info('sending "' + line + '" via telnet Handler')
        self.clear_read_buffer()
        self.last_result = ''
        if '\r\n' not in line:
            line += '\r\n'

        self.write(line)
        self.logger.info('Line sent')
        if not use_pattern:
            self.logger.info('Reading very eager')
            result = ''
            temp_result = None
            time.sleep(2)
            while temp_result != '':

                temp_result = self.read_very_eager()
                result += temp_result

                # result = self.read_very_eager()
                self.last_result_stripped = self.strip_first_line(self.strip_last_line(result))
                self.logger.info('read complete')

        else:
            self.logger.info('expecting pattern set')
            if len(patterns) == 0:
                patterns = self.default_prompt_set
            try:
                result = self.expect(patterns)
            except:
                self.last_pattern_index = -1
                try:
                    self.logger.debug(result[2])
                except:
                    self.logger.debug('unable to log result')
                return self.last_pattern_index, self.last_result, self.last_result_stripped
            self.last_result = result[2]
            self.last_result_stripped = self.strip_first_line(self.strip_last_line(result[2]))
            self.last_pattern_index = result[0]
            self.logger.info('Expect complete')
            self.logger.info('Last Pattern Index: ' + str(self.last_pattern_index))
        self.logger.debug(self.last_result)
        self.logger.debug(self.last_result_stripped)
        return self.last_pattern_index, self.last_result, self.last_result_stripped


def __main__():
    pass

if __name__ == '__main__':
    __main__()