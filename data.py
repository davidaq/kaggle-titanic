import util
import re
import math

def str_to_number():
	fields = ['Survived', 'Age', 'SibSp', 'Parch', 'Fare']
	def fn(item):
		for f in fields:
			item[f] = float('0' + item[f]) if f in item else 0
		return item
	return util.each(fn)

def extract_title_from_name():
	regex = re.compile('[A-Z][a-z]+\.')
	def fn(item):
		m = regex.search(item['Name'])
		item['Title'] = m.group() if m != None else ''
		return item
	return util.each(fn)

def family():
	def fn(item):
		item['Family'] = item['Parch'] + item['SibSp']
		item['SibFare'] = (1 + item['SibSp']) * item['Fare']
		return item
	return util.each(fn)

def ticket_prefix():
	regex = re.compile(' ?[0-9]+$')
	def fn(item):
		item['TicketPrefix'] = regex.sub('', item['Ticket'])
		item['HasTicketPrefix'] = item['TicketPrefix'] != ''
		item['HasCabin'] = item['Cabin'] != ''
		item['CabinPrefix'] = item['Cabin'][0] if item['Cabin'] != '' else None
		return item
	return util.each(fn)

def age():
	def fn(item):
		if item['Age'] == '':
			item['Age'] = '29'
		item['AgeEst'] = 1 if item['Age'].find('.5') else 0
		return item
	return util.each(fn)

def show_group(name):
	def fn(arr):
		s = set()
		for item in arr:
			if name in item:
					s.add(item[name])
		print(list(s))
		return arr
	return fn

def guess():
	def fn(item):
		item['NoAge'] = bool(item['Age'])
		item['MaybeMother'] = False
		if item['Sex'] == 'female' and item['Age'] and item['Parch']:
			age = float(item['Age'])
			child = int(item['Parch'])
			if age > 25 and age < 35:
				item['MaybeMother'] = True
		return item
	return util.each(fn)

def proc(raw):
	return util.pipe(raw, [
		# util.randkeep(5),
		# util.shuffle(),
		guess(),
		age(),
		str_to_number(),
		extract_title_from_name(),
		family(),
		ticket_prefix(),
		#normalize(),
		#show_group('TicketPrefix'),
		util.split({
			'x': [
				util.select([
					('NoAge', False, True),
					('Pclass', '1', '2', '3'),
					('Title',
							'Capt.', 'Col.', 'Countess.', 'Don.', 'Dr.',
							'Jonkheer.', 'Lady.', 'Major.', 'Master.', 'Miss.',
							'Mlle.', 'Mme.', 'Mr.', 'Mrs.', 'Ms.', 'Rev.', 'Sir.',
					),
					('CabinPrefix',
						'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'T',
					),
					('TicketPrefix',
							'W/C', 'C.A./SOTON', 'CA.', 'S.O.C.', 'LINE', 'S.O./P.P.', 'S.C./PARIS', 'A./5.', 'W.E.P.', 'S.P.', 'P/PP', 'W./C.', 'SCO/W', 'SC/AH', 'A/S', 'A/4.', 'WE/P', 'A/5', 'SW/PP', 'SOTON/OQ', 'SOTON/O2', 'SO/C', 'SC/PARIS', 'S.W./PP', 'SC/AH Basle', 'Fa', 'A/4', 'S.O.P.', 'STON/O2.', 'STON/O 2.', 'PC', 'PP', 'SC', 'C', 'S.C./A.4.', 'F.C.C.', 'C.A.', 'SC/Paris', 'A4.', 'SOTON/O.Q.', 'A.5.', 'A/5.', 'CA', 'F.C.'
					),
					('Sex', 'female', 'male'),
					('MaybeMother', False, True),
					'Age',
					('AgeEst', False, True),
					'SibSp', 'Parch', 'Family', 'Fare', 'SibFare',
					('HasTicketPrefix', False, True), 
					('Embarked', 'C', 'Q', 'S'),
				]),
				util.tensorize(),
			],
			'y': [
				util.select([
						('Survived', 0, 1),
						#('Survived', '0', '1'),
				]),
				util.tensorize(),
			],
			'meta': [
				util.select(['PassengerId']),
			],
		}),
	])

def train_data():
	raw = util.read_csv('train.csv')
	return proc(raw)

def exam_data():
	raw = util.read_csv('test.csv')
	return proc(raw)

if __name__ == '__main__':
	all = train_data()
	util.print([all['x'][0], all['y'][0]])
	# util.print(list(set(all)))
	# pp.pprint(list(x for x in all if x['Sex'] == 'male' and not 'Mr.' in x['Name']))
	# N = 5
	# S = random.randint(0, len(all) - N)
	# slice = all[S:S + N]
	# slice = feature_up(slice)
	# pp.pprint(slice)
