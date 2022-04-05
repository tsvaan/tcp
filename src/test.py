#!/usr/bin/python3
# coding=utf-8
__author__ = 'Vasily.A.Tsilko'
# Python 3.5+
# Simple test client for tcp_server.py

import asyncio
import datetime
import random

ADDRESS = ("localhost", 10000)
LOOPS = 100  # How many times will be send data string

async def tcp_client():
   
    for i in range(LOOPS):
        dt = datetime.datetime.now()
        time = dt.strftime("%H:%M:%S")
        ms = dt.strftime("%f")[:-3]
        group = random.randint(0, 2)
        
        reader, writer = await asyncio.open_connection(*ADDRESS)
        message = "{:0=4} C1 {}.{} 0{}\r".format(i, time, ms, group)
        print(f'Send: {message!r}')
        writer.write(message.encode())
        await writer.drain()
        writer.close()
        await writer.wait_closed()

asyncio.run(tcp_client())