import aftership


# aftership.api_key = 'PUT_YOUR_AFTERSHIP_KEY_HERE'


def create_tracking(slug, tracking_number):
    """Create tracking, return tracking ID
    """
    tracking = {'slug': slug, 'tracking_number': tracking_number}
    result = aftership.tracking.create_tracking(tracking=tracking, timeout=10)
    return result['tracking']['id']


def update_tracking(tracking_id, **values):
    aftership.tracking.update_tracking(tracking_id=tracking_id, tracking=values)
    return True


def get_tracking(*, tracking_id=None, slug=None, tracking_number=None,
                 fields=None):
    """Get tracking by tracking_id or slug + tracking_number
    """
    try:
        result = aftership.tracking.get_tracking(tracking_id=tracking_id,
                                                 slug=slug,
                                                 tracking_number=tracking_number,
                                                 fields=','.join(fields))
    except aftership.exception.NotFound:
        return None

    return result['tracking']


def delete_tracking(tracking_id):
    try:
        aftership.tracking.delete_tracking(tracking_id=tracking_id)
    except aftership.exception.NotFound:
        return False
    return True


if __name__ == '__main__':
    _tracking_id = create_tracking('usps', 'TEST12345678')
    print(f'tracking_id: {_tracking_id}')

    update_tracking(_tracking_id, title='new title')

    # Get tracking by tracking_id
    _tracking = get_tracking(tracking_id=_tracking_id, fields=['title', 'checkpoints'])
    print('Get tracking by tracking_id:', _tracking)

    # Get tracking by slug and tracking_number
    _tracking = get_tracking(slug='usps', tracking_number='HA19260817',
                             fields=['title', 'checkpoints'])
    print('Get tracking by slug and tracking_number:', _tracking)

    is_deleted = delete_tracking(_tracking_id)
    print('Delete tracking result:', is_deleted)
