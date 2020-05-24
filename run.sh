pip install -r requirements.txt
python test_cuda.py
python mnist.py --gpu | tee /log/mnist.log