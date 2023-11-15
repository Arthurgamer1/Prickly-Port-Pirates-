import socket

known_port = 50002

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('localhost', 55555))

while True:
    clients = []
    usernames = []
    while True:
        data, address = sock.recvfrom(128)
        usernames.append(data.decode())
        print(usernames)

        print('connection from: {}'.format(address))
        clients.append(address)

        #sock.sendto(b'ready', address)

        if len(clients) == 2:
            print('got 2 clients, sending details to each')
            break

    c1 = clients.pop()
    c1_addr, c1_port = c1
    user1 = usernames.pop()
    c2 = clients.pop()
    c2_addr, c2_port = c2
    user2 = usernames.pop()

    sock.sendto('{} {} {} {}'.format(c1_addr, c1_port, known_port, user1).encode(), c2)
    sock.sendto('{} {} {} {}'.format(c2_addr, c2_port, known_port, user2).encode(), c1)