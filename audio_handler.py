from threading import Lock
import subprocess

class AudioHandler():
    _lock = Lock()
    rx_process = None
    tx_process = None
    ip = "0.0.0.0"
    bitrate=0

    def __init__(self, ip, bitrate=12000):
        """ Audio handler consturctor

        ip = destination ip for streaming UPD  audio using tx
             This may be a specific computer or broadcast / multicast
        bitrate = audio bitrate for trx
        """
        self.ip = ip
        self.bitrate = bitrate #TODO: check if number and if bitrate supported (maybe check this while parsing args)
    #enddef

    def receive_audio(self):
        """ Start the audio receiving process using 'rx' if it is not already running.

        This function may throw an exception if the process could not be started
        """
        with self._lock:
            if self.tx_process:
                self.tx_process.terminate()
                self.tx_process = None
            #endif

            if not self.rx_process:
                self.rx_process = subprocess.Popen(["rx","-r", str(self.bitrate), "-c" ,"1"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                print("WARNING: trying to start multiple audio RX processes")
            #endif
        #endwith
    #enddef

    def send_audio(self):
        """ Start the audio transmit process using 'tx' if it is not already running.
        Using the IP provided in the constructor

        This function may throw an exception if the process could not be started
        """
        with self._lock:
            if self.rx_process:
                self.rx_process.terminate()
                self.rx_process = None
            #endif

            if not self.tx_process:
                self.tx_process = subprocess.Popen(["tx","-h", self.ip, "-r", str(self.bitrate), "-c" ,"1"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                print("WARNING: trying to start multiple audio TX processes")
            #endif
        #endwith
    #enddef

    def stop_all_audio(self):
        """Stop all audio rx or tx processes"""
        with self._lock:
            if self.rx_process:
                self.rx_process.terminate()
                self.rx_process = None
            if self.tx_process:
                self.tx_process.terminate()
                self.tx_process = None
            #endif
        #endiwth
    #enddef

    def __del__(self):
        self.rx_process.terminate()
        self.tx_process.terminate()
    #enddef

    