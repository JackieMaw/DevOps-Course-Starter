from flask import session

_DEFAULT_ITEMS = [
    { 'id': 1, 'status': 'To Do', 'title': 'List saved todo items' },
    { 'id': 2, 'status': 'To Do', 'title': 'Allow new items to be added' }
]

class session_repository:

    def get_items(self):
        return session.get('items', _DEFAULT_ITEMS.copy())

    def get_item(self, id):
        items = self.get_items()
        return next((item for item in items if item['id'] == int(id)), None)

    def add_item(self, title, status):
        items = self.get_items()

        # Determine the ID for the item based on that of the previously added item
        id = items[-1]['id'] + 1 if items else 0

        item = { 'id': id, 'title': title, 'status': status }
        items.append(item)
        session['items'] = items

        return item

    def update_item_status(self, id, status):
        existing_items = self.get_items()
        updated_items = [self.__update_status(existing_item, status) if existing_item['id'] == id else existing_item for existing_item in existing_items]
        session['items'] = updated_items

    def __update_status(self, existing_item, status):
        existing_item['status'] = status
        return existing_item

    def delete_item(self, id):
        items = self.get_items()
        item = self.get_item(id)
        items.remove(item)
        session['items'] = items