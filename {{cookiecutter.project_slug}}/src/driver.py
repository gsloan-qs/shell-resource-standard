from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface
from cloudshell.shell.core.driver_context import InitCommandContext, ResourceCommandContext, AutoLoadCommandContext, \
    AutoLoadAttribute, AutoLoadResource, AutoLoadDetails


class {{cookiecutter.driver_name}} (ResourceDriverInterface):

    def cleanup(self):
        """
        Destroy the driver session, this function is called everytime a driver instance is destroyed
        This is a good place to close any open sessions, finish writing to log files
        """
        pass

    def __init__(self):
        """
        ctor must be without arguments, it is created with reflection at run time
        """
        pass

    def initialize(self, context):
        """
        Initialize the driver session, this function is called everytime a new instance of the driver is created
        This is a good place to load and cache the driver configuration, initiate sessions etc.
        :param InitCommandContext context: the context the command runs on
        """
        pass

    def example_function(self, context):
        """
        A simple example function
        :param ResourceCommandContext context: the context the command runs on
        """
        pass

    def example_function_with_params(self, context, user_param1, user_param2):
        """
        An example function that accepts two user parameters
        :param ResourceCommandContext context: the context the command runs on
        :param str user_param1: A user parameter
        :param str user_param2: A user parameter
        """
        pass

    def _helper_function(self):
        """
        Private functions are always hidden, and will not be exposed to the end user
        """
        pass

    def orcestration_restore(self, context, saved_artifact):
        """
        Restores a saved artifact previously saved by the Shell driver
        :param ResourceCommandContext context: the context the command runs on
        :param str saved_artifact: The saved details object
        """
        '''
        The saved_artifact json must conform to the save and restore standard
        schema defined at: https://github.com/QualiSystems/sandbox_orchestration_standard/blob/master/save%20%26%20restore/saved_artifact_info.schema.json
        You can find more information and examples examples in the spec document at
         https://github.com/QualiSystems/sandbox_orchestration_standard/blob/master/save%20%26%20restore/save%20%26%20restore%20standard.md
        Example JSON:
        {

          "saved_artifacts_info": {
            "resource_name": "vcenter_01",
            "created_date": "4647-09-23T10:03:24.330Z",
            "restore_rules": {
              "requires_sames_resource": true
            },
            "saved_artifact": {
              "artifact_type": "vcenter_snapshot",
              "identifier": "snapshot1"
            }
          }
        }

        '''

        pass

    def orcestration_save(self, context, mode="shallow", custom_params = None):
        """
        An example function that accepts two user parametesrs
        :param ResourceCommandContext context: the context the command runs on
        :rtype: str
        :return A saved_artifact json string
        """
        '''
        The saved_artifact json must conform to the save and restore standard
        schema defined at: https://github.com/QualiSystems/sandbox_orchestration_standard/blob/master/save%20%26%20restore/saved_artifact_info.schema.json
        You can find more information and examples examples in the spec document at
        https://github.com/QualiSystems/sandbox_orchestration_standard/blob/master/save%20%26%20restore/save%20%26%20restore%20standard.md
        '''
        pass

    def get_inventory(self, context):
        """
        An example function that accepts two user parametesrs
        :param AutoLoadCommandContext context: the context the command runs on
        """
        '''
        # Add sub resources details
        sub_resources = [ AutoLoadResource(model ='Generic Chassis',name= 'Chassis 1', relative_address='1'),
          AutoLoadResource(model='Generic Module',name= 'Module 1',relative_address= '1/1'),
          AutoLoadResource(model='Generic Port',name= 'Port 1', relative_address='1/1/1'),
          AutoLoadResource(model='Generic Port', name='Port 2', relative_address='1/1/2'),
          AutoLoadResource(model='Generic Power Port', name='Power Port', relative_address='1/PP1')]


        attributes = [ AutoLoadAttribute(relative_address='', attribute_name='Location', attribute_value='Santa Clara Lab'),
                       AutoLoadAttribute('', 'Model', 'Catalyst 3850'),
                       AutoLoadAttribute('', 'Vendor', 'Cisco'),
                       AutoLoadAttribute('1', 'Serial Number', 'JAE053002JD'),
                       AutoLoadAttribute('1', 'Model', 'WS-X4232-GB-RJ'),
                       AutoLoadAttribute('1/1', 'Model', 'WS-X4233-GB-EJ'),
                       AutoLoadAttribute('1/1', 'Serial Number', 'RVE056702UD'),
                       AutoLoadAttribute('1/1/1', 'MAC Address', 'fe80::e10c:f055:f7f1:bb7t16'),
                       AutoLoadAttribute('1/1/1', 'IPv4 Address', '192.168.10.7'),
                       AutoLoadAttribute('1/1/2', 'MAC Address', 'te67::e40c:g755:f55y:gh7w36'),
                       AutoLoadAttribute('1/1/2', 'IPv4 Address', '192.168.10.9'),
                       AutoLoadAttribute('1/PP1', 'Model', 'WS-X4232-GB-RJ'),
                       AutoLoadAttribute('1/PP1', 'Port Description', 'Power'),
                       AutoLoadAttribute('1/PP1', 'Serial Number', 'RVE056702UD')]

        return AutoLoadDetails(sub_resources,attributes)
        '''
        pass
