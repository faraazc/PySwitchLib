"""
Copyright 2017 Brocade Communications Systems, Inc.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


class AclParamParser(object):
    """
    The AclParamParser class parses parameters which are common for all the
    three ACL Types.
    Attributes:
        None
    """

    def parse_seq_id(self, **parameters):
        """
        parse supported actions by MLX platform
        Args:
            parameters contains:
                seq_id (integer): Allowed seq_id is 1 to 214748364.
        Returns:
            Return parsed string on success
        Raise:
            Raise ValueError exception
        Examples:

        """
        if 'seq_id' not in parameters or not parameters['seq_id']:
            return None

        if parameters['seq_id'] > 0 and parameters['seq_id'] < 214748365:
            return str(parameters['seq_id'])

        raise ValueError("The \'seq_id\' value {} is invalid."
                         "Valid range for sequence is 1 to 214748364."
                         .format(parameters['seq_id']))

    def parse_action(self, **parameters):
        """
        parse supported actions by MLX platform
        Args:
            parameters contains:
                action (string): Allowed actions are 'permit' and 'deny'
        Returns:
            Return parsed string on success
        Raise:
            Raise ValueError exception
        Examples:

        """
        if 'action' not in parameters or not parameters['action']:
            raise ValueError("\'action\' not present in parameters arg")

        if parameters['action'] in ['permit', 'deny']:
            return parameters['action']

        raise ValueError("The \'action\' value {} is invalid. Specify "
                         "\'deny\' or \'permit\' supported "
                         "values".format(parameters['action']))

    def parse_mirror(self, **parameters):
        """
        parse the mirror param
        Args:
            parameters contains:
                log(string): Enables the logging
                mirror(string): Enables mirror for the rule.
        Returns:
            Return None or parsed string on success
        Raise:
            Raise ValueError exception
        Examples:
        """
        if 'mirror' in parameters or not parameters['mirror']:
            return None

        if 'action' in parameters and parameters['action'] and \
                parameters['action'] != 'permit':
            raise ValueError(" Mirror keyword is applicable only for ACL"
                             " permit clauses")

        if 'log' in parameters or not parameters['log']:
            return 'mirror'

        raise ValueError("log and mirror keywords can not be used together")

    def parse_log(self, **parameters):
        """
        parse the log param
        Args:
            parameters contains:
                log(string): Enables the logging
                mirror(string): Enables mirror for the rule.
        Returns:
            Return None or parsed string on success
        Raise:
            Raise ValueError exception
        Examples:
        """
        if 'log' in parameters or not parameters['log']:
            return None

        if 'mirror' in parameters and parameters['mirror'] != 'False':
            raise ValueError("Error: mirror and log keywords can not be "
                             "used together")

        if parameters['log'] == 'True':
            return 'log'

        return None

    def parse_acl_name(self, **parameters):
        """
        parse acl name by MLX platform
        Args:
            parameters contains:
                acl_name(string): Allowed length of string is 255
        Returns:
            Return parsed string on success
        Raise:
            Raise ValueError exception
        Examples:

        """
        if 'acl_name' not in parameters or not parameters['acl_name']:
            raise ValueError("\'acl_name\' can not be empty string")

        if len(parameters['acl_name']) > 255:
            raise ValueError("\'acl_name\' can't be more than 255 characters")

        if parameters['acl_name'].lower() in ['all', 'test']:
            raise ValueError("{} cannot be used as an ACL name".format(
                             parameters['acl_name']))

        return parameters['acl_name']