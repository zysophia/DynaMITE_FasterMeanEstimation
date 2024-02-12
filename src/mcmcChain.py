from abc import ABC, abstractmethod 
import numpy as np

class McmcChain(ABC):
    def __init__(self, startpoint):
        self.current = startpoint

    @abstractmethod
    def step(self):
        pass

class HcubeChain(McmcChain):
    def __init__(self, startpoint, n):
        self.n = n
        super().__init__(startpoint)
        # Generate and store rand values 
        self.randp = 0
        self.randlen = 10000
        self.randlazy = np.random.rand(self.randlen)
        self.randflip = np.random.randint(0, self.n, self.randlen)
    
    def step(self):
        lazy, flip = self.get_lazy_and_flip()
        if lazy > 0.5:
            return
        self.current[flip] = 1-self.current[flip] # flip the bit

    def get_lazy_and_flip(self):
        if self.randp < self.randlen:
            self.randp += 1
            return self.randlazy[self.randp-1], self.randflip[self.randp-1]
        else:
            self.randlazy = np.random.rand(self.randlen)
            self.randflip = np.random.randint(0, self.n, self.randlen)
            self.randp = 1
            return self.randlazy[0], self.randflip[0]


class TMcmcChain():
    def __init__(self, mcmcchain, T):
        self.T = T
        self.mcmcchain = mcmcchain
        self.current = []

    def step(self):
        vector = []
        for i in range(self.T):
            # print(self.mcmcchain.current)
            # print(vector)
            vector.append(self.mcmcchain.current.copy())
            self.mcmcchain.step()
            # print(self.mcmcchain.current)
        self.current = vector
