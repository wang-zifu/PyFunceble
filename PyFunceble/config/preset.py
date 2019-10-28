# pylint: disable=line-too-long
"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provide a way to preset the configuration before launching a specific test type.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    MIT License

    Copyright (c) 2017, 2018, 2019 Nissar Chababy

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""
# pylint: enable=line-too-long


from colorama import Fore, Style

import PyFunceble


class Preset:  # pragma: no cover
    """
    Check or update the global configuration based on some events.
    """

    # List all index which can be superset.
    # In other words if an index which is listed here
    # is also listed into PyFunceble.INTERN["custom_config_loaded"],
    # We do not update it.
    do_not_overwrite_if_customized = [
        "inactive_database",
        "no_files",
        "quiet",
        "timeout",
        "travis",
        "whois_database",
    ]

    def __init__(self):
        self.timeout()
        self.dns_lookup_over_tcp()
        self.syntax_test()
        self.multiprocess()

    @classmethod
    def switch(
        cls, variable, custom=False
    ):  # pylint: disable=inconsistent-return-statements
        """
        Switch PyFunceble.CONFIGURATION variables to their opposite.

        :param variable:
            The variable name to switch.
            The variable should be an index our configuration system.
            If we want to switch a bool variable, we should parse
            it here.
        :type variable: str|bool

        :param bool custom:
            Let us know if have to switch the parsed variable instead
            of our configuration index.

        :return:
            The opposite of the configuration index or the given variable.
        :rtype: bool

        :raises:
            :code:`Exception`
                When the configuration is not valid. In other words,
                if the PyFunceble.CONFIGURATION[variable_name] is not a bool.
        """

        if not custom:
            # We are not working with custom variable which is not into
            # the configuration.

            # We get the current state.
            current_state = dict.get(PyFunceble.CONFIGURATION, variable)
        else:
            # We are working with a custom variable which is not into the
            # configuration
            current_state = variable

        if isinstance(current_state, bool):
            # The current state is a boolean.

            if current_state:
                # The current state is equal to True.

                # We return False.
                return False

            # The current state is equal to False.

            # We return True.
            return True

        # The current state is not a boolean.

        # We set the message to raise.
        to_print = "Impossible to switch %s. Please post an issue to %s"

        # We raise an exception inviting the user to report an issue.
        raise Exception(to_print % (repr(variable), PyFunceble.LINKS.repo + "/issues."))

    @classmethod
    def __are_we_allowed_to_overwrite(cls, index):
        """
        Checks if we are allowed to overwrite an index.
        """

        return not (
            index in cls.do_not_overwrite_if_customized
            and "custom_loaded" in PyFunceble.INTERN
            and PyFunceble.INTERN["custom_loaded"]
            and "custom_config_loaded" in PyFunceble.INTERN
            and index in PyFunceble.INTERN["custom_config_loaded"]
        )

    @classmethod
    def disable(cls, indexes):
        """
        Set the given configuration index to :code:`False`.
        """

        if isinstance(indexes, list):
            for index in indexes:
                return cls.disable(index)

        if not cls.__are_we_allowed_to_overwrite(indexes):
            return None

        if indexes not in PyFunceble.CONFIGURATION or PyFunceble.CONFIGURATION[indexes]:
            PyFunceble.CONFIGURATION[indexes] = False

            PyFunceble.LOGGER.debug(
                f"CONFIGURATION.{indexes} switched to {PyFunceble.CONFIGURATION[indexes]}"
            )

            return None

        return None

    @classmethod
    def enable(cls, indexes):
        """
        Set the given configuration index to :code:`True`.
        """

        if isinstance(indexes, list):
            for index in indexes:
                return cls.enable(index)

        if not cls.__are_we_allowed_to_overwrite(indexes):
            return None

        if (
            indexes not in PyFunceble.CONFIGURATION
            or not PyFunceble.CONFIGURATION[indexes]
        ):
            PyFunceble.CONFIGURATION[indexes] = True

            PyFunceble.LOGGER.debug(
                f"CONFIGURATION.{indexes} switched to {PyFunceble.CONFIGURATION[indexes]}"
            )
            return None

        return None

    @classmethod
    def reset_counters(cls):
        """
        Reset the counters.
        """

        for status in ["up", "down", "invalid", "tested"]:
            # We loop through to the index of the autoContinue subsystem.

            # And we set the counter of the currently read status to 0.
            PyFunceble.INTERN["counter"]["number"][status] = 0
            PyFunceble.INTERN["counter"]["percentage"][status] = 0

        PyFunceble.LOGGER.debug(f"Counter resetted.")

    def syntax_test(self):
        """
        Disable the HTTP status code if we are
        testing for syntax
        """

        if PyFunceble.CONFIGURATION.syntax:
            # We are checking for syntax.

            # We deactivate the http status code.
            PyFunceble.HTTP_CODE.active = False

            should_be_disabled = ["generate_hosts"]
            should_be_enabled = ["plain_list_domain"]

            self.disable(should_be_disabled)
            self.enable(should_be_enabled)

    @classmethod
    def maximal_processes(cls):
        """
        Ensure that the number of maximal processes is alway >= 1.
        """

        if PyFunceble.CONFIGURATION.maximal_processes < 1:
            PyFunceble.CONFIGURATION.maximal_processes = 1

    @classmethod
    def multiprocess_merging_mode(cls):
        """
        Ensure that a valid merging mode is given.
        """

        # pylint: disable=line-too-long
        if not PyFunceble.CONFIGURATION.multiprocess_merging_mode or PyFunceble.CONFIGURATION.multiprocess_merging_mode.lower() not in [
            "end",
            "live",
        ]:
            PyFunceble.CONFIGURATION.multiprocess_merging_mode = "end"

        if PyFunceble.CONFIGURATION.db_type in ["mysql", "mariadb"]:
            PyFunceble.CONFIGURATION.multiprocess_merging_mode = "end"

    def simple_domain(self):
        """
        Prepare the global configuration for a domain
        test.
        """

        should_be_disabled = ["show_percentage", "whois_database"]

        for index in should_be_disabled:
            self.disable(index)

    def simple_url(self):
        """
        Prepare the global configuration for an URL test.
        """

        should_be_disabled = ["show_percentage", "whois_database"]

        self.disable(should_be_disabled)

    def complements(self):
        """
        Prepare the global configuration for a complements generation.
        """

        should_be_enabled = ["auto_continue"]

        self.enable(should_be_enabled)

    def file_url(self):
        """
        Prepare the global configuration for a list of URL to test.
        """

        should_be_disabled = ["generate_hosts"]
        should_be_enabled = ["no_whois", "plain_list_domain", "split"]

        self.disable(should_be_disabled)
        self.enable(should_be_enabled)

    def api(self):
        """
        Prepare the global configuration for a test from the API.
        """

        should_be_disabled = [
            "inactive_database",
            "auto_continue",
            "show_execution_time",
        ]
        should_be_enabled = ["quiet", "whois_database", "no_files"]

        self.disable(should_be_disabled)
        self.enable(should_be_enabled)

        if PyFunceble.CONFIGURATION.api_file_generation:
            PyFunceble.CONFIGURATION.no_files = False

    def multiprocess(self):
        """
        Prepare the global configuration for a test with multiple processes.
        """

        if PyFunceble.CONFIGURATION.multiprocess:
            if not PyFunceble.abstracts.Platform.is_windows():
                if (
                    PyFunceble.CONFIGURATION.db_type not in ["mysql", "mariadb"]
                    and not PyFunceble.CONFIGURATION.simple
                    and not PyFunceble.CONFIGURATION.quiet
                    and "multiprocess_warning_printed" not in PyFunceble.INTERN
                ):
                    print(
                        f"{Fore.RED + Style.BRIGHT}The "
                        f"{repr(PyFunceble.CONFIGURATION.db_type)} database type "
                        "is not recommended with the multiprocessing mode."
                    )

                    PyFunceble.INTERN["multiprocess_warning_printed"] = True

                self.maximal_processes()
                self.multiprocess_merging_mode()
            else:
                self.disable("multiprocess")

    @classmethod
    def timeout(cls):
        """
        Ensure that the timeout is always correct.
        """

        if cls.__are_we_allowed_to_overwrite("timeout") and (
            not PyFunceble.CONFIGURATION.timeout or PyFunceble.CONFIGURATION.timeout < 0
        ):
            PyFunceble.CONFIGURATION.timeout = float(3)

            PyFunceble.LOGGER.debug(
                f"CONFIGURATION.timeout switched to {PyFunceble.CONFIGURATION.timeout}"
            )

        if not isinstance(PyFunceble.CONFIGURATION.timeout, float):
            PyFunceble.CONFIGURATION.timeout = float(PyFunceble.CONFIGURATION.timeout)

            PyFunceble.LOGGER.debug(
                f"CONFIGURATION.timeout switched to {PyFunceble.CONFIGURATION.timeout}"
            )

        PyFunceble.DNSLOOKUP.update_lifetime(PyFunceble.CONFIGURATION.timeout)

    @classmethod
    def dns_lookup_over_tcp(cls):
        """
        Ensure that the DNS lookup over tcp is proprely set.
        """

        PyFunceble.DNSLOOKUP.tcp = PyFunceble.CONFIGURATION.dns_lookup_over_tcp