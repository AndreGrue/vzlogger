#!/usr/bin/env python3
#################################################################################
from typing import Any, List, Dict
import sys
import time
import threading
import generate_prototype as gp
import modbus_server as ms
import logging
_logger = logging.getLogger()


###
def modicon2adr(modicon: str) -> int:
    '''

    :param modicon:
    :return:
    '''
    madr = int(modicon)
    if 300000 < madr:
        return madr - 300000
    elif 400000 < madr:
        return madr - 400000
    else:
        return madr


###
def make_int(value: str) -> int:
    if '0x' in value:
        return int(value, 16)
    else:
        return int(value)


###
def type2value(dtype: str, value: str) -> Any:
    '''

    :param self:
    :param dtype:
    :param value:
    :return:
    '''
    if 'int16' == dtype or 'INT16' == dtype:
        return [int(value)]
    elif 'uint16' == dtype or 'UINT16' == dtype:
        return [int(value)]
    elif 'int32' == dtype or 'INT32' == dtype:
        return [0xFFFF & int(value), 0xFFFF0000 & int(value) >> 16]
    elif 'uint32' == dtype or 'UINT32' == dtype:
        return [0xFFFF & int(value), 0xFFFF0000 & int(value) >> 16]
    elif 'string' in dtype:
        return str(value)
    else:
        return None


###
class EM24ModbusDataBlock(ms.CustomModbusDataBlock):
    def getValues(self, address, count=1):
        """

        :param address:
        :param count:
        :return:
        """
        if address == 12 and count == 1:  # spezific handling for gavazzi id code
            value = [1650]
            _logger.info(f"modbus: get address = {address}, count = {count}, val = {value}")
        else:
            value = super().getValues(address, count)
        return value


###
class EM24ModbusConfig(ms.ModbusConfig):
    """

    """
    def __init__(self, config: List[Dict], host="", port=502, unit_id=1):
        self._config = config
        super().__init__(host, port, unit_id)

    def make_datablock(self):
        values = {}
        # _logger.debug(f'config = {self._config}')
        for i in self._config:
            address = modicon2adr(i['Modicon address'])
            init = i['Initial']
            dtype = i['Data type']
            values[address] = type2value(dtype, init)
            _logger.debug(f'modbus: config, adr={address}, type={dtype}, init={init}')

        _logger.debug(f'config = {values}')
        return EM24ModbusDataBlock(values, self._config)

    def update_context(self, slave_id, register, address, value):
        config = next(item for item in self._config if item["Modicon address"] == address)
        if config is not None:
            adr = modicon2adr(config['Modicon address']) - 1
            min = config['Min']
            max = config['Max']
            factor = float(config['Scale factor'])
            unit = config['Unit']
            length = config['Length']
            dtype = config['Data type']
            val = type2value(dtype, value * factor)

            super().update_context(0, 3, adr, val)


###
def main():
    csv_config = "data/em24_config.csv"
    config = gp.generate_prototype_dict(csv_config, delimiter=';')
    args = EM24ModbusConfig(config)

    x = threading.Thread(target=ms.run_modbus_server, args=(args, ))
    x.start()
    for i in range(0, 100):
        time.sleep(1)
        args.update_context(0, 0, '300001', 200+i)
    x.join()


###
if __name__ == "__main__":
    _logger.setLevel(logging.INFO)
    _logger.addHandler(logging.StreamHandler(sys.stdout))
    main()
