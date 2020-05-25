nvidia-smi
pip install -r requirements.txt
python test_cuda.py
python mnist.py --gpu | tee /artifacts/mnis_gpu.log
python mnist.py | tee /artifacts/mnist_cpu.log