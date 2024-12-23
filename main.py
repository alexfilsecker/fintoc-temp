from utils import get_companies_snapshots, get_snapshots, get_snapshot_data
from bank_statement import BankStatement

OUTPUT_PATH = "results_movements"

snapshots = get_snapshots()
companies_snapshots = get_companies_snapshots(snapshots)

for company, company_snapshots in companies_snapshots.items():
  bank_statement = BankStatement(company)
  for snapshot in company_snapshots:
    snapshot_data = get_snapshot_data(snapshot)
    bank_statement.update(snapshot_data)

  print(f"empresa {company}")
  bank_statement.show_movements()
  bank_statement.export_movements(OUTPUT_PATH)
  print()
