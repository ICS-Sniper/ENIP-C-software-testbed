from io_plc.IO_PLC import *

class P1:
	def __init__(self):
		# P1
		self.LIT101 = IO_AIN_FIT()
		self.FIT101 = IO_AIN_FIT()
		self.MV101  = IO_MV()
		self.P101   = IO_PMP_UV()
		self.P102   = IO_PMP_UV()

class P7:
	def __init__(self):
		# P1
		self.LIT701 = IO_AIN_FIT()
		self.FIT701 = IO_AIN_FIT()
		self.MV701  = IO_MV()
		self.P701   = IO_PMP_UV()
		self.P702   = IO_PMP_UV()

class P2:
	def __init__(self):
		# P2
		self.LS201  = IO_SWITCH()
		self.LS202  = IO_SWITCH()
		self.LSL203  = IO_SWITCH()
		self.LSLL203  = IO_SWITCH()
		self.MV201  = IO_MV()
		self.P201   = IO_PMP_UV()
		self.P202   = IO_PMP_UV()
		self.P203   = IO_PMP_UV()
		self.P204   = IO_PMP_UV()
		self.P205   = IO_PMP_UV()
		self.P206   = IO_PMP_UV()
		self.P207   = IO_PMP_UV()
		self.P208   = IO_PMP_UV()
		self.FIT201 = IO_AIN_FIT()
		self.AIT201 = IO_AIN_FIT()
		self.AIT202 = IO_AIN_FIT()
		self.AIT203 = IO_AIN_FIT()

class P8:
	def __init__(self):
		# P2
		self.LS801  = IO_SWITCH()
		self.LS802  = IO_SWITCH()
		self.LSL803  = IO_SWITCH()
		self.LSLL803  = IO_SWITCH()
		self.MV801  = IO_MV()
		self.P801   = IO_PMP_UV()
		self.P802   = IO_PMP_UV()
		self.P803   = IO_PMP_UV()
		self.P804   = IO_PMP_UV()
		self.P805   = IO_PMP_UV()
		self.P806   = IO_PMP_UV()
		self.P807   = IO_PMP_UV()
		self.P808   = IO_PMP_UV()
		self.FIT801 = IO_AIN_FIT()
		self.AIT801 = IO_AIN_FIT()
		self.AIT802 = IO_AIN_FIT()
		self.AIT803 = IO_AIN_FIT()

class P3:
	def __init__(self):
		# P3
		self.LIT301 = IO_AIN_FIT()
		self.FIT301 = IO_AIN_FIT()
		self.P301   = IO_PMP_UV()
		self.P302   = IO_PMP_UV()
		self.PSH301 = IO_SWITCH()
		self.DPSH301= IO_SWITCH()
		self.DPIT301= IO_AIN_FIT()
		self.MV301  = IO_MV()
		self.MV302  = IO_MV()
		self.MV303  = IO_MV()
		self.MV304  = IO_MV()

class P9:
	def __init__(self):
		# P3
		self.LIT901 = IO_AIN_FIT()
		self.FIT901 = IO_AIN_FIT()
		self.P901   = IO_PMP_UV()
		self.P902   = IO_PMP_UV()
		self.PSH901 = IO_SWITCH()
		self.DPSH901= IO_SWITCH()
		self.DPIT901= IO_AIN_FIT()
		self.MV901  = IO_MV()
		self.MV902  = IO_MV()
		self.MV903  = IO_MV()
		self.MV904  = IO_MV()

class P4:
	def __init__(self):
		# P4
		self.LS401  = IO_SWITCH()
		self.LIT401 = IO_AIN_FIT()
		self.UV401  = IO_PMP_UV()
		self.P401   = IO_PMP_UV()
		self.P402   = IO_PMP_UV()
		self.P403   = IO_PMP_UV()
		self.P404   = IO_PMP_UV()
		self.AIT401 = IO_AIN_FIT()
		self.AIT402 = IO_AIN_FIT()
		self.FIT401 = IO_AIN_FIT()

class P10:
	def __init__(self):
		# P4
		self.LS1001  = IO_SWITCH()
		self.LIT1001 = IO_AIN_FIT()
		self.UV1001  = IO_PMP_UV()
		self.P1001   = IO_PMP_UV()
		self.P1002   = IO_PMP_UV()
		self.P1003   = IO_PMP_UV()
		self.P1004   = IO_PMP_UV()
		self.AI1001 = IO_AIN_FIT()
		self.AIT1002 = IO_AIN_FIT()
		self.FIT1001 = IO_AIN_FIT()

class P5:
	def __init__(self):
		# P5
		self.AIT501 = IO_AIN_FIT()
		self.AIT502 = IO_AIN_FIT()
		self.AIT503 = IO_AIN_FIT()
		self.AIT504 = IO_AIN_FIT()
		self.PIT501 = IO_AIN_FIT()
		self.PIT502 = IO_AIN_FIT()
		self.PIT503 = IO_AIN_FIT()
		self.FIT501 = IO_AIN_FIT()
		self.FIT502 = IO_AIN_FIT()
		self.FIT503 = IO_AIN_FIT()
		self.FIT504 = IO_AIN_FIT()
		self.MV501  = IO_MV()
		self.MV502  = IO_MV()
		self.MV503  = IO_MV()
		self.MV504  = IO_MV()
#for Pressure Pump, we have VSD IO(normal) and VSD_In and VSD_Out, in total 3 I/O
		self.P501   = VSD()
		self.P502   = VSD()
		self.P501_VSD_In  = VSD_In()
		self.P502_VSD_In  = VSD_In()
		self.P501_VSD_Out = VSD_Out()
		self.P502_VSD_Out = VSD_Out()

class P11:
	def __init__(self):
		# P5
		self.AIT1101 = IO_AIN_FIT()
		self.AIT1102 = IO_AIN_FIT()
		self.AIT1103 = IO_AIN_FIT()
		self.AIT1104 = IO_AIN_FIT()
		self.PIT1101 = IO_AIN_FIT()
		self.PIT1102 = IO_AIN_FIT()
		self.PIT1103 = IO_AIN_FIT()
		self.FIT1101 = IO_AIN_FIT()
		self.FIT1102 = IO_AIN_FIT()
		self.FIT1103 = IO_AIN_FIT()
		self.FIT1104 = IO_AIN_FIT()
		self.MV1101  = IO_MV()
		self.MV1102  = IO_MV()
		self.MV1103  = IO_MV()
		self.MV1104  = IO_MV()
#for Pressure Pump, we have VSD IO(normal) and VSD_In and VSD_Out, in total 3 I/O
		self.P1101   = VSD()
		self.P1102   = VSD()
		self.P1101_VSD_In  = VSD_In()
		self.P1102_VSD_In  = VSD_In()
		self.P1101_VSD_Out = VSD_Out()
		self.P1102_VSD_Out = VSD_Out()

class P6:
	def __init__(self):
		# P6
		self.LSL601  = IO_SWITCH()
		self.LSL602  = IO_SWITCH()
		self.LSL603  = IO_SWITCH()
		self.LSH601  = IO_SWITCH()
		self.LSH602  = IO_SWITCH()
		self.LSH603  = IO_SWITCH()
		self.P601   = IO_PMP_UV()
		self.P602   = IO_PMP_UV()
		self.P603   = IO_PMP_UV()
		self.FIT601 = IO_AIN_FIT()

class P12:
	def __init__(self):
		# P6
		self.LSL1201  = IO_SWITCH()
		self.LSL1202  = IO_SWITCH()
		self.LSL1203  = IO_SWITCH()
		self.LSH1201  = IO_SWITCH()
		self.LSH1202  = IO_SWITCH()
		self.LSH1203  = IO_SWITCH()
		self.P1201   = IO_PMP_UV()
		self.P1202   = IO_PMP_UV()
		self.P1203   = IO_PMP_UV()
		self.FIT1201 = IO_AIN_FIT()		
