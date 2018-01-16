# Graphy
A chatbot to automatically generate summaries of text using evolutionary concept graphs and dependency analysis.	
## Motivation

### Why is this bot needed?
I found a bottleneck of communication when I worked as an engineer in a startup company. We usually use Slack to convey information such as new specifications to colleagues, and this lets us work remotely. However, sharing information with colleagues is sometimes difficult because the amount of information has a tendency to become huge and the speed of communication required is too high, so it is not realistic to absorb all information that comes through via Slack. So, we want to only have to concentrate on information that is relevant to us.

### What is the goal?
The goal of Graphy is to help us decide whether or not to read all our unread messages, and to let us get an idea of their content before reading them. This bot creates an image from the text by using dependency analysis. In addition, the nodes of important keywords are emphasized by color and size.
The following pictures are a demonstration using four paragraphs from an article from Microsoft News Center Japan. We can understand that this article says ‘cloud’ and ‘digital’ are accelerating because the nodes ‘cloud’, ‘digital’, and ‘accelerate’ stand out. If you are not interested in this content from the unread messages, you can skip over them. That is why this bot is useful in terms of supporting communication and saving time.

## System
This bot works using Python on Heroku. There are mainly two stages to create an image from text. The first stage is natural language processing by using the dependency analysis tools Juman and Knp. The second stage is image generation by using the graph visualization tool Graphviz. 

Language: Python  
Tool: Juman, Knp, Graphviz  
Platform: Heroku, Slack  
Data store: S3  

### Key point
The most difficult part in this project is weighting to node because it is important that we make a judgement of which words are keywords. In the end, I used the small world effect, from graph theory. It says that any arbitrary two vertices are likely connected by passing through a small number of vertices in the middle. Small world graphs have hub nodes such that the small world would be destroyed if these nodes are removed. I defined these hub nodes as the keywords of the whole text.

### Improvement
I still have things to improve in this project. Each node should have a link to the original text. This feature would allow you to read the original text easily if you wanted to.

