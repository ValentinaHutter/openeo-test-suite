from openeo_test_suite.lib.base import process_test_runner

class http(process_test_runner):

  def __init__(self, connection):
    self.connection = connection

  def list_processes(self):
    return self.connection.list_processes()
  
  def describe_process(self, process_id):
    return self.connection.describe_process(process_id)

  def execute(self, process):
    return self.connection.execute(process)
