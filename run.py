from quart import Quart, jsonify, request
import asyncio, os
from kademlia.network import Server

api = Quart(__name__)

def error(msg):
   return jsonify({'success': False, 'message': msg})

def success(msg):
    return jsonify({'success': True, 'message': msg})

@api.route('/api/set', methods=['GET'])
async def set():
    key = request.args.get('key')
    value = request.args.get('value')
    if not key or not value:
        return error('Required parameters: key, value')
    try:
        resp = await server.set(key, value)
        return success('{} => {}'.format(key, value))
    except Exception as e:
        return error(e)

@api.route('/api/get', methods=['GET'])
async def get():
    key = request.args.get('key')
    if not key:
        return error('Required parameters: key')
    try:
        resp = await server.get(key)
        return success("{} => {}".format(key, resp))
    except Exception as e:
        return error("{}".format(e))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    server = Server()
    server.listen(6881)
    bootstrap_node = (os.environ['BOOTSTRAP_NODE'], 6888)
    loop.run_until_complete(server.bootstrap([bootstrap_node]))
    api.run(host="0.0.0.0")
 
