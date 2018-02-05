# Graphy
A chatbot to automatically generate summaries of text using evolutionary concept graphs and dependency analysis.	
## Development
```
$ python app.py
```

## Production
To start a Droplet on DigitalOcean.
```
$ ssh root@<ipv4> // SSH Key registration required beforehand
$ nohup python app.py &
```

### Install Dependensies
Python packages
```
$ pip install -r requirements.txt
```

Graphviz
```
$ apt install graphviz
```

The commands of knp and juman
```
$ wget http://nlp.ist.i.kyoto-u.ac.jp/nl-resource/juman/juman-7.01.tar.bz2
$ tar jxvf juman-7.01.tar.bz2
$ cd juman-7.01
$ ./configure
$ make
$ make install

$ wget http://nlp.ist.i.kyoto-u.ac.jp/nl-resource/knp/knp-4.18.tar.bz2
$ tar jxvf knp-4.18.tar.bz2
$ cd knp-4.18
$ ./configure
$ make
$ sudo make install
```

### Stop
To stop a Droplet on DigitalOcean.
```
$ ps aux | grep nohup
$ ps aux | grep python
$ kill <PID>
```

## Upload files to DigitalOcean
```
$ scp -r ./* root@<ipv4>:/root/
```


## System
This bot works using Python on DigitalOcean. There are mainly two stages to create an image from text. The first stage is natural language processing by using the dependency analysis tools Juman and Knp. The second stage is image generation by using the graph visualization tool Graphviz. 

| Item       |             |
|:-----------|:------------|
| Language   | Python      |
| Tools      | Juman, Knp, Graphviz |
| Platform   | DegitalOcean, Slack        |
| Data store | S3          |

![graphy-system-archtecture](https://raw.githubusercontent.com/d0iasm/graphy/master/images/graphy_architecture.png)
