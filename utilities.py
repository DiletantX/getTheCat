def on_press(key):
    try:
        if key.char == 'q':
            print("Q key pressed. Exiting the loop.")
            return False  # Stop listener to exit the loop
    except AttributeError:
        pass
