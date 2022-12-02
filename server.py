import socketserver, threading, time, struct, ntplib

class ThreadedUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        current_thread = threading.current_thread()

        print("Hilo:", current_thread.name, "Cliente:", self.client_address, "mensaje recibido: ", data)

        #Parametros y conexion con el ntp chileno
        TIME1970 = 2208988800 #tiempo 0
        ntp = ntplib.NTPClient()
        ntpTime = ntp.request('2.cl.pool.ntp.org')
        true_time = ntpTime.tx_time

        #Codificacion data
        data = ntpTime.to_data()
        data_bytes = bytearray(data)
        new_time_data = struct.pack('!1I', TIME1970 + int(true_time))
        new_time_data_bytes = bytearray(new_time_data)
        data_bytes[40:43] = new_time_data_bytes
        ntpTime.from_data(data_bytes)

        #print
        print("Tiempo de conexion: ", time.ctime(true_time))
        print("Tiempo establecido: ", time.ctime(ntpTime.tx_time))
 
        #respuesta del server
        socket.sendto(data_bytes, self.client_address)

class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass

def main():

    HOST, PORT = "localhost", 3000
    
    server = ThreadedUDPServer((HOST, PORT), ThreadedUDPHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True

    try:
        server_thread.start()
        print("Servidor iniciado en:", HOST, "puerto", PORT)
        while True: time.sleep(100)
    except (KeyboardInterrupt, SystemExit):
        server.shutdown()
        server.server_close()
        exit()
main()