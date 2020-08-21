import requests, json, datetime
from tEntity import Card, Board, Me

class Trello():
	"""
	First Trello instance\n
	:def: search(boardId, query)\n
	:def: getBoard(boardId)\n
	:def: getMe()
	"""
	KEY = ""
	TOKEN = ""

	def __init__(self, _key, _token):
		self.KEY = _key
		self.TOKEN = _token
		self.baseUri = "https://api.trello.com"
		self.uriRequired = f"&key={self.KEY}&token={self.TOKEN}"

	def search(self, boardId, query):
		"""
		Search cards inside a board\n
		:return: list of Card
		"""
		response = json.loads(requests.get(f"{self.baseUri}/1/search?query={query}&idBoards={boardId}{self.uriRequired}&modelTypes=cards").content.decode('utf-8'))
		return [Card(self, c) for c in response]

	def getBoard(self, boardId):
		"""
		Get board
		:return: Board
		"""
		response = json.loads(requests.get(f"{self.baseUri}/1/boards/{boardId}?{self.uriRequired}").content.decode('utf-8'))
		return Board(self, response)

	def getMe(self):
		"""
		Get Me instance
		:return: Me
		"""
		response = json.loads(requests.get(f"{self.baseUri}/1/members/me/boards?{self.uriRequired}").content.decode('utf-8'))
		return Me(self, response)
