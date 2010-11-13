import ctypes
import ctypes.util
import PMD
import numpy
import warnings

#### Gains and conversion to/from DAC units #######

BIP5VOLTS = 'BIP5VOLTS'
UNI4VOLTS = 'UNI4VOLTS'
CONVERTDATA = 'CONVERTDATA'

FIRSTPORTA = PMD.DIO_PORTA
DIGITALOUT = PMD.DIO_DIR_OUT
DIGITALIN = PMD.DIO_DIR_IN

gain_str2pmd = {BIP5VOLTS:0x02,
                UNI4VOLTS:None,
                }

def cbToEngUnits( board, gain, value ):
    global _usbhandler
    device = _get_device(board)
    pmdgain = gain_str2pmd[gain]
    if gain.startswith('BIP'):
        # differential
        result = PMD.volts_FS( pmdgain, value )
    else:
        result = PMD.volts_SE( value )
    return result

def cbFromEngUnits( board, gain, value, xxx_hmm ):
    global _usbhandler
    device = _get_device(board)
    gain = gain_str2pmd[gain]
    import warnings
    warnings.warn("cbFromEngUnits not implemented")
    return int(value*100)


def cbAConvertData (BoardNum, NumPoints, ADData,
                    ChanTags):
    """Convert data collected by cbAInScan()

    Inputs
    ------
    BoardNum
    NumPoints
    ADData --  modified to contain the data array
    ChanTags --  modified to contain the channel tag array

    """
    raise NotImplementedError("This function not yet implemented")

### USB nuts and bolts ###################

class _USBHandler:
    def __init__(self,board):
        if board != 0:
            raise ValueError("only board 0 is supported")
        device0 = PMD.FindInterface( PMD.USB1208FS_PID )
        PMD.usbDConfigPort_USB1208FS(device0, PMD.DIO_PORTA, PMD.DIO_DIR_OUT)
        PMD.usbDConfigPort_USB1208FS(device0, PMD.DIO_PORTB, PMD.DIO_DIR_IN)
        self.devices = [ device0 ]
    def __del__(self):
        self.close()
    def close(self):
        for device in self.devices:
            PMD.usbReset_USB1208FS(device)
_usbhandler = None


def _get_device(board):
    global _usbhandler

    if _usbhandler is None:
        _usbhandler = _USBHandler(board)

    if board != 0:
        raise ValueError("only board 0 is supported")

    return _usbhandler.devices[board]

### The "meat" #######################

def cbAIn( board, channel, gain ):
    """Read A/D input channel

    Inputs
    ------

    BoardNum
    Chan
    Gain
    DataValue

    Outputs
    -------
    DataValue

    """
    global _usbhandler
    device = _get_device(board)
    value = PMD.usbAIn_USB1208FS(device,channel,gain_str2pmd[gain])
    return value

def cbAInScan( board, LowChan, HighChan, Count,
               Rate, Gain, ADData, Options):
    """Scan range of A/D channels and store samples in an array

    Inputs
    ------

    BoardNum
    LowChan
    HighChan
    Count
    Rate
    Gain
    ADData -- modified to contain the sampled data
    Options

    Outputs
    -------

    Rate

    """
    global _usbhandler
    device = _get_device(board)

    if not Options == CONVERTDATA:
        raise NotImplementedError("The only option I currently understand is CONVERTDATA")

    ADData = numpy.asarray(ADData)
    if ADData.dtype != numpy.int16:
        raise TypeError("argument ADData must be (convertable to) a numpy int16 array")

    # in the test-usb1208FS.c example program, the single grab is done before calling scan
    svalue = PMD.usbAIn_USB1208FS(device, 0, gain_str2pmd[Gain])
    options = PMD.AIN_EXECUTION
    count, rate = PMD.usbAInScan_USB1208FS(device, LowChan, HighChan, Count,
                                           Rate, options, ADData)
    return rate

def cbAOut( board, chan, gain, value):
    global _usbhandler
    gain_str2pmd[gain]
    device = _get_device(board)
    if gain != UNI4VOLTS:
        raise ValueError("Only UNI4VOLTS supported for output gain")
    return PMD.usbAOut_USB1208FS(device, chan, value)

def cbCInit(board):
    device = _get_device(board)
    PMD.usbInitCounter_USB1208FS(device)

def cbCRead(board):
    device = _get_device(board)
    return PMD.usbReadCounter_USB1208FS(device)

def cbDConfigPort(board,port,direction):
    device = _get_device(board)
    return PMD.usbDConfigPort_USB1208FS(device, port, direction)

def cbDOut(board,port,value):
    device = _get_device(board)
    return PMD.usbDOut_USB1208FS(device, port, value)
