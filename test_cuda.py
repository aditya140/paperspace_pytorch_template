import torch
import sys

print(f"""
------------------------------Testing Cuda------------------------------
""")
print("+"*30)
print('__Python VERSION:', sys.version)
print('__pyTorch VERSION:', torch.__version__)
print('__CUDA VERSION')
from subprocess import call
print('__CUDNN VERSION:', torch.backends.cudnn.version())
print('__Number CUDA Devices:', torch.cuda.device_count())
print('__Devices__')
call(["nvidia-smi", "--format=csv", "--query-gpu=index,name,driver_version,memory.total,memory.used,memory.free"])
print('\tActive CUDA Device: GPU', torch.cuda.current_device())
print ('\tAvailable devices ', torch.cuda.device_count())
print ('\tCurrent cuda device ', torch.cuda.current_device())
print("+"*30)
print("""
------------------------------Testing Complete--------------------------
""")