import aftership

aftership.api_key = 'PUT_YOUR_AFTERSHIP_KEY_HERE'


def batch_predict_estimated_delivery_date():
    result = aftership.estimated_delivery_date.batch_predict_estimated_delivery_date(
        [
            {
                "slug": "fedex",
                "service_type_name": "FEDEX HOME DELIVERY",
                "origin_address": {
                    "country": "USA",
                    "state": "WA",
                    "postal_code": "98108",
                    "raw_location": "Seattle, Washington, 98108, USA, United States"
                },
                "destination_address": {
                    "country": "USA",
                    "state": "CA",
                    "postal_code": "92019",
                    "raw_location": "El Cajon, California, 92019, USA, United States"
                },
                "weight": {
                    "unit": "kg",
                    "value": 8
                },
                "estimated_pickup": {
                    "order_time": "2021-07-01 15:04:05",
                    "order_cutoff_time": "20:00:00",
                    "business_days": [
                        1,
                        2,
                        3,
                        4,
                        5,
                        6,
                        7
                    ],
                    "order_processing_time": {
                        "unit": "day",
                        "value": 0
                    }
                }
            }
        ]
    )
    return result['estimated_delivery_dates']


if __name__ == '__main__':
    list = batch_predict_estimated_delivery_date()
    print(list)
