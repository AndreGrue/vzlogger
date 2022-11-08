#!/usr/bin/env python3
#################################################################################
import socket

# try to import C parser then fallback in pure python parser.
try:
    from http_parser.parser import HttpParser
except ImportError:
    from http_parser.pyparser import HttpParser
import json

#################################################################################
config = {}
config['1a2e9a30-499f-11ed-bc9c-e1eef2f79f94'] = {'uuid': '1a2e9a30-499f-11ed-bc9c-e1eef2f79f94', 'name': 'Energy IN',
                                                  'register': 2222, 'tm': 0, 'value': 0.0}
config['e66150c0-499f-11ed-861f-0bacdd4bde80'] = {'uuid': 'e66150c0-499f-11ed-861f-0bacdd4bde80', 'name': 'Energy OUT',
                                                  'register': 2222, 'tm': 0, 'value': 0.0}
config['836080a0-48d5-11ed-a8d2-b7e8221ba8dc'] = {'uuid': '836080a0-48d5-11ed-a8d2-b7e8221ba8dc', 'name': 'Voltage L1',
                                                  'register': 2222, 'tm': 0, 'value': 0.0}
config['765c38f0-48d5-11ed-a701-6de734b17f2c'] = {'uuid': '765c38f0-48d5-11ed-a701-6de734b17f2c', 'name': 'Voltage L2',
                                                  'register': 2222, 'tm': 0, 'value': 0.0}
config['68ed2b30-48d5-11ed-be74-27d2b336553f'] = {'uuid': '68ed2b30-48d5-11ed-be74-27d2b336553f', 'name': 'Voltage L3',
                                                  'register': 2222, 'tm': 0, 'value': 0.0}
config['690adb20-48d4-11ed-afb1-85eadc94cb00'] = {'uuid': '690adb20-48d4-11ed-afb1-85eadc94cb00', 'name': 'Current L1',
                                                  'register': 2222, 'tm': 0, 'value': 0.0}
config['789eb380-48d4-11ed-b0c0-516a703616a4'] = {'uuid': '789eb380-48d4-11ed-b0c0-516a703616a4', 'name': 'Current L2',
                                                  'register': 2222, 'tm': 0, 'value': 0.0}
config['50ad3b40-48d4-11ed-89e8-1b722d3ecac8'] = {'uuid': '50ad3b40-48d4-11ed-89e8-1b722d3ecac8', 'name': 'Current L3',
                                                  'register': 2222, 'tm': 0, 'value': 0.0}
config['6b0fa3a0-48d1-11ed-af3b-9d97bcef9c65'] = {'uuid': '6b0fa3a0-48d1-11ed-af3b-9d97bcef9c65', 'name': 'Power L1',
                                                  'register': 2222, 'tm': 0, 'value': 0.0}
config['5b52ec20-48d1-11ed-b268-39d935326b4e'] = {'uuid': '5b52ec20-48d1-11ed-b268-39d935326b4e', 'name': 'Power L2',
                                                  'register': 2222, 'tm': 0, 'value': 0.0}
config['49c8bd30-48d1-11ed-b94d-6faf0be07371'] = {'uuid': '49c8bd30-48d1-11ed-b94d-6faf0be07371', 'name': 'Power L3',
                                                  'register': 2222, 'tm': 0, 'value': 0.0}
config['f7bd32e0-48d0-11ed-a6b7-1f623e4f7ffb'] = {'uuid': 'f7bd32e0-48d0-11ed-a6b7-1f623e4f7ffb', 'name': 'Power',
                                                  'register': 2222, 'tm': 0, 'value': 0.0}
config['e8db9430-48d5-11ed-a68d-978eb98d6807'] = {'uuid': 'e8db9430-48d5-11ed-a68d-978eb98d6807', 'name': 'Frequency',
                                                  'register': 2223, 'tm': 0, 'value': 0.0}

#################################################################################
# Define socket host and port
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 63333

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print('Listening on port %s ...' % SERVER_PORT)

p = HttpParser()

while True:
    # Wait for client connections
    client_connection, client_address = server_socket.accept()

    # Get the client request
    # request = client_connection.recv(2048)
    # print(request)
    # print('\n\n\n\n\n\n\n\n\n\n')

    body = []
    while True:
        data = client_connection.recv(2048)
        if not data:
            break

        recved = len(data)
        nparsed = p.execute(data, recved)
        assert nparsed == recved

        if p.is_headers_complete():
            # print( p.get_headers())
            pass

        if p.is_partial_body():
            body.append(p.recv_body())

        if p.is_message_complete():
            break

    # print("".join(body))
    # print(body)
    # print(type(body[0]))
    data_json = body[0].decode("utf-8")
    data_dict = json.loads(data_json)
    # print(data_dict['data'])
    for uuid_data in data_dict['data']:
        # print(uuid_data['uuid'], ' = ', uuid_data['tuples'])
        uuid = uuid_data['uuid']
        tm = uuid_data['tuples'][0][0]
        val = uuid_data['tuples'][0][1]
        uuid_conf = config[uuid]
        uuid_conf['tm'] = tm
        uuid_conf['value'] = val

    for c in config.items():
        print(c)

    # print(data_json)
    # print(type(data_json))

    print('\n')

    # Send HTTP response
    response = 'HTTP/1.1 200 OK\n\n'
    client_connection.sendall(response.encode())
    client_connection.close()

# Close socket
server_socket.close()



