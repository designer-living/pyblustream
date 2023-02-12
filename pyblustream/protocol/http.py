import asyncio
import logging
import aiohttp
from asyncio import Task
from xml.etree import ElementTree
from pyblustream.listener import MatrixConfig
from typing import Any, Optional

from pyblustream.listener import SourceChangeListener


def extract_inputs(xml_tree):
    return extract(xml_tree, "input")


def extract_outputs(xml_tree):
    return extract(xml_tree, "output")


def extract(xml_tree, node_name, name_tag="name"):
    data = {}
    for count, node in enumerate(xml_tree.iter(node_name)):
        input_name = node.find(name_tag).text
        input_name = input_name.replace("_", " ")
        input_id = count + 1
        data[input_id] = input_name
    return data


class MatrixHttpProtocol:

    _update_task: Optional[Task[Any]]

    # noinspection SpellCheckingInspection
    def __init__(self, hostname, callback: SourceChangeListener, port=80, poll_interval_seconds=60):
        self._logger = logging.getLogger(__name__)
        self._poll_interval_seconds = poll_interval_seconds
        self._poll = True
        # noinspection HttpUrlsUsage
        self._url = f"http://{hostname}:{port}/cgi-bin/getxml.cgi?xml=mxsta"

        self._source_change_callback = callback
        self._loop = asyncio.get_event_loop()

        self._update_task = None

    def connect(self):
        self._logger.info("Connecting HTTP")
        self._poll = True
        self._update_task = self._loop.create_task(self._update())

    def close(self):
        self._poll = False
        self._update_task.cancel()

    async def _update(self):
        async with aiohttp.ClientSession(loop=self._loop) as session:
            while self._poll:
                self._logger.info(f"Polling {self._url}")
                async with session.get(self._url) as response:
                    if response.status == 200:
                        response_text = await response.text()
                        self._logger.debug(f"Response {response_text}")

                        xml_tree = ElementTree.fromstring(response_text)

                        inputs = extract_inputs(xml_tree)
                        outputs = extract_outputs(xml_tree)
                        mac = "UNSET"
                        dev_name = "UNSET"
                        software_version = "UNSET"
                        input_ports = -1
                        output_ports = -1
                        for data in xml_tree.iter("webserver"):
                            mac = data.find("mac").text.strip()
                            break
                        for data in xml_tree.iter("mxsta"):
                            dev_name = data.find("devname").text.strip()
                            software_version = data.find("softver").text.strip()
                            input_ports = data.find("inputport").text.strip()
                            output_ports = data.find("outputport").text.strip()
                            break

                        # TODO a listener for this
                        matrix_config = MatrixConfig(
                            mac=mac,
                            name=dev_name,
                            version=software_version,
                            inputs=inputs,
                            outputs=outputs,
                        )
                        self._logger.info("inputs")
                        self._logger.info(inputs)
                        self._logger.info("outputs")
                        self._logger.info(outputs)

                    else:
                        self._logger.error("error", response)
                await asyncio.sleep(self._poll_interval_seconds)
