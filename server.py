import os
import re
import json
import logging
import asyncio
import concurrent.futures
from itertools import islice
from contextlib import suppress
from tempfile import _get_candidate_names #, _get_default_tempdir

import jwt
import aioredis
from aiohttp import web
from werkzeug.security import check_password_hash

MAX_PAYLOAD_SIZE = 2**30 # 1GB
SECRET_APP_KEY = os.environ['SECRET_KEY'] # may raise exception
GEMM = 'bin/gemm'
GEMV = 'bin/gemv'

# export SECRET_KEY=secret
# admin:password

# u:{username}:pwd

valid_name = re.compile('^[A-Za-z]{1}[A-Za-z0-9]*$')

routes = web.RouteTableDef()


def io_read(filename, mode='r'):
    with open(filename, mode) as f:
        return f.read()


def io_write(wd, mode='w'):
    for filename, data in wd.items():
        with open(filename, mode) as f:
            f.write(data)


def clean_temp_files(*filenames):
    with suppress(FileNotFoundError):
        for i in filenames:
            os.remove(i)


def check_request_token(token, remote):
    try: 
        data = jwt.decode(token, SECRET_APP_KEY, algorithms="HS256")
    except jwt.exceptions.InvalidTokenError as e:
        logging.info(f'request from {remote} with invalid token {str(e)}')
        return None
    except jwt.exceptions.DecodeError as e:
        logging.info(f'request from {remote} with DecodeError {str(e)}')
        return None
    except jwt.exceptions.InvalidSignatureError as e:
        logging.info(f'request from {remote} with InvalidSignatureError {str(e)}')
        return None
    else:
        return data['username']


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
async def handle_gemm(request):
    loop = asyncio.get_running_loop()
    idata = await request.json()
    if (u := check_request_token(idata.get('token'), request.remote)) == None:
        return web.json_response({'status': 'Error', 'message': 'Bad token'})
    logging.info(f'request from user {u}')

    try:
        m, n, k = idata['m'], idata['n'], idata['k']
    except KeyError:
        logging.info(f'user {u} got bad data (m/n/k)')
        return web.json_response({'status': 'Error', 'message': 'Provide m, n, k'})

    f_A, f_B, f_C, f_Z = [i for i in islice(_get_candidate_names(), 4)]
    try:
        wd = {f_A: idata['A'], f_B: idata['B'], f_C: idata['C']}
        alpha, beta = idata['alpha'], idata['beta']
    except KeyError:
        logging.info(f'user {u} got bad data (A/B/C/alpha/beta)')
        return web.json_response({'status': 'Error', 'message': 'Provide A, B, C, alpha and beta'})
    else:    
        with concurrent.futures.ThreadPoolExecutor() as pool:
            await loop.run_in_executor(pool, io_write, wd)

    proc = await asyncio.create_subprocess_shell(
        f'./{GEMM} {m} {n} {k} {alpha} {beta} {f_A} {f_B} {f_C} {f_Z}',
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL)
    
    await proc.wait()

    if proc.returncode != 0:
        logging.error(f'cuda executable returned {proc.returncode}')
        return web.json_response({'status': 'Error', 'message': f'cuda executable returned {proc.returncode}'})

    with concurrent.futures.ThreadPoolExecutor() as pool:
        result_data = await loop.run_in_executor(pool, io_read, f_Z)

    with concurrent.futures.ThreadPoolExecutor() as pool:
        await loop.run_in_executor(pool, clean_temp_files, f_A, f_B, f_C, f_Z) 

    return web.json_response({'status': 'Ok', 'message': '', 'result': result_data})


@routes.post('/gemv')
async def handle_gemv(request):
    loop = asyncio.get_running_loop()
    idata = await request.json()
    if (u := check_request_token(idata.get('token'), request.remote)) == None:
        return web.json_response({'status': 'Error', 'message': 'Bad token'})
    logging.info(f'request from user {u}')


    return web.json_response({'status': 'Ok', 'message': 'Message'})


redis = aioredis.from_url("redis://localhost")
app = web.Application(client_max_size=MAX_PAYLOAD_SIZE)
app.add_routes(routes)
logging.basicConfig(level=logging.INFO) # filename='server.log', 

if __name__ == '__main__':
    web.run_app(app, port=6677)
