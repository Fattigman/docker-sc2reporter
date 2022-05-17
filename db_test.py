# test for get_all_samples()
async def test_get_all_samples():
    samples = await get_all_samples()
    assert len(samples) > 0