import json


def test_found_account(client):
    account_number = "555001"
    response = client.get("/account/"+account_number)
    assert response.status_code == 200

    data = response.json
    assert data["account_number"] == account_number
    assert data["balance"] == 10000
    assert data["customer_name"] == "Bob Martin"


def test_not_found_account(client):
    account_number = "555003"
    response = client.get("/account/"+account_number)
    assert response.status_code == 404


def test_validate_required_transfer(client):
    response = client.post(
        "/account/555003/transfer",
        json={},
        content_type='application/json',
    )
    assert response.status_code == 400

    data = response.json
    assert data["message"] == "to_account_number, amount are required"

    # required to_account_number
    response = client.post(
        "/account/555003/transfer",
        json={"amount": 1000},
        content_type='application/json',
    )
    assert response.status_code == 400

    data = response.json
    assert data["message"] == "to_account_number is required"

    # required amount
    request = json.dumps({"to_account_number": "555003"})
    response = client.post(
        "/account/555003/transfer",
        data=request,
        content_type='application/json',
    )
    assert response.status_code == 400

    data = response.json
    assert data["message"] == "amount is required"


def test_validate_transfer(client):
    # numeric amount
    response = client.post(
        "/account/555003/transfer",
        json={"to_account_number": "555003", "amount": "a"},
        content_type='application/json',
    )
    assert response.status_code == 400

    data = response.json
    assert data["message"] == "amount must be numeric"

    # amount > 0
    response = client.post(
        "/account/555003/transfer",
        json={"to_account_number": "555003", "amount": 0},
        content_type='application/json',
    )
    assert response.status_code == 400

    data = response.json
    assert data["message"] == "amount must be more than 0"

    # self transfer
    response = client.post(
        "/account/555003/transfer",
        json={"to_account_number": "555003", "amount": 1000},
        content_type='application/json',
    )
    assert response.status_code == 400

    data = response.json
    assert data["message"] == "can't self transfer"

    # from_account_number not found
    response = client.post(
        "/account/555003/transfer",
        json={"to_account_number": "555004", "amount": 1000},
        content_type='application/json',
    )
    assert response.status_code == 404

    data = response.json
    assert data["message"] == "from_account_number not found"

    # to_account_number not found
    response = client.post(
        "/account/555001/transfer",
        json={"to_account_number": "555003", "amount": 1000},
        content_type='application/json',
    )
    assert response.status_code == 404

    data = response.json
    assert data["message"] == "to_account_number not found"
