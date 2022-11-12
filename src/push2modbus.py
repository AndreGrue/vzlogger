#!/usr/bin/env python3
#################################################################################
import generate_prototype as gp
import http_server as httpd

#################################################################################
config = { i['uuid'] : i for i in gp.generate_prototype_dict(csvfile = "data/config.csv")}




#################################################################################
# define socket host and port
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 63333

###
def main():
    httpd.run(handler_class=httpd.PostHttpHandler, host=SERVER_HOST, port=SERVER_PORT)

###
if __name__ == "__main__":
    main()

