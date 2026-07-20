# Import TestClient to simulate API requests
from fastapi.testclient import TestClient

# Import the FastAPI app instance from the controller module
from main import app

# Create a TestClient instance for the FastAPI app
client = TestClient(app)

# Define a test function for reading a specific sheep
def test_read_sheep():
    # Send a GET request to the endpoint "/sheep/1"
    response = client.get("/sheep/1")

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Assert that the response JSON matches the expected data
    assert response.json() == {
        # Expected JSON structure
        "id": 1,
        "name": "Spice",
        "breed": "Gotland",
        "sex": "ewe"
    }

# Define a test function for creating a sheep
def test_add_sheep():
    # Prepare the new sheep data in a dictionary form
    sheep_data_name = {
        "id": 7,
        "name": "Edna",
        "breed": "Suffolk",
        "sex": "ewe"
    }

    # Send a POST request to the endpoint "/sheep" with the new sheep data
    # Arguments should be your endpoint and new sheep data
    response = client.post("/sheep", json=sheep_data_name)

    # Assert that the response status code is 201 (Created)
    assert response.status_code == 201

    # Verify that the sheep was actually added to the database by retrieving the new sheep
    get_response = client.get(f"/sheep/{sheep_data_name['id']}")
    assert get_response.json()["name"] == sheep_data_name["name"]

# Define a test function for reading all sheep
def test_read_all_sheep():
    # Send a GET request to the endpoint "/sheep"
    response = client.get("/sheep")

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Assert that the response is a list
    assert isinstance(response.json(), list)

    # Assert that the usual sheep are present (6 + any added during testing)
    assert len(response.json()) >= 6

def test_update_sheep():
    # Prepare the updated sheep data in a dictionary format
    sheep_data_name = {
        "id": 2,
        "name": "Blondie",
        "breed": "Polypay",
        "sex": "wether" # changed from "ram" to "wether" (castrated male sheep) to confirm update took effect
    }

    # Send a PUT request to the endpoint "/sheep/2" with the updated sheep data
    response = client.put("/sheep/2", json=sheep_data_name)

    # Assert that the response status is 200 (OK)
    assert response.status_code == 200

    # Verify that the sheep are updated in the database by retrieving it again
    assert response.json() == sheep_data_name

def test_delete_sheep():
    # Send a DELETE request to the endpoint "/sheep/3"
    response = client.delete("/sheep/3")

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Assert that the response JSON is the remaining list of sheep
    remaining_sheep = response.json()
    assert isinstance(remaining_sheep, list)

    # Assert that the deleted sheep (id 3) is no longer in the list
    assert all(sheep["id"] != 3 for sheep in remaining_sheep)

    # Verify that the sheep was actually removed by trying to retrieve it
    get_response = client.get("/sheep/3")
    assert get_response.status_code == 404