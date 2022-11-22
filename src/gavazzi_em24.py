#!/usr/bin/env python3
#################################################################################
from typing import Any
import sys
import generate_prototype as gp
import modbus_server as ms

import logging
_logger = logging.getLogger()


###
class EM24ModbusDataBlock(ms.CustomModbusDataBlock):
    """
    """
    def __init__(self, values, config):
        self._config = config
        super().__init__(values)

    def setValues(self, address, value, use_as_default=False):
        """

        :param address:
        :param value:
        :param use_as_default:
        :return:
        """
        super().setValues(address, value, use_as_default)

    def getValues(self, address, count=1):
        """

        :param address:
        :param count:
        :return:
        """
        if address == 12 and count == 1:  # set gavazzi id code
            value = [1650]
            _logger.info(f"modbus: get address = {address}, count = {count}, val = {value}")
        else:
            value = super().getValues(address, count)
        return value


###
class EM24ModbusConfig(ms.ModbusConfig):
    """

    """
    def __init__(self, csv_config: str, host="", port=502, unit_id=30):
        self._csv_config = csv_config
        self._config = gp.generate_prototype_dict(csvfile=self._csv_config, delimiter=';')
        super().__init__(host, port, unit_id)

    def _make_int(self, value: str) -> int:
        if '0x' in value:
            return int(value, 16)
        else:
            return int(value)

    def _type2val(self, dtype: str, value: str) -> Any:
        if 'int16' == dtype or 'INT16' == dtype:
            return int(value)
        elif 'uint16' == dtype or 'UINT16' == dtype:
            return self._make_int(value)
        elif 'int32' == dtype or 'INT32' == dtype:
            return [0xFFFF0000 & int(value) >> 16, 0xFFFF & int(value)]
        elif 'uint32' == dtype or 'UINT32' == dtype:
            return [0xFFFF0000 & int(value) >> 16, 0xFFFF & int(value)]
        elif 'string' in dtype:
            return str(value)
        else:
            return None

    @staticmethod
    def _modicon2adr(modicon: str) -> int:
        madr = int(modicon)
        if 300000 < madr:
            return madr - 300000
        elif 400000 < madr:
            return madr - 400000
        else:
            return madr

    def make_datablock(self):
        values = {}
        # _logger.debug(f'config = {self._config}')
        for i in self._config:
            address = self._modicon2adr(i['Modicon address'])
            init = i['Initial']
            dtype = i['Data format']
            values[address] = self._type2val(dtype, init)
            _logger.debug(f'modbus: config, adr={address}, type={dtype}, init={init}')

        _logger.debug(f'config = {values}')
        return EM24ModbusDataBlock(values, self._config)


###
def main():
    args = EM24ModbusConfig(csv_config="data/em24_config.csv")
    server = ms.run_modbus_server(args)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
    server.shutdown()


###
if __name__ == "__main__":
    _logger.setLevel(logging.INFO)
    _logger.addHandler(logging.StreamHandler(sys.stdout))
    main()
