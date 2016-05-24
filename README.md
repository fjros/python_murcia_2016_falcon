A primer on Falcon
==================

This repo contains the code and slides of a short talk given at the
[Python Murcia](http://www.meetup.com/es-ES/Meetup-de-Python-en-Murcia/) meetup in May 2016. The
objective is to introduce REST API development via [Falcon](http://falconframework.org) through
some simple examples.

You can spin up a virtual server with the environment employed during the talk:

* Install Vagrant and the following plugins

```bash
vagrant plugin install vagrant-hostsupdater
vagrant plugin install vagrant-vbguest
```

* Provision the virtual server

```bash
git clone https://github.com/fjros/python_murcia_2016_falcon
cd python_murcia_2016_falcon/
vagrant up
```

* Log into the server and run the sample application

```bash
vagrant ssh
```

```bash
PYTHONPATH=/vagrant:$PYTHONPATH gunicorn -b 0.0.0.0:8000 music:api
```

License
-------

Copyright 2016 Francisco Javier Ros Muñoz

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
