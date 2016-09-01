import Exscript
from Exscript.protocols import SSH2, Telnet
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
        self.account = Exscript.Account(username,password)
        self.default_prompt_list = ['.*#', '.*>']
        if protocol.lower() == 'telnet':
            try:

                self.handler = Telnet()
                self.handler.set_prompt(self.default_prompt_list)
                self.handler.connect(address, port)

                self.handler.login(self.account)

            except:
                raise IOError('Unable to connect to device')

        elif protocol.lower() == 'ssh':
            try:
                self.handler = SSH2()
                self.handler.set_prompt(self.default_prompt_list)
                self.handler.connect(address, port)
                self.handler.login(self.account)
            except:
                raise IOError('Unable to connect to device')

        elif protocol.lower() == 'auto':
            try:
                self.handler = SSH2()
                self.handler.set_prompt(self.default_prompt_list)
                self.handler.connect(address, port)
                self.handler.login(self.account)
            except:
                try:
                    self.handler = Telnet()
                    self.handler.set_prompt(self.default_prompt_list)
                    self.handler.connect(address, port)
                    self.handler.login(self.account)
                except:
                    raise IOError('Unable to connect to device')
        else:
            raise AttributeError('invalid protocol')

    def send_and_receive(self, command, pattern_list=None):

        if pattern_list:
            if type(pattern_list) != list:
                pattern_list = [pattern_list]
            self.handler.set_prompt(pattern_list)
        else:
            pattern_list = self.default_prompt_list
            self.handler.set_prompt(self.default_prompt_list)

        resultcode, match = self.handler.execute(command)

        return resultcode, pattern_list[resultcode], match.string # Pattern index, pattern, buffer

    def expect(self, pattern_list=None):
        if pattern_list:
            if type(pattern_list) != list:
                pattern_list = [pattern_list]
        else:
            pattern_list = self.default_prompt_list


        returncode, match = self.handler.expect(pattern_list)

        return returncode, pattern_list[returncode], match.string # Pattern index, pattern, buffer



def __main__():
    session = Cli('localhost','23','greg-s', 'jgT777810', protocol = 'Telnet')
    result = session.send_and_receive('hostname')
    print result

if __name__ == '__main__':
    __main__()