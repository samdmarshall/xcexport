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

from __future__           import absolute_import
from .xcspec              import *
from ..Helpers.Logger     import Logger
from .XCSpecCompiler      import *
from .XCSpecProductType   import *
from .XCSpecBuildStep     import *
from .XCSpecBuildSettings import *
from .XCSpecFileType      import *
from .XCSpecTool          import *
from .XCSpecLinker        import *
from .XCSpecBuildPhase    import *
from .XCSpecBuildSystem   import *
from .XCSpecPackageType   import *
from .XCSpecArchitecture  import *


XCSPEC_TYPE_RESOLVER = {
    'Compiler': XCSpecCompiler,
    'ProductType': XCSpecProductType,
    'BuildStep': XCSpecBuildStep,
    'BuildSettings': XCSpecBuildSettings,
    'FileType': XCSpecFileType,
    'Tool': XCSpecTool,
    'Linker': XCSpecLinker,
    'BuildPhase': XCSpecBuildPhase,
    'BuildSystem': XCSpecBuildSystem,
    'Architecture': XCSpecArchitecture,
    'PackageType': XCSpecPackageType,
};

def xcspec_resolver(dictionary):
    global XCSPEC_TYPE_RESOLVER;
    if dictionary['Type'] in XCSPEC_TYPE_RESOLVER.keys():
        return (True, XCSPEC_TYPE_RESOLVER[dictionary['Type']]);
    else:
        Logger.write().warning('UNKNOWN "%s" TYPE!' % dictionary['Type']);
    return (False, None);