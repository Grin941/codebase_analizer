Code base analizer
==================
[![Build Status](https://travis-ci.org/Grin941/codebase_analizer.svg?branch=master)](https://travis-ci.org/Grin941/codebase_analizer)
[![Coverage by codecov.io](https://codecov.io/gh/Grin941/codebase_analizer/branch/master/graphs/badge.svg?branch=master)](https://codecov.io/gh/Grin941/codebase_analizer?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/65bf84d5b1d79f1584f7/maintainability)](https://codeclimate.com/github/Grin941/codebase_analizer/maintainability)

Module displays most popular words found in your codebase.

## Requirements

* Python 2.7.X or 3.X

## Installation

```
$ make
```

## Usage

```
$ python codebase_analizer.py your_project_path/url_to_clone_repo_from
```

For more information type: ```$ python codebase_analizer.py -h```

## Testing
```
$ PYTHONPATH=. pytest
```
