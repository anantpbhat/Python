#!/usr/bin/env python

import argparse, requests

class BaseCl():
  def __init__(self):
    parser = argparse.ArgumentParser(description="Trigger an AnsibleTower template job using API interface")
    parser.add_argument("-l", "--limit", type=str, default="sandbox.testing.com", help="Specify Host Limit")
    parser.add_argument("-C", "--cmds", type=str, default="id; uptime", help="List out commands separated by semicolon")
    parser.add_argument("-R", "--root", type=bool, default=False, help="Run listed commands as root")
    self.args = parser.parse_args()
    self.url = "https://ansibletower.testing.com/api/v2/job_template/22642/launch"
    self.Head = {
      "Authorization": "Bearer <token string>",
      "Content Type": "application/json"
    }
    self.Args = {
      "limit": self.args.limit,
      "extra_vars": {
        "GatherFacts": False,
        "Become_Root": self.args.root,
        "runcmd_cmd": self.args.cmds
      }
    }

class MainProg(BaseCl):
  def main(self):
    resp = requests.post(self.url, headers = self.Head, json = self.Args, verify = False)
    print(resp.json())


if __name__ == "__main__":
  ans_tower_api = MainProg()
  ans_tower_api.main()
