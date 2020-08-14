from flask import request, jsonify
from feedparser import helper as fch


def roothandler():
    if request.method == 'GET':

        finalResponse = {}
        finalResponse['api_source'] = 'https://github.com/aksty/parssfeed'
        urlreq = request.args.get('url')
        page = request.args.get('page')
        query = request.args.get('q')

        if page is None:
            page = -1
        else:
            page = int(page)
        if query is None:
            query = ""
        if urlreq is not None:
            finalResponse['feedResults'] = fch.specSource(urlreq, page, query, cacheflag=False)
            if len(finalResponse['feedResults']) == 0:
                finalResponse['feedResults'] = {'message': 'No results'}
                return jsonify(finalResponse), 404
            try:
                if finalResponse['feedResults']['error']:
                    return jsonify(finalResponse), 400
            except Exception as e:
                pass
            return jsonify(finalResponse)
        finalResponse['feed_sources'] = fch.configs['sources']
        return jsonify(finalResponse)
