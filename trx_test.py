import RPi.GPIO as GPIO

ptt_pin = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(ptt_pin, GPIO.OUT)

running = True

while running:
  try:  
      i = input("TRX-TEST> ")
      if i == "exit":
          running = False
      elif i in ["T", "t"]:
          GPIO.output(ptt_pin, 1)
      elif i in ["R", "r"]:
          GPIO.output(ptt_pin, 0)
      elif i in ["S" ,"s"]:
          standby()
      else:
          print("unknown command")
      #endif
  except:
      print("Exiting")
      running = False
#endwhile

GPIO.output(ptt_pin, 0)
GPIO.cleanup()
