# Poolboys

## Introduction
In our search for a means to pool our Chia resources in the pre-poolable plot era, we have created Poolboys.
Poolboys will transfer block rewards to a list of wallet addresses in the pool, based on the number of plots
you contribute to the pool. 

Poolboys exists off a few different components, many still in development. The components are listed below:

## Poolboys Tracker
The Poolboys tracker monitors the legitimate participation in the pool. It does this by monitoring your 
`chia farm summary` and `chia plots check` (in development). Your farming status is then sent to a remote server where
it is stored and checked for irregularities.

## Poolboys GUI
The Poolboys GUI allows (anonymous) inspection of the connected pool members and their stake in the pool.  

### Installation
In order to install Poolboys, clone the repository that contains the components:

```
    $ git clone https://github.com/pieterhelsen/poolboys.git
```

Now create a copy of `config-template.ini` and change the settings accordingly

```
    $ cd poolboys
    $ cp config-template.ini config.ini
    $ nano config.ini
```

Finally, run `install.sh` (with `sudo` privileges) and install the components you need.

```
    $ . ./install.sh
```

This will create and start a `systemd` service, which you can control with the following commands:

```
    $ sudo systemctl status chia-poolboys.service
    $ sudo systemctl restart chia-poolboys.service
    $ sudo systemctl start chia-poolboys.service
    $ sudo systemctl stop chia-poolboys.service
```

### Debugging

If some error occurred and your `systemd` service has shut down, make sure to check out the following log files:

```
    $ sudo journalctl -u chia-poolboys.service
    $ nano /var/log/chia/poolboys.log # this can be changed in the config file. 
```