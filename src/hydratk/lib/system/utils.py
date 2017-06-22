# -*- coding: utf-8 -*-
"""A useful module for misc utils

.. module:: lib.system.utils
   :platform: Unix
   :synopsis: A useful module for misc utils.
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

import pkgutil
import pkg_resources
from pip._vendor.pkg_resources import DistributionNotFound


class Utils():
    """Class Utils
    """

    @staticmethod
    def module_version(module):
        """Methods gets module version

        Args:
           module (str): full module name

        Returns:
           str: version

        """

        return pkg_resources.get_distribution(module).version

    @staticmethod
    def module_loaded(module):
        """Methods checks if module is already loaded

        Args:
           module (str): full module name

        Returns:
           bool: resukt

        """

        result = False
        # unused importer and ispkg
        for _, modname, _ in pkgutil.iter_modules():
            if modname == module:
                result = True
                break
        return result

    @staticmethod
    def module_exists(module_name):
        """Methods checks if module exists

        Args:
           module (str): full module name

        Returns:
           bool: result

        """

        try:
            pkg_resources.get_distribution(module_name)
            return True
        except pkg_resources.DistributionNotFound:
            return False

    @staticmethod
    def module_version_ok(min_version, cur_version):
        """Methods checks if module is version compliant

        Args:
           min_version (str): minimum module version
           cur_version (str): current module version

        Returns:
           bool: result

        """

        from distutils.version import LooseVersion
        return LooseVersion(cur_version) >= LooseVersion(min_version)
