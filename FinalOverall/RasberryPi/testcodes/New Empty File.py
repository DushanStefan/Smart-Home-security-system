import RPi.GPIO as GPIO
import time
#GPIO.setwarnings(False)



GPIO.setmode(GPIO.BCM)
servopin=18
GPIO.setup(servopin,GPIO.OUT)

pwm=GPIO.PWM(servopin,50)#50 HZ

def set_angle(angle):
    duty_cycle=(angle/18)+2
    #print('hel1')
    GPIO.output(servopin,True)#pwm.ChangeDutyCycle(duty_cycle)
    #print('hel2')
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(1)
    
    #print('hel3')
    GPIO.output(servopin,False)
    pwm.ChangeDutyCycle(0)
    #print('hel4')
    
    
pwm.start(0)   
set_angle(0)
time.sleep(1)
set_angle(180)
time.sleep(1)
pwm.stop()
GPIO.cleanup()