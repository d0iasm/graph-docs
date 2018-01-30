# Graphy
A chatbot to automatically generate summaries of text using evolutionary concept graphs and dependency analysis.	
## Development
```py
$ python app.py
```

## Productio
To start Dyno of this bot
```
$ heroku ps:scale bot=1
```

To stop Dyno of this bot
```
$ heroku ps:scale bot=0
```

## System
This bot works using Python on Heroku. There are mainly two stages to create an image from text. The first stage is natural language processing by using the dependency analysis tools Juman and Knp. The second stage is image generation by using the graph visualization tool Graphviz. 

Language: Python  
Tool: Juman, Knp, Graphviz  
Platform: Heroku, Slack  
Data store: S3  

![graphy-system-archtecture](https://raw.githubusercontent.com/d0iasm/graphy/master/images/graphy_architecture.png)
