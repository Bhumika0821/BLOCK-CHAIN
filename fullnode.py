from fastapi import FastAPI, BackgroundTasks, Request
import uvicorn
import requests
import asyncio
import logging
import sys


from blockchain import Blockchain
from wallet import Wallet


logger = logging.getLogger("Blockchain")

app = FastAPI()
app.config = {}
app.jobs = {}

### TASKS         
def mine(event):
    logger.info('>>>>>>>>>> Starting mining loop')
    while True:
        try:
            def check_stop():
                return event.is_set()
            logger.info(f'>> Starting new block mining')
            _BC.helpfunc_mine_block(check_stop)
            logger.info(f'>> New block mined')
            print("updated blockchain")
            print(_BC.blockchain)
            if event.is_set():
                return
        except asyncio.CancelledError:
            logger.info('>>>>>>>>>> Mining loop stopped')
            return
        except Exception as e:
            logger.exception(e)



@app.on_event("startup")
async def on_startup():
    loop = asyncio.get_running_loop()
    
    if app.config['mine']:
        app.jobs['mining'] = asyncio.Event()
        loop.run_in_executor(None, mine, app.jobs['mining'])
    
@app.on_event("shutdown")
async def on_shutdown():
    if app.jobs.get('mining'):
        app.jobs.get('mining').set()
    



if __name__ == "__main__":

    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)

    _W = Wallet.create()
    _BC = Blockchain(20, _W)
    
    app.config['wallet'] = _W
    app.config['bc'] = _BC

    app.config['nodes'] = set(['127.0.0.1:8000'])
    app.config['mine'] = 1



    print("private key of node is :" + str(_W.private_address))
    print("public key of node is :" + str(_W.public_address))
    
    
    
    _BC.create_first_block()
    uvicorn.run(app, host="127.0.0.1", port=8000, access_log=True)

    