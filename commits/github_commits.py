# -*- coding: utf-8 -*-

# author: drummyfish
# I give this code to public domain.

import logging
import json

try:
  # python 2
  from urllib2 import urlopen
  from urllib2 import HTTPError
except ImportError:
  # python 3
  from urllib.request import urlopen
  from urllib.request import HTTPError

from pelican import signals

logger = logging.getLogger(__name__)

CONFIG_KEY = "COMMIT_REPO"
TEST_REPO = ""               # your test repo here

class Commits(object):

  def __init__(self, gen):
    self.content = None
    self.gen = gen
    
    url = "https://api.github.com/repos/" + self.gen.settings[CONFIG_KEY] + "/commits?per_page=1000"

    try:
      request = urlopen(url)
      encoding = request.headers["content-type"].split("charset=")[-1]
      response = request.read().decode(encoding)
    except HTTPError:
      logger.warning("unable to open " + url)
      return

    self.content = json.loads(response)

  def process(self):
    if self.content is None:
      return []

    commits = []

    for commit in self.content:
      commits.append({
        "message": commit["commit"]["message"],
        "date": commit["commit"]["author"]["date"].split("T")[0],
        "time": commit["commit"]["author"]["date"].split("T")[1],
        "url": commit["html_url"],
        "sha": commit["sha"]
        })           

    return commits

def initialize(gen):
  if not CONFIG_KEY in gen.settings.keys():
    logger.warning(CONFIG_KEY + " not set")
  else:
    gen.commit_plugin_instance = Commits(gen)

def fetch(gen, metadata):
  gen.context["commits"] = gen.commit_plugin_instance.process()

def register():
  signals.article_generator_init.connect(initialize)
  signals.article_generator_context.connect(fetch)

if __name__ == "__main__":
  # test stuff here
  
  test_gen = type('test', (object,), {})()
  test_gen.settings = {CONFIG_KEY: TEST_REPO}

  commits = Commits(test_gen)

  for commit in commits.process():
    print(commit)
