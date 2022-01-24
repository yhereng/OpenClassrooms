from booking_details import flight

def test_flight_or_city():
    assert flight(or_city='Paris').or_city == "Paris"

def test_flight_dst_city():
    assert flight(dst_city='London').dst_city == "London"

def test_flight_budget():
    assert flight(or_city=1000).or_city == 1000