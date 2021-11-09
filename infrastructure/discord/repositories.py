from google.cloud import datastore

import logging
from datetime import datetime


class Repository:

    def __init__(self):
        self._database = datastore.Client()

    def _get_key(self, kind=None):
        if not kind:
            kind = self._kind
        return self._database.key(kind)

    def _get_entity(self, kind=None):
        key = self._get_key()
        entity = datastore.Entity(key=key)
        return entity

    def _get_records(self, kind=None, filter=None):
        if not kind:
            kind = self._kind
        logging.info(f'Query {kind} kind')
        if filter:
            query = self._database.query(kind=kind)
            result = query.add_filter(filter[0], filter[1], filter[2]).fetch()
        else:
            result = self._database.query(kind=kind).fetch()
        records = []
        for entity in result:
            self.add_id(entity)
            records.append(entity)
        return records

    @staticmethod
    def add_id(entity):
        entity['id'] = entity.key.id
        return entity

    def _get_record(self, key, kind=None):
        if not kind:
            kind = self._kind
        key = self._database.key(kind, key)
        entity = self._database.get(key)
        if entity is None:
            return
        return self.add_id(entity)

    def _delete_record(self, key, kind=None):
        if not kind:
            kind = self._kind
        logging.warning(f'Deleting {kind}, {key}')
        key = self._database.key(kind, key)
        self._database.delete(key)

    def delete_record(self, id):
        record = self._get_record(id)
        self._delete_record(record.key.id)




class UserRepositoryDis(Repository):

    def __init__(self):
        self._kind = 'User'
        super(UserRepositoryDis, self).__init__()

    def add_user(self, username):
        logging.warning(f'Add new user: {username}')
        user = self._get_entity()
        user['username'] = username
        self._database.put(user)
        return user.key.id

    def get_users(self):
        logging.info(f'Getting users')
        return self._get_records()

    def get_user(self, user_name):
        logging.info(f'Getting user for {user_name}')
        users = self._get_records(filter=('username', '=', user_name))
        logging.info(f'found {len(users)} users')
        if len(users) > 1:
            raise RuntimeError(f'unexpected number of users for username: {user_name}, {len(users)}')
        elif len(users) == 1:
            return users[0]
        else:
            return None

    def get_user_by_id(self, id):
        logging.info(f'Getting user by id: {id}')
        return self._get_record(id)

    def delete_user(self, id):
        user = self.get_user_by_id(id)
        logging.warning(f'Admin delete user : {user["username"]}')
        self._delete_record(id)


class PostRepositoryDis(Repository):

    def __init__(self):
        self._kind = 'Post'
        self._user_repository = UserRepositoryDis()
        super(PostRepositoryDis, self).__init__()

    def add_post(self,body, user_id):
        username = self._user_repository.get_user_by_id(user_id)['username']
        logging.warning(f'Add new post fron user : {username}')
        post = self._get_entity()
        post['body'] = body
        post['author_id'] = user_id
        post['created'] = datetime.now()
        self._database.put(post)

    def get_post(self, post_id):
        logging.info(f'Getting post on id: {post_id} ')
        return self._get_record(post_id)

    def delete_post(self, post_id):
        logging.warning(f'Delete post: {post_id}')
        self._delete_record(post_id)

    def update_post(self, title, body, post_id):
        logging.warning(f'Update post: {post_id}')
        with self._database.transaction():
            post = self.get_post(post_id)
            post['title'] = title
            post['body'] = body
            self._database.put(post)

    def get_posts(self, user_id=None):
        logging.info(f'Getting posts')
        if not user_id:
            posts = self._get_records()
        else:
            posts = self._get_records(filter=('author_id', '=', user_id))
        logging.info(f'found {len(posts)} posts')
        self._prepare_posts(posts)
        return posts

    def _prepare_posts(self, posts):
        authors = {}
        statuses = {}
        # Join
        for post in posts:
            status = self._user_status_repository.get_status(post['author_id'])
            if post['author_id'] in authors:
                username = authors[post['author_id']]
            else:
                username = self._user_repository.get_user_by_id(post['author_id'])['username']
                authors[post['author_id']] = username
            post['username'] = username
            post['status'] = status['status_msg']