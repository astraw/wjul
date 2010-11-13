import ctypes
import ctypes.util
import sys

HID_RET_SUCCESS = 0

# debug level
HID_DEBUG_NONE = 0x0
HID_DEBUG_ERRORS = 0x1
HID_DEBUG_WARNINGS = 0x2
HID_DEBUG_NOTICES = 0x4
HID_DEBUG_TRACES = 0x8
HID_DEBUG_ASSERTS = 0x10
HID_DEBUG_NOTRACES = HID_DEBUG_ERRORS | HID_DEBUG_WARNINGS | HID_DEBUG_NOTICES | HID_DEBUG_ASSERTS
HID_DEBUG_ALL = HID_DEBUG_ERRORS | HID_DEBUG_WARNINGS | HID_DEBUG_NOTICES | HID_DEBUG_TRACES | HID_DEBUG_ASSERTS
######

if sys.platform.startswith('linux'):
    libhid = ctypes.cdll.LoadLibrary('/usr/lib/libhid.so')
elif sys.platform.startswith('darwin'):
    path=ctypes.util.find_library('libhid')
    libhid = ctypes.cdll.LoadLibrary(path)

if 0:
    # enable libhid debug output
    class FILE(ctypes.Structure):
        pass
    FILE_P = ctypes.POINTER(FILE)
    PyFile_AsFile = ctypes.pythonapi.PyFile_AsFile
    PyFile_AsFile.argtypes = [ctypes.py_object]
    PyFile_AsFile.restype = FILE_P
    stdout_file = PyFile_AsFile(sys.stdout)
    stderr_file = PyFile_AsFile(sys.stderr)

    libhid.hid_set_debug(HID_DEBUG_ALL)
    libhid.hid_set_debug_stream(stderr_file)
    libhid.hid_set_usb_debug(0)

def init():
    return libhid.hid_init()
def cleanup():
    return libhid.hid_cleanup()
