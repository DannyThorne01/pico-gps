from machine import Pin, I2C, UART
import time

gps = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

try:
    gps.write(b'$PMTK314,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0*28\r\n')
    
    while True:
        if gps.any():
            try:
                #prints in Coordinated Universal time UTC Time
                # Order - GGA -> GSA -> RMC -> VTG
                # Example - $$GPGGA,233103.000,0648.8074,N,05808.7368,W,1,04,4.85,1.1,M,-35.1,M,,*57
                # 23nd hour 31rd minute 03.000 seconds , latitude, North or South, Longitude, East or West,
                # 1 - yes fix, 4- # satellites, 4.85- how diluted is signal,1.1 -elevation, M(eteres) 
                # $GPGSV,4,1,13,  13,62,187,20, 19,43,144,, 11,38,015,,  21,37,350,*74 - I found 13 satellites
                # -> 13 elevation62heading187signalStrength20
                # DB strength 20 -30 weak, 30-40 good signal
                # 
                byte = gps.read(1).decode('ascii')
                print(byte,end='')
            except UnicodeError:
                print('.', end='')
         
    
except KeyboardInterrupt:
    print("\n . . . Cleaning up UART")
    gps.deinit()
    time.sleep(1)
    print ("Cleanly Exited UART")
    