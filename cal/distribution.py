import random
import bisect
import math
import scipy.integrate as integrate
from scipy.stats import norm, chi2
from typing import Union


# 构建一个类，其他的类都继承于该类，包含以下属性：样本数
class Distribution:
    def __init__(self, sample_num):
        self.sample_num = sample_num

    def __str__(self):
        return "sample_num: " + str(self.sample_num)

    def __repr__(self):
        return self.__str__()

    # 两个分布相加
    def __add__(self, other):
        sample_num = self.sample_num + other.sample_num
        return Distribution(sample_num)

    # 从该分布中分离一个分布（减法）
    def __sub__(self, other):
        if other.sample_num > self.sample_num:
            raise Exception("sample_num should be less than self.sample_num") # 限制其他的样本数不能超过自己的样本数，否则抛出异常
        elif other.sample_num == self.sample_num:
            return Distribution(0)
        else:
            sample_num = self.sample_num - other.sample_num
            return Distribution(sample_num)

    def pdf(self, x):
        """概率密度函数"""
        pass

    def cdf(self, x):
        """累积分布函数, 返回x的累积概率, 即pdf的积分"""
        pass

    def inverse_cdf(self, p):
        """反向累积分布函数, 返回累积概率为p的x, 即cdf的逆函数"""
        pass

    def sample(self, sample_num):
        """从该分布中取样"""
        pass


# 构建一个类，继承基类，代表离散型随机变量的正态分布，包含以下属性：均值、方差、样本数
class SingleNormalDistribution(Distribution):
    def __init__(self, mean, variance, sample_num):
        """
        :param mean: 均值
        :param variance: 方差
        :param sample_num: 样本数
        """
        super().__init__(sample_num)
        self.mean = mean # 均值
        self.variance = variance # 方差

    def __str__(self):
        return "mean: " + str(self.mean) + ", variance: " + str(self.variance) + ", sample_num: " + str(self.sample_num)

    def __repr__(self):
        return self.__str__()

    # 两个正态分布相加
    def __add__(self, other):
        mean = (self.mean * self.sample_num + other.mean * other.sample_num) / (self.sample_num + other.sample_num)
        variance = (self.variance * self.sample_num + other.variance * other.sample_num) / (
                    self.sample_num + other.sample_num) + (
                               self.mean - other.mean) ** 2 * self.sample_num * other.sample_num / (
                               self.sample_num + other.sample_num) ** 2
        sample_num = self.sample_num + other.sample_num
        return SingleNormalDistribution(mean, variance, sample_num)

    # 从该正态分布中分离一个正态分布（减法）
    def __sub__(self, other):
        if other.sample_num > self.sample_num:
            raise Exception("sample_num should be less than self.sample_num") # 限制其他的样本数不能超过自己的样本数，否则抛出异常
        elif other.sample_num == self.sample_num:
            return SingleNormalDistribution(0, 0, 0)
        else:
            sample_num = self.sample_num - other.sample_num
            mean = (self.mean * self.sample_num - other.mean * other.sample_num) / (sample_num)
            variance = (self.variance * self.sample_num - other.variance * other.sample_num) / (sample_num) + (
                        self.mean - other.mean) ** 2 * self.sample_num * other.sample_num / (sample_num) ** 2
            return SingleNormalDistribution(mean, variance, sample_num)
        
    def pdf(self, x):
        """概率密度函数"""
        return 1 / (self.variance ** 0.5 * 2 * math.pi) * math.exp(-(x - self.mean) ** 2 / (2 * self.variance))
    
    def cdf(self, x):
        """累积分布函数"""
        return norm.cdf(x, self.mean, self.variance ** 0.5)
    
    def inverse_cdf(self, p):
        """反向累积分布函数"""
        return norm.ppf(p, self.mean, self.variance ** 0.5)

    def sample(self, num):
        """从该正态分布中取样"""
        samples = []
        for i in range(num):
            u = random.random()
            x = self.inverse_cdf(u)
            samples.append(x)
        return samples


# 构建一个类，继承基类，代表卡方分布，包含以下属性：自由度、样本数
class ChiSquareDistribution(Distribution):
    def __init__(self, dof, sample_num):
        """
        :param dof: 自由度
        :param sample_num: 样本数
        """
        super().__init__(sample_num)
        self.dof = dof # 自由度

    def __str__(self):
        return "dof: " + str(self.dof) + ", sample_num: " + str(self.sample_num)

    def __repr__(self):
        return self.__str__()

    # 两个卡方分布相加
    def __add__(self, other):
        # 自由度加权相加
        dof = self.sample_num / (self.sample_num + other.sample_num) * self.dof + other.sample_num / (self.sample_num + other.sample_num) * other.dof
        sample_num = self.sample_num + other.sample_num
        return ChiSquareDistribution(dof, sample_num)

    # 从该卡方分布中分离一个卡方分布（减法）
    def __sub__(self, other):
        if other.sample_num > self.sample_num:
            raise Exception("sample_num should be less than self.sample_num") # 限制其他的样本数不能超过自己的样本数，否则抛出异常
        elif other.sample_num == self.sample_num:
            return ChiSquareDistribution(lambda: 0, 0)
        else:
            dof = self.sample_num / (self.sample_num - other.sample_num) * self.dof - other.sample_num / (self.sample_num - other.sample_num) * other.dof
            sample_num = self.sample_num - other.sample_num
            return ChiSquareDistribution(dof, sample_num)
        
    def pdf(self, x):
        """概率密度函数"""
        return chi2.pdf(x, self.dof)
    
    def cdf(self, x):
        """累积分布函数"""
        return chi2.cdf(x, self.dof)

    def inverse_cdf(self, p):
        """反向累积分布函数"""
        return chi2.ppf(p, self.dof)


    # 从该卡方分布中取样
    def sample(self, num):
        samples = []
        for i in range(num):
            u = random.random()
            x = self.inverse_cdf(u)
            samples.append(x)
        return samples


# 构建一个类，代表多个正态分布的混合分布，包含以下属性：正态分布列表
class MixtureDistribution:
    def __init__(self, distribution_list: list[Union[SingleNormalDistribution, 'MixtureDistribution']]):
        self.distribution_list = distribution_list
        self.merge_dist = self.merge() 
        self.components = self.traverse_distribution() # 从混合分布中取出所有的单正态分布
        self.samples = 0

    def __str__(self):
        return "distribution_list: " + str([str(distribution) for distribution in self.distribution_list])

    def __repr__(self):
        return self.__str__()

    # 两个混合分布相加、【需要得到加和之后的样本均值样本方差样本数】   
    def __add__(self, other):
        distribution_list = self.distribution_list + other.distribution_list
        return MixtureDistribution(distribution_list)

    # 混合分布内的正态分布合成为一个正态分布，返回该正态分布
    def merge(self):

        merge_dist = SingleNormalDistribution(0, 0, 0)

        for dist in self.distribution_list:
            if isinstance(dist, MixtureDistribution):
                merge_dist += dist.merge()
            else:
                merge_dist += dist

        return merge_dist


    #递归遍历分布,获取底层的所有正态分布
    def traverse_distribution(self):
    
        distributions = [] 

        for dist in self.distribution_list:
            if isinstance(dist, SingleNormalDistribution):
                # 终止条件:如果是正态分布,添加到结果列表中
                distributions.append(dist)
            elif isinstance(dist, MixtureDistribution):
                # 递归条件:如果是混合分布,遍历其每个成分分布
                distributions.extend(dist.components)
            
            else:
            # 错误条件:既不是正态分布也不是混合分布
                raise ValueError('Unsupported distribution type')
        
        return distributions

    # 从混合分布中取样，从列表中的正态分布取样的概率与正态分布的样本数成正比
    def sample(self, num):
        distributions = self.traverse_distribution()
        samples = []
        total_sample_num = sum(dist.sample_num for dist in distributions)
        for dist in distributions:
            dist_sample_num = int(num * dist.sample_num / total_sample_num)
            dist_samples = dist.sample(dist_sample_num)
            samples += dist_samples
        return samples
        