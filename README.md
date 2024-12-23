# Fintoc T2

This is my assessment to be hired by fintoc :)

## How to run it

Simple, clone and run with python (I used 3.12 but it should not matter that much)

```bash
git clone https://github.com/alexfilsecker/fintoc-temp.git
cd fintoc-temp
python main.py
```

## Explanation

My solution can be described in the following steps:

0. Instantiate the `BankStatement` class with an attribute called movements. This will be a dictionary where values are the movements and it's keys will be either the bank's internal id or a generated id made by combining all invariant attributes of a movement.
1. Read a snapshot and parse the movements into Fintoc's `Movement` format.
2. Create a `snapshot_keys` set, to store our keys for each snapshot.
3. If a movement has an id provided by the bank use that one. If not, generate an ID by combining invariant attributes.
4. If that id is already in `snapshot_keys`, we add a `"+"` to the end of it until it is unique again. This ensures that all movements in a snapshot are valid.
5. Now add or update the movement.

Additionally, I must say that I have considered the newest movement description to be the one stored, so movements that have already been added will be changing if the description changes from one snapshot to another.

