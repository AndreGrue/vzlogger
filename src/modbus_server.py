#!/usr/bin/env python3
#################################################################################
from typing import Any
import sys
import generate_prototype as gp

from pymodbus.device import ModbusDeviceIdentification

from pymodbus.datastore import (
    ModbusServerContext,
    ModbusSlaveContext,
    ModbusSparseDataBlock,
    ModbusSequentialDataBlock,
)
from pymodbus.transaction import (
    ModbusSocketFramer,
)

from pymodbus.server import (
    StartAsyncSerialServer,
    StartAsyncTcpServer,
    StartTcpServer,
    StartAsyncTlsServer,
    StartAsyncUdpServer,
)

import logging
_logger = logging.getLogger()


###
class CustomModbusDataBlock(ModbusSparseDataBlock):
    """

    """
    def setValues(self, address, value, use_as_default=False):
        super().setValues(address, value, use_as_default)
        _logger.debug(f"modbus: set {address} = {value}")

    def getValues(self, address, count=1):
        value = super().getValues(address, count)
        _logger.debug(f"modbus: get {address} = {value}")
        return value


###
class ModbusConfig(object):
    """
    """
    def __init__(self, host="", port=502, unit_id=1):
        #
        self.host = host
        self.port = port
        # "ascii", "binary", "rtu", "socket" or "tls"
        self.framer = ModbusSocketFramer
        #
        # datablock = ModbusSequentialDataBlock.create()
        datablock = self.make_datablock()
        slave_context = ModbusSlaveContext(di=datablock, co=datablock, hr=datablock, ir=datablock, unit=unit_id)
        single = True
        self.server_context = ModbusServerContext(slaves=slave_context, single=single)
        #
        self.identity = ModbusDeviceIdentification(
            info_name={
                "VendorName": "AndreGrue",
                "ProductCode": "VLKSZHLRLGGR",
                "VendorUrl": "https://github.com/AndreGrue/vzlogger",
                "ProductName": "VLKSZHLRLGGR Modbus Server",
                "ModelName": "VLKSZHLRLGGR Modbus Server",
                "MajorMinorRevision": "v0.1.0_0",
            })

    def make_datablock(self):
        return CustomModbusDataBlock.create()

    def update_context(self, slave_id, register, address, values):
        """
        :param slave_id:
        :param register:
        :param address:
        :param values:
        :return:
        """
        txt = f"modbus: update, slave_id={slave_id}, register={register}, address={address}, values: {str(values)}"
        _logger.debug(txt)
        # self.server_context[slave_id].setValues(register, address, values)
        self.server_context.setValues(register, address, values)


###
class ModbusConfigCSV(ModbusConfig):
    """
    """
    def __init__(self, csv_config: str, host="", port=502, unit_id=1):
        self._csv_config = csv_config
        self._config = gp.generate_prototype_dict(csvfile=self._csv_config, delimiter=';')
        super().__init__(host, port, unit_id)

    def _type2val(self, dtype: str, value: str) -> Any:
        if 'int16' == dtype:
            return int(value)
        elif 'uint16' == dtype:
            return int(value)
        elif 'int32' == dtype:
            return int(value)
        elif 'uint32' == dtype:
            return int(value)
        elif 'string' in dtype:
            return str(value)

    def make_datablock(self):
        values = {}
        # _logger.debug(f'config = {self._config}')
        for i in self._config:
            address = int(i['Address'])
            init = i['Initial']
            dtype = i['Type']
            values[address] = self._type2val(dtype, init)
            _logger.debug(f'modbus: config, adr={address}, type={dtype}, init={init}')

        _logger.debug(f'config = {values}')
        return CustomModbusDataBlock(values)


###
def run_modbus_server(args):
    """
        Run server
    """
    txt = f"modbus: start server, listening on {args.host}:{args.port}"
    _logger.info(txt)

    server = StartTcpServer(
        context=args.server_context,  # Data storage
        identity=args.identity,  # server identify
        address=(args.host, args.port),  # listen address
        # custom_functions=[],  # allow custom handling
        framer=args.framer,  # The framer strategy to use
        # handler=None,  # handler for each session
        allow_reuse_address=True,  # allow the reuse of an address
        # ignore_missing_slaves=True,  # ignore request to a missing slave
        # broadcast_enable=False,  # treat unit_id 0 as broadcast address,
        # timeout=1,  # waiting time for request to complete
        # TBD strict=True,  # use strict timing, t1.5 for Modbus RTU
        # defer_start=False,  # Only define server do not activate
    )
    return server


###
def main():
    # args = ModbusConfig(unit_id=30)
    args = ModbusConfigCSV(unit_id=30, csv_config="data/modbus_field_list.csv")
    server = run_modbus_server(args)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
    server.shutdown()


###
if __name__ == "__main__":
    _logger.setLevel(logging.DEBUG)
    _logger.addHandler(logging.StreamHandler(sys.stdout))
    main()

