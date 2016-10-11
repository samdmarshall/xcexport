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
from pbPlist          import pbPlist
from ..Helpers.Logger import Logger
from .xcspec_resolver import xcspec_resolver

def xcspecLoadFromContentsAtPath(spec_path):
    items = list()
    if spec_path.endswith('spec'):
        contents = pbPlist.PBPlist(spec_path).root;
        Logger.write().debug('Loading spec at path:\n> %s' % spec_path)
        if contents is not None:
            if hasattr(contents, 'keys'):
                if spec_path.endswith('pbfilespec') and 'Type' not in contents.keys():
                    contents['Type'] = 'FileType';
                constructor = xcspec_resolver(contents);
                if constructor[0] is True:
                    items.append(constructor[1](contents));
                else:
                    Logger.write().warn('Tried to load spec file at "%s" but could not resolve type' % spec_path);
            else:
                for spec_item in contents:
                    if spec_path.endswith('pbfilespec') and 'Type' not in spec_item.keys():
                        spec_item['Type'] = 'FileType';
                    constructor = xcspec_resolver(spec_item);
                    if constructor[0] is True:
                        items.append(constructor[1](spec_item));
                    else:
                        Logger.write().warn('Tried to load spec file at "%s" but could not resolve type' % spec_path);
                if len(contents) == 0:
                    Logger.write().warn('No specs loaded from file at "%s"' % spec_path); 
    return items;