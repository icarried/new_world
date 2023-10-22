import unittest
from distribution import MixtureDistribution, SingleNormalDistribution
import matplotlib.pyplot as plt

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
        self.assertEqual(distribution3.mean, 15) # 断言两个正态分布相加后的均值
        self.assertEqual(distribution3.variance, 6.75) # 断言两个正态分布相加后的方差
        self.assertEqual(distribution3.sample_num, 300)

if __name__ == '__main__':
    # unittest.main()
    distribution1 = SingleNormalDistribution(15, 4, 10)
    distribution2 = SingleNormalDistribution(5, 7, 100)
    Mix1 = MixtureDistribution([distribution1, distribution2])
    distribution3 = SingleNormalDistribution(32, 4, 200)
    Mix2 = MixtureDistribution([Mix1, distribution3])
    print(Mix2.sample(9))
    
    # 绘制直方图进行验证
    plt.hist(Mix2.sample(10000), bins=100)
    plt.show()
   
