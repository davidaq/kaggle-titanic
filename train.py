import util
from data import train_data, exam_data
data = train_data()
print(len(data['x'][0]), len(data['y'][0]))

import tensorflow as tf
from keras.layers import Activation
import model as m
from Logger import Logger

#model = m.create_autoencoder_model(len(data['x'][0]))
#model.compile(
#	optimizer="adadelta",
#	loss="mse",
#	metrics=['accuracy']
#)
#
#model.fit(data['x'][100:], data['x'][100:], batch_size=10, epochs=4000)
#
#m.autoencoder_model_to_classifier_model(model, len(data['y'][0]))
model = m.create_model(len(data['x'][0]), len(data['y'][0]))
#model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])
model.compile(
	optimizer="adam",
	loss="categorical_crossentropy",
	metrics=['accuracy']
)
model.fit(data['x'][50:], data['y'][50:], batch_size=100, epochs=800, verbose=0, callbacks=[Logger(100)])

score, accuracy = model.evaluate(data['x'][:50], data['y'][:50], batch_size=10)
print()
print(score, accuracy)

data = exam_data()
prediction = model.predict(data['x'])
result = []
for i, x in enumerate(data['meta']):
		result.append({
				'PassengerId':x['PassengerId'],
				'Survived': prediction[i][0], #int(round(prediction[i][2])),
		}) 
util.write_csv(result, 'result.csv')

