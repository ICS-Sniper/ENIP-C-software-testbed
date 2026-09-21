#this is the PLC 7 logic, it's about the very same thing as that in the real plc.
###### Existing emulator libraries ################
from devices import PLC
from utils import SCADA_ADDR, SCADA_TAGS
from utils import IP
import time
import multiprocessing
# from multiprocessing import Process
import threading

# from logicblock.logicblock import SETD
from logicblock.logicblock import *
from controlblock.controlblock import *
from logicblock.logicblock import bit_2_signed_integer
from logicblock.logicblock import signed_integer_2_bit
from utils import getdata, setdata

interval = 60
timeout = 20
time_interval = 1

class plc7(PLC):
	'plc7 logic'


	def pre_loop(self):

		### Initialization block #######
		self.k = 0 # counter for number of iterations

		self.hmiplantreseton = 1
		self.hmiplantautoon = 1
		self.hmiplantautooff = 0
		self.hmimv101avl = 1
		self.hmip101avl = 1
		self.hmip102avl = 1
		self.hmip1permissiveon = 1
		self.hmip2permissiveon = 0
		self.hmip3permissiveon = 0
		self.hmip4permissiveon = 0
		self.hmilit101hty = 1
		self.hmilit101all = 0
		self.hmimv201status = 1
		self.hmip101permissive = bit_2_signed_integer([1]*16)
		self.hmip102permissive = bit_2_signed_integer([1]*16)
		self.hmip101status = 1
		self.hmip101shutdown = bit_2_signed_integer([0]*16)
		self.hmip102status = 1
		self.hmip102shutdown = bit_2_signed_integer([0]*16)
		self.hmiplantstop = 0
		self.hmip1state = 1
		self.hmiplantready = 0
		self.hmiplantstart = 0
		self.hmilit101al = 0
		self.hmilit101ahh = 0
		self.hmilit101ah = 0
		self.hmilit301al = 0
		self.hmilit301ah = 0
		self.hmip1shutdown = 1
		self.hmimv101auto = 1
		self.hmiprawwaterdutyselection = 1
		self.hmip101auto = 1
		self.hmip101reset = 0
		self.hmip101sd = bit_2_signed_integer([0] * 16)
		self.hmip102auto = 1
		self.hmip102reset = 0
		self.hmip102sd = bit_2_signed_integer([0] * 16)
		self.hmip101msgpermissive = bit_2_signed_integer([0] * 6)
		self.hmip102msgpermissive = bit_2_signed_integer([0] * 6)
		self.hmip101msgshutdown = bit_2_signed_integer([0] * 6)
		self.hmip102msgshutdown = bit_2_signed_integer([0] * 6)
		self.hmiselectedpmpnotavl = 0
		self.hmip101fault = 0
		self.hmip102fault = 0
		self.hmimv101fto = 0
		self.hmimv101ftc = 0
		self.hmimv101open = 1
		self.hmimv101close = 0
		self.hmifit101hty = 0
		self.hmifit101ahh = 0
		self.hmifit101ah = 0
		self.hmifit101al = 0
		self.hmifit101all = 0
		self.hmimv101status = 1
		self.hmibothpmpnotavl = 0
		self.hmimv101reset = 1
		self.hmipumprunning = 0

		self.P_RAW_WATER_DUTY_FB = Duty2_FBD()
		self.P101_FB = PMP_FBD(self.hmip101avl,self.hmip101fault,self.hmip101shutdown)
		self.P102_FB = PMP_FBD(self.hmip102avl,self.hmip102fault,self.hmip102shutdown)
		self.LIT101_FB = AIN_FBD(self.hmilit101hty,self.hmilit101ahh,self.hmilit101ah,self.hmilit101al,self.hmilit101all)
		self.MV101_FB = MV_FBD(self.hmimv101fto,self.hmimv101ftc,self.hmimv101open,self.hmimv101close)
		self.FIT101_FB = FIT_FBD(self.hmifit101hty,self.hmifit101ahh,self.hmifit101ah,self.hmifit101al,self.hmifit101all)
		self.TON_FIT102_P1_TM = TONR(10)
		self.TON_FIT102_P2_TM = TONR(10)
		self.Mid_MV101_AutoInp = self.hmimv101status-1
		self.Mid_P_RAW_WATER_DUTY_AutoInp = self.hmip101status-1
		self.Mid_FIT101_Flow_Hty = 1
		self.Mid_P_RAW_WATER_DUTY_AutoInp = 1
		self.Min_Test = 0
		self.hmip1state_prev = 0

		################## multiprocessing manager ###########
		manager = multiprocessing.Manager()
		self.shared = manager.dict({
            "hmiplantreseton": self.hmiplantreseton,
            "hmiplantautoon": self.hmiplantautoon,
            "hmiplantautooff": self.hmiplantautooff,
            # "hmip1permissiveon": self.hmip1permissiveon,
			"hmip2permissiveon": self.hmip2permissiveon,
			"hmip3permissiveon": self.hmip3permissiveon,
			"hmip4permissiveon": self.hmip4permissiveon,
			"hmimv201status": self.hmimv201status,
			"hmiplantstop": self.hmiplantstop,
			# "hmiplantready": self.hmiplantready,
			"hmiplantstart": self.hmiplantstart,
			"hmilit301al": self.hmilit301al,
			"hmilit301ah": self.hmilit301ah,
        })

		#######################################################
		time.sleep(10)
		print ("	PLC7 started\n")


	def fetchData(self, state):
		print("PLC7 data transmission starting at", time.time())
		self.shared["hmiplantreseton"] = getdata(self,'HMI.PLANT.Reset_On',SCADA_ADDR,self.shared["hmiplantreseton"])
		self.shared["hmiplantautoon"] = getdata(self,'HMI.PLANT.Auto_On',SCADA_ADDR,self.shared["hmiplantautoon"])
		self.shared["hmiplantautooff"] = getdata(self,'HMI.PLANT.Auto_Off',SCADA_ADDR,self.shared["hmiplantautooff"])
		self.shared["hmiplantstop"] = getdata(self, 'HMI.PLANT.Stop',SCADA_ADDR,self.shared["hmiplantstop"])
		if state == 1:
		  # self.shared["hmip1permissiveon"] = getdata(self, 'HMI.P7.Permissive_On',SCADA_ADDR,self.shared["hmip1permissiveon"])
		  self.shared["hmip2permissiveon"] = getdata(self, 'HMI.P8.Permissive_On',SCADA_ADDR,self.shared["hmip2permissiveon"])
		  self.shared["hmip3permissiveon"] = getdata(self, 'HMI.P9.Permissive_On',SCADA_ADDR,self.shared["hmip3permissiveon"])
		  self.shared["hmip4permissiveon"] = getdata(self, 'HMI.P10.Permissive_On',SCADA_ADDR,self.shared["hmip4permissiveon"])
		  self.shared["hmiplantstart"] = getdata(self, 'HMI.PLANT.Start',SCADA_ADDR,self.shared["hmiplantstart"])
		if state == 2 or state == 3:
		  self.shared["hmimv201status"] = getdata(self, 'HMI.MV801.Status', SCADA_ADDR,self.shared["hmimv201status"])
		  # self.shared["hmiplantready"] = getdata(self, 'HMI.PLANT.Ready',SCADA_ADDR,self.shared["hmiplantready"])
		  self.shared["hmilit301al"] = getdata(self, 'HMI.LIT901.AL', SCADA_ADDR,self.shared["hmilit301al"])
		  self.shared["hmilit301ah"] = getdata(self, 'HMI.LIT901.AH', SCADA_ADDR,self.shared["hmilit301ah"])


	def Actuator(self):
		self.IO.MV701.DI_ZSO = self.IO.MV701.DO_Open
		self.IO.MV701.DI_ZSC = self.IO.MV701.DO_Close
		self.IO.P701.DI_Run = self.IO.P701.DO_Start
		self.IO.P702.DI_Run = self.IO.P702.DO_Start

	def Plant(self):
		self.h_t101=0
		self.p = {"f_mv101":2.3*1000000000/3600,"S_t101":1.5*1000000,"S_t301":1.5*1000000,"S_t401":1.5*1000000,"S_t601":1.5*1000000,"S_t601":1.5*1000000,"S_t602":1.5*1000000,"f_p101":2.0*1000000000/3600,"f_mv201":2.0*1000000000/3600,"f_p301":2.0*1000000000/3600,"f_mv302":2.0*1000000000/3600,"f_p602":2.0*1000000000/3600,"f_p401":2.0*1000000000/36001,"f_mv501":2.0*1000000000/3600,"f_mv502":0.00006111,"f_mv503":0.00049,"f_p601":2.0*1000000000/36001,"LIT101_AL":0.2,"LIT101_AH":0.8,"LIT301_AL":0.2,"LIT301_AH":0.8,"LIT401_AL":0.2,"LIT401_AH":0.8,"LIT601_AL":0.2,"LIT601_AH":0.8,"LIT602_AL":0.2,"LIT602_AH":0.8,"cond_AIT201_AL":250,"cond_AIT201_AH":260,"ph_AIT202_AL":6.95,"ph_AIT202_AH":7.05,"orp_AIT203_AL":420,"orp_AIT203_AH":500,"cond_AIT503_AH":260,"h201_AL":50,"h202_AL":4,"h203_AL":15,"cond_AIT503_AL":250,"cond_AIT503_AH":260,"orp_AIT402_AL":420,"orp_AIT402_AH":500,"omega_inlet":0.001}  # critical plant parameters

		if self.IO.MV701.DI_ZSO == 1:
			self.h_t101=self.h_t101+self.p['f_mv101'] / self.p['S_t101']
		if self.IO.P701.DI_Run == 1 or self.IO.P702.DI_Run == 1: #P101, drawing water from tank101
			self.h_t101=self.h_t101-self.p['f_p101'] / self.p['S_t101']

		self.hmilit101pv = 	self.result[self.k]

		if type(self.hmilit101pv) != type('a'):
			self.hmilit101ahh, self.hmilit101ah, self.hmilit101al, self.hmilit101all = ALM(self.hmilit101pv, 1100, 800, 500, 250)


		self.result.append(self.result[self.k]+self.h_t101*time_interval)

		self.k = self.k + 1


	def Iteration(self):

		p = multiprocessing.Process(target=self.fetchData, args=(self.hmip1state,))
		p.start()
		p.join(timeout)
		if p.is_alive():
			print("Timeout reached, could not fetch all recent data")
			p.terminate()
			p.join()
		else:
			print("Data fetching completed")

		self.hmiplantreseton = self.shared["hmiplantreseton"]
		self.hmiplantautoon = self.shared["hmiplantautoon"]
		self.hmiplantautooff = self.shared["hmiplantautooff"]
		self.hmip2permissiveon = self.shared["hmip2permissiveon"]
		self.hmip3permissiveon = self.shared["hmip3permissiveon"]
		self.hmip4permissiveon = self.shared["hmip4permissiveon"]
		self.hmimv201status = self.shared["hmimv201status"]
		self.hmiplantstop = self.shared["hmiplantstop"]
		self.hmiplantstart = self.shared["hmiplantstart"]
		self.hmilit301al = self.shared["hmilit301al"]
		self.hmilit301ah = self.shared["hmilit301ah"]

		iter_start = time.time()
		print("PLC7 State: ", self.hmip1state)

		if self.hmiplantreseton:
			self.hmimv101reset = 1
			self.hmip101reset = 1
			self.hmip102reset = 1
		if self.hmiplantautoon:
			self.hmimv101auto = 1
			self.hmip101auto = 1
			self.hmip102auto = 1
		if self.hmiplantautooff:
			self.hmimv101auto = 0
			self.hmip101auto = 0
			self.hmip102auto = 0

		self.hmip1permissiveon = self.hmimv101avl and (self.hmip101avl or self.hmip102avl)
		self.hmiplantready = self.hmip1permissiveon and self.hmip2permissiveon and self.hmip3permissiveon and self.hmip4permissiveon

		self.hmip101permissive_arr = signed_integer_2_bit(self.hmip101permissive)
		self.hmip101permissive_arr[0] = int(self.hmilit101hty and not self.hmilit101all)
		self.hmip101permissive_arr[1] = int(self.hmimv201status == 2)
		self.hmip101permissive = bit_2_signed_integer(self.hmip101permissive_arr)
		print(self.hmip101permissive_arr, self.hmip101permissive)

		self.hmip101msgpermissive_arr = signed_integer_2_bit(self.hmip101msgpermissive)
		self.hmip101msgpermissive_arr[1] = self.hmip101permissive_arr[0]
		self.hmip101msgpermissive_arr[2] = self.hmip101permissive_arr[1]
		self.hmip101msgpermissive = bit_2_signed_integer(self.hmip101msgpermissive_arr)

		self.hmip102permissive_arr = signed_integer_2_bit(self.hmip102permissive)
		self.hmip102permissive_arr[0] = int(self.hmilit101hty and not self.hmilit101all)
		self.hmip102permissive_arr[1] = int(self.hmimv201status == 2)
		self.hmip102permissive = bit_2_signed_integer(self.hmip102permissive_arr)


		self.hmip102msgpermissive_arr = signed_integer_2_bit(self.hmip102msgpermissive)
		self.hmip102msgpermissive_arr[1] = self.hmip102permissive_arr[0]
		self.hmip102msgpermissive_arr[2] = self.hmip102permissive_arr[1]
		self.hmip102msgpermissive = bit_2_signed_integer(self.hmip102msgpermissive_arr)


		self.hmip101sd_arr = signed_integer_2_bit(self.hmip101sd)
		self.hmip101sd_arr[0] = int(self.hmilit101hty and self.hmilit101all)
		self.hmip101sd_arr[1] = int((self.hmip101status == 2) and (self.hmimv201status != 2))
		self.hmip101sd_arr[2] = int(self.TON_FIT102_P1_TM.DN)
		self.hmip101sd = bit_2_signed_integer(self.hmip101sd_arr)


		if self.TON_FIT102_P1_TM.DN:
			print ("timeout")

		self.hmip101msgshutdown_arr = signed_integer_2_bit(self.hmip101msgshutdown)
		self.hmip101shutdown_arr = signed_integer_2_bit(self.hmip101shutdown)
		self.hmip101msgshutdown_arr[1] = self.hmip101shutdown_arr[0]
		self.hmip101msgshutdown_arr[2] = self.hmip101shutdown_arr[1]
		self.hmip101msgshutdown_arr[3] = self.hmip101shutdown_arr[2]
		self.hmip101msgshutdown = bit_2_signed_integer(self.hmip101msgshutdown_arr)

		self.hmip102sd_arr = signed_integer_2_bit(self.hmip102sd)
		self.hmip102sd_arr[0] = int(self.hmilit101hty and self.hmilit101all)
		self.hmip102sd_arr[1] = int((self.hmip102status == 2) and (self.hmimv201status != 2))
		self.hmip102sd_arr[2] = int(self.TON_FIT102_P2_TM.DN)
		self.hmip102sd = bit_2_signed_integer(self.hmip102sd_arr)
		self.hmip102msgshutdown_arr = signed_integer_2_bit(self.hmip102msgshutdown)
		self.hmip102shutdown_arr = signed_integer_2_bit(self.hmip102shutdown)
		self.hmip102msgshutdown_arr[1] = self.hmip102shutdown_arr[0]
		self.hmip102msgshutdown_arr[2] = self.hmip102shutdown_arr[1]
		self.hmip102msgshutdown_arr[3] = self.hmip102shutdown_arr[2]
		self.hmip102msgshutdown = bit_2_signed_integer(self.hmip102msgshutdown_arr)

		if self.hmiplantstop:
			self.hmip1shutdown = 1

		if self.hmip1state == 1:
			self.hmip1state_prev = 1
			self.Mid_MV101_AutoInp = 0
			self.Mid_P_RAW_WATER_DUTY_AutoInp = 0
			self.hmip1ready = 0
			if self.hmiplantready and self.hmiplantstart and self.hmip1permissiveon:
				self.hmip1state = 2


		elif self.hmip1state == 2:
			self.hmip1state_prev = 2
			self.Mid_MV101_AutoInp = SETD(self.hmilit101al, self.hmilit101ah, self.Mid_MV101_AutoInp)
			self.Mid_P_RAW_WATER_DUTY_AutoInp = SETD(self.hmimv201status == 2 and self.hmilit301al, self.hmimv201status != 2 or self.hmilit301ah, self.Mid_P_RAW_WATER_DUTY_AutoInp)
			if self.hmip1shutdown:
				self.hmip1state = 3
				self.hmip1shutdown = 0

		elif self.hmip1state == 3:
			self.hmip1state_prev = 3
			self.Mid_MV101_AutoInp = SETD(self.hmilit101al, self.hmilit101ah, self.Mid_MV101_AutoInp)
			self.Mid_P_RAW_WATER_DUTY_AutoInp = SETD(self.hmimv201status == 2 and self.hmilit301al,
													 self.hmimv201status != 2 or self.hmilit301ah,
													 self.Mid_P_RAW_WATER_DUTY_AutoInp)

			if self.hmilit101ah and self.hmilit301ah:
				self.Mid_MV101_AutoInp=0
				self.Mid_P_RAW_WATER_DUTY_AutoInp=0
				self.hmip1state = 2

			if self.hmip1shutdown:
				self.hmip1state = 1
				self.hmip1state_prev = 3
				self.hmip1shutdown = 0

		self.hmimv101status_upd, self.hmimv101avl = self.MV101_FB.MV_FBD(self.Mid_MV101_AutoInp, self.IO.MV701, self.hmimv101auto)
		if self.hmimv101status_upd!= -99:
			self.hmimv101status = self.hmimv101status_upd
		self.hmibothpmpnotavl, self.hmiselectedpmpnotavl_upd, self.hmipumprunning = self.P_RAW_WATER_DUTY_FB.Duty2_FBD(self.Mid_P_RAW_WATER_DUTY_AutoInp, self.hmip101status, self.hmip101avl, self.hmip102status, self.hmip102avl, self.hmiprawwaterdutyselection)
		if self.hmiselectedpmpnotavl_upd != -99:
			self.hmiselectedpmpnotavl = self.hmiselectedpmpnotavl_upd
		self.hmip101status_upd, self.hmip101fault, self.hmip101avl, self.hmip101shutdown = self.P101_FB.PMP_FBD(self.P_RAW_WATER_DUTY_FB.Start_Pmp1, self.IO.P701, self.hmip101auto, self.hmip101reset, self.hmip101permissive, self.hmip101sd)
		if self.hmip101status_upd != -99:
			self.hmip101status = self.hmip101status_upd
		self.hmip102status_upd, self.hmip102fault, self.hmip102avl, self.hmip102shutdown = self.P102_FB.PMP_FBD(self.P_RAW_WATER_DUTY_FB.Start_Pmp1, self.IO.P702, self.hmip102auto, self.hmip102reset, self.hmip102permissive, self.hmip102sd)
		if self.hmip102status_upd != -99:
			self.hmip102status = self.hmip102status_upd

		############# Physical process simulation code ################
		self.Actuator()
		self.Plant()
		############# Physical process simulation ends here ###########

		### All setdata() function calls start here ##

		setdata(self, 'HMI.MV701.Reset',SCADA_ADDR,self.hmimv101reset)
		setdata(self, 'HMI.P701.Reset',SCADA_ADDR,self.hmip101reset)
		setdata(self, 'HMI.P702.Reset',SCADA_ADDR,self.hmip102reset)

		setdata(self, 'HMI.MV701.Auto',SCADA_ADDR,self.hmimv101auto)
		setdata(self, 'HMI.P701.Auto',SCADA_ADDR,self.hmip101auto)
		setdata(self, 'HMI.P702.Auto',SCADA_ADDR,self.hmip102auto)

		setdata(self, 'HMI.P7.Permissive_On',SCADA_ADDR,self.hmip1permissiveon)
		setdata(self, 'HMI.PLANT.Ready',SCADA_ADDR, self.hmiplantready)

		setdata(self, 'HMI.P701.Permissive',SCADA_ADDR,self.hmip101permissive)

		setdata(self, 'HMI.P701.MSG_Permissive',SCADA_ADDR,self.hmip101msgpermissive)
		setdata(self, 'HMI.P702.Permissive',SCADA_ADDR,self.hmip102permissive)
		setdata(self, 'HMI.P702.MSG_Permissive',SCADA_ADDR,self.hmip102msgpermissive)
		setdata(self, 'HMI.P701.SD',SCADA_ADDR,self.hmip101sd)
		setdata(self, 'HMI.P701.MSG_Shutdown',SCADA_ADDR,self.hmip101msgshutdown)
		setdata(self, 'HMI.P702.SD',SCADA_ADDR,self.hmip102sd)
		setdata(self, 'HMI.P702.MSG_Shutdown',SCADA_ADDR,self.hmip102msgshutdown)

		setdata(self, 'HMI.P7.Shutdown',SCADA_ADDR,self.hmip1shutdown)
		if self.hmip1state_prev == 1:
		  setdata(self, 'HMI.P7.Ready',SCADA_ADDR,0)
		  if self.hmip1state == 2:
		    setdata(self, 'HMI.P7.State',SCADA_ADDR,2)
		    self.hmip1state_prev = 0
		elif self.hmip1state_prev == 2:
		  if self.hmip1state == 3:
		    setdata(self, 'HMI.P7.State',SCADA_ADDR,3)
		    setdata(self, 'HMI.P7.Shutdown',SCADA_ADDR,0)
		    self.hmip1state_prev = 0
		elif self.hmip1state_prev == 3:
		  if self.hmip1state == 2:
		    setdata(self, 'HMI.P7.State',SCADA_ADDR,2)
		    self.hmip1state_prev = 0
		  if self.hmip1state == 1:
		    setdata(self, 'HMI.P7.State',SCADA_ADDR,1)
		    setdata(self, 'HMI.P7.Shutdown',SCADA_ADDR,0)
		    self.hmip1state_prev = 0
		#######

		setdata(self, 'HMI.MV701.Status',SCADA_ADDR,self.hmimv101status)
		setdata(self, 'HMI.MV701.Avl',SCADA_ADDR,self.hmimv101avl)

		setdata(self, 'HMI.P_RAW_WATER_DUTY_DUP.Both_Pmp_Not_Avl',SCADA_ADDR,self.hmibothpmpnotavl)
		setdata(self, 'HMI.P_RAW_WATER_DUTY_DUP.Selected_Pmp_Not_Avl',SCADA_ADDR,self.hmiselectedpmpnotavl)
		setdata(self, 'HMI.P_RAW_WATER_DUTY_DUP.Pump_Running',SCADA_ADDR,self.hmipumprunning)

		setdata(self, 'HMI.P701.Status',SCADA_ADDR,self.hmip101status)
		setdata(self, 'HMI.P701.Fault',SCADA_ADDR,self.hmip101fault)
		setdata(self, 'HMI.P701.Avl',SCADA_ADDR,self.hmip101avl)
		setdata(self, 'HMI.P701.Shutdown',SCADA_ADDR,self.hmip101shutdown)

		setdata(self, 'HMI.P702.Status',SCADA_ADDR,self.hmip102status)
		setdata(self, 'HMI.P702.Fault',SCADA_ADDR,self.hmip102fault)
		setdata(self, 'HMI.P702.Avl',SCADA_ADDR,self.hmip102avl)
		setdata(self, 'HMI.P702.Shutdown',SCADA_ADDR,self.hmip102shutdown)

		setdata(self, 'HMI.LIT701.Pv',SCADA_ADDR,self.hmilit101pv)

		if type(self.hmilit101pv) != type('a'):
		  setdata(self, 'HMI.LIT701.AHH',SCADA_ADDR,self.hmilit101ahh)
		  setdata(self, 'HMI.LIT701.AH',SCADA_ADDR,self.hmilit101ah)
		  setdata(self, 'HMI.LIT701.AL',SCADA_ADDR,self.hmilit101al)
		  setdata(self, 'HMI.LIT701.ALL',SCADA_ADDR,self.hmilit101all)

		print("PLC7 data transmission ending at", time.time())
		########## setdata() calls end here #############################
		elapsed = time.time() - iter_start
		print('PLC7 Iteration time:', elapsed)
		# time.sleep(5)

	def _launch_next(self):
		# Schedule the next call
		threading.Timer(interval, self._launch_next).start()
		# Launch network functions in a thread
		t = threading.Thread(target=self.Iteration)
		t.daemon = True
		t.start()

	def Pre_Main_Raw_Water(self,IO):
	# def main_loop(self):
		self.IO = IO
		self.result=[505]
		self._launch_next()
		while True:
			time.sleep(1)
