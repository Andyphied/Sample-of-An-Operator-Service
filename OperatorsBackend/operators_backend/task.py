# import requests
import copy
from operators_backend import celery
from operators_backend.db import db
from operators_backend.models import OperatorModel
from operators_backend.collections import OperatorCollection
from operators_backend import celeryconfig


def init_celery(celery, app):
    celery.config_from_object(celeryconfig)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask


@celery.task(name='Update Mongo')
def sql_to_mongo():

    queries = (OperatorModel
               .query
               .filter(OperatorModel.move > 0)
               .all())
    error = 0
    count = 0
    if queries:
        for query in queries:
            test = copy.deepcopy(query)
            data_dict = test.__dict__
            data_dict.pop('_sa_instance_state', None)
            data_dict.pop('move', None)
            if query.move == 2:
                _id = data_dict['id']
                data_dict.pop('id', None)
                operator = OperatorCollection.objects(id=_id)
                operator = operator.update(**data_dict)

            if query.move == 1:
                operator = OperatorCollection(**data_dict)
                operator.save()

            try:
                query.move = 0
                db.session.add(query)

            except Exception:
                error += 1

            count += 1

        db.session.commit()
        print(f'{count} task done, with {error} error(s)')

    else:
        print('no work to be done, going back to sleep')


@celery.task(name='Update Sql Data')
def mongo_to_sql():

    queries = OperatorCollection.objects(updated=1)
    error = 0
    count = 0
    if queries:
        for query in queries:
            _id = query.id

            try:
                operator = OperatorModel.query.get(_id)
                operator.status = query.status
                operator.pin = query.pin
                query.updated = 0
                db.session.add(operator)

            except Exception:
                error += 1

            count += 1

        db.session.commit()
        print(f'{count} task done, with {error} error(s)')

    else:
        print('no work to be done, going back to sleep')
