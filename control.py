
import socket


class Commands:
    sTX = b"T"
    sRX = b"R"
    sNA = b"N"
    sTEST = b"TEST"
#endlcass

class States:
    tx = 1
    rx = 2
    no_audio = 3
#endclass

class RadioServer:
    ip = 0
    port = 0

    def __init__(self, ip, port):
        #TODO: move radio server here
        pass

    def __del__():
        pass
#endclass

class OperatorClient:
    ip = 0
    port = 0

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self._open_conn_and_send(Commands.sTEST)
    #enddef

    def __del__(self):
        self.standby_no_audio()
    #enddef

    def transmit(self):
        self._open_conn_and_send(Commands.sTX)
    #enddef

    def receive(self):
        self._open_conn_and_send(Commands.sRX)
    #enddef

    def standby_no_audio(self):
        self._open_conn_and_send(Commands.sNA)
    #enddef

    def dial_dtmf(self, dtmf_string):
        self._open_conn_and_send(str.encode(dtmf_string))
    #enddef


    def _open_conn_and_send(self, tx_rx_none):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((self.ip, self.port))     
            client.send(tx_rx_none)
            response = client.recv(4096)
            client.shutdown(socket.SHUT_RDWR)
            client.close()
        except ConnectionRefusedError:
            print(f"ERROR: connection to {self.ip}:{self.port} refused")
        #endtry
    #enddef
#endclass