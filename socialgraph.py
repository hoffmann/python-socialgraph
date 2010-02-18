#!/usr/bin/env python 
# -*- coding: utf-8 -*-

"""
interface to google social graph api

http://code.google.com/apis/socialgraph/
"""

import sys
import cjson
import urllib
import httplib2
from sets import Set

class Api(object):
    """wraps http api to google social graph"""
    def __init__(self):
        #for debugging purpose
        self._last_request = None

    def _post(self, url, params):
        h = httplib2.Http()
        data = urllib.urlencode(params)
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        resp, content = h.request(url, "POST", headers=headers, body=data) 
        self._last_request = dict(url=url, params=params, res=resp, content=content, method="POST")
        return cjson.decode(content)

    def _get(self, url, params):
        h = httplib2.Http()
        request = url +"?"+ urllib.urlencode(params)
        resp, content = h.request(request, "GET")
        self._last_request = dict(url=url, params=params, res=resp, content=content, method="GET")
        return cjson.decode(content)

    def lookup(self, q, edo=1, edi=0, fme=0, pretty=1, sgn=0):
        """ query the social graph API
        
        The lookup method gives you low-level access to the Social Graph API's
        underlying directed graph. It lets you list all the edges out of or
        into a given node.
        
        q   Comma-separated list of URIs    Which nodes the social graph to query
        edo	boolean	                        Return edges out from returned nodes
        edi	boolean	                        Return edges in to returned nodes
        fme	boolean	                        Follow me links, also returning reachable nodes
        pretty boolean	                    Pretty-print returned JSON
        sgn	boolean	                        Return internal representation of nodes

        see: http://code.google.com/apis/socialgraph/docs/lookup.html
        """
        baseurl = "http://socialgraph.apis.google.com/lookup"
        return self._get(baseurl, dict(q=q, edo=edo, edi=edi, fme=fme, pretty=pretty, sgn=sgn))


    def otherme(self, q, pretty=1, sgn=0):
        """query person's other identifiers

        The otherme method gives you an easy way to query a person's other
        idenfitiers (e.g. URLs) based on one or more identifiers for that
        person that you do know.

        q	    Comma-separated list of URIs.	The identifiers (URLs, emails, etc) which you 
                                                do know for the person.
        pretty	boolean	                        Pretty-print returned JSON.
        sgn 	boolean	                        Return internal representation of nodes


        see: http://code.google.com/apis/socialgraph/docs/otherme.html
        """
        baseurl = "http://socialgraph.apis.google.com/otherme"
        return self._get(baseurl, dict(q=q, pretty=pretty, sng=sgn)) 



    def testparse(self, url, body, contentType="text/html", urlFormat="base"):
        """test your site's XFN or FOAF to see what the Social Graph API's parsers find in it
        
        url         The hypothetical URL.
        body        Required. The document body.
        contentType Required. The Content-Type header, possibly including a charset.
        urlFormat   Optional One of "raw", "sgn" or "base"

        see: http://code.google.com/apis/socialgraph/docs/testparse.html
        """
        baseurl = "http://socialgraph.apis.google.com/testparse"
        return self._post(baseurl, dict(url=url, body=body, contentType=contentType, urlFormat=urlFormat))


    def testparse_url(self, url):
        """download url and feed it through testparse"""

        body = urllib.urlopen(url).read()
        return self.testparse(url, body)


    def lookup_incoming_me(self, url):
        """return all incoming me links"""
        resp = self.lookup(url, edo=0, edi=1)
        links = []
        node = resp["nodes"].get(url)
        if node is None:
            return []
        references = node.get("nodes_referenced_by", {})
        for ref in references:
            if "me" in references[ref]["types"]:
                links.append(ref)
        return links



    def lookup_outgoing_me(self, url):
        """return all outgouing me links"""
        resp = self.lookup(url, edo=1, edi=0)
        links = []
        #todo resove canonical mapping for url
        node = resp["nodes"].get(url)
        if node is None:
            return []
        references = node.get("nodes_referenced", {})
        for ref in references:
            if "me" in references[ref]["types"]:
                links.append(ref)
        return links
