class HomePageCardItem:
    def __init__(self, template, title, description, meta, icon, url="#"):
        self.template = template
        self.title = title
        self.description = description
        self.meta = meta
        self.icon = icon
        self.url = url

    def get_info(self):
        return {
            'template': self.template,
            'title': self.title,
            'description': self.description,
            'meta': self.meta,
            'icon': self.icon,
            'url': self.url
        }


class HomePage:
    def __init__(self):
        self.card_items = []

    def get_card_items(self):
        return self.card_items

    def add_card_item(self, card_item: HomePageCardItem):
        self.card_items.append(card_item)

    def to_json(self) -> dict:
        return {
            'card_items': [card_item.get_info() for card_item in self.card_items]
        }


class HomePageFactory:
    @classmethod
    def create_home_page(cls) -> HomePage:
        page = HomePage()
        
        page.add_card_item(HomePageCardItem(
            "new/components/card_info.html",
            "Total employee", "10",
            "HR1", "/assets/img/icons/icon_group.svg",
            url='/hr/employee/')
        )
        
        page.add_card_item(HomePageCardItem(
            "new/components/card_info.html",
            "Total sale", "100",
            "SALE", "/assets/img/icons/icon_group.svg",
            url='/hr/employee/')
        )
        
        page.add_card_item(HomePageCardItem(
            "new/components/card_info.html",
            "Total customers", "1500",
            "CRM", "/assets/img/icons/icon_group.svg",
            url='/hr/employee/')
        )
        
        page.add_card_item(HomePageCardItem(
            "new/components/card_info.html",
            "Products", "225",
            "WMS", "/assets/img/icons/icon_group.svg",
            url='/hr/employee/')
        )
        return page
