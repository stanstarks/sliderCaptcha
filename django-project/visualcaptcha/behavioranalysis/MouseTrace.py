import json
import numpy as np
from os import path
from hashlib import md5
from django.core.cache import cache

class MouseTrace(object):

    # @param trace is read as a string
    # @param assetsPath. By default, it will be ./assets. This is for demo use. Should always use architecture easy to query
    # @param defaultTraces is optional. List of recorded traces in json map
    def __init__(self, trace='', label='UNKNOWN'):
        # oeprations is a dict of 
        self.trace = trace
        self.assetsPath = '/home/stan/github/visualCaptcha/assets'
        if trace:
            self.label = label
            if not cache.has_key('list'):
                cache.set('list', [])
                cache.set('inc', 1)
                self.readJSON()
                print 'DEBUG_MOUSETRACE: readJSON'
            self.metaTrace = self.getMetaTrace()

    def writeCache(self):
        traceKeys = cache.get('list')
        traceKeys.append(self.metaTrace['md5'])
        cache.set('list', traceKeys)
        cache.set(self.metaTrace['md5'],
                  {'path':self.metaTrace['path'],
                   'label':self.metaTrace['label']})
        
                             
    def checkReplay(self):
        # not implemented, not possible for now
        return cache.has_key(self.metaTrace['md5'])

    def saveTrace(self):
        self.writeCache()
        self.writeTrace()
        if not cache.has_key('inc'):
            cache.set('inc', 1)
            print 'DEBUG_MOUSETRACE: inc is not in cache'
        inc = cache.get('inc')
        if inc > 0:
            cache.set('inc', 1)
            self.writeJSON()
        else:
            cache.set('inc', inc+1)
                
    def checkRobot(self):
        data = json.loads(self.trace)
        xs = data[u'dragging']
        # claim robot if
        # 1. dragging to fast
        #if len(xs) < 1000:
            #print 'DEBUG_MOUSETRACE_ROBOT: 1 dragging to fast'
            #return True

        # 2. final movement too fast
        # if the final 5 frame finished within 0.2 seconds:
        #if xs[-1][2] - xs[-5][2] < 1:
            #print 'DEBUG_MOUSETRACE_ROBOT: 2 finished quickly'
            #return True

        # 3. dragging too straight
        #ys = np.array(xs)
        #if max(ys[:,1]) - min(ys[:,1]) < 1:
         #   print 'DEBUG_MOUSETRACE_ROBOT: 3 dragging straight line'
          #  return True
        
        # 4. no horizontal acceleration
        #ys = np.array(xs).astype(float)
        #accs = (ys[1:,0]-ys[:-1,0]) * 100 / (ys[1:,2]-ys[:-1,2])
        #astd = np.std(accs)
        #print 'DEBUG_MOUSETRACE_ROBOT: accs std', astd
        #if np.std(accs) < 10:
            #print 'DEBUG_MOUSETRACE_ROBOT: 4 no horizontal acc'
            #return True
        return False

    def getMetaTrace(self):
        metaTrace = {}
        metaTrace['md5'] = md5(self.trace).hexdigest()
        metaTrace['path'] = '{}.trace'.format(len(cache.get('list')))
        metaTrace['label'] = self.label
        return metaTrace

    def readJSON(self):
        filePath = self.assetsPath + '/traces.json'
        if (not path.isfile(filePath)):
            return None

        json_data = open(filePath)
        data = json.load(json_data)
        cache.clear()
        traceKeys = []
        for record in data:
            cache.set(record['md5'], {'path':record['path'], 'label':record['label']})
            traceKeys.append(record['md5'])
        cache.set('list', traceKeys)
        

    def writeTrace(self):
        traceFileName = self.metaTrace['path']
        traceFile = open(self.assetsPath + '/traces/' + traceFileName, 'w')
        print 'DEBUG_MOUSETRACE: writing to '+traceFileName
        traceFile.write(self.trace)
        traceFile.close()

    def writeJSON(self):
        filePath = self.assetsPath+'/traces.json'
        rs = []
        for key in cache.get('list'):
            record = {}
            record['md5'] = key
            cachedValue = cache.get(key)
            record['path'] = cachedValue['path']
            record['label'] = cachedValue['label']
            rs.append(record)
        jsonFile = open(filePath, 'w')
        json.dump(rs, jsonFile)
        jsonFile.close()
            

