Code base analizer
==================
[![Build Status](https://travis-ci.org/Grin941/codebase_analizer.svg?branch=master)](https://travis-ci.org/Grin941/codebase_analizer)

Module displays most popular words found in your codebase.

Only verbs in function names are handling in a current version.

## Requirements

* Python 2.X or 3.X

## Installation

```
$ pip install -r requirements.txt
$ python setup.py install
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
