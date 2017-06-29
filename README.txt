PELICAN COMMITS PLUGIN
======================

This plugin allows you to retrieve commits of a specified GitHub project with Pelican framework.
The purpose I made it for was to embed the list of recent commits made to my GitHub webpage directly into it.

INSTALLATION
============

1. Put the "commits" folder to your "plugin" folder.
2. Add the plugin to your "pelicanconf.py" file:

  PLUGINS = [..., "commits" ,...]

3. Specify the repository (also in "pelicanconf.py"):

  COMMIT_REPO = "owner/repo"

USE
===

In your templates, "commits" array will be accessible, in which each item has these attributes:

- "message"
- "sha"
- "url"
- "date"
- "time"

For example:

<ul>
  {% for commit in commits %}
    {% if loop.index < 5 %}
      <li><a href="{{commit.url}}"> {{ commit.date }} ({{ commit.time}}): {{ commit.message }} </a> </li>
    {% endif %}
  {% endfor %}
</ul>
