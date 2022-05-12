# RemoteRadioPTT

Minimalistic program for remotely controlling PTT of a (Ham-)radio transceiver and streaming audio over a private IP-Network.

This is yet another remote PTT software.  
This one works without mumble or any other server but requires connection between the remote computer (at radio) and the operators computer via a private network.  
As this is intended for usage on a local area network there is no authentication or encryption used.  

The goal was to keep both ends as simple as possible.


## Dependencies / Credits

* trx by Mark Hills (http://www.pogo.org.uk/~mark/trx/). 
* RPi.GPIO by Ben Croston (https://pypi.org/project/RPi.GPIO/)
* pynput by Moses Palmér (https://pypi.org/project/pynput/)
* dtmf (see dtmf.py) by Noah Spurrier (http://www.noah.org/wiki/tones) ([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/))
* Pulseaudio (installed on the raspberrypi)

## Install / Build

### trx
On both the operators PC and the raspberry run:

```
git clone http://www.pogo.org.uk/~mark/trx.git
cd trx
make
mkdir ~/bin/
cp rx tx ~/bin
# check if your $PATH includes ~/bin
# if not, add "~/bin" to your $PATH
```

### python dependencies (on operator PC)
```
pip3 install pynput
```

### python dependencies (on remote PC)
```
pip3 install RPi.GPIO pyaudio numpy
```

Now you should be able to run `radio.py` on the raspbery and `computer.py` on the operators PC.

## radio.py

Runs on a raspberry pi (zero) and handles PTT as well as audio streaming through trx (rx and tx).  
A GPIO pin is used to control the PTT key, audio in/out is done via a standard USB soundcard.  
PTT commands are received via TCP (radio.py runs a server).

Due to speed limitations the processes for `rx` and `tx` have to started and stopped accordingly (see `audio_handler.py`)


## computer.py

Runs on the operators PC.  
Audio streaming is done again with trx.  
PTT is done through monitoring the keyboard for a specific key (in this calse it's the 'ALT'-key).  
PTT commands are sent via TCP to the server in radio.py.

Usage:  

```
exit:   will exit the program
T:      continuous transmit
R:      switch to receive (disables standby)
S:      standby (disable all audio streaming on remote),
        can only be disabled with 'R'
SR:     standby but keep receiving
D<Nums> Send DTMF Numbers. <Nums> is a string of numbers
        example: 'D12345' would send "12345"
        All DTMF-Numbers/Charactes are available
help:   print help 
```


## TODO
- [ ] Error-handling in radio.py
- [ ] Command-Line Arguments for Host/Port in raido.py and computer.py
- [x] Locking mechanism in radio.py
- [ ] Find another soultion that doesn't use pulseadio because some users might not want to use that on a raspberrypi
- [ ] better exception handling
- [ ] Radio Power on / off
- [ ] Interlock to prevent radio access while other applications e.g. direwolf are in control
- [ ] find reason for latency / reason why audio is not audible for the first few seconds when switching to receive
- [ ] Move argument handling to separate file class (as it is the same for )
