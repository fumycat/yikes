import os
import re
import json
import logging
import datetime
import asyncio
import concurrent.futures
from tempfile import _get_candidate_names, _get_default_tempdir

import jwt
import aioredis
from aiohttp import web
from werkzeug.security import check_password_hash

MAX_PAYLOAD_SIZE = 2**30 # 1GB
SECRET_APP_KEY = os.environ['SECRET_KEY'] # may raise exception

# export SECRET_KEY=secret
# admin:password

# u:{username}:pwd

valid_name = re.compile('^[A-Za-z]{1}[A-Za-z0-9]*$')

routes = web.RouteTableDef()


def io_write(filename, data, mode='w'):
    with open(filename, mode) as f:
        f.write(data)

@routes.post('/auth')
async def auth(request):
    idata = await request.json()
    username = idata.get('username')
    password = idata.get('password')
    if not username or not password or not valid_name.match(username):
        return web.json_response({'status': 'Error', 'message': 'Provide username and password'})

    p_hash = await redis.get(f'u:{username}:pwd')

    if not p_hash:
        return web.json_response({'status': 'Error', 'message': 'User doesn\'t exist'})
    
    p_hash = p_hash.decode()

    if check_password_hash(p_hash, password):
        token = jwt.encode({'username' : username}, SECRET_APP_KEY)
        return web.json_response({'status': 'Ok', 'token': token})
    else:
        return web.json_response({'status': 'Error', 'message': 'Wrong password'})


@routes.post('/gemm')
async def handle(request):
    idata = await request.json()
    print(idata)
    return web.json_response({'status': 'Ok', 'message': 'Message'})


@routes.post('/upload')
async def test_upload(request):
    loop = asyncio.get_running_loop()
    idata = await request.json()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        await loop.run_in_executor(pool, io_write, 'test.txt', idata['data'])

    return web.json_response({'status': 'Ok', 'message': 'Message'})


redis = aioredis.from_url("redis://localhost")
app = web.Application(client_max_size=MAX_PAYLOAD_SIZE)
app.add_routes(routes)
logging.basicConfig(level=logging.INFO) # filename='server.log', 

'''
async def po():
    cctest = await redis.get('u:admin:pwd')
    print(cctest, type(cctest))

asyncio.run(po())
exit()
'''

if __name__ == '__main__':
    web.run_app(app, port=6677)
