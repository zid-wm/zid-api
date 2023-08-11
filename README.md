# vZID ARTCC API

## Introduction

The vZID ARTCC API is meant to serve as a backend system to service the vZID website, Discord server, training system, and more. The backend is written primarily in Python using the Django framework.

## Local Development

### Prerequisites

Developers will need to meet the following requirements prior to local development:

- Have Python and Pip installed on your system. The easiest way to manage various versions of Python on your system is 
to use [Pyenv](https://github.com/pyenv/pyenv), for which installation instructions can be found
[here](https://github.com/pyenv/pyenv#installation). If you are not able to use Pyenv, make sure that 
Python 3.11.4 is installed.

- The vZID API uses [Pipenv](https://pipenv.pypa.io/en/latest/) as a package manager. Once you have installed Python
on your system, run the following command to install Pipenv:
```shell
pip install --user pipenv
```

### Initial Setup

#### Configuration Files

For local development, the API uses a combination of two files: a `.env` file, and a `*-properties.yml` file. 
The `*-properties.yml` file contains most configuration items, with the `.env` file loaded when Pipenv starts 
to let the program know where to look for the properties file. Both files should be placed in the root directory.
**Neither of these files should EVER be committed to source control.**

```dotenv
# SAMPLE .env FILE

# ENVIRONMENT must be set. The best practice is to set it to "local".
ENVIRONMENT=local

# USE_SQLITE is an optional parameter, if you would like to use the more 
# lightweight Sqlite database for local testing. The default value is False.
# If not set, the API will default to Postgresql.
USE_SQLITE=True
```

```yaml
# Sample *-properties.yml file
# The wildcard character must be replaced with the ENVIRONMENT value set in .env

# The only top-level value should be zid
zid:
  local: # Must also match ENVIRONMENT value set in .env
    website_domain: zidartcc.org # Base domain of the site--"localhost" is perfectly valid for local testing
    secret_key: "abc123" # Django secret key--generate a random key and place it here

    db: # Database parameters--optional if USE_SQLITE=True in .env file
      host: 127.0.0.1 # 127.0.0.1 or localhost if running Postgresql locally
      port: 5432 # Postgresql default port is 5432
      name: zidartcc # Name of the database--must be created before running the API
      user: ziduser # Master username--must be created before running the API
      password: zidpassword # Master password

    vatusa:
      url: "https://api.vatusa.net/v2" # VATUSA API base URL
      key: "abc123" # VATUSA API key (non-production key should be used when testing)

    # List all towered fields. List must be enclosed in double quotes (") and
    # each field should be enclosed in single quotes (').
    controlled_fields: "['ABC', 'DEF', 'GHI']"
```

There is a file named `github-properties.yml` which is committed to source control. This is used for pull request 
checks and should not be modified or deleted unless an additional parameter is required to test.

#### Starting the Server
Install all required python packages. If you're using Pyenv, this command will automatically install and select 
Python 3.11.4 as the version.
```shell
pipenv install --dev
``` 

Make and apply the initial migrations to your local database.
```shell
pipenv run python manage.py makemigrations
pipenv run python manage.py migrate
```

Start the development server. To run the server on the default port (8000), run `pipenv run server`. To manually
select a port, run `pipenv run server ####`, where `####` is the port.

### Testing

The vZID API uses PyTest for unit testing. Code coverage is enforced and all pull requests to `main` must have a 
minimum of 80% coverage (as well as 100% of tests passing).

To run all unit tests, use the following command:
```shell
pipenv run test
```

PyLint is used to lint files and enforce code quality. All pull requests to `main` must have a minimum PyLint 
score of 8.0. To run PyLint, use the following command:
```shell
pipenv run lint
```

## Contributing

Contributions are always welcome and encouraged. Changes should be made on a personal fork of the repository, and
a pull request to `main` should be opened.

Certain checks are run on all pull requests to the `main` branch. All pull requests must meet the following 
requirements:

- No merge conflicts
- 100% of unit tests pass
- Code coverage during unit tests a minimum of 80%
- PyLint score a minimum of 8.0
- One approval from a vZID ARTCC web team member with repository write access
