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
from ..Helpers        import xcrun
from ..Helpers.Logger import Logger
from ..XCSpec         import xcspec_helper
from ..XCSpec         import XCSpecCompiler

class Environment(object):

    def __init__(self):
        self.specs = list()
        self.__loadXcodeSpecFiles()
        # updating specs to point to each other and form inheritence.
        for spec_item in self.specs:
            if spec_item.basedOn is not None:
                found_specs = [spec for spec in self.specs if spec_item.basedOn == spec.identifier]
                if len(found_specs) > 0:
                    spec_item.basedOn = found_specs[0]
                else:
                    Logger.write().error('Did not find base spec for identifier "%s"' % spec_item.basedOn)

    def __findSpecsOptionsWithName(self, option_name):
        results = list()
        build_setting_specs = [spec for spec in self.specs if spec.identifier == os.environ.get('GCC_VERSION') and spec.contents.get('IsAbstract') == 'NO']
        for spec in build_setting_specs:
            Logger.write().debug('Analyzing spec "%s"...' % spec.identifier)
            build_setting_options = spec.contents.get('Options')
            if build_setting_options is not None:
                results.extend([option for option in build_setting_options if option.get('Name') == option_name])
        return results

    def __loadXcodeSpecFiles(self):
        Logger.write().info('Looking for Xcode installation...')
        search_path = os.path.normpath(os.path.join(xcrun.resolve_developer_path(), '../Plugins'))
        search_extension = 'spec'
        found_specs = list()
        if os.path.exists(search_path) is False:
            print(search_path)
            Logger.write().error('Unable to find an installation of Xcode! Please make sure that `xcode-select` is setup correctly!')
        else:
            found_specs = [os.path.join(root, name) for root, _, files in os.walk(search_path, followlinks=False) for name in files if name.endswith(search_extension)]
            Logger.write().info('Loading Xcode specification files...')
            for spec_path in found_specs:
                specs_in_file = xcspec_helper.xcspecLoadFromContentsAtPath(spec_path)
                for spec in specs_in_file:
                    Logger.write().debug('Loading specification: "%s"...' % spec.identifier)
                self.specs.extend(specs_in_file)

    def compilerFlags(self, environment_variable):
        results = list()
        Logger.write().info('Resolving compiler flags...')
        environment_variables = os.environ
        for env_var in environment_variables:
            found_options = self.__findSpecsOptionsWithName(env_var)
            options_with_flags = [option for option in found_options if option.get('CommandLineFlag') or option.get('CommandLineArgs')]
            if len(options_with_flags):
                results.extend(options_with_flags)
        for item in results:
            print(item)
        # os.environ[environment_variable] = ' '.join(results)

    def linkerFlags(self, environment_variable):
        results = list()
        Logger.write().info('Resolving linker flags...')
        environment_variables = os.environ
        os.environ[environment_variable] = ' '.join(results)
