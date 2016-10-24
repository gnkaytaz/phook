#!/usr/bin/env python
# phook.py
import os
from mercurial import util
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def linter(ui, repo, **kwargs):
    linter_cmd = "puppet-lint --with-context --with-filename --fail-on-warnings --no-80chars-check --no-autoloader_layout-check --no-only_variable_string-check "
    manifests_dir = os.path.join(repo.root, "manifests")

    for root, dirs, files in os.walk(manifests_dir):
      for f in files:
        if f.endswith(".pp"):
          file_path = os.path.join(root, f)
          command = linter_cmd + file_path
          logging.debug(command)
          ui.system(command)

def erbcheck(ui, repo, **kwargs):
    erbcheck_cmd = "cat {} | erb -x -T '-' | ruby -c > /dev/null"
    manifests_dir = os.path.join(repo.root, "templates")

    for root, dirs, files in os.walk(manifests_dir):
      for f in files:
        if f.endswith(".erb"):
          file_path = os.path.join(root, f)
          command = erbcheck_cmd.format(file_path)
          logging.debug(command)
          err = ui.system(command)
          if err:
            raise util.Abort("Error occurred in {}".format(file_path))


def ppcheck(ui, repo, **kwargs):
    ppcheck_cmd = "puppet parser validate {}"
    manifests_dir = os.path.join(repo.root, "manifests")

    for root, dirs, files in os.walk(manifests_dir):
      for f in files:
        if f.endswith(".pp"):
          file_path = os.path.join(root, f)
          command = ppcheck_cmd.format(file_path)
          logging.debug(command)
          err = ui.system(command)
          if err:
            raise util.Abort("Error occurred in {}".format(file_path))

def check(ui, repo, **kwargs):
  linter(ui, repo)
  erbcheck(ui, repo)
  ppcheck(ui, repo)
