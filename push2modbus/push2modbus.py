#!/usr/bin/env python3
#################################################################################
import json
import pathlib
import threading
import argparse
import generate_prototype as gp
import http_server as httpd
import modbus_server as ms
import gavazzi_em24 as em24


#################################################################################
parser = argparse.ArgumentParser(description='push2modbus - vzlogger modbus server')
parser.add_argument('-c', '--configuration', type=pathlib.Path, required=True, help='a CSV configuration file')
args = parser.parse_args()


#################################################################################
import sys
import logging
_logger = logging.getLogger()


#################################################################################
# define socket host and port
http_server_host = '127.0.0.1'
http_server_port = 63333
csv_config_file = args.configuration
config = gp.generate_prototype_dict(csv_config_file, delimiter=';')
em24_args = em24.EM24ModbusConfig(config, port=502)
config_dict = {i['uuid']: i for i in config}


#################################################################################
class VolkszaehlerPushHandler(httpd.PostHttpHandler):
    def handle_content(self, content: str):
        """ handle content """
        # print("content: \n%s" % (content))
        data_dict = json.loads(content)
        # print(data_dict['data'])
        for uuid_data in data_dict['data']:
            # print(uuid_data['uuid'], ' = ', uuid_data['tuples'])
            uuid = uuid_data['uuid']
            tm = uuid_data['tuples'][0][0]
            val = uuid_data['tuples'][0][1]
            if uuid in config_dict:
                uuid_conf = config_dict[uuid]
                uuid_conf['tm'] = tm
                uuid_conf['value'] = val
                em24_args.update_context(0, 0, uuid_conf['Modicon address'], float(val))
                # print(uuid_conf)


#################################################################################
###
def main():
    thrd = threading.Thread(target=ms.run_modbus_server, args=(em24_args, ))
    thrd.start()
    httpd.run(handler_class=VolkszaehlerPushHandler, host=http_server_host, port=http_server_port)
    thrd.join()


###
if __name__ == "__main__":
    _logger.setLevel(logging.INFO)
    _logger.addHandler(logging.StreamHandler(sys.stdout))
    main()
