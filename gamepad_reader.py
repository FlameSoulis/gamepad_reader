"""Importing PyGame"""
import pygame

pygame.init()
MASTER_CLOCK = pygame.time.Clock()
MASTER_CLOCK_TIME = 144

JOYSTICK_HANDLE = None
JOYSTICK_TO_USE = None
JOYSTICK_AXES = {}
JOYSTICK_BUTTONS = {}

def setupJoystick():
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
    if len(a) != len(b):
        return False
    for _value in range(len(a)):
        if a[_value] != b[_value]:
            return False
    return True

#Setup the joystick
setupJoystick()
JOYSTICK_HANDLE = pygame.joystick.Joystick(JOYSTICK_TO_USE)
JOYSTICK_HANDLE.init()

# Setup the temporary arrays
TEMP_JOYSTICK_AXES = {}
TEMP_JOYSTICK_BUTTONS = {}

# Main Loop
EXIT_LOOP = False
while not EXIT_LOOP:
    try:
        #Take a sip
        MASTER_CLOCK.tick(MASTER_CLOCK_TIME)

        #Run some updates
        pygame.event.get()

        # Grab the Axis data
        for _axis in range(JOYSTICK_HANDLE.get_numaxes()):
            JOYSTICK_AXES[_axis] = round(JOYSTICK_HANDLE.get_axis(_axis),3)
        #print(f"Axes:{JOYSTICK_AXES}")

        # Grab the Button data
        for _button in range(JOYSTICK_HANDLE.get_numbuttons()):
            JOYSTICK_BUTTONS[_button] = JOYSTICK_HANDLE.get_button(_button)
        #print(f"Buttons:{JOYSTICK_BUTTONS}")

        # Do we have any updates?
        if not compareInputs(TEMP_JOYSTICK_AXES, JOYSTICK_AXES):
            print(f"Axes:{JOYSTICK_AXES}")
        if not compareInputs(TEMP_JOYSTICK_BUTTONS, JOYSTICK_BUTTONS):
            print(f"Btns:{JOYSTICK_BUTTONS}")
        
        # Update our temporary values
        TEMP_JOYSTICK_AXES =  JOYSTICK_AXES.copy()
        TEMP_JOYSTICK_BUTTONS = JOYSTICK_BUTTONS.copy()
    except KeyboardInterrupt:
        print("Keyboard Interrupt Detected - Closing")
        break

pygame.quit()