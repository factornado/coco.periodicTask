import logging
from tornado import escape


def do(config):
    # Get a task and parse it.
    r = config.services.tasks.tasks.get(task=config.conf['tasks']['do'])
    if r.status_code != 200:
        return {'nb': 0, 'code': r.status_code, 'reason': r.reason, 'ok': False}

    task = r.json()
    task_key = task['_id'].split('/')[-1]
    task_values = map(escape.url_unescape, escape.url_unescape(task_key).split('/'))

    logging.debug('GOT task_key: {}'.format(task_key))
    logging.debug('GOT task_values: {}'.format(task_values))
    try:
        # Do something with the task.
        out = do_something(task_values, config)

        # Set the task as `done`.
        config.services.tasks.tasks.put(
            task=config.conf['tasks']['do'],
            key=escape.url_escape(task_key),
            status='done',
            lastPost=task['lastPost'],
            )
        return {
            'nb': out['nb'],
            'details': out,
            'taskValues': list(task_values),
            'ok': True,
            }
    except Exception as e:
        # Set the task as `fail`.
        config.services.tasks.tasks.put(
            task=config.conf['tasks']['do'],
            key=escape.url_escape(task_key),
            status='fail',
            lastPost=task['lastPost'],
            )
        return {'nb': 1,
                'taskValues': list(task_values),
                'ok': False,
                'reason': e.__repr__(),
                }


def do_something(task_values, config):
    logging.info('...doing something with task {}...'.format(list(task_values)))
    return {'ok': True, 'nb': 1}
