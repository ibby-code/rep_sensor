import board
import digitalio
import storage

switch = digitalio.DigitalInOut(board.D4)

switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

# readonly if D4 connected to ground
storage.remount("/", readonly=switch.value)