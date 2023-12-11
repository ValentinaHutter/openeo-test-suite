from openeo_test_suite.lib.process_runner.base import ProcessTestRunner
from openeo_driver.ProcessGraphDeserializer import process_registry_2xx
import numpy

class Vito(ProcessTestRunner):

  def list_processes(self):
    return process_registry_2xx.get_specs()
  
  def describe_process(self, process_id):
    return process_registry_2xx.get_spec(process_id)

  def execute(self, process):
    node = process["process_graph"]["node"]
    fn = process_registry_2xx.get_function(node["process_id"])
    return fn(node["arguments"], env=None)

  def decode_data(self, data):
    # Converting numpy dtypes to native python types
    if isinstance(data, numpy.generic):
      if data.size == 1:
        return data.item()
      elif data.size > 1:
        return data.tolist()

    return data