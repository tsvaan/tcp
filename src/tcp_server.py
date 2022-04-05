#!/usr/bin/python3
# coding=utf-8
__author__ = 'Vasily.A.Tsilko'
# Python 3.5+
# TCP Server

import asyncio

"""
In fact this couple of variables should be located in  appropriate def's,
because global variables is evil. But I was pop them here for testers best overview.
"""
ADDRESS = ("localhost", 10000)  # Server host and port, where it waiting a connection
FILENAME = "test.txt"           # Name of file where data will be added

async def get_it (reader, writer):
    data = await reader.readuntil(separator=b'\r')
    msg = data.decode()
    
    try:
        with open (FILENAME, "a") as out:
            out.write(msg)
            out.flush()
            out.close()
    except Exception:
        print("Something wrong with file!")
    
    if msg[21:23] == "00":
        print ("Cпортсмен, нагрудный номер {} прошёл отсечку {} в {}".format(msg[0:4], msg[5:7], msg[8:18]))

    writer.write(b"done\n")
    await writer.drain()
    writer.close()
    await writer.wait_closed()
    return

def main():
    loop = asyncio.get_event_loop()
    factory = asyncio.start_server(get_it, *ADDRESS)
    server = loop.run_until_complete(factory)
    print ("\nServer started")
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print ("\nClosing server")
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()

if __name__ == "__main__":
    main()