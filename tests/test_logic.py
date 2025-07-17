import pytest
import json
from unittest.mock import patch, MagicMock
from ec2pricing import fetch_regions, fetch_pricing_data, extract_prices

@patch("ec2pricing.boto3.client")
def test_fetch_regions(mock_boto_client):
    mock_ec2 = MagicMock()
    mock_ec2.list_regions.return_value = {
        "Regions": [{"RegionName": "us-east-1"}, {"RegionName": "eu-west-1"}]
    }
    mock_boto_client.return_value = mock_ec2

    regions = fetch_regions()
    assert "us-east-1" in regions
    assert "eu-west-1" in regions
    assert len(regions) == 2

@patch("ec2pricing.boto3.client")
def test_fetch_pricing_data(mock_boto_client):
    mock_pricing = MagicMock()
    mock_pricing.get_products.side_effect = [
        {
            "PriceList": [json.dumps({
                "product": {
                    "attributes": {"regionCode": "us-east-1", "operatingSystem": "Linux"}
                },
                "terms": {
                    "OnDemand": {
                        "abc": {
                            "priceDimensions": {
                                "xyz": {"pricePerUnit": {"USD": "0.0116"}}
                            }
                        }
                    }
                }
            })],
            "NextToken": None
        }
    ]
    mock_boto_client.return_value = mock_pricing

    result = fetch_pricing_data("t2.micro", "linux")
    assert isinstance(result, list)
    assert "product" in result[0]

def test_extract_prices():
    sample_data = [{
        "product": {
            "attributes": {
                "regionCode": "us-east-1",
                "operatingSystem": "Linux"
            }
        },
        "terms": {
            "OnDemand": {
                "xyz": {
                    "priceDimensions": {
                        "abc": {
                            "pricePerUnit": {"USD": "0.0123"}
                        }
                    }
                }
            }
        }
    }]
    price = extract_prices(sample_data, "us-east-1", "Linux")
    assert price == "$0.0123"

