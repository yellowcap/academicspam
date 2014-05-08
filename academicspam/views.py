from django.http import HttpResponse#, HttpResponseRedirect
from django.template import RequestContext, loader
#from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.decorators import login_required

###############################################################################
#@login_required
def index(request):
    template = loader.get_template('index.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))
