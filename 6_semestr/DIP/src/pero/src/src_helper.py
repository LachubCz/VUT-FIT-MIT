import subprocess
import os
import sys
utf8stdout = open(1, 'w', encoding='utf-8', closefd=False)


def setGPU():
    freeGpu = subprocess.check_output(
        'nvidia-smi -q | grep "Minor\|Processes" | grep "None" -B1 | tr -d " " | cut -d ":" -f2 | sed -n "1p"', shell=True)

    if len(freeGpu) == 0:
        print ('No free GPU available!', file=utf8stdout)
        sys.exit(1)

    os.environ['CUDA_VISIBLE_DEVICES'] = freeGpu.decode().strip()

    return int(freeGpu.strip())
