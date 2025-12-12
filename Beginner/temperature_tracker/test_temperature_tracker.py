import pytest

import temperature_tracker as tt
import temperature as temp

def test_min_temp():
    temp_data = tt.init()
    min_temp = tt.get_min_temp(temp_data)
    assert min_temp == 19
    
def test_max_temp():
    temp_data = tt.init()
    max_temp = tt.get_max_temp(temp_data)
    assert max_temp == 30

def test_avg_temp():
    temp_data = tt.init()
    avg_temp = tt.get_avg_temp(temp_data)
    assert avg_temp == 25