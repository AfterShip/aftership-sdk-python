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


def get_tracking(tracking_id, fields=None):
    """Get tracking
    """
    try:
        result = aftership.tracking.get_tracking(tracking_id=tracking_id, fields=','.join(fields))
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
    tid = create_tracking('usps', 'HA19260817')
    update_tracking(tid, title='new title')
    tracking = get_tracking(tid, fields=['title', 'checkpoints'])
    is_deleted = delete_tracking(tid)
    print(tracking)
