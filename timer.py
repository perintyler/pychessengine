import time

SHOULD_PRINT = True


class MethodProfile:

    def __init__(self,name):
        self.name = name
        self.timesRun = self.timeSpent = 0

    def addTime(self,time):
        self.timesRun += 1
        self.timeSpent += time

    def __str__(self):
        if self.timesRun == 0: return 'never ran ' + self.name
        averageRuntime = self.timeSpent / self.timesRun
        return '' + self.name + '\t\t' + str(self.timesRun) + '\t\t' + str(averageRuntime)
        # return f'{self.name}\t\t\t{self.timesRun}\t\t{averageRuntime}'

methods = set()

def timeit(method):

    profile = MethodProfile(method.__name__)
    methods.add(profile)

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        executionTime = te-ts
        
        profile.addTime(executionTime)


        if profile.name == 'get_best_move':

            for m in methods:
                if m.name != 'get_best_move':
                    print(m)

        return result


    return timed