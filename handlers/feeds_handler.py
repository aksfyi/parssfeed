from flask import request, jsonify
from feedparser import helper as fch


def feedshandler():
    finalResponse = {}
    finalResponse['api_source'] = 'https://github.com/aksty/parssfeed'
    finalResponse['feed_sources'] = fch.configs['sources']
    page = request.args.get('page')
    query = request.args.get('q')
    if page is None:
        page = 1
    else:
        page = int(page)
    ltst = "feed" if fch.configs['api_url'][-1] == '/' else "/feed"
    if query is not None:
        res = fch.searchFilter(fch.finallist, query)
        totalPages = int(len(res) / fch.configs['itemsPerPage'])
        mod = len(res) % fch.configs['itemsPerPage']
        if mod > 0:
            totalPages = totalPages + 1
        finalResponse['totalPages'] = int(totalPages)
        finalResponse['next'] = fch.configs['api_url'] + ltst + '?page=' + str(page + 1) + '&q=' + query if int(
            totalPages) > page else "end"
    else:
        res = fch.finallist
        totalPages = len(res) / fch.configs['itemsPerPage']
        mod = len(res) % fch.configs['itemsPerPage']
        if mod > 0:
            totalPages = totalPages + 1
        finalResponse['totalPages'] = int(totalPages)
        finalResponse['next'] = fch.configs['api_url'] + ltst + '?page=' + str(page + 1) if int(
            totalPages) > page else "end"
    startIndex = (page - 1) * fch.configs['itemsPerPage']
    finalResponse['feedResults'] = res[startIndex: startIndex + fch.configs['itemsPerPage']]
    if len(finalResponse['feedResults']) == 0:
        finalResponse['feedResults'] = {'message': 'No matching results'}
        return jsonify(finalResponse), 404
    return jsonify(finalResponse)
