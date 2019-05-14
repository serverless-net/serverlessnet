# Serverlessnet

Serverlessnet is an emulator for rapid prototyping of serverless IoT network for experimental purposes.  Virtual topologies of IoT devices are created and connected through a serverless framework, and can be controlled through an intuitive UI.  Custom lambda functions can be executed through a connection to an OpenWhisk instance.  This system can easily be used to test the fault tolerance of an IoT network as well.

## Why Serverlessnet?

Serverless frameworks are the natural way to run LAN outside the cloud.  As IoT devices often have limited computational power, serverless frameworks offer the capability to offload CPU to more powerful remote networks, in this case, the instance of OpenWhisk.  Running this network outside the cloud allows for more robust IoT systems that can deal with network outages.  There are multiple ways of achieving this; however, having this system be serverless provides a higher level of abstraction for the developer, as functions can be written without knowledge of system processes and frameworks.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Give examples
```

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

## Deployment

Add additional notes about how to deploy this on a live system

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
