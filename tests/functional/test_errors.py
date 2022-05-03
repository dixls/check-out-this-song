from http import HTTPStatus



def test_404(test_app):

    with test_app.test_client() as test_client:
        response = test_client.get("/this-page-definitely-does-not-exist")
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert b"404" in response.data