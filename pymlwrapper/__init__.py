# -*- coding:utf8 -*-

import sys
sys.path.append('../lib')
from meli import Meli

class MeliWrapperError(Exception):
    pass

class MeliWrapperNotImplemented(NotImplementedError):
    pass


class MeliCollection(object):
    def __init__(self, data, paging):
        self.data = data
        self.paging = paging
        self.index = len(data)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index = self.index - 1
        return self.data[self.index]



class MeliWrapper(Meli):

    available_methods = ['get', 'post', 'put', 'delete', 'options']

    site_ids = [
            {u'id': u'MLB', u'url': 'https://auth.mercadolivre.com.br', u'name': u'Brasil'},
            {u'id': u'MCO', u'url': 'https://auth.mercadolibre.com.co', u'name': u'Colombia'},
            {u'id': u'MEC', u'url': 'https://auth.mercadolibre.com.ec', u'name': u'Ecuador'},
            {u'id': u'MHN', u'url': 'https://auth.mercadolibre.com.ho', u'name': u'Honduras'},
            {u'id': u'MPE', u'url': 'https://auth.mercadolibre.com.pe', u'name': u'Perú'},
            {u'id': u'MLM', u'url': 'https://auth.mercadolibre.com.mx', u'name': u'Mexico'},
            {u'id': u'MNI', u'url': 'https://auth.mercadolibre.com.nc', u'name': u'Nicaragua'},
            {u'id': u'MPT', u'url': 'https://auth.mercadolibre.com.pt', u'name': u'Portugal'},
            {u'id': u'MLV', u'url': 'https://auth.mercadolibre.com.ve', u'name': u'Venezuela'},
            {u'id': u'MRD', u'url': 'https://auth.mercadolibre.com.do', u'name': u'Dominicana'},
            {u'id': u'MLC', u'url': 'https://auth.mercadolibre.cl', u'name': u'Chile'},
            {u'id': u'MCR', u'url': 'https://auth.mercadolibre.com.cr.', u'name': u'Costa Rica'},
            {u'id': u'MBO', u'url': 'https://auth.mercadolibre.com.bo', u'name': u'Bolivia'},
            {u'id': u'MSV', u'url': 'https://auth.mercadolibre.com.sl', u'name': u'El Salvador'},
            {u'id': u'MPY', u'url': 'https://auth.mercadolibre.com.py', u'name': u'Paraguay'},
            {u'id': u'MCU', u'url': 'https://auth.mercadolibre.com.cu', u'name': u'Cuba'},
            {u'id': u'MGT', u'url': 'https://auth.mercadolibre.com.gm', u'name': u'Guatemala'},
            {u'id': u'MLA', u'url': 'https://auth.mercadolibre.com.ar', u'name': u'Argentina'},
            {u'id': u'MPA', u'url': 'https://auth.mercadolibre.com.pa', u'name': u'Panamá'},
            {u'id': u'MLU', u'url': 'https://auth.mercadolibre.com.uy', u'name': u'Uruguay'}
        ]

    site_id = 'MLA'

    def api_call(self, path='', body=None, params={}, method='get'):
        if not params.get('access_token'):
            params.update({'access_token': self.access_token})

        if method not in self.available_methods:
            raise MeliWrapperNotImplemented("This method `%s` is not valid or not implemented" % method)

        _method = getattr(self, method)

        if method in ['post', 'put']:
            response = _method(path, body, params)
        else:
            response = _method(path, params)

        if not response.ok:
            try:
                return response.json()
            except:
                raise MeliWrapperError("Something is not ok\r\n%s" % response.reason)

        return response.json()


    def me():
        """
        Return my own user profiel
        """
        return self.get_user()


    def get_user(id='me'):
        return self.api_call('/users/%s' % id)


    def get_categories(id=None):
        """
        Return category information or root categories
        """
        if not id:
            endpoint = '/sites/%s/categories' % self.site_id
        else:
            endpoint = '/categories/%s' % id

        return self.api_call(endpoint)


    def get_items(user_id, limit=50, offset=0):
        """
        Return all items by user_id
        """

        args = {
                'site_id': seld.site_id, 
                'seller_id': seller_id,
                'limit': limit,
                'offset': offset
                }

        data = self.api_call("/sites/%(site_id)s/search?seller_id=%(seller_id)s&limit=%(limit)s&offset=%(offset)s" % args)

        paging = data.get('paging')
        result = data.get('results')
        collection = MeliCollection(result, paging)

        return collection

