import Mouse


def set_windows_state(field, state):
    if state == 9:    # Normal
        print()
    elif state == 6:  # Minimize
        print()
    elif state == 3:  # Maximize
        print()


def hide(field):
    raise Exception("Not implemented.")


def show(field):
    raise Exception("Not implemented.")


def activate(field):
    Mouse.click(field)


def close(field):
    Mouse.click(field)


def get_size(handle):
    rect = wintypes.RECT()
    resp = user32.GetWindowRect(handle, ctypes.pointer(rect))
    if resp != 1:
        raise Exception("Window not found.")
    return (rect.left, rect.top, rect.right, rect.bottom)


def set_size(handle, rect):
    user32.MoveWindow(handle, rect[0], rect[1], rect[2], rect[3], True)


def _get_center(field):
    w = field.width / 2
    h = field.height / 2
    return (field.x + w, field.y + h)