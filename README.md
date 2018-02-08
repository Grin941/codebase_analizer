Code base analizer
==================
[![Build Status](https://travis-ci.org/Grin941/codebase_analizer.svg?branch=master)](https://travis-ci.org/Grin941/codebase_analizer)
[![Coverage by codecov.io](https://codecov.io/gh/Grin941/codebase_analizer/branch/master/graphs/badge.svg?branch=master)](https://codecov.io/gh/Grin941/codebase_analizer?branch=master)

Module displays most popular words found in your codebase.

Only verbs in function names are handling in a current version.

## Requirements

* Python 2.7.X or 3.X

## Installation

```
$ make
```

## Usage

```
$ python code_base_analizer.py your_project_path
```

For more information type: ```$ python code_base_analizer.py -h```

## Testing
```
$ PYTHONPATH=. pytest
```
