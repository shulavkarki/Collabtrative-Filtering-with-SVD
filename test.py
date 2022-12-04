import pytest
from starlette.testclient import TestClient 

from app import app, topN_recommendation


client = TestClient(app)

print(f"Clients: {client}")
def produce_usecases(n):
    listi = []
    for i in range(0, n):
        json_blob = {"user_id": i, "n_items": 10}
        listi.append(json_blob)
    return listi

usecases = produce_usecases(6040)
# print(usecases)


# @pytest.mark.parametrize("user_id,n_items", usecases)
# def test_simple_usecase(user_id, n_items):
#     resp = client.post('/recommend/', json=usecases)
#     response = topN_recommendation(user_id, n_items)
#     assert response.status_code == 200


def test_recommendation():
    # check_json = {'user_id': 5737, 'n_items': 10}
    for key_vals in usecases:
        resp = client.post("/recommend/", json=key_vals)
        assert resp.status_code == 200