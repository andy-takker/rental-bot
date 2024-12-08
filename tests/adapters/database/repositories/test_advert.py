from rental_bot.adapters.database.repositories.advert import AdvertRepository


async def test_find_new__empty_saved(advert_repository: AdvertRepository) -> None:
    new_ids = {"1", "2", "3"}
    find_new = await advert_repository.find_new(external_ids=new_ids, source="source")
    assert find_new == new_ids
