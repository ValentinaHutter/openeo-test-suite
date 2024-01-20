from openeo_test_suite.lib.process_runner.base import ProcessTestRunner


class Http(ProcessTestRunner):
    def __init__(self, connection):
        self.connection = connection

    def list_processes(self):
        return self.connection.list_processes()

    def execute(self, id, arguments):
        process = {
            "process_graph": {
                "node": {
                    "process_id": id,
                    "arguments": arguments,
                    "result": True,
                }
            }
        }
        return self.connection.execute(process)

    def is_json_only(self) -> bool:
        return True
