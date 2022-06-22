from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
import asyncio
import time
import board
import neopixel

# NEOPIXEL
pixel_pin = board.D18
num_pixels = 12
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

def turn_off():
    pixels.fill((0, 0, 0))
    pixels.show()
    time.sleep(0.01)

def ring_anim(wait):
    turn_off()
    for i in range(num_pixels):
        pixels[i] = (255, 0, 0)
        pixels.show()
        time.sleep(wait)
        # time.sleep(1)
    turn_off()

def filter_handler(address, *args):
    print(f"{address}: {args}")
    if address == "/record" and len(args) > 0:
        t_rec_ = args[0]
        dly_pix_ = t_rec_ / float(num_pixels)
        print(t_rec_, dly_pix_)
        ring_anim(dly_pix_)

dispatcher = Dispatcher()
dispatcher.map("/record", filter_handler)

ip = "127.0.0.1"
port = 1337

async def loop():
    turn_off()

    for i in range(100):
        print(f"Loop {i}")
        await asyncio.sleep(1)

async def init_main():
    server = AsyncIOOSCUDPServer((ip, port), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()  # Create datagram endpoint and start serving

    await loop()  # Enter main loop of program

    transport.close()  # Clean up serve endpoint

if __name__ == "__main__":
    asyncio.run(init_main())