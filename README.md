# Postman-to-CSV

A CLI which consumes a Postman results file in JSON format and outputs a simple CSV file of the results.

## Installation

```shell
pip install postman-to-csv
```

## Usage

A few examples:

```shell
# Convert the JSON results to CSV without any build information
postman-to-csv \
    --input 'test-results.json' \
    --output 'test-results.csv'

# Flesh out additional information about the build
postman-to-csv \
    --input 'test-results.json' \
    --output 'test-results.csv' \
    --projectname 'my-web-api' \
    --branch 'release' \
    --buildnumber '1.2.3.4' \
    --deployenv 'stage' \
    --testtype 'integration'

# Providing all of the available flags
postman-to-csv \
    --input 'test-results.json' \
    --output 'test-results.csv' \
    --projectname 'my-test-project' \
    --branch 'release' \
    --buildnumber '1.2.3.4' \
    --buildtarget 'AnyCPU' \
    --buildstatus 'pass' \
    --deployenv 'stage' \
    --testtype 'integration'
```

## Limitations

This was built to provide a simplified data format that could be used to load the results of Postman tests into a data store for tracking and metrics. It is based on the output format from Newman 4.2.3 and contain minimal information about the test cases and assertions. If you need more complete information, I would recommend that you parse the JSON directly.

## Publishing Updates to PyPi

For the maintainer - to publish an updated version of ssm-search, increment the version number in version.py and run the following:

```shell
docker build -f ./Dockerfile.buildenv -t postman-to-csv:build .
docker run --rm -it --entrypoint make postman-to-csv:build publish
```

At the prompts, enter the username and password to the pypi.org repo.

## Testing

Test execution in a container using packaged test files.

```shell
docker build -f ./Dockerfile.buildenv -t postman-to-csv:build .
docker run -it postman-to-csv:build
postman-to-csv --input <postman JSON> --output <output file name>
```
