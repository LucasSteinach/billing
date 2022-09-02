from datetime import datetime


class Balance:
    def __init__(self, id_client, init_balance):
        self.id_client = id_client
        self.current_value = init_balance
        self.last_changing = datetime.now()
        self.status = 'Active'

    def activate(self):
        self.status = 'Active'

    def deactivate(self):
        self.status = 'Inactive'


class Transaction:
    def __init__(self, id_, id_client, id_service, action_type, parameter, date_time):
        self.id = id_
        self.id_client = id_client
        self.id_service = id_service
        self.action_type = action_type  # "Write-off", "Add"
        self.parameter = parameter
        self.datetime = date_time

    def calculate_balance(self, balance: Balance):
        if balance.status == "Inactive":
            return f'Transaction error!  User {balance.id_client} balance is inactive'
        else:
            pass
