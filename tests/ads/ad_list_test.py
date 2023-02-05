import pytest

from ads.serializers import AdListSerializer
from tests.factories import AdFactory


@pytest.mark.django_db
def test_ad_list(client):
    ad_list = AdFactory.create_batch(3)

    response = client.get('/ad/')

    assert response.status_code == 200
    assert response.data == {"count": 3,
                             "next": None,
                             "previous": None,
                             "results": AdListSerializer(ad_list, many=True).data}
