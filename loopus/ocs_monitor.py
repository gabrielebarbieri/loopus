from pythonosc import dispatcher, osc_server


if __name__ == "__main__":
    ip = '127.0.0.1'


    def analyse(*args):
        for x in args:
            print(type(x))
            print(x)
            print()

    dispatcher = dispatcher.Dispatcher()
    dispatcher.map('/live/clip/state', print)

    server = osc_server.ThreadingOSCUDPServer((ip, 9000), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()
