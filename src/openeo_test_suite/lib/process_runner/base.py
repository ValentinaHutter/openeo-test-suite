from typing import List, Dict, Any

class ProcessTestRunner:

  # Returns a list of all processes supported by the backend
  # Follows definition of the same function in the openEO Python client
  def list_processes(self) -> List[Dict]:
    pass
  
  # Returns single process description
  # Follows definition of the same function in the openEO Python client
  def describe_process(self, process_id: str) -> Dict:
    pass

  # Executes a user-defined process
  # Follows definition of the same function in the openEO Python client
  def execute(self, process: Dict) -> Any:
    pass
  
  # Converts a labeled array from the JSON object representation (type: labeled-array) to the internal backend representation
  # openEO process tests specification -> backend
  def encode_labeled_array(self, data: Dict) -> Any:
    raise Exception("labeled arrays not implemented yet")

  # Converts a datacube from the JSON object representation (type: datacube) to the internal backend representation
  # openEO process tests specification -> backend
  def encode_datacube(self, data: Dict) -> Any:
    raise Exception("datacubes not implemented yet")

  # Converts data from the internal backend representation to the process test / JSON5 representation
  # For example: numpy values to JSON data types, labeled-array or datacube to JSON object representation
  # backend -> openEO process tests specification
  def decode_data(self, data: Any) -> Any:
    return data
  
  # Defines whether the backend only supports JSON input or not.
  # If True, the runner will skip all tests that contain non JSON values such as infinity and NaN.
  def is_json_only(self) -> bool:
    return False
