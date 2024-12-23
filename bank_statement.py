import json
from typing import List, Dict, Any, Set, Tuple, Generator
from datetime import datetime


class BankStatement:
  def __init__(self, name: str) -> None:
    """
    BankStatement has a main attribute called movements.
    It is a dictionary where the keys are either the id provided by the snapshot
    or a generated key made by combining all invariant values in a movement and
    the values are the movements.
    """

    self.name = name  # Used only to write output into a file
    self.movements: Dict[str, Dict[str, Any]] = dict()

  def parse_json_movement(self, json_movement: Dict[str, Any]):
    """Here we parse a movement from a snapshot into fintoc's Movement format"""

    common_keys = [
        "id",
        "amount",
        "accountable_date",
        "date",
        "description",
    ]

    movement = {}
    for key in common_keys:
      if key in json_movement:
        movement[key] = json_movement[key]
      else:
        movement[key] = None

    if json_movement["type"] == "outbound":
      movement["amount"] *= -1

    if len(json_movement["movement_meta"]) == 0:
      movement["recipient_account"] = None
      movement["sender_account"] = None
      return movement

    meta = json_movement["movement_meta"]
    movement_type = json_movement["type"]

    if movement_type == "outbound":
      account_key = "recipient"
      other_key = "sender"
    else:
      account_key = "sender"
      other_key = "recipient"

    account_data = {
        "rut": meta[f"{account_key}_rut"],
        "number": meta[f"{account_key}_account"],
        "bank": meta[f"{account_key}_bank"],
    }

    movement[f"{account_key}_account"] = account_data
    movement[f"{other_key}_account"] = None

    return movement

  def parse_snapshot_movements(
        self, snapshot_data: Dict[str, Any]
      ) -> List[Dict[str, Any]]:
    """Parses all movements from the snapshot data and returns them in a list"""

    json_movements = snapshot_data["movements"]

    snapshot_movements = []

    for json_movement in json_movements:
      snapshot_movement = self.parse_json_movement(json_movement)
      snapshot_movements.append(snapshot_movement)

    return snapshot_movements

  def generate_id(self, movement: Dict[str, Any]) -> str:
    """
    Generates an id by combining all the invariant attributes of a movement
    """

    invariable_keys = {
        "accountable_date": str,
        "date": str,
        "amount": str,
        "sender_account": json.dumps,
        "recipient_account": json.dumps
    }

    generated_id = ""

    count = 0
    for key, func in invariable_keys.items():
      value = movement[key]
      generated_id += func(value)
      if count != len(invariable_keys) - 1:
        generated_id += "+"

      count += 1

    return generated_id

  def update(self, snapshot_data: Dict[str, Any]) -> None:
    """
    Updates the movements dictionary with the new movements from the snapshot
    """
    snapshot_movements = self.parse_snapshot_movements(snapshot_data)

    snapshot_keys: Set[str] = set()

    for movement in snapshot_movements:
      snapshot_id = movement["id"]

      if snapshot_id is not None:
        self.movements[snapshot_id] = movement
        continue

      generated_id = self.generate_id(movement)
      while generated_id in snapshot_keys:
        generated_id += "+"

      snapshot_keys.add(generated_id)
      self.movements[generated_id] = movement

  def strf_movement(
      self, movement: Dict[str, Any]
      ) -> Tuple[str, datetime, int]:
    """
    Converts a movement into a human readable string. Additionally returns
    the accountable date and the amount of the movement to sort them.
    """

    accountable_date_str = movement["accountable_date"]
    amount = movement["amount"]
    description = movement["description"]

    try:
      accountable_date = datetime.strptime(
          accountable_date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
      accountable_date = datetime.fromisoformat(accountable_date_str)

    accountable_date_str = accountable_date.strftime("%d-%m-%Y")

    movement_str = f"{accountable_date_str} | {amount} | {description}"

    return movement_str, accountable_date, amount


  def movements_generator(self) -> Generator[str, None, None]:
    """Sorts movements and returns a generator of them"""

    movements_tuples = []
    for movement_str in self.movements.values():
      movement_str, accountable_date, amount = self.strf_movement(movement_str)
      movements_tuples.append((accountable_date, amount, movement_str))

    movements_tuples.sort(key=lambda x: (x[0], x[1]))

    for _, _, movement_str in movements_tuples:
      yield movement_str

  def show_movements(self) -> None:
    """Prints out movements in a human readable way"""

    for movement in self.movements_generator():
      print(movement)

  def export_movements(self, output_path) -> None:
    """Exports movements into the necessary path"""

    with open(f"{output_path}/empresa_{self.name.lower()}.txt", "w") as file:
      file.write(f"Numero de movimientos: {len(self.movements)}\n")
      for movement in self.movements_generator():
        file.write(movement + "\n")
