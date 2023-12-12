from openeo_test_suite.lib.process_runner.http import Http

class VitoHttp(Http):

    def __init__(self, connection):
        super().__init__(connection)
        self.connection.authenticate_basic("alice", "alice123")

    def list_processes(self):
        return self.connection.list_processes()
    
    def describe_process(self, process_id):
        return self.connection.describe_process(process_id)

    def execute(self, process):
        return self.connection.execute(process)
