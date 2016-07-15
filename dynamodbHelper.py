from __future__ import print_function
import boto3
from boto3.dynamodb.conditions import Key, Attr

class dynamodb_connection:
	
	def __init__(self, table_name = 'Customer'):
		self.db = boto3.resouce('dynamodb',
			aws_access_key_id = '',
			aws_secret_access_key = '',
			region_name = '')

		self.table = self.db.Table(table_name)

	def switch_table(self, table_name):
		self.table = self.db.Table(table_name)

	def get_account_balance(self, id, account_name):
		response = self.table.query(
			KeyConditionExpression = Key('id').eq(id)
			)

		if response['Count'] == 0:
			print("no result")
		elif response['Count'] > 1:
			print("find duplicated entries")
		else:
			accounts = response["Items"][0]["Accounts"]
			for account in accounts:
				if account["AccountName"] == account_name:
					return float(account["Amount"])
		return False

if __name__ == '__main__':
	dynamodb = dynamodb_connection(table_name = "Customer")
	print(dynamodb.get_account_balance("123", "Trading"))
