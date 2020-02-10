import os
import pickle
import unittest

from tests.utils import TEST_FIXTURE_PATH


class TestRun(unittest.TestCase):

    def test_run_container(self):
        with open(os.path.join(TEST_FIXTURE_PATH, 'run_container/input/1581363101667_args.pkl'), 'rb') as in_data:
            data = pickle.load(in_data)
            print(data)
