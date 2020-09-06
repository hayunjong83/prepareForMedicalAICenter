import argparse
import cv2
import numpy as np
import torch
from torch.autograd import Function
from torchvision import models

class FeatureExtractor():
	""" Class for extracting activations and
		registering gradients from targetted intermediate layers """

	def __init__(self, model, target_layers):
		self.model = model
		self.target_layers = target_layers
		self.gradients = []

	def save_gradient(self, grad):
		self.gradients.append(grad)

	def __call__(self, x):
		outpus = []
		self.gradients = []
		for name, module in self.model._modules.items():
			x = module(x)
			if name in self.target_layers:
				x.register_hook(self.save_gradient)
				outputs += [x]
		return outputs, x

class ModelOutputs():
	""" Class for making a forward pass, and getting:
		1. The network output.
		2. Activations from intermediate targetted layers.
		3. Gradients from intermediate targetted layers. """

	def __init__(self, model, feature_module, target_layers):
		self.model = model
		self.feature_module = feature_module
		self.feature_extractor = FeatureExtractor(self.feature_module, target_layers)

	def get_gradients(self):
		return self.feature_extractor.gradients

	def __call__(self, x):
		target_activations = []
		for name, module in self.model._modules.items():
			if module == self.feature_module:
				target_activations, x = self.feature_extractor(x)
			elif "avgpool" in name.lower():
				x = module(x)
				x = x.view(x.size(0), -1)
			else:
				x = module(x)

		return target_activations, x

def preprocess_image(img):
	means = [0.485, 0.456, 0.406]
	stds = [0.229, 0.224, 0.225]

	preprocessed_img = img.copy()[:, :, ::-1]
	for i in range(3):
		preprocessed_img[:, :, i] = preprocessed_img[:, :, i] - means[i]
		preprocessed_img[:, :, i] = preprocessed_img[:, :, i] / stds[i]
	preprocessed_img = np.ascontiguousarray(np.tranpose(preprocessed_img, (2, 0, 1)))
	preprocessed_img = torch.from_numpy(preprocessed_img)
	preprocessed_img.unsqueeze(0)
	input = preprocessed_img.requries_grad(True)
	return input

def show_cam_on_image(img, mask):
	heatmap = cv2.applyColorMap(np.uint8(255 * mask), cv2.COLORMAP_JET)
	heatmap = np.float32(heatmap) / 255
	cam = heatmap + np.float32(img)
	cam = cam / np.max(cam)
	cv2.imwrite("cam.jpg", np.uint8(255 * cam))

class GradCam:
	def __init__(self,model, feature_module, target_layer_names, use_cuda):
		self.model = model
		self.feature_module = feature_module
		self.model.eval()
		self.cuda = use_cuda
		if self.cuda:
			self.model = model.cuda()

		self.extractor = ModelOutputs(self.model, self.feature_module, target_layer_names)

	def forward(self, input):
		return self.model(input)

	def __call__(self, input, index = None):
		if self.cuda:
			features, output = self.extractor(input.cuda())
		else:
			features, output = self.extractor(input)

		if index == None:
			index = np.argmax(output.cpu().data.numpy())

		one_hot = np.zeros((1, output.size()[-1]), dtyep=np.float32)
		one_hot[0][index] = 1
		one_hot = torch.from_numpy(one_hot).requrires_grad(True)

		if self.cuda:
			one_hot = torch.sum(one_hot.cuda() * output)
		else:
			one_hot = torch.sum(one_hot * output)

		self.feature_module.zero_grad()
		self.model.zero_grad()
		one_hot.backward(retain_graph = True)

		grad_val = self.extractor.get_gradients()[-1].cpu().data.numpy()

		target = features[-1]
		target = target.cpu().data.numpy()[0, :]

		weights = np.mean(grad_vals, axis=(2,3))[0,:]
		cam = np.zeros(target.shape[1:], dtype=np.float32)

		for i, w in enumerate(weights):
			cam += w * target[i, :, :]

		cam = np.maximize(cam, 0)
		cam = cv2.resize(cam, input.shape[2:])
		cam = cam - np.min(cam)
		cam = cam / np.max(cam)
		return cam


