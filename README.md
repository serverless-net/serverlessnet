# Serverlessnet

Serverlessnet is an emulator for rapid prototyping of serverless IoT network for experimental purposes.  Virtual topologies of IoT devices are created and connected through a serverless framework, and can be controlled through an intuitive UI.  Custom lambda functions can be executed through a connection to an OpenWhisk instance.  This system can easily be used to test the fault tolerance of an IoT network as well.

## Why Serverlessnet?

Serverless frameworks are the natural way to run LAN outside the cloud.  As IoT devices often have limited computational power, serverless frameworks offer the capability to offload CPU to more powerful remote networks, in this case, the instance of OpenWhisk.  Running this network outside the cloud allows for more robust IoT systems that can deal with network outages.  There are multiple ways of achieving this; however, having this system be serverless provides a higher level of abstraction for the developer, as functions can be written without knowledge of system processes and frameworks.

## Internal Workings

![](https://serverless-net.github.io/serverlessnet/IMG_2432.png)

### Containernet

Containernet consists of a controller and a Mininet switch that controls any number of buttons, actuators, and one relayer.  These buttons act as the "on and off switches" for the actuators, and the relayer uses the information from the buttons to trigger OpenWhisk tasks, the results of which will be sent to the actuators.  The actuators will then send their updated states to the UI API, as will be discussed below.

### OpenWhisk

The OpenWhisk module consists of several workers executing custom lambda functions.  This module does the heavy computing for the switches and actuators.

### The Relayer Architecture

One of the main issues of OpenWhisk is that it is not containerizable.  OpenWhisk consists of many containers, and having nested Docker containers is not ideal.  OpenWhisk is also extremely hard to scale due to the multitude of containers.  Therefore, we decided to create one instance of OpenWhisk running separately from our general architecture, which will be accessed only through our relayer.  A side effect to this is that the computing instance can be modularized, and this instance of OpenWhisk can be replaced with any other computing instances.

### UI

The UI is a Flask application run on the local machine.  This UI provides visualizations of simple switches and actuators (denoted by circles), and updates the actuators accordingly when its corresponding switch is pressed.  When the switch is pressed, a post request, with the port number of the switch, is sent to the UI API.  The UI also polls the SQL DB every second to receive information on how to change the actuator, for example, turning it from red to black depending on its current state.

### UI API

The UI API is a containerized Flask application that acts as the communicator between the UI, Containernet, and SQL DB.  This API receives the state information from the actuators, and sends a post request to the SQL DB to update the state in the table.  When the UI API receives a post request from the UI, it will forward the information to Containernet for processing.

### SQL DB

The SQL Database is a containerized Flask application whose purpose is to access and update the database file that was initialized with its Docker container.  

## High-Level Setup

First, we clear all existing actions that OpenWhisk may be running at that time.  Then, we choose any of our custom actions for OpenWhisk to run.
Next, we run a setup script to initialize Containernet.  This allows us to use docker containers as hosts in the topology.  Then, we initialize any number of buttons and actuators with a program.  These button and actuator connections will be written to a json file, which will be fetched by both the database and the UI in their initializations.  
Last, we create the Docker containers for the database and UI API with their respective Dockerfiles, and launch the UI on our local machine.

## Issues Encountered

We decided to use Containernet instead of Mininet because Containernet provides us with the capability of using Docker containers as hosts in the emulated network.  We have also decided to use OpenWhisk instead of OpenLambda.  This is because OpenLambda does not seem to be in active development, and OpenWhisk is the industry standard.  We also ran into installation issues for OpenWhisk on Debian, thus we have a native installation on Ubuntu.

## Limitations

Even as this system is highly scalable, it is limited by the memory on the network servicing Containernet.  Therefore, it is possible for instance, to use this in an experimental setting for a school campus network emulation, but difficult or near impossible for a whole city's network.  OpenWhisk provides functionalities to allow different machines to handle the load of the workers, or run on a separate machine entirely, which can reduce the load.

## Future Work

We hope others can adopt this system to create custom IoT network initializations, as in the real world, devices can act both as buttons and actuators, and message types including fanout, topics, and headers.  We also hope that the containers acting as the buttons and actuators can be customized as actual device emulators.  Theoretically, multiple relayers can also be introduced into the system, which would control various computing instances used by different buttons and actuators.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

On Remote Machine:

Ubuntu

OpenWhisk

Docker


### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Built With

* [Containernet](https://containernet.github.io/) - Mininet Network Emulator
* [Docker](https://www.docker.com/) - Docker containers
* [OpenWhisk](https://openwhisk.apache.org/) - Used to run lambda functions

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Jessica Huynh** (https://github.com/jessicah25)
* **Jerry Lin** (https://github.com/)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Jan Janak
* Pekka Karhula
