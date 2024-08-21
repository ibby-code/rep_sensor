# Write your code here :-)
import time
import board
import neopixel
import digitalio
import busio
import microcontroller
import adafruit_bno055

REFRESH_RATE_HZ = 25 

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255) 

switch = digitalio.DigitalInOut(board.A1)
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 0.3
led = digitalio.DigitalInOut(board.LED)
led.switch_to_output()
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)

readonly_switch = digitalio.DigitalInOut(board.D4)
readonly_switch.direction = digitalio.Direction.INPUT
readonly_switch.pull = digitalio.Pull.UP

def write_value(val, file = None, flush = False): 
    if file:
        fp.write(val)
        if flush:
            fp.flush()
    else:
        print(val)

def run_loop(file = None):
    activated = False
    switchValue = False
    while True:
        time.sleep(1.0 / REFRESH_RATE_HZ)
        if not switchValue and switch.value:
            activated = not activated
            # start a new entry
            if activated:
                write_value('\n', file)
                write_value('Accel:Gryo:Quarternion:LinearAccel:Gravity\n', file)
        switchValue = switch.value

        if activated:
            pixel.fill(GREEN) if file else pixel.fill(BLUE) 
            write_value(f'{sensor.acceleration}:{sensor.gyro}:{sensor.quaternion}:{sensor.linear_acceleration}:{sensor.gravity}\n', file, True)
        else:
            pixel.fill(RED)

if readonly_switch.value:
    run_loop()
else:
    try:
        with open("/log.txt", "a") as fp:
            run_loop(fp)
    except OSError as e:  # Typically when the filesystem isn't writeable...
        delay = 0.5  # ...blink the LED every half second.
        if e.args[0] == 28:  # If the file system is full...
            delay = 0.25  # ...blink the LED faster!
        while True:
            led.value = not led.value
            time.sleep(delay)