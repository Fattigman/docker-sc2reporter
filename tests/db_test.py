from db.db import *
from models.models import *

# test for get_single_sample()
async def test_get_single_sample():
    sample = await get_single_sample("sc2-1040")
    assert sample["sample_id"] == "sc2-1040"

# test for get_all_samples()
async def test_get_all_samples():
    samples = await get_all_samples()
    assert len(samples) > 0

# test for get_user()
async def test_get_user():
    user = await get_user("Test")
    assert user["username"] == "Test"