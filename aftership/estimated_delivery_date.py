from .request import make_request
from .response import process_response

__all__ = ['batch_predict_estimated_delivery_date']


def batch_predict_estimated_delivery_date(estimated_delivery_dates, **kwargs):
    """Batch predict the estimated delivery dates
    """
    response = make_request('POST', 'estimated-delivery-date/predict-batch',
                            json=dict(estimated_delivery_dates=estimated_delivery_dates), **kwargs)
    return process_response(response)
