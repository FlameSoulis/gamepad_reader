"""Importing PyGame & WebSocketServer"""
import pygame
from websocket_server import WebsocketServer

# PyGame initialization and setup
pygame.init()
MASTER_CLOCK = pygame.time.Clock()
MASTER_CLOCK_TIME = 144

# Some globals for joysticks
JOYSTICK_HANDLE = None
JOYSTICK_TO_USE = None
JOYSTICK_AXES = []
JOYSTICK_BUTTONS = []

# Some globals for websockets
WEBSOCKET_SERVER = None
WEBSOCKET_PORT = 5309

def setupJoystick():
    """Runs a setup sequence for picking the right joystick"""
    # Keep an eye on the globals
    global JOYSTICK_TO_USE

    print(f"Total Joysticks Found:{pygame.joystick.get_count()}")
    for _x in range(pygame.joystick.get_count()):
        print(f"{_x} - {pygame.joystick.Joystick(_x).get_name()}")

    print("Press a button on the controller you wish to use.")
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    EXIT_LOOP = False
    while not EXIT_LOOP:
        MASTER_CLOCK.tick(MASTER_CLOCK_TIME)
        pygame.event.get()
        for _x in range(pygame.joystick.get_count()):
            for _y in range(joysticks[_x].get_numbuttons()):
                if joysticks[_x].get_button(_y):
                    JOYSTICK_TO_USE = _x
                    EXIT_LOOP = True

    print(f"Using {pygame.joystick.Joystick(JOYSTICK_TO_USE).get_name()}")
    for _x in range(pygame.joystick.get_count()):
        joysticks[_x].quit()

def compareInputs(a,b):
    """Compares two arrays and returns true if all is the same"""
    if len(a) != len(b):
        return False
    for _value in range(len(a)):
        if a[_value] != b[_value]:
            return False
    return True

def arrayDump(arg):
    """Dumps an array to a CSV."""
    export_variable = ""
    for index,value in enumerate(arg):
        export_variable += str(value)
        if (index + 1) != len(arg):
            export_variable += ','
    return export_variable

def new_user_notice(_client, _server):
    """Notifies console when a new user joins."""
    print()
    print("New connection!")
    print()

#Setup the joystick
print()
setupJoystick()
JOYSTICK_HANDLE = pygame.joystick.Joystick(JOYSTICK_TO_USE)
JOYSTICK_HANDLE.init()

# Setup the arrays
JOYSTICK_AXES = list(range(JOYSTICK_HANDLE.get_numaxes()))
JOYSTICK_BUTTONS = list(range(JOYSTICK_HANDLE.get_numbuttons()))
TEMP_JOYSTICK_AXES = []
TEMP_JOYSTICK_BUTTONS = []

# Get the websocket server going
print(f"Starting Websocket Server on port {WEBSOCKET_PORT}...")
WEBSOCKET_SERVER = WebsocketServer(host='0.0.0.0', port=WEBSOCKET_PORT)
WEBSOCKET_SERVER.set_fn_new_client(new_user_notice)
WEBSOCKET_SERVER.run_forever(True)

# Main Loop
print()
EXIT_LOOP = False
while not EXIT_LOOP:
    try:
        #Take a sip and run some updates
        MASTER_CLOCK.tick(MASTER_CLOCK_TIME)
        pygame.event.get()

        # Grab the Axis data
        for _axis in range(JOYSTICK_HANDLE.get_numaxes()):
            JOYSTICK_AXES[_axis] = round(JOYSTICK_HANDLE.get_axis(_axis),3)

        # Grab the Button data
        for _button in range(JOYSTICK_HANDLE.get_numbuttons()):
            JOYSTICK_BUTTONS[_button] = JOYSTICK_HANDLE.get_button(_button)

        # Do we have any updates?
        if not compareInputs(TEMP_JOYSTICK_AXES, JOYSTICK_AXES):
            print(f"Axes:{JOYSTICK_AXES}")
            WEBSOCKET_SERVER.send_message_to_all(arrayDump(["axes"]+JOYSTICK_AXES))
        if not compareInputs(TEMP_JOYSTICK_BUTTONS, JOYSTICK_BUTTONS):
            print(f"Btns:{JOYSTICK_BUTTONS}")
            WEBSOCKET_SERVER.send_message_to_all(arrayDump(["btns"]+JOYSTICK_BUTTONS))
        
        # Update our temporary values
        TEMP_JOYSTICK_AXES =  JOYSTICK_AXES.copy()
        TEMP_JOYSTICK_BUTTONS = JOYSTICK_BUTTONS.copy()

    except KeyboardInterrupt:
        print("Keyboard Interrupt Detected - Closing")
        break

pygame.quit()