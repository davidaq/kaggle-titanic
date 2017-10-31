from keras.models import Sequential
from keras.layers import Input, Dense, Activation, Dropout
from keras.layers.normalization import BatchNormalization
import math

def create_model(input_len, output_len):
	#model = Sequential()
	#model.add(Dense(1, activation='sigmoid', input_shape=(input_len,)))
	#return model
	return Sequential([
		Activation('tanh', input_shape=(input_len,)),
		Dense(800, use_bias=True),
		Dropout(0.9),
		#BatchNormalization(),
		Activation('relu'),
		#Dense(10, use_bias=True),
		#Activation('tanh'),
		Dense(output_len),
		Activation('softmax'),
	])

#def create_autoencoder_model(input_len):
#	return Sequential([
#		Dense(int(input_len / 4), input_shape=(input_len,)),
#		Activation('relu'),
#		Dense(input_len),
#	])
#
#def autoencoder_model_to_classifier_model(model, output_len):
#	model.layers.pop()
#	model.add(Dense(50))
#	model.add(Activation('relu'))
#	model.add(Dense(output_len))
#	model.add(Activation('softmax'))
#
