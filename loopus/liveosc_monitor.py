from pythonosc import dispatcher, osc_server
import asyncio


if __name__ == "__main__":
    ip = '127.0.0.1'

    dispatcher = dispatcher.Dispatcher()
    dispatcher.set_default_handler(print)

    server = osc_server.ThreadingOSCUDPServer((ip, 9000), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()
