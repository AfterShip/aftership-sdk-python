import aftership


# aftership.api_key = 'PUT_YOUR_AFTERSHIP_KEY_HERE'


def add_notification(tracking_id, emails=None, smses=None, webhook=None):
    update_params = {}
    if emails:
        update_params['emails'] = emails
    if smses:
        update_params['smses'] = smses
    if webhook:
        update_params['webhook'] = webhook

    if not update_params:
        raise ValueError('You must specify one of emails, smses or webhook')

    aftership.notification.add_notification(tracking_id=tracking_id, notification=update_params)


def list_notifications(tracking_id):
    notification = aftership.notification.list_notifications(tracking_id=tracking_id)
    return notification


def delete_all_notification(tracking_id):
    result = list_notifications(tracking_id)
    notification = result['notification']
    aftership.notification.remove_notification(tracking_id=tracking_id, notification=notification)


def create_tracking(slug, tracking_number):
    """Create tracking, return tracking ID
    """
    tracking = {'slug': slug, 'tracking_number': tracking_number}
    result = aftership.tracking.create_tracking(tracking=tracking, timeout=10)
    return result['tracking']['id']


def delete_tracking(tracking_id):
    try:
        aftership.tracking.delete_tracking(tracking_id=tracking_id)
    except aftership.exception.NotFound:
        return False
    return True


if __name__ == '__main__':
    delete_tracking('jmclbpqav9syfk72s8a0k019')
    tid = create_tracking('china-post', '40419890604404')
    add_notification(tid, 'support@aftership.com')
    delete_all_notification(tid)
    notifications = list_notifications(tid)
    delete_tracking(tid)
