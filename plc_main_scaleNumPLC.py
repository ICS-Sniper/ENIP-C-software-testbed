#Sample command: sudo python3 plc1_main.py

from real_plc_scaleNumPLC import plc1, plc2, plc3, plc4, plc5, plc6, plc7, plc8, plc9, plc10, plc11, plc12
import sys,os
sys.path.insert(0,os.getcwd())
# from SCADA import H
from IO import *
import numpy as np
from trace_check.get_data import get_all_input_with_sensors
from trace_check.get_data import get_waterlevels
from trace_check.get_data import get_full_log
from trace_check.get_data import print_all_output
import csv
from datetime import datetime
import os
import shutil
import time
from threading import Thread
from utils import PLC1_DATA, PLC1_PROTOCOL, PLC1_ADDR, PLC2_PROTOCOL, PLC2_ADDR, PLC2_DATA, PLC3_PROTOCOL, PLC3_ADDR, PLC3_DATA, PLC4_PROTOCOL, PLC4_ADDR, PLC4_DATA, PLC5_PROTOCOL, PLC5_ADDR, PLC5_DATA, PLC6_PROTOCOL, PLC6_ADDR, PLC6_DATA, PLC7_PROTOCOL, PLC7_ADDR, PLC7_DATA, PLC8_PROTOCOL, PLC8_ADDR, PLC8_DATA, PLC9_PROTOCOL, PLC9_ADDR, PLC9_DATA, PLC10_PROTOCOL, PLC10_ADDR, PLC10_DATA, PLC11_PROTOCOL, PLC11_ADDR, PLC11_DATA, PLC12_PROTOCOL, PLC12_ADDR, PLC12_DATA
####################################################################


# Initiating Plant
# Plant = plant(time_interval,maxstep)
# Defining I/O
IO_P1 = P1()
IO_P2 = P2()
IO_P3 = P3()
IO_P4 = P4()
IO_P5 = P5()
IO_P6 = P6()
IO_P7 = P7()
IO_P8 = P8()
IO_P9 = P9()
IO_P10 = P10()
IO_P11 = P11()
IO_P12 = P12()


if __name__ == "__main__":
    print ("Initializing PLCs\n")
    PLC1 = plc1.plc1(name='plc1',
            protocol=PLC1_PROTOCOL,
            memory=PLC1_DATA,
            disk=PLC1_DATA)

    PLC2 = plc2.plc2(name='plc2',
            protocol=PLC2_PROTOCOL,
            memory=PLC2_DATA,
            disk=PLC2_DATA)

    PLC3 = plc3.plc3(name='plc3',
            protocol=PLC3_PROTOCOL,
            memory=PLC3_DATA,
            disk=PLC3_DATA)
    #
    PLC4 = plc4.plc4(name='plc4',
            protocol=PLC4_PROTOCOL,
            memory=PLC4_DATA,
            disk=PLC4_DATA)
    #
    PLC5 = plc5.plc5(name='plc5',
            protocol=PLC5_PROTOCOL,
            memory=PLC5_DATA,
            disk=PLC5_DATA)

    PLC6 = plc6.plc6(name='plc6',
            protocol=PLC6_PROTOCOL,
            memory=PLC6_DATA,
            disk=PLC6_DATA)

    PLC7 = plc7.plc7(name='plc7',
            protocol=PLC7_PROTOCOL,
            memory=PLC7_DATA,
            disk=PLC7_DATA)

    PLC8 = plc8.plc8(name='plc8',
            protocol=PLC8_PROTOCOL,
            memory=PLC8_DATA,
            disk=PLC8_DATA)

    PLC9 = plc9.plc9(name='plc9',
            protocol=PLC9_PROTOCOL,
            memory=PLC9_DATA,
            disk=PLC9_DATA)

    PLC10 = plc10.plc10(name='plc10',
            protocol=PLC10_PROTOCOL,
            memory=PLC10_DATA,
            disk=PLC10_DATA)

    PLC11 = plc11.plc11(name='plc11',
            protocol=PLC11_PROTOCOL,
            memory=PLC11_DATA,
            disk=PLC11_DATA)

    PLC12 = plc12.plc12(name='plc12',
            protocol=PLC12_PROTOCOL,
            memory=PLC12_DATA,
            disk=PLC12_DATA)

    time.sleep(10)

    p1 = Thread(target=PLC1.Pre_Main_Raw_Water, args=(IO_P1,))
    p2 = Thread(target=PLC2.Pre_Main_UF_Feed_Dosing, args=(IO_P2,))
    p3 = Thread(target=PLC3.Pre_Main_UF_Feed, args=(IO_P3,))
    p4 = Thread(target=PLC4.Pre_Main_RO_Feed_Dosing, args=(IO_P4,))
    p5 = Thread(target=PLC5.Pre_Main_High_Pressure_RO, args=(IO_P5,))
    p6 = Thread(target=PLC6.Pre_Main_Product, args=(IO_P6,))
    p7 = Thread(target=PLC7.Pre_Main_Raw_Water, args=(IO_P7,))
    p8 = Thread(target=PLC8.Pre_Main_UF_Feed_Dosing, args=(IO_P8,))
    p9 = Thread(target=PLC9.Pre_Main_UF_Feed, args=(IO_P9,))
    p10 = Thread(target=PLC10.Pre_Main_RO_Feed_Dosing, args=(IO_P10,))
    p11 = Thread(target=PLC11.Pre_Main_High_Pressure_RO, args=(IO_P11,))
    p12 = Thread(target=PLC12.Pre_Main_Product, args=(IO_P12,))

    print("Starting first PLC")
    p1.start()
    print("Starting second PLC")
    p2.start()
    print("Starting third PLC")
    p3.start()
    # time.sleep(5)
    print("Starting fourth PLC")
    p4.start()
    print("Starting fifth PLC")
    p5.start()
    print("Starting sixth PLC")
    p6.start()
    print("Starting seventh PLC")
    p7.start()
    print("Starting eighth PLC")
    p8.start()
    print("Starting ninth PLC")
    p9.start()
    print("Starting tenth PLC")
    p10.start()
    print("Starting eleventh PLC")
    p11.start()
    print("Starting twelfth PLC")
    p12.start()
