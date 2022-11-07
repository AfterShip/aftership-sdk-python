import aftership

aftership.api_key = 'asak_61f861873c394225ecd4fc981b339458'
aftership.api_secret = 'assk_e8b4b3c4441a478afd4726de1867e522'


def get_enabled_courier_names():
    result = aftership.courier.list_couriers(signature_type="AES")
    courier_list = [courier['name'] for courier in result['couriers']]
    return courier_list


def get_supported_courier_names():
    result = aftership.courier.list_all_couriers(signature_type="AES")
    courier_list = [courier['name'] for courier in result['couriers']]
    return courier_list


if __name__ == '__main__':
    enabled_couriers = get_enabled_courier_names(signature_type="AES")
    print(enabled_couriers)
