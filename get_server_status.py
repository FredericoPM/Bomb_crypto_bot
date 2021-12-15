import requests
import json    
import asyncio
import global_variables

async def main():
    loop = asyncio.get_event_loop()
    request = loop.run_in_executor(None, requests.get, 'https://bombcryptosimulator.com/apidata.txt')
    response = await request 
    response_body = json.loads(response.text)
    global_variables.server_status = response_body['status']

asyncio.run(main())

