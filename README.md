# coco.periodicTask

A webservice with python and tornado, that binds to coco.registry and runs periodically

### Requirements

To run this service, you need to have :

* `conda` and `supervisord` installed. See [coco.main](https://github.com/factornado/coco.main)
* A service `coco.registry` than is up and running. See [coco.registry](https://github.com/factornado/coco.registry)
* A service `coco.tasks` than is up and running. See [coco.tasks](https://github.com/factornado/coco.tasks)


### Installation

Clone the repository somewhere.

    git clone https://github.com/factornado/coco.periodicTask

Run the `deploy.sh` script and specify where you want to set the service
and what will be it's name and version:

    ./coco.periodicTask/deploy.sh ./coco.main/services/mytask mytask v1

Build the service environment etc:

    ./coco.main/services/mytask/make.sh

Edit the `config.yml` and tune the parameters.
(You may eventually need to replace the registry url if it's not listening at `http://localhost:8800`.)

Restart supervisor:

    source activate supervisor
    supervisorctl reload
    supervisorctl start all

You should be able to test your service through the registry:

    curl http://localhost:8800/mytask/foo

    > Hello from service mytask. You've asked for uri foo

And you shall see in the logs that the task is executing periodically:

    tail -100 /tmp/mytask.log                                                         
    
    > 2017-02-20 19:17:40,270 (main.py:21)- INFO - ================================================================================             
    > 2017-02-20 19:17:40,271 (main.py:74)- INFO - Listening on port 42420                                                                      
    > 2017-02-20 19:17:52,369 (todo.py:80)- INFO - Finished scanning for new tasks. Found 4 in 1 loops.                                         
    > 2017-02-20 19:17:57,297 (do.py:51)- INFO - ...doing something with task ['A', '0']...                                                     
    > 2017-02-20 19:17:57,305 (do.py:51)- INFO - ...doing something with task ['A', '1']...                                                     
    > 2017-02-20 19:17:58,294 (do.py:51)- INFO - ...doing something with task ['A', '2']...                                                     
    > 2017-02-20 19:17:58,299 (do.py:51)- INFO - ...doing something with task ['B', '2']...                                                     
    > 2017-02-20 19:18:02,355 (todo.py:80)- INFO - Finished scanning for new tasks. Found 4 in 1 loops.                                         
    > 2017-02-20 19:18:06,294 (do.py:51)- INFO - ...doing something with task ['A', '0']...                                                     
    > 2017-02-20 19:18:06,301 (do.py:51)- INFO - ...doing something with task ['A', '1']...                                                     
    > 2017-02-20 19:18:07,297 (do.py:51)- INFO - ...doing something with task ['B', '2']...                                                     
    > 2017-02-20 19:18:07,297 (do.py:51)- INFO - ...doing something with task ['A', '2']...                                                     
    > 2017-02-20 19:18:12,370 (todo.py:80)- INFO - Finished scanning for new tasks. Found 5 in 1 loops.                                         
    > 2017-02-20 19:18:15,295 (do.py:51)- INFO - ...doing something with task ['A', '0']...                                                     
    > 2017-02-20 19:18:15,299 (do.py:51)- INFO - ...doing something with task ['A', '1']...                                                     
    > 2017-02-20 19:18:16,294 (do.py:51)- INFO - ...doing something with task ['A', '2']...                                                     
    > 2017-02-20 19:18:16,300 (do.py:51)- INFO - ...doing something with task ['B', '2']...                                                     
    > 2017-02-20 19:18:17,293 (do.py:51)- INFO - ...doing something with task ['B', '1']...                                                     
    > ...