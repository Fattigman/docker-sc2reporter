import pytest
from api.endpoints.dashboard import fill_graph_data

def test_fill_graph_data():
    graph_list = [
        {'date': '2021-03-16', 'pango_count': 1, 'pangolin': 'B.1.474'},
        {'date': '2021-03-17', 'pango_count': 1, 'pangolin': 'B.1.160'},
    ]
    
    result = fill_graph_data(graph_list)
    
    expected = [
        {'date': '2021-03-16', 'pango_count': 1, 'pangolin': 'B.1.474'},
        {'date': '2021-03-16', 'pango_count': 0, 'pangolin': 'B.1.160'},
        {'date': '2021-03-17', 'pango_count': 1, 'pangolin': 'B.1.160'},
        {'date': '2021-03-17', 'pango_count': 0, 'pangolin': 'B.1.474'}
    ]
    
    assert result == expected, f"Expected {expected}, but got {result}"

def test_fill_graph_data_no_data():
    # Empty input list
    graph_list = []
    
    result = fill_graph_data(graph_list)
    expected = []
    
    assert result == expected, f"Expected {expected}, but got {result}"

# More test cases can be added as per your requirements.