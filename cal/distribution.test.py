import unittest
from distribution import SingleNormalDistribution

class TestSingleNormalDistribution(unittest.TestCase):
    def setUp(self):
        self.distribution1 = SingleNormalDistribution(10, 4, 100)
        self.distribution2 = SingleNormalDistribution(20, 9, 200)

    def test_init(self):
        self.assertEqual(self.distribution1.mean, 10)
        self.assertEqual(self.distribution1.variance, 4)
        self.assertEqual(self.distribution1.sample_num, 100)

    def test_str(self):
        self.assertEqual(str(self.distribution1), "mean: 10, variance: 4, sample_num: 100")

    def test_add(self):
        distribution3 = self.distribution1 + self.distribution2
        self.assertEqual(distribution3.mean, 15)
        self.assertEqual(distribution3.variance, 6.75)
        self.assertEqual(distribution3.sample_num, 300)

if __name__ == '__main__':
    # unittest.main()
    distribution1 = SingleNormalDistribution(15, 4, 150)
    distribution2 = SingleNormalDistribution(15, 4, 100)
    distribution3 = distribution1 - distribution2
    print(distribution3)
