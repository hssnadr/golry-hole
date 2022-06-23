from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
import asyncio

import golry_pixels as gpx

# MAIN
running = False

# GOLRY RING
golrypix = gpx.GolryPixels(12)
color_rec = (255,0,0)
color_play = (0,0,255)

# OSC
ip = "127.0.0.1"
port = 1337

def handle_osc(address, *args):
    global running
    print(f"{address}: {args}")

    if address == "/record" and len(args) > 0:
        t_rec_ = args[0]
        golrypix.play_loadring(t_rec_, color_rec)
    
    if address == "/play" and len(args) > 0:
        t_rec_ = args[0]
        # golrypix.play_loadring(t_rec_, color_play)

    if address == "/quit":
        running = False

dispatcher = Dispatcher()
dispatcher.map("/record", handle_osc)
dispatcher.map("/play", handle_osc)
dispatcher.map("/quit", handle_osc)

async def loop():
    global running
    global golrypix

    running = True
    while running:
        golrypix.update()
        await asyncio.sleep(0.1)

async def init_main():
    server = AsyncIOOSCUDPServer((ip, port), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()  # Create datagram endpoint and start serving

    await loop()  # Enter main loop of program

    transport.close()  # Clean up serve endpoint

if __name__ == "__main__":
    asyncio.run(init_main())