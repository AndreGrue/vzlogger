#!/usr/bin/env python3
#################################################################################
import json
import asyncio

import generate_prototype as gp
import http_server as httpd
import modbus_server as md


#################################################################################
import sys
import logging
_logger = logging.getLogger()


#################################################################################
# define socket host and port
HTTP_SERVER_HOST = '127.0.0.1'
HTTP_SERVER_PORT = 63333

config = {i['uuid']: i for i in gp.generate_prototype_dict(csvfile="data/config.csv")}
md_args = md.ModbusArgs(unit_id=30)


#################################################################################
class VolkszaehlerPushHandler(httpd.PostHttpHandler):
    def handle_content(self, content: str):
        """ handle content """
        #print("content: \n%s" % (content))
        data_dict = json.loads(content)
        # print(data_dict['data'])
        for uuid_data in data_dict['data']:
            # print(uuid_data['uuid'], ' = ', uuid_data['tuples'])
            uuid = uuid_data['uuid']
            tm = uuid_data['tuples'][0][0]
            val = uuid_data['tuples'][0][1]
            if uuid in config:
                uuid_conf = config[uuid]
                uuid_conf['tm'] = tm
                uuid_conf['value'] = val
                md_args.update_context(0, 3, int(uuid_conf['register']), int(val))
                print(uuid_conf)


#################################################################################
###
def main():
    asyncio.run(md.run_modbus_server(md_args), debug=True)
    httpd.run(handler_class=VolkszaehlerPushHandler, host=HTTP_SERVER_HOST, port=HTTP_SERVER_PORT)


###
if __name__ == "__main__":
    _logger.setLevel(logging.DEBUG)
    _logger.addHandler(logging.StreamHandler(sys.stdout))
    main()
