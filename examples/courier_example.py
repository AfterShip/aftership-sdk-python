import aftership

aftership.api_key = 'PUT_YOUR_AFTERSHIP_KEY_HERE'


def get_enabled_courier_names():
    result = aftership.courier.list_couriers()
    courier_list = [courier['name'] for courier in result['couriers']]
    return courier_list


def get_supported_courier_names():
    result = aftership.courier.list_all_couriers()
    courier_list = [courier['name'] for courier in result['couriers']]
    return courier_list


if __name__ == '__main__':
    enabled_couriers = get_enabled_courier_names()
    print(enabled_couriers)
