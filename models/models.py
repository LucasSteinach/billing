
# class Service:

class Transaction:
    def __init__(self, id_relation, id_client, action_type, parameter, date_time):
        self.id_relation = id_relation
        self.id_client = id_client
        self.action_type = action_type  # "regular", "one-off"
        self.parameter = parameter
        self.datetime = date_time


class Balance:
    def __init__(self, id_client, init_balance, date_time, status):
        self.id_client = id_client
        self.current_value = init_balance
        self.last_changing = date_time
        self.status = status

    def activate(self):
        self.status = 'Active'

    def deactivate(self):
        self.status = 'Inactive'

    def calculate(self, withdrawn):
        if self.status == "Inactive":
            return f'Transaction error!  User {self.id_client} balance is inactive'
        else:
            self.current_value -= summ
