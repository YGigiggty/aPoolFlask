import logging
import time
from flask import request


def Recode_request_logs(response,*args,**kwargs):
    now_time =time.time()
    request_start_time = getattr(request, 'request_start_time', None)
    user_id =getattr(request,id,None)

    format_str=(
        '%(remote_addr)s request: [%(status)s] %(method)s, url: %(url)s, '
        'args: %(args)s, json: %(json)s, '
        'request_start_time: %(request_start_time)s, response_time: %(response_time)s, '
        'user_id: %(user_id)s, '
    )
    data =dict(
        remote_addr =request.remote_addr,
        status =response.status,
        method =request.method,
        url =request.url,
        args =request.args,
        json =request.get_json(silent=True),
        request_start_time =str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())),
        response_time =now_time-request_start_time,
        user_id =user_id,
    )
    logger =logging.getLogger("response")
    logger.info(format_str,data)
    return response