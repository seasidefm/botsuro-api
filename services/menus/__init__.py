from repositories.sanity import Sanity


class AlbumMenus:
    def __init__(self):
        self.sanity = Sanity(use_archive_link=True)

    def get_album_menus(self):
        return self.sanity.get_album_menus()

    def get_album_menu(self, slug: str, bypass_cache=False):
        return self.sanity.get_unique_album_menu(slug, bypass_cache=bypass_cache)
