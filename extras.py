# create dummy content to search. Run from the shell

import random
from public.models import *

search_terms = ['Alpha', 'Bravo', 'Charlie', 'Delta', 'Echo', 'Foxtrot']

for x in range(0, 100):
    a_title = "article{}".format((x + 1))
    a, a_created = Article.objects.get_or_create(title=a_title)
    for y in range(0, 2):
        random_index = int(random.random() * len(search_terms))
        search_term = search_terms[random_index]
        p_title = "page{}".format((y + 1))
        p, p_created = Page.objects.get_or_create(article=a, title=a_title + p_title)
        p.body = ("This is the page body for " + a_title + " " + p_title + " you can search for this term: " + search_term)
        p.save()

