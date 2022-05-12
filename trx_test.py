import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)

running = True

while running:
  try:  
      i = input("TRX-TEST> ")
      if i == "exit":
          running = False
      elif i in ["T", "t"]:
          GPIO.output(21, 1)
      elif i in ["R", "r"]:
          GPIO.output(21, 0)
      elif i in ["S" ,"s"]:
          standby()
      else:
          print("unknown command")
      #endif
  except:
      print("Exiting")
      running = False
#endwhile

GPIO.output(21, 0)
GPIO.cleanup()
