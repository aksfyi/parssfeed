from flask import request,jsonify
from feedparser import helper as fch


def sourcehandler(rt):
    finalResponse = dict()
    finalResponse['api_source'] = 'https://github.com/aksty/parssfeed'
    finalResponse['feed_sources'] = fch.configs['sources']
    page = request.args.get('page')
    query = request.args.get('q')
    sourceinfo = request.args.get('sourceinfo')
    if sourceinfo is not None:
        if sourceinfo == "1" or sourceinfo.lower() == "true":
            finalResponse['source_info'] = fch.channelinfo(fch.configs['sources'][rt.strip()])
            return jsonify(finalResponse)
    if page is None:
        page = -1
    else:
        page = int(page)
    if query is None:
        query = ""
    cacheflag = True if page == 1 or page == 2 or page == -1 else False
    res = fch.specSource(fch.configs['sources'][rt.strip()], page, query, cacheflag)
    finalResponse['feedResults'] = res
    finalResponse['source_info'] = fch.channelinfo(fch.configs['sources'][rt.strip()])
    if len(finalResponse['feedResults']) == 0:
        finalResponse['feedResults'] = {'message': 'No matching results'}
        return jsonify(finalResponse), 404
    return jsonify(finalResponse)
