import importlib
import inspect
import numpy

from openeo_pg_parser_networkx import OpenEOProcessGraph, ProcessRegistry
from openeo_processes_dask.process_implementations.core import process
from openeo_pg_parser_networkx.process_registry import Process

from openeo_test_suite.lib.process_runner.base import ProcessTestRunner

def create_process_registry():
  process_registry = ProcessRegistry(wrap_funcs=[process])

  processes_from_module = [
    func
    for _, func in inspect.getmembers(
      importlib.import_module("openeo_processes_dask.process_implementations"),
      inspect.isfunction,
    )
  ]

  specs_module = importlib.import_module("openeo_processes_dask.specs")
  specs = {
    func.__name__: getattr(specs_module, func.__name__)
    for func in processes_from_module
  }

  for func in processes_from_module:
    process_registry[func.__name__] = Process(
        spec=specs[func.__name__], implementation=func
    )

  return process_registry

registry = create_process_registry()

class Dask(ProcessTestRunner):

  def list_processes(self):
    return map(lambda process: process.spec, registry.values())
  
  def describe_process(self, process_id):
    return registry[process_id].spec

  def execute(self, process):
    parsed = OpenEOProcessGraph(pg_data=process)
    callable = parsed.to_callable(process_registry = registry)
    return callable()

  def decode_data(self, data):
    # Converting numpy dtypes to native python types
    if isinstance(data, numpy.ndarray) or isinstance(data, numpy.generic):
      if data.size == 1:
        return data.item()
      elif data.size > 1:
        return data.tolist()

    return data