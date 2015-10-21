import os
import re
import json
import random
import mimetypes
from PIL import Image
from behavioranalysis import Behavior

class Slider(object):

    # @param session is the default session object
    # @param Assets path. By default, it will be ./assets
    # @param defaultImages is optional. Defaults to the array inside ./images.json. The path is relative to ./assets/images/
    # @param defaultAudios is optional. Defaults to the array inside ./audios.json. The path is relative to ./assets/audios/
    def __init__(self, session={}, assetsPath='', defaultImages=[]):
        # Attach the session object reference to visualCaptcha
        self.session = session

        # If no assetsPath is specified, set the default
        if (not assetsPath or assetsPath == ''):
            self.assetsPath = os.path.dirname(os.path.realpath(__file__)) + '/assets'
        else:
            self.assetsPath = assetsPath

        # If there are no defaultImages, get them from ./images.json
        if (not defaultImages or len(defaultImages) == 0):
            defaultImages = self.utilReadJSON(self.assetsPath + '/sliders.json')

        # Attach the images object reference to visualCaptcha
        self.sliderOptions = defaultImages

    # Generate a new valid option
    # @param numberOfOptions is optional. Defaults to 5
    def generate(self): 
        # Save previous image & audio options from session
        oldSliderOption = self.getSliderOption()

        # Reset the session data
        self.session.clear()
        self.setFailedCount(0)

        # Select a random image as slider, pluck current valid image option
        condition = True
        while condition:
            newSliderOption = random.choice(self.sliderOptions)
            condition = (oldSliderOption and oldSliderOption['path'] == newSliderOption['path'])

        self.session.set('sliderOption', newSliderOption)

        # select part of the image to crop
        sliderPosition = random.uniform(0, 100)
        self.session.set('sliderPosition', sliderPosition)

        self.session.set('sliderData', {
            'sliderPosition': sliderPosition
        })

    # Stream image file given an index in the session visualCaptcha images array
    # @param headers object. used to store http headers for streaming
    # @param index of the image in the session images array to send
    # @param isRetina boolean. Defaults to false
    def streamImage(self, headers, isForeground=False, isRetina=False):
        imageOption = self.getSliderOption()
        # If there's no imageOption, we set the file name as empty
        imageFileName = imageOption['path'] if imageOption else ''
        imageFilePath = self.assetsPath + '/sliders/' + imageFileName

        # If the index is non-existent, the file name will be empty, same as if the options weren't generated
        if (imageFileName != ''):
            position = self.getSliderPosition()
            img = Image.open(imageFilePath)
            w, h = img.size
            l = int(w*7*position/9/100) + w/9
            u = h/2 - 20
            if isForeground:
                img = img.crop((l, u, l+40, u+40))
                imageFileName = re.sub(r'(?i)\.png', '_slider.png', imageFileName)
                imageFilePath = re.sub(r'(?i)\.png', '_slider.png', imageFilePath)
            else:
                alpha = 0.5
                pix = img.load()
                for x in xrange(l, l+40):
                    for y in xrange(u, u+40):
                        pix[x, y] = tuple(map(lambda x:int(x * alpha + 20 * (1-alpha)), pix[x,y]))
                imageFileName = re.sub(r'(?i)\.png', '_bg.png', imageFileName)
                imageFilePath = re.sub(r'(?i)\.png', '_bg.png', imageFilePath)
            img.save(imageFilePath)
            f = open(imageFilePath)
            content = f.read()
            f.close()
            #self.session.set(imageFileName, content)
            return self.utilStreamFile(headers, imageFilePath)

        return False

    def setFailedCount(self, count):
        self.session.set('failedCount', count)

    def getFailedCount(self):
        return self.session.get('failedCount')
    
    # Get data to be used by the frontend
    def getInteractions(self):
        return self.session.get('interactions')

    # Get the current validImageOption
    def getSliderOption(self):
        return self.session.get('sliderOption')

    def getSliderPosition(self):
        return self.session.get('sliderPosition')

    def getSliderData(self):
        return self.session.get('sliderData')

    # Validate the sent image value with the validImageOption
    def validateSlider(self, sentPosition):
        sliderPosition = self.getSliderPosition()
        print sliderPosition, sentPosition
        if abs(sliderPosition - float(sentPosition)) > 3:
            count = self.getFailedCount()
            print count
            if count > 5:
                self.generate()
            else:
                self.setFailedCount(count+1)
            return False
        return True

    # Read input file as JSON
    def utilReadJSON(self, filePath):
        if (not os.path.isfile(filePath)):
            return None

        json_data = open(filePath)
        data = json.load(json_data)
        json_data.close()

        return data

    # Stream file from path
    def utilStreamFile(self, headers, filePath):
        if (not os.path.isfile(filePath)):
            return False

        mimeType = self.getMimeType(filePath)

        # Set the appropriate mime type
        headers['Content-Type'] = mimeType

        # Make sure this is not cached
        headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        headers['Pragma'] = 'no-cache'
        headers['Expires'] = 0

        f = open(filePath)
        content = f.read()
        f.close()

        # Add some noise randomly, so images can't be saved and matched easily by filesize or checksum
        # content += self.utilRandomHex( random.randint(0, 1500) )

        return content

    # Get File's mime type
    def getMimeType(self, filePath):
        return mimetypes.guess_type(filePath)[0]

    # Behavior related funtions
    def validateBehavior(self, sentInteractions, defaultTraces=[]):
        behavior = Behavior(sentInteractions)
        return behavior.validate()

    def writeJSON(self):
        Behavior({}).writeJSON()

    def readJSON(self):
        Behavior({}).readJSON()


