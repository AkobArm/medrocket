from pydantic import BaseModel, Field, ValidationError, parse_raw_as
import api
import config


class ToDo(BaseModel):
    user_id: int = Field(alias='userId', default=None)
    id: int = None
    title: str = None
    completed: bool = None


class Geolocation(BaseModel):
    lat: str = None
    lng: str = None


class Address(BaseModel):
    street: str = None
    suite: str = None
    city: str = None
    zipcode: str = None
    geo: Geolocation = None


class Company(BaseModel):
    name: str
    catch_phrase: str = Field(alias='catchPhrase', default=None)
    bs: str = None


class Users(BaseModel):
    id: int
    name: str
    username: str
    email: str
    address: Address = None
    phone: str = None
    website: str = None
    company: Company


def parse(obj, data):
    try:
        parse_data = parse_raw_as(list[obj], data)
    except ValidationError as err:
        raise Exception(f'В файле введены некорректные данные. Проверьте!:\n {err.json()}')
    return parse_data


def get():
    users = parse(Users, api.get_data(config.API_USERS))
    todos = parse(ToDo, api.get_data(config.API_TODOS))
    tasks_list_users = {}

    for td in todos:
        if td.user_id is not None and td.id is not None and\
                td.title is not None and td.completed is not None:
            if tasks_list_users.get(str(td.user_id)) is None:
                tasks_list_users[str(td.user_id)] = {
                    'completed_tasks': [],
                    'remaining_tasks': []
                }

            title = td.title if len(td.title) <= 48 else td.title[:48] + '...'
            if td.completed:
                tasks_list_users[str(td.user_id)]['completed_tasks'].append(title)
            else:
                tasks_list_users[str(td.user_id)]['remaining_tasks'].append(title)
    del todos

    for us in users:
        if tasks_list_users.get(us.id) is None:
            tasks_list_users[str(us.id)] = {
                    'completed_tasks': [],
                    'remaining_tasks': []
                }

        tasks_list_users[str(us.id)].update({
            'username': us.username,
            'name': us.name,
            'email': us.email,
            'company_name': us.company.name
        })
    del users
    return tasks_list_users
