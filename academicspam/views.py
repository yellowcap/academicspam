"""Main views for this project, such as index login/logout etc"""

from django.http import HttpResponse#, HttpResponseRedirect
from django.template import RequestContext, loader
#from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from spamparser.models import ParseResult

###############################################################################
@login_required
def index(request):
    """View for index page of academicspam"""

    pres = ParseResult.objects.filter()[:10]
    count = ParseResult.objects.filter().count()

    template = loader.get_template('index.html')
    context = RequestContext(request, {
        'parseresults': pres,
        'parsecount': count
    })
    return HttpResponse(template.render(context))
