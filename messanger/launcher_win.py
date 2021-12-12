import subprocess

processes = []

while True:
    action = input('Select action: q - exit, s - start server and clients, x - close all terminals: ')

    if action == 'q':
        break
    elif action == 's':
        processes.append(subprocess.Popen('python server.py',
                                          creationflags=subprocess.CREATE_NEW_CONSOLE))
        for i in range(2):
            processes.append(subprocess.Popen(f'python client.py -m send -n Sender_{i + 1}',
                                              creationflags=subprocess.CREATE_NEW_CONSOLE))
        for i in range(5):
            processes.append(subprocess.Popen(f'python client.py -m listen -n Listener_{i + 1}',
                                              creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif action == 'x':
        while processes:
            proc = processes.pop()
            proc.kill()
