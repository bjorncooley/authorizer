import json

from flask import make_response

def get_request_data(request, required_params):
    
    data = {}
    if request.method == 'GET':
        for param in required_params:
            if param not in request.args:
                raise ValueError("%s must be included in request " % param)
            data[param] = request.args.get(param)

    elif request.method == 'POST':            
        if not request.data:
            raise ValueError("Request body must contain data")
        try:
            data = json.loads(request.data.decode("utf-8"))
        except TypeError:
            raise TypeError("Data must be compatible with JSON")

        for param in required_params:
            if param not in data:
                raise ValueError("%s must be included in request" % param)

    return data


def handle_error(message, logger, status_code=500):
    logger.error(message)
    return make_response(message, status_code)
    