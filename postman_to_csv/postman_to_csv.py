# -*- coding: utf-8 -*-

import argparse
import csv
import datetime
import json
import os
import sys


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='Path to the Postman results file to parse')
    parser.add_argument('--output', required=True, help='Path to the CSV file that will be generated')
    parser.add_argument('--projectname', required=False, help='Project being tested')
    parser.add_argument('--branch', required=False, help='Branch being tested')
    parser.add_argument('--buildnumber', required=False, help='Build number being tested')
    parser.add_argument('--buildtarget', required=False, help='Build target being tested')
    parser.add_argument('--buildstatus', required=False, help='Status of the build')
    parser.add_argument('--deployenv', required=False, help='Environment that the build is being deployed to')
    parser.add_argument('--testtype', required=False, help='Type of test being executed')
    return parser


def read_test_results_file(input_file):
    try:
        with open(input_file, 'r') as test_results_file:
            test_results = json.load(test_results_file)
    except IOError as error:
        print('Unable to open input file ' + input_file + ': ' + error.strerror)
        sys.exit(31)
    except json.decoder.JSONDecodeError as error:
        print('Unable to decode input file ' + input_file + ': ' + str(error))
        sys.exit(32)

    if 'run' not in test_results:
        print('No run property found in input data')
        sys.exit(33)

    if 'executions' not in test_results['run']:
        print('No run.executions property found in input data')
        sys.exit(34)

    return test_results


def build_header():
    return [
        'Run Date',
        'Test Type',
        'Project Name',
        'Branch',
        'Build Number',
        'Build Status',
        'Build Target',
        'Deploy Environment',
        'Testing Application',
        'Test Step',
        'Assertion',
        'Result',
        'Error Message'
    ]


def build_detail(run_date, args, execution, assertion):
    if 'error' not in assertion:
        return [
            run_date, 
            args.testtype, 
            args.projectname, 
            args.branch, 
            args.buildnumber, 
            args.buildstatus, 
            args.buildtarget, 
            args.deployenv, 
            'postman', 
            execution['item']['name'], 
            assertion['assertion'], 
            'PASSED',
            '-'
        ]
    else:
        return [
            run_date, 
            args.testtype, 
            args.projectname, 
            args.branch, 
            args.buildnumber, 
            args.buildstatus, 
            args.buildtarget, 
            args.deployenv, 
            'postman', 
            execution['item']['name'], 
            assertion['assertion'], 
            'FAIL', 
            assertion['error']['message']
        ]


def main():
    here = os.path.abspath(os.path.dirname(__file__))
    about = {}
    with open(os.path.join(here, 'version.py'), 'r') as f:
        exec(f.read(), about)

    print('Postman to CSV version {}'.format(about['__version__']))

    parser = create_parser()
    args = parser.parse_args()

    test_results = read_test_results_file(args.input)
    run_date = datetime.datetime.utcnow().replace(microsecond = 0, tzinfo=datetime.timezone.utc).isoformat()

    try:
        with open(args.output, 'w') as output_file:
            file_writer = csv.writer(output_file, delimiter=',', quoting=csv.QUOTE_ALL, lineterminator='\n')
            stdout_writer = csv.writer(sys.stdout, delimiter=',', quoting=csv.QUOTE_ALL)
            
            header = build_header()
            file_writer.writerow(header)
            stdout_writer.writerow(header)

            for execution in test_results['run']['executions']:

                if 'assertions' not in execution:
                    print('No assertions found in execution ' + execution['item']['name'])
                    continue

                for assertion in execution['assertions']:
                    csv_detail = build_detail(run_date, args, execution, assertion)
                    stdout_writer.writerow(csv_detail)
                    file_writer.writerow(csv_detail)
    except IOError as error:
        print('Unable to write to output file ' + args.output + ': ' + error.strerror)
        sys.exit(4)
    except:
        error = sys.exc_info()[0]
        print('Unexpected error: ' + error)
        sys.exit(5)
