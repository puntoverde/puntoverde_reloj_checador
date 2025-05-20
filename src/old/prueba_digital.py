import ctypes
from ctypes import *

print("hi digital persona")

def scan_fingerprint():
    dll_path = "C:\\Program Files\\DigitalPersona\\One Touch SDK\\C-C++\\Lib\\x64\\dpfpdd.dll"

    try:
        dpfpddDll = ctypes.CDLL(dll_path)
    except OSError:
        print(f"Library not found at {dll_path}")
        return

    if not init_dpfpdd(dpfpddDll):
        return


def init_dpfpdd(dpfpddDll):   
    # dpfpdd_init = dpfpddDll.dpfpdd_init
    print('aqui...',dpfpddDll.dpfpdd_init)
    # dpfpdd_init.argtypes = []
    # dpfpdd_init.restype = c_int
    # result = dpfpdd_init()
    # print(f"dpfpdd_init result: {result}")
    # if result != 0:
    #     # self.label.setText("Initialization failed")
    #     print("inicializacion fallida")
    #     return False
    return True

scan_fingerprint()