import requests
import logging

from pywb.utils.wbexception import AccessException, NotFoundException
from pywb.utils.wbexception import BadRequestException, WbException
from pywb.cdx.cdxobject import CDXObject
from pywb.utils.canonicalize import canonicalize


#===================================================================
class WarcBaseClientIndexServer(object):
    """
    This class is an example of a custom index server designed to
    connect to the WarcBrowserServlet in the warcbase project and retrieve
    a cdx-like index.
    
    The index format is a 3 field 'timestamp\tmime\tfilename' and the remaining
    necessary CDXObject fields are filled in automatically
    """
    
    HTTPS_PREFIX = 'https://'
    HTTP_PREFIX = 'http://'

    def __init__(self, paths, **kwargs):
        self.warcbase_path = paths
        logging.debug('Initing WarcBase Client: ' + paths)

    def load_cdx(self, **params):
        url = params['url']

        # force http prefix
        if url.startswith(self.HTTPS_PREFIX):
            url = self.HTTP_PREFIX + url[len(self.HTTPS_PREFIX):]
        elif not url.startswith(self.HTTP_PREFIX):
            url = self.HTTP_PREFIX + url

        request_uri = self.warcbase_path + '*/' + url
        print(request_uri)

        response = self._load_response(request_uri)

        if len(response.content) == 0:
            return

        lines = response.content.split('\n')

        for line in lines:
            yield self.convert_line(line, url)

    def convert_line(self, line, url):
        timestamp, mime, filename = line.split('\t')

        cdx = CDXObject()
        cdx['urlkey'] = canonicalize(url)
        cdx['timestamp'] = timestamp
        cdx['original'] = url
        cdx['mimetype'] = mime
        cdx['statuscode'] = '200'
        cdx['digest'] = '-'
        cdx['length'] = '-1'
        cdx['offset'] = '0'
        cdx['filename'] = filename
        
        return cdx

    def _load_response(self, request_uri):
        try:
            return requests.get(request_uri)

        except Exception:
            raise WbException('Error reading from: ' + request_uri)

        if result.status_code != 200:
            raise BadRequestException('Invalid status code: {0}'.format(result.status_code))
