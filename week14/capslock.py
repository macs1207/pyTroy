import win32api


locks = [0x90, 0x14, 0x91]
previous_status = [0, 0, 0]
key_name = ["NumLock", "CapsLock", "Scroll Lock"]

while True:
    for lock in locks:
        status = win32api.GetKeyState(lock)
        status = status & 1
        if status != previous_status[locks.index(lock)]:
            previous_status[locks.index(lock)] = status
            for i in range(3):
                print(
                    f'{key_name[i]}: {"ON" if previous_status[i] else "OFF":<6s}', end='')
                if i == 2:
                    print()
