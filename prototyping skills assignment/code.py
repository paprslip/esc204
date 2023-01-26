'''
ESC204H1S 2023 Prototyping Skills Assignment
2359ET XX February 2023
Claire Zhang, Terrence Zhang
'''
#Libraries
import board
import digitalio
import time

#State class implements finite state machine as an object
class State:
    def __init__(self, r_addr, g_addr, b_addr):
        self.led_state = 0
        self.prev_state = True

        self.r_led = LED(r_addr)
        self.g_led = LED(g_addr)
        self.b_led = LED(b_addr)

    def update_state(self):                 # state machine has 3 states, represented by 0,1,2
        if self.led_state < 2:
            self.led_state += 1
        else:
            self.led_state = 0

    def update_led(self):                   # changes led based on the state
        if self.led_state is 0:             # 0: all LEDs off
            self.r_led.off()
            self.g_led.off()
            self.b_led.off()

        elif self.led_state is 1:           # 1: red and green LEDs
            self.r_led.on()
            self.g_led.off()
            self.b_led.on()

        else:                               # 2: red, green, blue LEDs
            self.r_led.on()
            self.g_led.on()
            self.b_led.on()
        

    def counter(self, button):              # Counter registers true/false cycles, i.e. full down up button presses
        curr_state = button
        if curr_state is not self.prev_state:
            if curr_state is True:
                self.update_state()
                self.update_led()
                print('Readiness Level: ', self.led_state)
                
        self.prev_state = curr_state

# Implement LEDs as a class to make life easier
class LED:                                  
    def __init__(self, addr):
        self.led = digitalio.DigitalInOut(addr)
        self.led.direction = digitalio.Direction.OUTPUT
        self.led.value = False
    
    def on(self):                           # Turn LEDs on
        self.led.value = True

    def off(self):                          # Turn LEDs off
        self.led.value = False
        
    def toggle(self):                       # Switch (i.e. if off, then toggle on)
        if self.led.value is True:
            self.led.value = False
        else:
            self.led.value = True

# Implement buttons as a class
class Btn:
    def __init__(self, addr):
        self.button = digitalio.DigitalInOut(addr)
        self.button.direction = digitalio.Direction.INPUT
        self.button.pull = digitalio.Pull.UP



# Main
state_machine = State(board.GP14, board.GP15, board.GP13)       # initialize state machine object w/ mapped LEDs
board_button = Btn(board.GP12)                                  # initialize button
indicator_led = LED(board.LED)                                  # initialize LED mapped to the board LED

print('Air defense active.')
print('Readiness level on initialization: ', state_machine.led_state)

while True:                                                     # loop to ensure code runs indefinitely
    indicator_led.toggle()                                      # LED will toggle every clock cycle to indicate system is on
    state_machine.counter(board_button.button.value)
    time.sleep(0.05)                                            # delay to prevent cycling (hold time + setup time violations)
    state_machine.counter(board_button.button.value)
    time.sleep(0.05) 
