import RPi.GPIO as GPIO
import time

class Button:
    def __init__(self, pin_input_):
        self.pin_input = pin_input_
        self.last_sens = 0
        self.state_sens = 1
        self.last_debounce = 0
        self.old_state = 0
        # GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_input, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def update(self):
        sens_ = GPIO.input(self.pin_input)
        if sens_ != self.last_sens:
            self.last_debounce = time.time()

        if time.time() - self.last_debounce > 0.1:
            if sens_ != self.state_sens:
                self.state_sens = sens_
        
        self.last_sens = sens_

    def get_state(self) -> bool:
        state_ = False
        if self.state_sens == 0 :
            state_ = True
        return state_
    
    def get_bang(self) -> bool:
        state_ = False
        if self.state_sens == 0 and self.old_state == 1:
            state_ = True
        self.old_state = self.state_sens
        return state_

    def __del__(self):
        print("quitting button")
        GPIO.cleanup()

if __name__ == '__main__':
    button = Button(17)
    while True :
        button.update()
        print(button.get_state())
        time.sleep(0.01)
