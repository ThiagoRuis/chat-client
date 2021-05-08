import responses

from ir_micro.config import settings
from ir_micro.models.database import VersionControl


@pytest.mark.usefixtures('create_database')
@pytest.mark.routes
class TestReportsListEndpoint:
    token = '6b29724069986cc04b5cc4f3e1f2d22276221795'
    url = '/v1/reports'

    def test_without_authorization_header(self, client):
        response = client.get(self.url)
        assert response.status_code == 401
        assert response.json == {'detail': 'No auth token provided.'}

    def test_without_bearer_in_header(self, client):
        response = client.get(self.url, headers={'Authorization': self.token})
        assert response.status_code == 401
        assert response.json == {'detail': 'No auth token provided.'}

    @responses.activate
    def test_with_token_expired(self, client):
        responses.add(
            method=responses.GET,
            url=f'{settings.MINHA_CONTA_URL}/rest-api/session/remaining-session-time',
            json={'detail': 'Invalid token'},
            status=401,
        )

        response = client.get(self.url, headers={'Authorization': f'Token {self.token}'})
        assert response.status_code == 401
        assert response.json == {'detail': 'Token Expired'}

    @responses.activate
    def test_list_reports_with_success(
        self, client, authentication_service, user_profile, party, create_reports
    ):
        responses.add(
            method=responses.GET,
            url=f'{settings.MINHA_CONTA_URL}/rest-api/session/remaining-session-time',
            json={'remaining_seconds': 900},
            status=200,
        )

        responses.add(
            method=responses.GET,
            url=authentication_service.user_profile_by_token_endpoint,
            json=user_profile,
            status=200,
        )

        response = client.get(self.url, headers={'Authorization': f'Token {self.token}'})
        assert response.status_code == 200