from . import MouseTrace

class Behavior(object):

    # @param interactions is the interaction object
    # @param assetsPath. By default, it will be ./assets. This is for demo use. Should always use architecture easy to query
    # @param defaultTraces is optional. Array of recorded traces.
    def __init__(self, interactions={}, defaultTraces=[], assetsPath=''):
        # oeprations is a dict of 
        self.interactions = interactions

    def get(self, key):
        return self.interactions[key]

    def isEmpty(self, key):
        return key in self.interactions
    
    def validate(self):
        # Validate mouse trace
        if 'mouseTrace' in self.interactions:
            return self.validateMouseTrace()
        return 'EMPTY_MOUSE_TRACE';

    def validateMouseTrace(self):
        # 1. Search history records for a behavior match. The dataset should be updated constantly and the algorithm should run upon a rolling basis
        # 2. To improve the performance, an inverted index database (or similar data structure) is demanded.
        mouseTrace = MouseTrace.MouseTrace(self.getMouseTrace(), label='HUMAN')
        # print 'DEBUG_BEHAVIOR: cache("list") ', mouseTrace.getList()
        if mouseTrace.checkReplay(): return 'failedReplay'
        if mouseTrace.checkRobot(): return 'failedRobot'
        mouseTrace.saveTrace()
        return None

    def getMouseTrace(self):
        return self.interactions['mouseTrace']

    def writeJSON(self):
        MouseTrace().writeJSON()

    def readJSON(self):
        MouseTrace().readJSON()
