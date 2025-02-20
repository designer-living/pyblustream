import aiohttp
from .matrix import Matrix


class ACM(Matrix):
    def __init__(self, hostname, port):
        super().__init__(hostname, port)
        self.output_details: dict[str, int] = {}
        self.input_details: dict[str, int] = {}

    def get_input_image_url(self, input_id):
        return f"http://{self.hostname}/cgi-bin/capture.cgi?hostip={self.input_details.get(input_id, {}).get('ip')}"

    def get_output_image_url(self, output_id):
        return f"http://{self.hostname}/cgi-bin/capture.cgi?hostip={self.output_details.get(output_id, {}).get("ip")}"

    def get_initial_output_source_id(self, output_id):
        return self.output_details.get(output_id, {}).get("input_id", "")

    def send_guest_command(self, guest_is_input, guest_id, command):
        return self._protocol.send_guest_command(guest_is_input, guest_id, command)

    def _process_meta_data(self, metadata_json):
        # Extract required fields
        netsta = metadata_json.get("netsta", {})
        syssta = metadata_json.get("syssta", {})

        self.mac = netsta.get("cmac", "")
        self.device_name = syssta.get("devname", "")
        self.firmware_version = syssta.get("softver", "")

        # Extract input names
        inputs = metadata_json.get("in", [])
        for input in inputs:
            id = input.get("id", None)
            name = input.get("name", None)
            if id is not None and name is not None:
                self.inputs_by_id[id] = name
                self.inputs_by_name[name] = id
                self.input_details[id] = {
                    "ip": input.get("ip", ""),
                    "ver": input.get("ver", ""),
                }

        # Extract output names
        outputs = metadata_json.get("out", [])
        for output in outputs:
            id = output.get("id", None)
            output_name = output.get("name", "").replace("_", " ")
            self.outputs_by_id[id] = output_name
            self.outputs_by_name[output_name] = id
            self.output_details[id] = {
                "ip": output.get("ip", ""),
                "ver": output.get("ver", ""),
                "input_id": output.get("fr", ""),
            }

    async def _get_matrix_metadata(self) -> str:
        url = f"http://{self.hostname}/cgi-bin/getjson.cgi?json=mxsta"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response_text = await response.text()
                import json

                return json.loads(response_text)
