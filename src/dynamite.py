import numpy as np
from mcmcChain import HcubeChain, TMcmcChain
import time

class McMcPro():
    def __init__(self, chain1, chain2, Lambda, func, R, eps, delta, rel=None):
        self.Lambda = Lambda
        self.func = func
        self.R = R
        self.eps = eps
        self.delta = delta
        self.rel = rel # This is optional to prevent overfloating from 1/x where x is close to zero
        if not self.rel:
            self.rel = 1/(1-self.Lambda)
        self.chain1 = chain1
        self.chain2 = chain2
        # self.chain1vals = []
        # self.chain2vals = []
        self.chainLen = 0
        self.chain1sum = 0
        self.chain2sum = 0
        self.varsum = 0

    def extendChains(self, m):
        # nchain1 = [0]*m
        # nchain2 = [0]*m
        for i in range(m):
            self.chain1.step()
            self.chain2.step()
            v1, v2 = self.func(self.chain1.current), self.func(self.chain2.current)
            # print("current should be vector", self.chain1.current, v1, '\n')
            # nchain1[i] = v1
            # nchain2[i] = v2
            self.chain1sum += v1
            self.chain2sum += v2
            self.varsum += (v1-v2)**2
            self.chainLen += 1

        # self.chain1vals += nchain1
        # self.chain2vals += nchain2
        # self.chainLen = len(self.chain1vals)
        
        return 

    def getMean(self):
        # return (np.mean(self.chain1vals) + np.mean(self.chain2vals))/2
        return (self.chain1sum + self.chain2sum) / self.chainLen / 2

    def getVariance(self):
        # return sum([(x1-x2)*(x1-x2) for (x1, x2) in zip(self.chain1vals, self.chain2vals)])/self.chainLen/2
        return self.varsum / self.chainLen / 2

    def varianceBound(self, var, I):
        return var + \
        (11+np.sqrt(21))*(1+self.Lambda/np.sqrt(21))*self.R*self.R*np.log(3*I/self.delta) * self.rel /self.chainLen + \
        np.sqrt((1+self.Lambda)*self.R*self.R*np.log(3*I/self.delta)*var * self.rel /self.chainLen)

    def bernsteinBound(self, u, I):
        return 10*self.R*np.log(3*I/self.delta) * self.rel /self.chainLen + \
        np.sqrt((1+self.Lambda)*np.log(3*I/self.delta)*u * self.rel /self.chainLen)

    def mean_estimate(self):
        I = max(1, int(np.log2(self.R/2/self.eps)))
        alpha = (1+self.Lambda)*np.log(3*I/self.delta)*self.R * self.rel /self.eps
        print("alpha = {:.4e}".format(alpha))
        m = 0
        print(f"I = {I}")
        for i in range(1, I+1):
            new_m = int(np.ceil(alpha*2**i))
            self.extendChains(new_m - m)
            mu = self.getMean()
            var = self.getVariance()
            u = self.varianceBound(var, I)
            b = self.bernsteinBound(u, I)
            print(f"The {i}th round, mu = "+"{:.4e}".format(mu)+", var = "+"{:.4e}".format(var)+", Bbound = "+"{:.2e}".format(b))
            if b<=self.eps:
                print("Early Terminate")
                return mu, var, i, b, self.chainLen
        return mu, var, I, b, self.chainLen



class Dynamite():
    def __init__(self, chain1, chain2, Lambda, func, R, eps, delta, rel=None):
        self.Lambda = Lambda
        self.func = func
        self.R = R
        self.eps = eps
        self.delta = delta
        self.chain1 = chain1
        self.chain2 = chain2
        self.rel = rel # This is optional to prevent overfloating from 1/x where x is close to zero
        if not self.rel:
            self.rel = 1/(1-self.Lambda)
        # self.chain1vals = []
        # self.chain2vals = []
        # self.chainLen = 0

        self.T = int(np.ceil((1+self.Lambda)*self.rel*np.log(np.sqrt(2))))
        self.favg = lambda x: np.mean([func(x[i]) for i in range(len(x))])

        self.Tchain1 = TMcmcChain(self.chain1, self.T)
        self.Tchain2 = TMcmcChain(self.chain2, self.T)


    def mean_estimate(self):
        mcpro = McMcPro(self.Tchain1, self.Tchain2, self.Lambda**self.T, self.favg, self.R, self.eps, self.delta, self.rel)
        return mcpro.mean_estimate()


if __name__ == '__main__':

    def run():
        n = 30
        k = 2
        eps = 0.005
        delta = 0.05
        Lambda = 1-1/n
        isRed2 = lambda x: int(sum(x)%k)
        print(f"n={n}, k={k}, func = sum(x)%k, true mean = {1/k}, eps = {eps}, delta = {delta}")
        # chain1 = HcubeChain(np.random.randint(0,2,n), n)
        # chain2 = HcubeChain(np.random.randint(0,2,n), n)
        # mcproHcube = McMcPro(chain1 = chain1, chain2 = chain2, Lambda = Lambda, func = isRed2, R = 1, eps = eps, delta = delta)
        # mcproHcube.mean_estimate()
        chain1 = HcubeChain(np.random.randint(0,2,n), n)
        chain2 = HcubeChain(np.random.randint(0,2,n), n)
        dynamiteHcube = Dynamite(chain1 = chain1, chain2 = chain2, Lambda = Lambda, func = isRed2, R = 1, eps = eps, delta = delta)
        dynamiteHcube.mean_estimate()
    
    start_time = time.perf_counter()
    [run() for i in range(1)]
    end_time = time.perf_counter()
    print(f"Run Dynamite in {end_time - start_time:0.4f} seconds")