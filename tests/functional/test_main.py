from http import HTTPStatus



def test_root(test_app):

    with test_app.test_client() as test_client:
        response = test_client.get("/")
        assert response.status_code == HTTPStatus.OK


