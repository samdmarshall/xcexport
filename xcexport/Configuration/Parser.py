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
if sys.version_info >= (3, 0):
    import configparser as ConfigParserCompat
else:
    import ConfigParser as ConfigParserCompat
from .                           import Constants
from ..Helpers.OrderedDictionary import OrderedDictionary
from ..Helpers.Logger            import Logger

class Parser(object):

    def __init__(self, file_path):
        self.config_file_path = os.path.normpath(file_path)
        self.contents = None
        if os.path.exists(self.config_file_path) is True:
            self.contents = ConfigParserCompat.ConfigParser(dict_type=OrderedDictionary)
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
        has_valid_sections = set(self._sections()) == set({Constants.BuildSettings, Constants.Exportables, Constants.Runnables})
        if has_valid_sections is True:
            has_valid_build_settings = set(self._options(Constants.BuildSettings)) == set({Constants.BuildSettings_export})
            if has_valid_build_settings is False:
                Logger.write().error('Configuration file at path "%s" has an invalid "%s" defintion!' % (self.config_file_path, Constants.BuildSettings))
            has_valid_exportables = set(self._options(Constants.Exportables)) == set({Constants.Exportables_compiler, Constants.Exportables_linker})
            if has_valid_exportables is False:
                Logger.write().error('Configuration file at path "%s" has an invalid "%s" defintion!' % (self.config_file_path, Constants.Exportables))
            has_valid_runnables = set(self._options(Constants.Runnables)) == set({Constants.Runnables_tool})
            if has_valid_runnables is False:
                Logger.write().error('Configuration file at path "%s" has an invalid "%s" defintion!' % (self.config_file_path, Constants.Runnables))
            is_valid = has_valid_build_settings and has_valid_exportables and has_valid_runnables
        else:
            Logger.write().error('Configuration file at path "%s" does not have the correct headers!' % self.config_file_path)
        return is_valid

    def buildSettings(self):
        return dict(self.contents.items(Constants.BuildSettings))

    def exportables(self):
        return dict(self.contents.items(Constants.Exportables))

    def runnables(self):
        return dict(self.contents.items(Constants.Runnables))
