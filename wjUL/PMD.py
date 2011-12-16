import ctypes
import ctypes.util
import numpy
import hid

__all__ = [
            'USB1208FS_PID',
            'DIO_PORTA',
            'DIO_PORTB',

            'DIO_DIR_OUT',
            'DIO_DIR_IN',

            'FindInterface',
            'usbDConfigPort_USB1208FS',
            'usbDOut_USB1208FS',
            'usbBlink_USB1208FS',

            ]

# constants ##############
USB1208FS_PID = 0x0082

DIO_PORTA = 0x00
DIO_PORTB = 0x01

DIO_DIR_OUT = 0x00
DIO_DIR_IN  = 0x01

AIN_EXECUTION = 0x1
AIN_TRANSFER_MODE = 0x2
AIN_TRIGGER = 0x4

##########################

path=ctypes.util.find_library('mcclibhid')
if path is None:
    raise ImportError('cannot find library mcclibhid')
mcclibhid = ctypes.cdll.LoadLibrary(path)

# prototypes ############
__u8 = ctypes.c_uint8
__u16 = ctypes.c_uint16
__u32 = ctypes.c_uint32
__s16 = ctypes.c_int16

class HIDInterface(ctypes.Structure):
    _fields_ = [('dev_handle',ctypes.c_void_p),
                ('device',ctypes.c_void_p),
                ('interface',ctypes.c_int),
                ('id',ctypes.c_char*32),
                ('hid_data',ctypes.c_void_p),
                ('hid_parser',ctypes.c_void_p),
                ]
LP_c_short = ctypes.POINTER( ctypes.c_int16 )

HIDInterfacePtr = ctypes.POINTER( HIDInterface )
HIDInterfacePtrPtr = ctypes.POINTER( HIDInterfacePtr )

#int PMD_Find_Interface(HIDInterface** hid, int interface, int productID);
mcclibhid.PMD_Find_Interface.restype = ctypes.c_int
mcclibhid.PMD_Find_Interface.argtypes = [
    HIDInterfacePtrPtr,ctypes.c_int,ctypes.c_int]

mcclibhid.usbReset_USB1208FS.restype = ctypes.c_int
mcclibhid.usbReset_USB1208FS.argtypes = [HIDInterfacePtr]

mcclibhid.usbBlink_USB1208FS.restype = None
mcclibhid.usbBlink_USB1208FS.argtypes = [HIDInterfacePtr]

mcclibhid.usbDConfigPort_USB1208FS.restype = None
mcclibhid.usbDConfigPort_USB1208FS.argtypes = [HIDInterfacePtr]

mcclibhid.usbDIn_USB1208FS.restype = None
mcclibhid.usbDIn_USB1208FS.argtypes = [HIDInterfacePtr,
                                       __u8, ctypes.POINTER(__u8)]

mcclibhid.usbDOut_USB1208FS.restype = None
mcclibhid.usbDOut_USB1208FS.argtypes = [HIDInterfacePtr,
                                       __u8, __u8]

mcclibhid.usbAIn_USB1208FS.restype = ctypes.c_short
mcclibhid.usbAIn_USB1208FS.argtypes = [
    HIDInterfacePtr, __u8, __u8]

mcclibhid.usbAInScan_USB1208FS.restype = ctypes.c_int
mcclibhid.usbAInScan_USB1208FS.argtypes = [
    HIDInterfacePtrPtr, __u8, __u8, __u32,
    ctypes.POINTER( ctypes.c_float), __u8, ctypes.POINTER(__s16) ]

mcclibhid.usbAInStop_USB1208FS.restype = None
mcclibhid.usbAInStop_USB1208FS.argtypes = [HIDInterfacePtr]

mcclibhid.usbAOut_USB1208FS.restype = None
mcclibhid.usbAOut_USB1208FS.argtypes = [HIDInterfacePtr, __u8, __u16]

mcclibhid.usbAOutScan_USB1208FS.restype = ctypes.c_int
mcclibhid.usbAOutScan_USB1208FS.argtypes = [HIDInterfacePtrPtr,
                                            __u8, __u8, __u32,
                                            ctypes.POINTER(ctypes.c_float),
                                            __u8, ctypes.POINTER(__s16)]

mcclibhid.volts_FS.restype = ctypes.c_float
mcclibhid.volts_FS.argtypes = [ctypes.c_int, __s16]

mcclibhid.volts_SE.restype = ctypes.c_float
mcclibhid.volts_SE.argtypes = [__s16]

mcclibhid.usbInitCounter_USB1208FS.restype = None
mcclibhid.usbInitCounter_USB1208FS.argtypes = [HIDInterfacePtr]

mcclibhid.usbReadCounter_USB1208FS.restype = __u32
mcclibhid.usbReadCounter_USB1208FS.argtypes = [HIDInterfacePtr]

#########################

hid_inited=False
def _init_hid():
    global hid_inited
    if not hid_inited:
        ret = hid.init()
        if ret != hid.HID_RET_SUCCESS: raise RuntimeError('hid.init() failed')
        hid_inited=True

class Device:
    def __init__(self):
        self.hid = (HIDInterfacePtr*4)() # in C: hid = HIDInterface[4]
        self.interface=None
    def _get(self,i):
        """returns pointer to member structure"""
        return ctypes.byref(self.hid[i])
    def _set_interface(self,i):
        self.interface=i
    def g2(self,i):
        """returns member structure"""
        return self.hid[i]

def FindInterface(PID):
    global _hid_interfaces_global

    _init_hid()
    d = Device()

    for i in range(4):
        interface = mcclibhid.PMD_Find_Interface( d._get(i),i,PID)
        if interface < 0:
            raise RuntimeError('device not found')
        d._set_interface(interface)
    return d

def usbDConfigPort_USB1208FS(device, port, direction):
    mcclibhid.usbDConfigPort_USB1208FS( device.g2(0), port, direction)

def usbDOut_USB1208FS(device, port, value):
    mcclibhid.usbDOut_USB1208FS( device.g2(0), port, value)

def usbReset_USB1208FS(device):
    return mcclibhid.usbReset_USB1208FS(device.g2(0))

def usbBlink_USB1208FS(device):
    mcclibhid.usbBlink_USB1208FS(device.g2(0))

def usbAIn_USB1208FS(device, channel, voltage_range):
    return mcclibhid.usbAIn_USB1208FS( device.g2(0), channel, voltage_range)

def usbAInScan_USB1208FS(device, lowchannel, highchannel, count,
                         frequency, options, data):
    frequency = ctypes.c_float(frequency)
    count = mcclibhid.usbAInScan_USB1208FS(device.g2(0), lowchannel, highchannel, count,
                                           ctypes.byref(frequency), options,
                                           data.ctypes.data_as(ctypes.POINTER(__s16)))
    return count, frequency.value

def usbAInStop_USB1208FS(device):
    return mcclibhid.usbAInStop_USB1208FS(device.g2(0))

def usbAOut_USB1208FS(device, channel, value):
    return mcclibhid.usbAOut_USB1208FS( device.g2(0), channel, value)

def volts_FS( gain, num ):
    num_new = int(num)
    assert num_new == num
    return mcclibhid.volts_FS(gain,num_new)

def volts_SE( num ):
    return mcclibhid.volts_SE(num)

def usbInitCounter_USB1208FS( device ):
    mcclibhid.usbInitCounter_USB1208FS( device.g2(0) )

def usbReadCounter_USB1208FS( device ):
    count = mcclibhid.usbReadCounter_USB1208FS( device.g2(0) )
    return count

