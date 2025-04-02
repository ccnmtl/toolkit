from django.core.files.base import File, ContentFile
from django.test import TestCase
import os
from ...aboelela.process import process


class BasicTest(TestCase):
    def test_root(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_smoketest(self):
        response = self.client.get("/smoketest/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'PASS')


class AboelelaTest(TestCase):
    files = os.listdir(os.getcwd() + '/toolkit/main/tests/test_data')

    def test_files_present(self):
        self.assertIsNotNone(self.files)
        self.assertIsNot(self.files, 0)
        self.assertTrue('testItems.csv' in self.files)
        self.assertTrue('testResults.csv' in self.files)

    def test_processor(self):
        files = []
        for file in self.files:
            self.assertIn('.csv', file)
            try:
                test_data = File(open(
                    f'{os.getcwd()}/toolkit/main/tests/test_data/{file}',
                    'rb+'), file)
                self.assertEqual(file, test_data.name)
                files.append(test_data)
            except OSError as e:
                print(e)
        self.assertEqual(len(files), 2)
        processed = process(files, False)
        self.assertIsInstance(processed, ContentFile)
        processed.open('r')
        # [:-2] to slice off the \r\n characters
        headers = processed.readline()[:-2]
        target = ','.join(['UNI (ID)', 'Bloom Level', 'Category', 'Max Score',
                           'Student Score', '% Correct'])
        self.assertEqual(headers, target)
