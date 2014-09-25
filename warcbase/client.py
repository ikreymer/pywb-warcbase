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
        self._load_colls()

    def load_cdx(self, **params):
        print(params)
        prefix = ''

        is_text = (params.get('output') == 'text')

        # lookup collection prefix
        filters = params.get('filter')
        if filters:
            for f in filters:
                if f.startswith('prefix:'):
                    prefix = f[7:]

        # special path for list all
        if params.get('listColls') and is_text:
            self._load_colls()
            return '\n'.join(self.colls)
 
        url = params['url']
        
        # force http prefix
        if url.startswith(self.HTTPS_PREFIX):
            url = self.HTTP_PREFIX + url[len(self.HTTPS_PREFIX):]
        elif not url.startswith(self.HTTP_PREFIX):
            url = self.HTTP_PREFIX + url

        request_uri = self.warcbase_path
        request_uri += prefix
        request_uri += '*/' + url

        try:
            response = requests.get(request_uri)
        except Exception:
            raise WbException('Error reading from: ' + request_uri)

        if response.status_code != 200:
            if response.status_code == 500:
                self._invalid_collection(prefix)
            else:
                raise BadRequestException('Invalid status code: {0}'.format(response.status_code))
        
        if len(response.content) == 0:
            msg = 'No Captures found for: ' + url
            raise NotFoundException(msg, url=url)

        lines = response.content.rstrip().split('\n')

        if len(lines[0].split('\t')) != 3:
            self._invalid_collection(prefix)

        resp_iter = self.iter_cdx(lines, url)
        if is_text:
            resp_iter = self.iter_text(resp_iter)

        return resp_iter

    def iter_cdx(self, lines, url):
        for line in lines:
            yield self.convert_line(line, url)

    def iter_text(self, cdx_iter):
        for cdx in cdx_iter:
            yield str(cdx)

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

    def _load_colls(self):
        self.colls = []
        try:
            response = requests.get(self.warcbase_path + '/')
            if response.status_code == 200:
                self.colls = response.content.rstrip().split('\n')

        except Exception:
            pass

    def _invalid_collection(self, prefix):
        msg = 'Sorry, <b>{0}</b> is not a valid collection. '.format(prefix.strip('/'))
        msg += 'Available collections are: <b>{0}</b>'.format(', '.join(self.colls))
        raise NotFoundException(msg)


