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
import shlex
import argparse
from .version              import __version__ as XCEXPORT_VERSION
from .Helpers.Logger       import Logger
from .                     import Configuration
from .Configuration.Parser import Parser
from .Resolver.Environment import Environment
from .Helpers              import Executor

# Main
def main(argv=sys.argv[1:]):
    # setup the argument parsing
    parser = argparse.ArgumentParser(description='Tool for Xcode External Build System Targets')
    parser.add_argument(
        '--version',
        help='Displays the version information',
        action='version',
        version=XCEXPORT_VERSION
    )
    parser.add_argument(
        'config_file',
        metavar='<path>',
        help='Path to the pyconfig file to use to generate a xcconfig file',
    )
    parser.add_argument(
        '--quiet',
        help='Silences all logging output',
        default=False,
        action='store_true'
    )
    parser.add_argument(
        '--verbose',
        help='Adds verbosity to logging output',
        default=False,
        action='store_true'
    )
    parser.add_argument(
        '--no-ansi',
        help='Disables the ANSI color codes as part of the logger',
        default=False,
        action='store_true'
    )
    parser.add_argument(
        '--debug',
        help=argparse.SUPPRESS,
        default=False,
        action='store_true'
    )
    args = parser.parse_args(argv)

    # perform the logging modifications before we do any other operations
    Logger.disableANSI(args.no_ansi)
    Logger.enableDebugLogger(args.debug)
    Logger.isVerbose(args.verbose)
    Logger.isSilent(args.quiet)

    if args.config_file is not None:
        config_parser = Parser(args.config_file)

        working_env = Environment()

        working_env.compilerFlags(config_parser.exports().get(Configuration.Constants.Exports_compiler))
        working_env.linkerFlags(config_parser.exports().get(Configuration.Constants.Exports_linker))

        if os.environ.get('ACTION') is None:
            Logger.write().error('no ACTION variable defined in the inherited environment, please ensure that xcexport is run from within Xcode!')
            sys.exit()

        execution_action = os.environ['ACTION']
        if execution_action == '':
            execution_action = 'build'

        command = shlex.split(config_parser.actions()[execution_action])
        if os.fork() == 0:  
            os.execvp(command[0], command)
        else:
            os.wait()

if __name__ == "__main__": # pragma: no cover
    main()
