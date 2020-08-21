from dateutil.parser import parse
import json, requests

class Card():
	def __init__(self, client, card):
		self.client = client
		self.card = card
		self.id = self.card['id']

	def __repr__(self):
		return f"<Trello-Card {self.id}>"

	def __str__(self):
		return json.dumps(self.card)

	def __iter__(self):
		return iter(self.card)

	def __getattr__(self, key):
		if key in self.card:
			return self.card[key]
		else:
			raise KeyError(key)

	def update(self, key, val):
		if key in self.card:
			requests.put(f'{self.client.baseUri}/1/cards/{self.id}/', {'key':self.client.KEY, 'token':self.client.TOKEN, key: val})
			self.card[key] = val
			return True
		else:
			raise KeyError(key)

	def writeOut(self, filename):
		with open(filename, 'w') as f:
			f.writelines(json.dumps(self.card), indent=4)
			f.close()

class BoardList():

	def __init__(self, client, _list):
		self.client = client
		self._list = _list
		self.id = self._list['id']

	def __str__(self):
		return json.dumps(self._list, indent=4)

	def __repr__(self):
		return f"<Trello-BoardList {self.id}>"

	def __iter__(self):
		return iter(self._list)

	def __getattr__(self, key):
		if key in self._list:
			return self._list[key]
		else:
			raise KeyError(key)

	def getCards(self):
		"""
		Get all cards of BoardList
		:return: list of Card
		"""
		response = json.loads(requests.get(f"{self.client.baseUri}/1/lists/{self.id}/cards?{self.client.uriRequired}").content.decode('utf-8'))
		return [Card(self.client, c) for c in response]

	def getCardByName(self, cardName):
		"""
		Get card by Name
		:return: Card or list of Card
		"""
		r = []
		cards = self.getCards()
		for card in cards:
			if card.name == cardName:
				r.append(card)
		if len(r) > 1:
			return r
		elif len(r) == 0:
			return None
		else:
			return r[0]

	def createCard(self, cardName, cardDescription=''):
		response = requests.post(f"{self.client.baseUri}/1/cards", {'key':self.client.KEY, 'token':self.client.TOKEN, 'name':cardName, 'desc':cardDescription, 'idList':self.id})
		if response.status_code == 200:
			return Card(self.client, json.loads(response.content.decode('utf-8')))
		else:
			raise Exception(f'Creation of card error [{response.status_code}]: {response.content.decode("utf-8")}')

class Board():
	def __init__(self, client, board):
		self.client = client
		self.board = board
		self.id = self.board['id']

	def __str__(self):
		return json.dumps(self.board, indent=4)

	def __repr__(self):
		return f"<Trello-Board {self.id}>"

	def __iter__(self):
		return iter(self.board)

	def __getattr__(self, key):
		if key in self.board:
			return self.board[key]
		else:
			raise KeyError(key)

	def writeOut(self, filename):
		"""
		Write the Board on a JSON file\n
		:params: filename string
		"""
		with open(filename, 'w') as f:
			f.writelines(json.dumps(self.board, indent=4))
			f.close()

	# CARDS
	def getCards(self):
		"""
		Get all cards from Board\n
		:return: list of Card
		"""
		response = json.loads(requests.get(f"{self.client.baseUri}/1/boards/{self.id}/cards?{self.client.uriRequired}").content.decode('utf-8'))
		return [Card(self.client, c) for c in response]

	def getCard(self, id):
		"""
		Get card by ID
		:return: Card
		"""
		response = json.loads(requests.get(f"{self.client.baseUri}/1/cards/{self.id}?{self.client.uriRequired}").content.decode('utf-8'))
		return Card(self.client, response)

	def getCardByName(self, cardName):
		"""
		Get card by Name
		:return: Card or list of Card
		"""
		r = []
		cards = self.getCards()
		for card in cards:
			if card.name == cardName:
				r.append(card)
		if len(r) > 1:
			return r
		elif len(r) == 0:
			return None
		else:
			return r[0]

	# LISTS
	def getLists(self):
		"""
		Get all lists from Board\n
		:return: list of BoardList
		"""
		response = json.loads(requests.get(f"{self.client.baseUri}/1/boards/{self.id}/lists?{self.client.uriRequired}").content.decode('utf-8'))
		return [BoardList(self.client, l) for l in response]

	def getList(self, listId):
		"""
		Get BoardList by ID\n
		:return: BoardList
		"""
		response = json.loads(requests.get(f"{self.client.baseUri}/1/lists/{self.id}?{self.client.uriRequired}").content.decode('utf-8'))
		return BoardList(self.client, response)

	def getListByName(self, listName):
		"""
		Get BoardList by Name\n
		:return: BoardList or list of BoardList
		"""
		r = []
		lists =  self.getLists()
		for boardList in lists:
			if boardList.name == listName:
				r.append(boardList)
		if len(r) > 1:
			return r
		elif len(r) == 0:
			return None
		else:
			return r[0]

	def createList(self, listName):
		response = requests.post(f"{self.client.baseUri}/1/boards/{self.id}/lists", {'key':self.client.KEY, 'token':self.client.TOKEN, 'name':listName})
		if response.status_code == 200:
			res = json.loads(response.content.decode('utf-8'))
			return BoardList(self.client, res)
		else:
			raise Exception(f'createList exception {response.status_code}: {response.content.decode("utf-8")}')

	def delete(self):
		"""
		Delete this Board\n
		:return: True\n
		:raise: Exception
		"""
		response = requests.delete(f"{self.client.baseUri}/1/boards/{self.id}?{self.client.uriRequired}")
		if response.status_code == 200:
			return True
		else:
			raise Exception(f'{response.status_code} : { response.content.decode("utf-8") }')

class Me():
	"""
	Represent your account\n
	:def: getBoards()\n
	:def: getBoardByName(string)\n
	:def: createBoard(string)\n
	"""
	def __init__(self, client, me):
		self.client = client
		self.me = me

	def __str__(self):
		return json.dumps(self.me)

	def __iter__(self):
		return iter(self.me)

	def getBoards(self):
		"""
		Get all boards you are in\n
		:return: list of Board
		"""
		return [Board(self.client, board) for board in self.me]

	def getBoardByName(self, name):
		"""
		Get first board by name\n
		:return: Board
		"""
		boards = self.getBoards()
		for board in boards:
			if board.name == name:
				return board

	def createBoard(self, boardName):
		"""
		Create a new board\n
		:return: Board or None
		"""
		response = requests.post(f"{self.client.baseUri}/1/boards/", data={'key':self.client.KEY, 'token':self.client.TOKEN, 'name':boardName})
		if response.status_code == 200:
			return Board(self.client, json.loads(response.content.decode('utf-8')))
		else:
			return None
