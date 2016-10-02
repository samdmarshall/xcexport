xcexport 
========

[![Code Climate](https://img.shields.io/codeclimate/github/samdmarshall/xcexport.svg)](https://codeclimate.com/github/samdmarshall/xcexport)
[![Test Coverage](https://img.shields.io/codeclimate/coverage/github/samdmarshall/xcexport.svg)](https://codeclimate.com/github/samdmarshall/xcexport/coverage)
[![CircleCI branch](https://img.shields.io/circleci/project/samdmarshall/xcexport/develop.svg)](https://circleci.com/gh/samdmarshall/xcexport/tree/develop)
[![Dependency Status](https://dependencyci.com/github/samdmarshall/xcexport/badge)](https://dependencyci.com/github/samdmarshall/xcexport)

**xcexport** is a tool for external build system targets in Xcode. It will examine the environment variables that are exported by Xcode when executing an external build system target and resolve the exported build settings into their corresponding compiler and linker flags.


## Contributing and Code of Conduct [![License](https://img.shields.io/badge/License-3--Clause%20BSD-blue.svg)](./LICENSE)
This project and related material has a Code of Conduct that is listed in the [contributing.md](./contributing.md) file. This must be read and adhered to when interacting with this project. Additionally this code is released under a 3-clause BSD license that you can read [here](./LICENSE).


## Requirements ![Python](https://img.shields.io/badge/Python2-2.7.10-brightgreen.svg) ![Python](https://img.shields.io/badge/Python3-3.5.0-brightgreen.svg)
This tool is built and tested against Python 2.7.10 and 3.5.0.


## Installation  [![homebrew](https://img.shields.io/badge/homebrew-HEAD-orange.svg)](https://github.com/samdmarshall/homebrew-formulae)
Via [homebrew](http://brew.sh):

	$ brew update
	$ brew tap samdmarshall/formulae
	$ brew install samdmarshall/formulae/xcexport

To install the tool from the repo, clone from Github then run the respective `make` command for the desired version.

### Installing for Python 2

	$ make build2

### Installing for Python 3

	$ make build3


## Usage
To use **xcexport**:

	$ xcexport <file path to the configuration file>

There are a number of flags that can be passed to modify the behavior of **xcexport**:

   Flags | Usage
-------------------|-----------------------------------------------------------
`--version`        | Displays the version of **xcexport** and exits
`--quiet`          | Silences all logging output
`--verbose`        | Logs additional information


