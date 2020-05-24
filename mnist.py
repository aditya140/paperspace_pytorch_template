import argparse
import torch
import torchvision
import time

n_epochs = 3
batch_size_train = 64
batch_size_test = 1000
learning_rate = 0.01
momentum = 0.5
log_interval = 10
random_seed = 1
torch.backends.cudnn.enabled = False
torch.manual_seed(random_seed)

def main(gpu):
		
	train_loader = torch.utils.data.DataLoader(
	  torchvision.datasets.MNIST('/files/', train=True, download=True,
								transform=torchvision.transforms.Compose([
								  torchvision.transforms.ToTensor(),
								  torchvision.transforms.Normalize(
									(0.1307,), (0.3081,))
								])),
	  batch_size=batch_size_train, shuffle=True)

	test_loader = torch.utils.data.DataLoader(
	  torchvision.datasets.MNIST('/files/', train=False, download=True,
								transform=torchvision.transforms.Compose([
								  torchvision.transforms.ToTensor(),
								  torchvision.transforms.Normalize(
									(0.1307,), (0.3081,))
								])),
	  batch_size=batch_size_test, shuffle=True)

	import torch.nn as nn
	import torch.nn.functional as F
	import torch.optim as optim

	class Net(nn.Module):
		def __init__(self):
			super(Net, self).__init__()
			self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
			self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
			self.conv2_drop = nn.Dropout2d()
			self.fc1 = nn.Linear(320, 50)
			self.fc2 = nn.Linear(50, 10)

		def forward(self, x):
			x = F.relu(F.max_pool2d(self.conv1(x), 2))
			x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
			x = x.view(-1, 320)
			x = F.relu(self.fc1(x))
			x = F.dropout(x, training=self.training)
			x = self.fc2(x)
			return F.log_softmax(x)

	device = torch.device('cuda:0' if (torch.cuda.is_available() and gpu) else 'cpu')
	print(f"\nTorch device : {device}\n")
	
	network = Net()
	optimizer = optim.SGD(network.parameters(), lr=learning_rate,
						  momentum=momentum)
	network.to(device)

	train_losses = []
	train_counter = []
	test_losses = []
	test_counter = [i*len(train_loader.dataset) for i in range(n_epochs + 1)]
	

	def train(epoch):
		network.train()
		for batch_idx, (data, target) in enumerate(train_loader):
			optimizer.zero_grad()
			data=data.to(device)
			target=target.to(device)
			output = network(data)
			loss = F.nll_loss(output, target)
			loss.backward()
			optimizer.step()
			if batch_idx % log_interval == 0:
				print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
					epoch, batch_idx * len(data), len(train_loader.dataset),
					100. * batch_idx / len(train_loader), loss.item()))
			train_losses.append(loss.item())
			train_counter.append(
				(batch_idx*64) + ((epoch-1)*len(train_loader.dataset)))
			torch.save(network.state_dict(), '/artifacts/model.pth')
			torch.save(optimizer.state_dict(), '/artifacts/optimizer.pth')

	def test():
		network.eval()
		test_loss = 0
		correct = 0
		with torch.no_grad():
			for data, target in test_loader:
				data=data.to(device)
				target=target.to(device)
				output = network(data)
				test_loss += F.nll_loss(output, target, size_average=False).item()
				pred = output.data.max(1, keepdim=True)[1]
				correct += pred.eq(target.data.view_as(pred)).sum()
		test_loss /= len(test_loader.dataset)
		test_losses.append(test_loss)
		print('\nTest set: Avg. loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
			test_loss, correct, len(test_loader.dataset),
			100. * correct / len(test_loader.dataset)))

	st=time.time()
	test()
	for epoch in range(1, n_epochs + 1):
	  	train(epoch)
	  	test()
	et = time.time()
	print(f"Time taken : {str(et-st)}")


if __name__=="__main__":
	parser = argparse.ArgumentParser(description='MNIST training')
	parser.add_argument('--gpu',action='store_true',help='Use GPU')
	args = parser.parse_args()
	main(args.gpu)
		
