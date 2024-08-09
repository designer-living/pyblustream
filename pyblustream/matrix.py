import aiohttp
from typing import Optional

from pyblustream.listener import MultiplexingListener
from pyblustream.protocol import MatrixProtocol
import xmltodict

class Matrix:

    def __init__(self, hostname, port):
        self.hostname : str = hostname
        self._multiplex_callback = MultiplexingListener()
        self._protocol = MatrixProtocol(hostname, port, self._multiplex_callback)
        self.outputs_by_id : dict[int, str] = {}
        self.outputs_by_name : dict[str, int] = {}
        self.inputs_by_id : dict[int, str] = {}
        self.inputs_by_name : dict[str, int] = {}
        self.mac : Optional[str] = None
        self.device_name : Optional[str] = None
        self.firmware_version : Optional[str] = None

    @property
    def output_names(self):
        return list(self.outputs_by_name.keys())

    @property
    def input_names(self):
        return list(self.inputs_by_name.keys())

    async def async_connect(self):
        await self._protocol.async_connect()
        metadata_json = await self._get_matrix_metadata()
        self._process_meta_data(metadata_json)

    def close(self):
        self._protocol.close()

    def change_source(self, input_id: int, output_id: int):
        self._protocol.send_change_source(input_id, output_id)

    def update_status(self):
        self._protocol.send_status_message()

    def status_of_output(self, output_id: int) -> Optional[int]:
        return self._protocol.get_status_of_output(output_id)

    def status_of_all_outputs(self) -> list[tuple[int, Optional[int]]]:
        return self._protocol.get_status_of_all_outputs()

    def turn_on(self):
        self._protocol.send_turn_on_message()

    def turn_off(self):
        self._protocol.send_turn_off_message()

    def is_on(self) -> bool:
        return self._protocol.is_matrix_on

    def register_listener(self, listener):
        self._multiplex_callback.register_listener(listener)

    def unregister_listener(self, listener):
        self._multiplex_callback.unregister_listener(listener)

    def _process_meta_data(self, metadata_json):
        # Extract required fields
        webserver = metadata_json.get('MATRIX', {}).get('webserver', {})
        mxsta = metadata_json.get('MATRIX', {}).get('mxsta', {})
        
        self.mac = webserver.get('mac', '')
        self.device_name = mxsta.get('devname', '')
        self.firmware_version = mxsta.get('softver', '')

        # Extract input names
        inputs = metadata_json.get('MATRIX', {}).get('input', [])
        input_names = [input_item.get('name', '').replace("_", " ") for input_item in inputs]
        for (index, input_name) in enumerate(input_names, start=1):
            self.inputs_by_id[index] = input_name
            self.inputs_by_name[input_name] = index

        # Extract output names
        outputs = metadata_json.get('MATRIX', {}).get('output', [])
        output_names = [output_item.get('name', '').replace("_", " ") for output_item in outputs]
        for (index, output_name) in enumerate(output_names, start=1):
            self.outputs_by_id[index] = output_name
            self.outputs_by_name[output_name] = index

    async def _get_matrix_metadata(self) -> str:
        url = f"http://{self.hostname}/cgi-bin/getxml.cgi?xml=mxsta"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response_text = await response.text()
                return xmltodict.parse(response_text)                
