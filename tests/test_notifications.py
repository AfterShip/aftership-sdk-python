# from unittest import TestCase

# import pytest

# import aftership

# from aftership import const

# class NotificationTestCase(TestCase):
#     # @pytest.mark.vcr()
#     # def test_list_notification(self):
#     #     response = aftership.notification.list_notifications(tracking_id='k5lh7dy7vvqeck71p5loe011')

#     # @pytest.mark.vcr()
#     # def test_aes_list_notification(self):
#     #     response = aftership.notification.list_notifications(tracking_id='k5lh7dy7vvqeck71p5loe011', 
#     #     signature_type=const.SIGNATURE_AES_HMAC_SHA256)
    
#     @pytest.mark.vcr()
#     def test_rsa_list_notification(self):
#         response = aftership.notification.list_notifications(tracking_id='k5lh7dy7vvqeck71p5loe011', 
#         signature_type=const.SIGNATURE_RSA_HMAC_SHA256,
#         rsa_private_key=const.RSA_PRIVATE_KEY)

#     # @pytest.mark.vcr()
#     # def test_add_notification(self):
#     #     response = aftership.notification.add_notification(tracking_id='k5lh7dy7vvqeck71p5loe011',
#     #                                                        notification={'emails': ['jk.zhang@aftership.com']})
    
#     # def test_aes_add_notification(self):
#     #     response = aftership.notification.add_notification(tracking_id='k5lh7dy7vvqeck71p5loe011',
#     #                                                        notification={"emails": ["jk.zhang@aftership.com"]}, 
#     #                                                        signature_type=const.SIGNATURE_AES_HMAC_SHA256)
#     def test_rsa_add_notification(self):
#         response = aftership.notification.add_notification(tracking_id='k5lh7dy7vvqeck71p5loe011',
#                                                            notification={"emails": ["jk.zhang@aftership.com"]}, 
#                                                            signature_type=const.SIGNATURE_RSA_HMAC_SHA256,
#                                                            rsa_private_key=const.RSA_PRIVATE_KEY)

#     # @pytest.mark.vcr()
#     # def test_remove_notification(self):
#     #     response = aftership.notification.remove_notification(tracking_id='k5lh7dy7vvqeck71p5loe011',
#     #                                                           notification={"emails": ["support@aftership.com"]})

#     # def test_aes_remove_notification(self):
#     #     response = aftership.notification.remove_notification(tracking_id='k5lh7dy7vvqeck71p5loe011',
#     #                                                           notification={"emails": ["support@aftership.com"]},
#     #                                                           signature_type=const.SIGNATURE_AES_HMAC_SHA256)

#     def test_rsa_remove_notification(self):
#         response = aftership.notification.remove_notification(tracking_id='k5lh7dy7vvqeck71p5loe011',
#                                                               notification={"emails": ["support@aftership.com"]},
#                                                               signature_type=const.SIGNATURE_RSA_HMAC_SHA256,
#                                                               rsa_private_key=const.RSA_PRIVATE_KEY)                                                         