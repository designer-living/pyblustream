import asyncio
import getopt
import logging
import sys

from pyblustream.listener import LoggingListener
from pyblustream.matrix import Matrix

STOP = asyncio.Event()


def print_usage():
    print('main.py -h <matrix ip address> [-p <port> -s <output_id> -o <output_id> -i <input_id> -a -l]')
    print('\t-h hostname or ip\t\t\tHostname or IP of the matrix - required')
    print('\t-p port\t\t\t\t\t\tPort of the matrix to connect to - defaults to 23')
    print('\t-o output_id -i input_id\tSet output ID to use input ID - both must be specified')
    print('\t-s output_id\t\t\t\tDisplay the input for this output ID must be specified as a string e.g. 02')
    print('\t-a\t\t\t\t\t\t\tDisplay the input for all outputs')
    print('\t-l\t\t\t\t\t\t\tContinue running and listen for source changes')


async def main(argv):
    ip = None
    port = 23
    input_id = None
    output_id = None
    status_output_id = None
    get_statuses = False
    listen = False
    try:
        opts, args = getopt.getopt(argv, "h:p:i:o:s:al", ["ip=", "port="])
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--ip"):
            ip = arg
        elif opt in ("-p", "--port"):
            port = arg
        elif opt in ("-i", "--input"):
            input_id = int(arg)
        elif opt in ("-o", "--output"):
            output_id = int(arg)
        elif opt in ("-s", "--status"):
            status_output_id = arg
        elif opt in ("-a", "--statuses"):
            get_statuses = True
        elif opt in ("-l", "--listen"):
            listen = True
    if ip is None:
        print_usage()
        sys.exit(2)
    elif input_id is not None and output_id is None:
        print("If you set input_id you must specify an output_id")
        sys.exit(2)
    elif output_id is not None and input_id is None:
        print("If you set output_id you must specify an input_id")
        sys.exit(2)

    logging.info("starting up..")

    matrix = Matrix(ip, port)
    if listen:
        matrix.register_listener(LoggingListener())
    matrix.connect()

    delay = 1
    if output_id is not None and input_id is not None:
        asyncio.create_task(change_source(delay, output_id, input_id, matrix))
        delay += 1

    if status_output_id is not None:
        asyncio.create_task(status(delay, status_output_id, matrix))
        delay += 1

    if get_statuses:
        asyncio.create_task(statuses(delay, matrix))
        delay += 1

    if not listen:
        await asyncio.create_task(schedule_exit(delay))
    await STOP.wait()


def ask_exit(*args):
    STOP.set()


async def schedule_exit(delay):
    await asyncio.sleep(delay)
    ask_exit()


async def done(delay):
    await asyncio.sleep(delay)


async def change_source(delay, output_id, input_id, matrix):
    await asyncio.sleep(delay)
    matrix.change_source(output_id, input_id)


async def status(delay, output_id, matrix):
    await asyncio.sleep(delay)
    current_status = matrix.status_of_output(output_id)
    logging.info(current_status)


async def statuses(delay, matrix):
    await asyncio.sleep(delay)
    current_statuses = matrix.status_of_all_outputs()
    logging.info(current_statuses)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main(sys.argv[1:]))
    except KeyboardInterrupt:
        ask_exit()
    logging.info("Finished")
