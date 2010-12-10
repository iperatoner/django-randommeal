from django.template import RequestContext, loader
from django.http import HttpResponse
from django.utils import simplejson as json

def render_template(request, template, mimetype=None, **kwargs):  
    """  
    `render_to_response` sucks. `render_template` takes template-locals as
    keyword arguments, not as a dict as positional argument.
    """  
    context_processor = RequestContext(request)
    return HttpResponse( 
        loader.render_to_string(template, kwargs, context_processor),
        mimetype=mimetype
    )

class JSONResponse(HttpResponse):
    def __init__(self, json_dict):
        HttpResponse.__init__(self, json.dumps(json_dict), mimetype='application/json')