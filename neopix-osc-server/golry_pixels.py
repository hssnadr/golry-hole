import time
import board
import neopixel
import math

pixel_pin = board.D18
ORDER = neopixel.GRB

class GolryPixels:
    def __init__(self, num_pix_):
        self.num_pix = num_pix_
        self.strip = neopixel.NeoPixel(pixel_pin, self.num_pix, brightness=0.2, auto_write=False, pixel_order=ORDER)
        self.timer_update_0 = time.monotonic()

        self.is_loadring = False
        self.time_loadring = 0.0
        # self.curindx_loadring = 0
        self.timer_loadring = 0.0
        self.color_loadring = (0, 0, 0)
        self.turn_off()

    def turn_off(self):
        self.strip.fill((0, 0, 0))
        self.strip.show()
    
    def play_loadring(self, time_, color_):
        self.curindx_loadring = 0
        self.time_loadring = time_
        self.color_loadring = color_
        self.timer_loadring = time.monotonic()
        self.is_loadring = True
        self.turn_off()

    def update_loadring(self):
        if self.is_loadring :
            ratio_ = (time.monotonic() - self.timer_loadring) / float(self.time_loadring)
            indx_float_ = self.num_pix * ratio_
            indx_ = int(indx_float_)
            next_ = indx_float_ - indx_

            # for i in range(self.num_pix):
            #     ratio_i_ = math.pow(ratio_, 4) * float(self.num_pix - i)
            #     if i == self.num_pix - 1:
            #         print(ratio_i_)
            #     if ratio_i_ < 1.0:
            #         # self.strip[i] = self.color_loadring
            #         r_ = int(ratio_i_ * self.color_loadring[0])
            #         g_ = int(ratio_i_ * self.color_loadring[1])
            #         b_ = int(ratio_i_ * self.color_loadring[2])
            #         self.strip[i] = (r_,g_,b_)
            #     else :
            #         self.strip[i] = self.color_loadring
            # else :
            #     self.strip.fill(self.color_loadring)
            #     self.is_loadring = False
            
            if indx_ < self.num_pix - 1:
                for i in range(indx_):
                    self.strip[i] = self.color_loadring
                r_ = int(next_ * self.color_loadring[0])
                g_ = int(next_ * self.color_loadring[1])
                b_ = int(next_ * self.color_loadring[2])
                self.strip[indx_] = (r_,g_,b_)
                # print(r_)
            else :
                self.strip.fill(self.color_loadring)
                self.is_loadring = False
    
    def update(self):
        if time.time() - self.timer_update_0 > 0.01:
            self.timer_update_0 = time.monotonic()
            self.update_loadring()
            self.strip.show()

    def __del__(self):
        print("quitting golry pixels")

if __name__ == '__main__':
    print("Golry pixels")
    
    time_ = 30.0
    ring_ = GolryPixels(12)
    ring_.play_loadring(time_, (255,0,0))
    
    t0_ = time.monotonic()
    while time.monotonic() - t0_ < time_ :
        ring_.update()
    
    del ring_
    print("over")