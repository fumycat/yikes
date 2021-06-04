import logging
import asyncio

import aioredis
from aiohttp import web

routes = web.RouteTableDef()

@routes.get('/gemm')
async def handle(request):
    idata = await request.json()
    print(idata)
    return web.json_response({'status': 'Ok', 'message': 'Message'})


app = web.Application()
app.add_routes(routes)

logging.basicConfig(filename='server.log', level=logging.INFO)

if __name__ == '__main__':
    web.run_app(app, port=6677)
