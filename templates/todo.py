import logging
from tornado import web, escape
import numpy as np


def todo(config):
    nb_created_tasks = 0

    # Get the lastScanObjectId
    # ########################
    try:
        # Update the task to `todo` whatever the `lastPost`.
        config.services.tasks.tasks.put(
            task=config.conf['tasks']['todo'],
            key=config.conf['tasks']['todo'],
            status='todo',
            lastPost=4102444800000000000,
            )
    except web.HTTPError as e:
        # This task has never been created.
        assert e.log_message == (
            'Task id {id}/{id} not found.'.format(
                id=config.conf['tasks']['todo'])), e.log_message

        config.services.tasks.tasks.post(
            task=config.conf['tasks']['todo'],
            key=config.conf['tasks']['todo'],
            data={},  # You can put some data here that tell you what's the last todo status.
            )

    logging.debug('Start scanning for new tasks')
    nb_loops = 0

    while True:
        # Get and self-assign the task.
        r = config.services.tasks.tasks.get(task=config.conf['tasks']['todo'])
        assert r.ok
        if r.status_code != 200:
            break
        task = r.json()

        # Do something with the task.
        for number in range(3):
            for letter in ['A', 'B']:
                if np.random.uniform() < 0.5:
                    task_key = escape.url_escape('{}/{}'.format(escape.url_escape(letter),
                                                                escape.url_escape(str(number))))
                    logging.debug('Set task {}'.format(task_key))
                    r = config.services.tasks.tasks.post(
                        task=config.conf['tasks']['do'],
                        key=escape.url_escape(task_key),
                        data={'letter': letter, 'number': number},
                        )
                    assert r.status_code == 200
                    nb_created_tasks += 1

        # Update the task to `done` if nothing happenned since last GET.
        config.services.tasks.tasks.put(
            task=config.conf['tasks']['todo'],
            key=config.conf['tasks']['todo'],
            status='done',
            lastPost=task['lastPost'],
            )

        nb_loops += 1

    # Set the task to `todo`.
    config.services.tasks.tasks.post(
        task=config.conf['tasks']['todo'],
        key=config.conf['tasks']['todo'],
        data={},
        )

    log_str = 'Finished scanning for new tasks. Found {} in {} loops.'.format(
        nb_created_tasks, nb_loops)
    if nb_created_tasks > 0:
        logging.info(log_str)
    else:
        logging.debug(log_str)

    return {'createdTasks': nb_created_tasks, 'loops': nb_loops}
