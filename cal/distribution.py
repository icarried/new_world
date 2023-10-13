import random
import bisect

# 构建一个类，代表离散型随机变量的正态分布，包含以下属性：均值、方差、样本数
class SingleNormalDistribution:
    def __init__(self, mean, variance, sample_num):
        self.mean = mean
        self.variance = variance
        self.sample_num = sample_num

    def __str__(self):
        return "mean: " + str(self.mean) + ", variance: " + str(self.variance) + ", sample_num: " + str(self.sample_num)
    
    def __repr__(self):
        return self.__str__()
    
    # 两个正态分布相加
    def __add__(self, other):
        mean = (self.mean * self.sample_num + other.mean * other.sample_num) / (self.sample_num + other.sample_num)
        variance = (self.variance * self.sample_num + other.variance * other.sample_num) / (self.sample_num + other.sample_num) + (self.mean - other.mean) ** 2 * self.sample_num * other.sample_num / (self.sample_num + other.sample_num) ** 2
        sample_num = self.sample_num + other.sample_num
        return SingleNormalDistribution(mean, variance, sample_num)
    
    # 从该正态分布中分离一个正态分布（减法）
    def __sub__(self, other):
        if other.sample_num > self.sample_num:
            raise Exception("sample_num should be less than self.sample_num")
        elif other.sample_num == self.sample_num:
            return SingleNormalDistribution(0, 0, 0)
        else:
            sample_num = self.sample_num - other.sample_num
            mean = (self.mean * self.sample_num - other.mean * other.sample_num) / (sample_num)
            variance = (self.variance * self.sample_num - other.variance * other.sample_num) / (sample_num) + (self.mean - other.mean) ** 2 * self.sample_num * other.sample_num / (sample_num) ** 2
            return SingleNormalDistribution(mean, variance, sample_num)
        
    # 从该正态分布中取样
    def sample(self):
        return random.normalvariate(self.mean, self.variance ** 0.5)
    

# 构建一个类，代表多个正态分布的混合分布，包含以下属性：正态分布列表
class MixtureDistribution:
    def __init__(self, distribution_list):
        self.distribution_list = distribution_list

    def __str__(self):
        return "distribution_list: " + [str(distribution) for distribution in self.distribution_list]
    
    def __repr__(self):
        return self.__str__()
    
    # 两个混合分布相加
    def __add__(self, other):
        distribution_list = self.distribution_list + other.distribution_list
        return MixtureDistribution(distribution_list)
    
    # 混合分布内的正态分布合成为一个正态分布，返回该正态分布
    def merge(self):
        merge_distribution = SingleNormalDistribution(0, 0, 0)
        for distribution in self.distribution_list:
            merge_distribution += distribution
        return merge_distribution
    
    # 从混合分布中取样，从列表中的正态分布取样的概率与正态分布的样本数成正比
    # 优化方法是预先计算每个分布的累积分布函数（CDF），然后使用二分查找来高效地从混合分布中取样
    def sample(self, sample_num):
        sample_list = []
        for i in range(sample_num):
            u = random.random()
            j = bisect.bisect_left(self.cdf, u)
            sample_distribution = self.distribution_list[j]
            sample_list.append(sample_distribution.sample())
        return sample_list
    
