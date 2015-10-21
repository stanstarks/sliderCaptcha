import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, redirect

from rest_framework.renderers import JSONRenderer

from visualcaptcha import Captcha, Session, Slider


def index(request):
    return render_to_response('index.html')


def start(request, howMany):
    visualCaptcha = Captcha(Session(request.session))

    visualCaptcha.generate(howMany)
    jsonFrontendData = JSONRenderer().render(visualCaptcha.getFrontendData())
    response = HttpResponse(content=jsonFrontendData)
    response['Access-Control-Allow-Origin'] = '*'

    return response

def startSlider(request):
    sliderCaptcha = Slider(Session(request.session))

    sliderCaptcha.generate()
    jsonFrontendData = JSONRenderer().render(sliderCaptcha.getSliderData())
    response = HttpResponse(content=jsonFrontendData)
    response['Access-Control-Allow-Origin'] = '*'

    return response

def getSlider(request, isForeground=False):
    sliderCaptcha = Slider(Session(request.session))
    headers = {}
    result = sliderCaptcha.streamImage(
        headers, isForeground)

    if result is False:
        return HttpResponse(result, headers, 404)

    return HttpResponse(result, headers)

def getImage(request, index):
    visualCaptcha = Captcha(Session(request.session))

    headers = {}
    result = visualCaptcha.streamImage(
        headers, index)

    if result is False:
        return HttpResponse(result, headers, 404)

    return HttpResponse(result, headers)


def getAudio(request, audioType='mp3'):
    visualCaptcha = Captcha(Session(request.session))

    headers = {}
    result = visualCaptcha.streamAudio(headers, audioType)

    if result is False:
        return HttpResponse(result, headers, 404)

    return HttpResponse(result, headers)

@csrf_exempt
def tryScroll(request):
    sliderCaptcha = Slider(Session(request.session))
    response = HttpResponse(status=403)
    if request.POST.get('interactions', None) is not None:
        message = sliderCaptcha.validateBehavior({
            'mouseTrace' : request.POST['interactions']})
        if message is None:
            if sliderCaptcha.validateSlider(
                    request.POST['position']):
                response = HttpResponse(status=200)
                message = 'validSlider'
            else:
                message = 'failedSlider'
    else:
        message = 'emptyPost'
    return HttpResponse(json.dumps({'message': message}))

@csrf_exempt
def trySubmission(request):
    visualCaptcha = Captcha(Session(request.session))
    frontendData = visualCaptcha.getFrontendData()

    # SpamBot detection using mouse track data
    # if request.POST.get(frontendData['userInteractions'], None) is not None:
    if None:
        status = visualCaptcha.validateBehavior(
                request.POST[frontendData['userInteractions']])
        if not status:
            response = HttpResponse(status=403)
            if status == 'REPLAY':
                return redirect('/?status=failedReplay')
            elif status == 'ROBOT':
                return redirect('/?status=failedROBOT')
            else: return redirect('/?status=failedUndefined')

    # If an image field name was submitted, try to validate it
    if request.POST.get(frontendData['imageFieldName'], None) is not None:
        if visualCaptcha.validateImage(
                request.POST[frontendData['imageFieldName']]):
            response = HttpResponse(status=200)
            return redirect('/?status=validImage')
        else:
            response = HttpResponse(status=403)
            return redirect('/?status=failedImage')
    elif request.POST.get(frontendData['audioFieldName'], None) is not None:
        # We set lowercase to allow case-insensitivity , but it's
        # actually optional
        if visualCaptcha.validateAudio(
                request.POST[frontendData['audioFieldName']].lower()):
            response = HttpResponse(status=200)
            return redirect('/?status=validAudio')
        else:
            response = HttpResponse(status=403)
            return redirect('/?status=failedAudio')
    else:
        response = HttpResponse(status=500)
        return redirect('/?status=failedPost')

    return response
