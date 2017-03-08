import logging
from tornado import escape
import numpy as np


def todo(config):
    nb_created_tasks = 0

    # We get the `todo` task.
    r = config.services.tasks.getByKey.get(
        task=config.conf['tasks']['todo'],
        key=config.conf['tasks']['todo'])
    if r.status_code == 204:
        # The task does not exist yet : we create it.
        r = config.services.tasks.action.put(
            task=config.conf['tasks']['todo'],
            key=config.conf['tasks']['todo'],
            action='stack',
            data={'nb': 0},  # You can put some data here to keep memory of current status.
            )

    logging.debug('Start scanning for new tasks')
    nb_loops = 0

    while True:
        # Get and self-assign the task.
        r = config.services.tasks.assignOne.put(task=config.conf['tasks']['todo'])
        if r.status_code != 200:
            break
        task = r.json()

        # Do something with the task.
        nb = task['data']['nb']
        for number in range(3):
            for letter in ['A', 'B']:
                if np.random.uniform() < 0.5:
                    task_key = escape.url_escape('{}/{}/{}'.format(nb, letter, number))
                    logging.debug('Set task {}'.format(task_key))
                    r = config.services.tasks.action.put(
                        task=config.conf['tasks']['do'],
                        key=escape.url_escape(task_key),
                        action='stack',
                        data={'letter': letter, 'number': number, 'nb': nb},
                        )
                    assert r.status_code == 200
                    nb += 1
                    nb_created_tasks += 1

        # Update the task to `done` if nothing happenned since last GET.
        r = config.services.tasks.action.put(
            task=config.conf['tasks']['todo'],
            key=config.conf['tasks']['todo'],
            action='success',
            data={'nb': nb},
            )

        nb_loops += 1

    # Set the task to `todo`.
    r = config.services.tasks.action.put(
        task=config.conf['tasks']['todo'],
        key=config.conf['tasks']['todo'],
        action='stack',
        data={'nb': nb},
        )

    log_str = 'Finished scanning for new tasks. Found {} in {} loops.'.format(
        nb_created_tasks, nb_loops)
    if nb_created_tasks > 0:
        logging.info(log_str)
    else:
        logging.debug(log_str)

    return {'createdTasks': nb_created_tasks, 'loops': nb_loops}
