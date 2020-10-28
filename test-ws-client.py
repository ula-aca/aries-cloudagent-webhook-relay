#!/usr/bin/env python3

# This executable can be used to test the websocket connection of a 
# aca-py message processor instance. 

import json
import asyncio
import os

import aiohttp
import argparse

parser = argparse.ArgumentParser(
    prog='test-ws-client',
    description="collects and cache's aca-py webhook calls until requested by controller."
    )

parser.add_argument('--api-key', '-k', action='store', help='the API key to use')
parser.add_argument('--host', '-H', action='store', default='0.0.0.0')
parser.add_argument('--port', '-p', action='store', default=8080)
args = parser.parse_args()

URL = f'ws://{args.host}:{args.port}/ws'

print(f'Connecting to: {URL}')
async def main():
    headers = {}
    if args.api_key:
        headers['Authorization'] = args.api_key
    session = aiohttp.ClientSession(headers=headers)
    async with session.ws_connect(URL) as ws:
        await ws.send_str(json.dumps({
          'auth': args.api_key,
          'fastForward': True
        }))
        async for msg in ws:
            print('Message received from server:')
            print(msg)
            print()
        print('done')


if __name__ == '__main__':
    print('Type "exit" to quit')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
