import json
import os
from typing import List, Dict, Any, Set, Tuple, Generator
from datetime import datetime


SNAPSHOTS_PATH = "drive/MyDrive/snapshots/"
OUTPUT_PATH = "results_movements"

def get_snapshots() -> List[str]:
  """Returns a list of all snapshot paths"""
  return os.listdir(SNAPSHOTS_PATH)

def get_companies_snapshots(snapshots: List[str]) -> Dict[str, List[str]]:
  """Returns a dictionary of companies and their snapshots paths"""
  companies = {}
  for snapshot in snapshots:
    if snapshot.split(".")[-1] != "json":
      continue

    company = snapshot.split("_")[1]

    if company not in companies:
      companies[company] = []

    companies[company].append(snapshot)

  return companies

def get_snapshot_data(snapshot_path):
  """Loads the snapshot json data into a dictionary and returns it"""
  with open(SNAPSHOTS_PATH + snapshot_path) as json_file:
    data = json.load(json_file)

  return data