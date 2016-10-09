# Copyright (c) 2016, Samantha Marshall (http://pewpewthespells.com)
# All rights reserved.
#
# https://github.com/samdmarshall/xcexport
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.
#
# 3. Neither the name of Samantha Marshall nor the names of its contributors may
# be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import sys
import configparser
from .                           import Constants
from ..Helpers.OrderedDictionary import OrderedDictionary
from ..Helpers.Logger            import Logger

class Parser(object):

    def __init__(self, file_path):
        self.config_file_path = os.path.normpath(file_path)
        self.contents = None
        if os.path.exists(self.config_file_path) is True:
            self.contents = configparser.ConfigParser(dict_type=OrderedDictionary)
            self.contents.read(self.config_file_path)
        if self.contents is not None:
            if self.validate() is True:
                Logger.write().info('Configuration file at path "%s" successfully parsed!' % self.config_file_path)
            else:
                Logger.write().error('Invalid configuration file at path "%s"!' % self.config_file_path)
        else:
            Logger.write().error('Configuration file at path "%s" does not exist!' % self.config_file_path)

    def _sections(self):
        return self.contents.sections()

    def _options(self, section):
        return self.contents.options(section)

    def validate(self):
        is_valid = False
        has_valid_sections = set(self._sections()) == set({Constants.BuildSettings, Constants.Exports, Constants.Actions})
        if has_valid_sections is True:
            has_valid_build_settings = set(self._options(Constants.BuildSettings)) == set({Constants.BuildSettings_export})
            if has_valid_build_settings is False:
                Logger.write().error('Configuration file at path "%s" has an invalid "%s" defintion!' % (self.config_file_path, Constants.BuildSettings))
            has_valid_exports = set(self._options(Constants.Exports)) == set({Constants.Exports_compiler, Constants.Exports_linker})
            if has_valid_exports is False:
                Logger.write().error('Configuration file at path "%s" has an invalid "%s" defintion!' % (self.config_file_path, Constants.Exports))
            actions_subset = set({Constants.Actions_build, Constants.Actions_install, Constants.Actions_clean, Constants.Actions_installhdrs, Constants.Actions_analyze, Constants.Actions_copyhdrs, Constants.Actions_copyrsrcs, Constants.Actions_installdebugonly, Constants.Actions_installprofileonly, Constants.Actions_installdebugprofileonly, Constants.Actions_installsrc, Constants.Actions_installrsrcs})
            has_valid_actions = set(self._options(Constants.Actions)).issubset(actions_subset)
            if has_valid_actions is False:
                Logger.write().error('Configuration file at path "%s" has an invalid "%s" defintion!' % (self.config_file_path, Constants.Actions))
            is_valid = has_valid_build_settings and has_valid_exports and has_valid_actions
        else:
            Logger.write().error('Configuration file at path "%s" does not have the correct headers!' % self.config_file_path)
        return is_valid

    def buildSettings(self):
        return dict(self.contents.items(Constants.BuildSettings))

    def exports(self):
        return dict(self.contents.items(Constants.Exports))

    def actions(self):
        return dict(self.contents.items(Constants.Actions))
