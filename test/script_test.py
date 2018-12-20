import subprocess
import unittest


class TestPostmanToCsv(unittest.TestCase):

#
# Setup and teardown
#

    def setUp(self):
        pass

    def tearDown(self):
        pass


#
# Tests
#

    def test_missing_input_parameter(self):
        command = [
            'postman-to-csv',
            '--output', './test-cases/test.csv'
        ]
        result = subprocess.call(command)
        self.assertEqual(result, 2, "Expected return code 2 for missing required parameter --input")


    def test_missing_output_parameter(self):
        command = [
            'postman-to-csv',
            '--input', './test-cases/test_results.json'
        ]
        result = subprocess.call(command)
        self.assertEqual(result, 2, "Expected return code 2 for missing required parameter --output")


    def test_missing_input_file(self):
        command = [
            'postman-to-csv',
            '--input', './test-cases/missing.json',
            '--output', './test-cases/missing.csv'
        ]
        result = subprocess.call(command)
        self.assertEqual(result, 31, "Expected return code 31 for missing input file")


    def test_not_json_input_file(self):
        command = [
            'postman-to-csv',
            '--input', './test-cases/not_json.txt',
            '--output', './test-cases/not_json.csv'
        ]
        result = subprocess.call(command)
        self.assertEqual(result, 32, "Expect error code 32 for a non-JSON input file")


    def test_no_run_block_input_file(self):
        command = [
            'postman-to-csv',
            '--input', './test-cases/no_run_block.json',
            '--output', './test-cases/no_run_block.csv'
        ]
        result = subprocess.call(command)
        self.assertEqual(result, 33, "Expect error code 33 for an input file without a run block")


    def test_no_executions_block_input_file(self):
        command = [
            'postman-to-csv',
            '--input', './test-cases/no_executions_block.json',
            '--output', './test-cases/no_executions_block.csv'
        ]
        result = subprocess.call(command)
        self.assertEqual(result, 34, "Expect error code 34 for an input file without an executions block within the run block")


    def test_invalid_output_file(self):
        command = [
            'postman-to-csv',
            '--input', './test-cases/test_results.json',
            '--output', '/not-a-folder/missing.csv'
        ]
        result = subprocess.call(command)
        self.assertEqual(result, 4, "Expected return code 4 for invalid output file")


    def test_input_file_exists(self):
        command = [
            'postman-to-csv',
            '--input', './test-cases/test_results.json',
            '--output', './test-cases/output.csv'
        ]
        result = subprocess.call(command)
        self.assertEqual(result, 0, "Expected return code 0 for a valid input file")


    def test_script_results(self):
        command = [
            'postman-to-csv',
            '--input', './test-cases/test_results.json',
            '--output', './test-cases/output.csv',
            '--projectname', 'my-test-project',
            '--branch', 'release',
            '--buildnumber', '1.2.3.4',
            '--buildtarget', 'AnyCPU',
            '--buildstatus', 'pass',
            '--deployenv', 'stage',
            '--testtype', 'integration'
        ]
        subprocess.call(command)
        with open('./test-cases/output.csv', 'r') as output_file:
            output = output_file.read()
        with open('./test-cases/expected.csv', 'r') as expected_file:
            expected = expected_file.read()
        self.assertEqual(len(output), len(expected), "Length of generated output did not match expected")
