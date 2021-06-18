class trello_repository:

    def get_items(self):
        return session.get('items', _DEFAULT_ITEMS.copy())

    def get_item(self, id):
        items = self.get_items()
        return next((item for item in items if item['id'] == int(id)), None)

    def add_item(self, title):
        items = self.get_items()

        # Determine the ID for the item based on that of the previously added item
        id = items[-1]['id'] + 1 if items else 0

        item = { 'id': id, 'title': title, 'status': 'Not Started' }
        items.append(item)
        session['items'] = items

        return item

    def save_item(self, item):
        existing_items = self.get_items()
        updated_items = [item if item['id'] == existing_item['id'] else existing_item for existing_item in existing_items]
        session['items'] = updated_items
        return item

    def delete_item(self, id):
        items = self.get_items()
        item = self.get_item(id)
        items.remove(item)
        session['items'] = items