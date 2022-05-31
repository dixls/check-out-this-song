from http import HTTPStatus



def test_404(client, app):
    response = client.get("/this-page-definitely-does-not-exist")
    assert response.status_code == HTTPStatus.NOT_FOUND
