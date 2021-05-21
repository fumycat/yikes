import unittest
import datetime
from subprocess import CalledProcessError
from contextlib import ExitStack
from main import process_matrix_mult

class MatrixMultErrorsTestCase(unittest.TestCase):
    def test_bad_dim(self):
        with self.assertRaises(CalledProcessError):
            with ExitStack() as stack:
                files = [stack.enter_context(open(fname)) for fname in ['test_cases/file0.txt', 'test_cases/tc_2.txt']]
                process_matrix_mult((files[0].read(), files[1].read()))

    def test_no_errors(self):
        with ExitStack() as stack:
            files = [stack.enter_context(open(fname)) for fname in ['test_cases/file0.txt', 'test_cases/file1.txt']]
            x = process_matrix_mult((files[0].read(), files[1].read()))
            self.assertTrue(x)


if __name__ == '__main__':
    unittest.main()
