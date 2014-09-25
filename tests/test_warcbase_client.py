import requests
from httmock import all_requests, urlmatch, HTTMock
from urlparse import urlsplit

from pywb.utils.wbexception import NotFoundException
from pytest import raises
from warcbase.client import WarcBaseClientIndexServer
from collections import OrderedDict


SAMPLE_INDEX = '{0}\ttext/html\t{2}\n{1}\ttext/html\t{3}\n'

#==============================================================================
@all_requests
def mock_warcbase_servlet_index(url, request):
    path = url.path
    ts1 = '20140102030000'
    ts2 = '20140203040506'

    if 'not.found.example.com' in url.path:
        return ''

    return SAMPLE_INDEX.format(ts1, ts2,
                               path.replace('*', ts1),
                               path.replace('*', ts2))


#==============================================================================
class TestWarcBase(object):
    def test_mock_query(self):
        with HTTMock(mock_warcbase_servlet_index):
            r = requests.get('http://localhost/prefix/*/http://example.com')
            lines = r.content.split('\n')
            assert lines[0] == '20140102030000\ttext/html\t/prefix/20140102030000/http://example.com'
            assert lines[1] == '20140203040506\ttext/html\t/prefix/20140203040506/http://example.com'

    def test_warcbase_index_query(self):
        client = WarcBaseClientIndexServer('http://localhost/context/')
     
        with HTTMock(mock_warcbase_servlet_index):
            cdx_iter = client.load_cdx(url='example.com')
            cdx = list(cdx_iter)

            assert len(cdx) == 2
            assert cdx[0] == OrderedDict(
                           [('urlkey', 'com,example)/'),
                            ('timestamp', '20140102030000'),
                            ('original', 'http://example.com'),
                            ('mimetype', 'text/html'),
                            ('statuscode', '200'),
                            ('digest', '-'),
                            ('length', '-1'),
                            ('offset', '0'),
                            ('filename', '/context/20140102030000/http://example.com')
                           ])

            assert cdx[1] == OrderedDict(
                           [('urlkey', 'com,example)/'),
                            ('timestamp', '20140203040506'),
                            ('original', 'http://example.com'),
                            ('mimetype', 'text/html'),
                            ('statuscode', '200'),
                            ('digest', '-'),
                            ('length', '-1'),
                            ('offset', '0'),
                            ('filename', '/context/20140203040506/http://example.com')
 
                            ])

    def test_not_found(self):
        client = WarcBaseClientIndexServer('http://localhost/context/')
        with HTTMock(mock_warcbase_servlet_index):
            with raises(NotFoundException):
                cdx_iter = client.load_cdx(url='http://not.found.example.com')


