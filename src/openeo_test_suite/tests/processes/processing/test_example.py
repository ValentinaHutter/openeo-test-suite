def test_add35(connection):
    pg = {
        "add35": {
            "process_id": "add",
            "arguments": {"x": 3, "y": 5},
            "result": True,
        }
    }
    response = connection.execute(pg)
    assert response == 8
