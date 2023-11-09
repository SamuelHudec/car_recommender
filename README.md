# Car recommender using public dataset

## Environment setup

To use this library/repo, make sure that you have Python >= `3.9.*` - we recommend using [pyenv][] for managing different
Python versions (see: [how to install pyenv on MacOS][]).

This project defines dependencies in [pyproject.toml](./pyproject.toml) according to [PEP-621](https://peps.python.org/pep-0621/)
For development create virtual env with:
```bash
python -m venv venv
source venv/bin/activate
```
Then run:
```bash
make install
```

## Front end

Suggested website wireframes for better intuition (please ignore my poor drawing skills):
![image](images/img_1.jpeg)
![image](images/img_2.jpeg)

As simple as possible, we are swallowed by ADs on every page, so I prefer simplicity in design.
This means, easy to navigate on the web, you don't want the customer to get lost while searching for a product, 
nor should there be a dead end when traveling through the web inspiringly. Various recommenders will be used for this. 
ňSide note, there should be an inspirational element, sometimes even a pseudo-random recommendation 
(not part of this repo).

__Main page__

Only search and carousels sorted by the popularity of some basic character (for cars, I would guess manufacturers). 
To get started, I would choose the arrangement according to domestic manufacturers and continue with the most 
affordable ones (in CZ Škoda, VW, ...) or download data from the latest car sales census. On the main page, there would 
be an option to click on a product detail and an option to click on various category pages. I would divide the 
individual boxes in carousels into popular, golden middle, luxury. I'm not going to comment on Search, it's for 
longer and is not the subject of the repo.

__Category page__ 

For example manufacturer, price category etc

__Product detail__

Photo box of the item (vehicle) other features, below that there would be other carousels for similar vehicles 
with a similar price, with similar features and anything that makes sense to the customer. For example:
- vehicles where he could get more for a small extra payment (higher performance, etc.). Here, in my opinion, it is important to be able to communicate to the customer what he is currently looking at. That is, it depends on the description of the carousel. 
- vehicles that look similar 
- same color (there are people who make decisions mainly based on color)

__Features__

UX feature which can increase value for users is __Smart search box__ (its also recommender) 
it will sort and standardize when searching. According to experience, this is the main point of entry, here I would 
suggest some contrastive learning driven by sematic neural search (I know it works). That is, someone writes: 
"a nice red car" -> throws out a list of options without manual navigation.
Another one, __Compare tool__ build a UX recommender so that the recommended vehicles are displayed next to each 
other so that they can be easily compared. At the same time, vehicle on detail would be first.
	
Technical feature, which might increase value for users is __Personalised recommenders__  not only to display what the 
user has already seen, but to recommend the next step from the sessions, what he would like to see/buy (NLP).	

__Technical aspect__

Its hard to say what technologies use for mentioned project. It depends on the customer. I assume that he already has 
a website ready and running (lives) somewhere, so I would adapt to what he has. if it uses AWS, I would use its tools 
or tools that are well integrated. In the case of GCP, I know that Google has everything from artifact repo, through 
cloud storage, Bigquery, vertex AI, etc. Every technology has pros and cons, it is important to know about them. The 
reason why I would choose the whole package of the most preferred ones is clear, they will communicate more easily 
in all aspects.

## Software engineering

I wrapped the data in the flexible API where I chose the simplest flask form. There are several options like django or 
fastapi, but for me the more familiar way is via flask. I implemented GET, PUT and DELETE which should be enough 
for this task. Data handling is done by pandas what is not the best way, but pandas methods make my coding easier.
Run api using:
```bash
python -m src.api.api
```
You can play or test api by [notebook](./notebooks/API_demo.ipynb).


## Data engineering / Data science

```bash
python -m scripts.create_max_profit_reco
```

Future for recommendation can be [generative AI][]

## DevOps / Infrastructure


[pyenv]: https://github.com/pyenv/pyenv#installationbrew
[how to install pyenv on MacOS]: https://jordanthomasg.medium.com/python-development-on-macos-with-pyenv-2509c694a808
[generative AI]: https://arxiv.org/abs/2305.05065