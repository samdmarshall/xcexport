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

class xcspec(object):
    
    def __init__(self, spec_data):
        self.contents = spec_data;
        self.identifier = '';
        self.type = '';
        self.name = '';
        self.basedOn = None;
        if 'Identifier' in self.keys():
            self.identifier = str(self.contents['Identifier'])
        if 'Type' in self.keys():
            self.type = self.contents['Type']
        if 'Name' in self.keys():
            self.name = self.contents['Name']
        if 'BasedOn' in self.keys():
            self.basedOn = self.contents['BasedOn']
    
    def __attrs(self):
        return (self.identifier, self.type)
    
    def __repr__(self):
        return '(%s : %s : %s)' % (type(self), self.name, self.identifier)
    
    def __eq__(self, other):
        return isinstance(other, type(self)) and self.identifier == other.identifier and self.type == other.type
    
    def __hash__(self):
        return hash(self.__attrs())
    
    def isValid(self):
        return self.contents is not None
    
    def hasKeys(self):
        if self.isValid():
            return hasattr(self.contents, 'keys')
        else:
            return False
    
    def keys(self):
        results = list()
        if not self.isValid():
            return results
        if self.hasKeys():
            return self.contents.keys()
        else:
            return results
    
    def valueForKey(self, key):
        value = None
        if not self.isValid():
            return value
        if self.hasKeys():
            value = self.contents.get(key)
        return value
    
    def inheritedTypes(self):
        types = [str(self.identifier)];
        if self.basedOn is not None:
            parent = self.basedOn.inheritedTypes()
            types.extend(parent)
        return types