import unittest
import subprocess

class TestAppRuns(unittest.TestCase):
    def test_a30000b1(self):
        output = subprocess.check_output("python run_model.py --likelihood-matrix ./dev/a30000b1.lik --phonemes ./dicos/phonemes --zre-dict ./dicos/zre.dict", shell=True)
        results = []
        for i, item in enumerate(output.split('\n')):
            if item != '':
                results.append(item.split()[0])

        ground_truth = ['nula','jedna','t\xf8i','\xe8ty\xf8i','dev\xect','p\xect','osm','sedm','\xb9est']

        try:
            for i in range(len(ground_truth)):
                self.assertEqual(ground_truth[i], results[i])

        except:
            for i, item in enumerate(map(None, ground_truth, results)):
                print(i, item)
            raise

    def test_a30001b1(self):
        output = subprocess.check_output("python run_model.py --likelihood-matrix ./dev/a30001b1.lik --phonemes ./dicos/phonemes --zre-dict ./dicos/zre.dict", shell=True)
        results = []
        for i, item in enumerate(output.split('\n')):
            if item != '':
                results.append(item.split()[0])

        ground_truth = ['dev\xect','p\xect','dva','\xb9est','sedm','osm','jedna','t\xf8i','nula','\xe8ty\xf8i']

        try:
            for i in range(len(ground_truth)):
                self.assertEqual(ground_truth[i], results[i])

        except:
            for i, item in enumerate(map(None, ground_truth, results)):
                print(i, item)
            raise

    def test_a30002b1(self):
        output = subprocess.check_output("python run_model.py --likelihood-matrix ./dev/a30002b1.lik --phonemes ./dicos/phonemes --zre-dict ./dicos/zre.dict", shell=True)
        results = []
        for i, item in enumerate(output.split('\n')):
            if item != '':
                results.append(item.split()[0])

        ground_truth = ['jedna','\xe8ty\xf8i','dev\xect','nula','\xb9est','dva','p\xect','sedm','t\xf8i','osm']

        try:
            for i in range(len(ground_truth)):
                self.assertEqual(ground_truth[i], results[i])

        except:
            for i, item in enumerate(map(None, ground_truth, results)):
                print(i, item)
            raise

    def test_a30003b1(self):
        output = subprocess.check_output("python run_model.py --likelihood-matrix ./dev/a30003b1.lik --phonemes ./dicos/phonemes --zre-dict ./dicos/zre.dict", shell=True)
        results = []
        for i, item in enumerate(output.split('\n')):
            if item != '':
                results.append(item.split()[0])

        ground_truth = ['\xb9est','osm','jedna','t\xf8i','nula','p\xect','sedm','dva','\xe8ty\xf8i','dev\xect']

        try:
            for i in range(len(ground_truth)):
                self.assertEqual(ground_truth[i], results[i])

        except:
            for i, item in enumerate(map(None, ground_truth, results)):
                print(i, item)
            raise

    def test_a30004b1(self):
        output = subprocess.check_output("python run_model.py --likelihood-matrix ./dev/a30004b1.lik --phonemes ./dicos/phonemes --zre-dict ./dicos/zre.dict", shell=True)
        results = []
        for i, item in enumerate(output.split('\n')):
            if item != '':
                results.append(item.split()[0])

        ground_truth = ['\xe8ty\xf8i','jedna','\xb9est','t\xf8i','p\xect','osm','dev\xect','dva','sedm','nula']

        try:
            for i in range(len(ground_truth)):
                self.assertEqual(ground_truth[i], results[i])

        except:
            for i, item in enumerate(map(None, ground_truth, results)):
                print(i, item)
            raise

if __name__ == "__main__":
    unittest.main()
