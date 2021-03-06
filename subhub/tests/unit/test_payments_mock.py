import logging

import stripe
from mockito import when, mock, unstub

from subhub.api import payments
from subhub.exceptions import ClientError

logging.basicConfig(level=logging.DEBUG)


def test_check_stripe_subscriptions():
    response = mock(
        {
            "id": "cus_tester1",
            "object": "customer",
            "subscriptions": {"data": [{"status": "active", "id": "sub_123"}]},
            "sources": {"data": [{"id": "src_123"}]},
        },
        spec=stripe.Customer,
    )
    when(stripe.Customer).retrieve(id="cus_tester1").thenReturn(response)
    test_subscriptions = payments.check_stripe_subscriptions("cus_tester1")
    assert test_subscriptions[0]["id"] == "sub_123"
    assert test_subscriptions[0]["status"] == "active"
    unstub()


def test_check_stripe_subscriptions_cancelled():
    cancelled_sub = {"status": "cancelled", "id": "sub_124", "cancel_at": 232322}

    cancel_response = mock(
        {
            "id": "cus_tester2",
            "object": "customer",
            "subscriptions": {"data": [cancelled_sub]},
            "sources": {"data": [{"id": "src_123"}]},
        },
        spec=stripe.Customer,
    )

    delete_response = mock(
        {"id": "cus_tester2", "object": "customer", "sources": []}, spec=stripe.Customer
    )
    when(stripe.Customer).retrieve(id="cus_tester2").thenReturn(cancel_response)
    when(stripe.Customer).delete_source("cus_tester2", "src_123").thenReturn(
        delete_response
    )
    test_cancel = payments.check_stripe_subscriptions("cus_tester2")
    assert test_cancel[0]["status"] == "cancelled"
    unstub()


def test_check_stripe_subscriptions_fail():
    cancel_response = mock(
        {
            "id": "cus_tester3",
            "object": "customer",
            "subscriptions": {"data": []},
            "sources": {"data": [{"id": "src_123"}]},
        },
        spec=stripe.Customer,
    )
    delete_response = mock(
        {"id": "cus_tester3", "object": "customer", "sources": []}, spec=stripe.Customer
    )
    when(stripe.Customer).retrieve(id="cus_tester3").thenReturn(cancel_response)
    when(stripe.Customer).delete_source("cus_tester3", "src_123").thenReturn(
        delete_response
    )
    test_fail = payments.check_stripe_subscriptions("cus_tester3")
    logging.info(f"test fail {test_fail}")
    assert test_fail == []
    unstub()
