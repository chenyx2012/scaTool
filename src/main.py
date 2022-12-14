# -*- coding: utf-8 -*-
from concurrent.futures import ThreadPoolExecutor
import json
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from scancode import cli
from tornado.concurrent import run_on_executor
import config
from reposca.itemLicSca import ItemLicSca
from reposca.licenseCheck import LicenseCheck
from reposca.prSca import PrSca

from tornado import gen

from util.postOrdered import infixToPostfix

class Main(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(1000)

    @gen.coroutine
    def get(self):
        """get请求"""
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        prUrl = self.get_argument('prUrl')
        result = yield self.block(prUrl)
        self.finish(str(result))

    @gen.coroutine
    def post(self):
        '''post请求'''
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        prUrl = self.get_argument('prUrl')
        result = yield self.block(prUrl)
        self.finish(str(result))
    
    @run_on_executor
    def block(self, prUrl):
        prSca = PrSca()
        result = prSca.doSca(prUrl)
        jsonRe = json.dumps(result)
        return jsonRe
 
class LicSca(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(1000)

    @gen.coroutine
    def get(self):
        """get请求"""
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        url = self.get_argument('purl')
        url = json.loads(url)
        result = yield self.block(url)
        self.finish(result)

    @gen.coroutine
    def post(self):
        '''post请求'''
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        url = self.get_argument('purl')    
        url = json.loads(url)
        result = yield self.block(url)
        self.finish(result)
    
    @run_on_executor
    def block(self, url):
        itemLic = ItemLicSca()
        result = itemLic.scaPurl(url)
        jsonRe = json.dumps(result)
        return jsonRe
    
class ItemSca(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(1000)

    @gen.coroutine
    def get(self):
        """get请求"""
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        url = self.get_argument('url')
        result = yield self.block(url)
        self.finish(str(result))

    @gen.coroutine
    def post(self):
        '''post请求'''
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        url = self.get_argument('url')    
        result = yield self.block(url)
        self.finish(str(result))
    
    @run_on_executor
    def block(self, url):
        itemLic = ItemLicSca()
        result = itemLic.licSca(url)
        jsonRe = json.dumps(result)
        return jsonRe

application = tornado.web.Application([(r"/sca", Main), (r"/lic", LicSca), (r"/doSca", ItemSca),])

if __name__ == '__main__':
    httpServer = tornado.httpserver.HTTPServer(application)
    httpServer.bind(config.options["port"])   
    httpServer.start(1)
    tornado.ioloop.IOLoop.current().start()