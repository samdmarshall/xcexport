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
from pbPlist          import pbPlist
from ..Helpers        import xcrun
from ..Helpers.Logger import Logger

if sys.version_info >= (3, 0):
    def getObjectForUnicodeKey(dictionary, key):
        return dictionary.get(key)
else:
    def getObjectForUnicodeKey(dictionary, key):
        return dictionary.get(str(key), dictionary.get(unicode(key)))

class Environment(object):

    def __init__(self):
        self.specs = list()
        self.__loadXcodeSpecFiles()

    def __findSpecsOptionsWithName(self, option_name):
        results = list()
        for spec in self.specs:
            options_list = getObjectForUnicodeKey(spec, 'Options')
            for option in options_list:
                name = getObjectForUnicodeKey(option, 'Name')
                if option_name == name:
                    results.append(option)
        return results

    def __loadXcodeSpecFiles(self):
        Logger.write().info('Looking for Xcode installation...')
        search_path = os.path.normpath(os.path.join(xcrun.resolve_developer_path(), '../Plugins'))
        search_extension = 'spec'
        found_specs = list()
        if os.path.exists(search_path) is False:
            Logger.write().error('Unable to find an installation of Xcode! Please make sure that `xcode-select` is setup correctly!')
        else:
            found_specs = [os.path.join(root, name) for root, _, files in os.walk(search_path, followlinks=False) for name in files if name.endswith(search_extension)]
            Logger.write().info('Loading Xcode specification files...')
            for spec_path in found_specs:
                specs_in_file = list()
                spec_file_contents = pbPlist.PBPlist(spec_path)
                Logger.write().debug('Found specification file at:\n> %s' % spec_path)
                contents_is_dictionary = hasattr(spec_file_contents.root, 'keys')
                if contents_is_dictionary is False:
                    contents = [dict(spec) for spec in spec_file_contents.root]
                    specs_in_file.extend(contents)
                else:
                    specs_in_file.append(spec_file_contents.root.nativeType())
                build_setting_specs = [spec for spec in specs_in_file if (spec.get('Options') or spec.get(u'Options')) is not None]
                for spec in build_setting_specs:
                    Logger.write().debug('Loading specification: "%s"...' % spec.get('Identifier', spec.get(u'Identifier')))
                if len(build_setting_specs):
                    self.specs.extend(build_setting_specs)

    def compilerFlags(self):
        results = list()
        Logger.write().info('Resolving compiler flags...')
        environment_variables = os.environ
        for env_var in environment_variables:
            found_options = self.__findSpecsOptionsWithName(env_var)
            if len(found_options):
                print(found_options)
        return results

    def linkerFlags(self):
        results = list()
        Logger.write().info('Resolving linker flags...')
        environment_variables = os.environ
        for env_var in environment_variables:
            found_options = self.__findSpecsOptionsWithName(env_var)
            if len(found_options):
                print(found_options)
        return results
