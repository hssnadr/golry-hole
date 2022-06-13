import RPi.GPIO as GPIO
import time

class Button:
    def __init__(self, pin_input_):
        self.pin_input = pin_input_
        self.last_sens = 0
        self.state_sens = 0
        self.last_debounce = 0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_input, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def update(self):
        sens_ = GPIO.input(self.pin_input) # reverse val
        if sens_ != self.last_sens:
            self.last_debounce = time.time()

        if time.time() - self.last_debounce > 0.1:
            if sens_ != self.state_sens:
                self.state_sens = sens_
                print("HEEEERRRREEEEEE")
        
        self.last_sens = sens_

    def getState(self) -> bool:
        state_ = False
        if self.state_sens == 0:
            state_ = True
        return state_
    
    def __del__(self):
        print("quitting button")
        GPIO.cleanup()

if __name__ == '__main__':
    button = Button(17)
    while True :
        button.update()
        print(button.getState())
        time.sleep(0.01)
