from keras.callbacks import Callback

class Logger(Callback):
	def __init__(self,display=100):
		self.elapse = 0
		self.display = display

	def on_epoch_end(self,batch,logs={}):
		self.elapse += 1
		if self.elapse % self.display == 0:
			print('%d/%d - Batch Loss: %.4f, Acc: %.4f' % (self.elapse, self.params['epochs'], logs['loss'], logs['acc']))

