import datetime
from actual import Actual
from actual.queries import get_transactions
from box.utils.yaml.utils import load_config
from typing import Any
from pytz import timezone
from pydantic import BaseModel
from box.utils.email.utils import send_email

class Transaction(BaseModel):
    amount: float | None
    payee: str | None

class TodayTransactions(BaseModel):
    transactions: list[Transaction]
    total: float 


def load_actual_config() -> dict[str, Any]:
    return load_config("actual")

def get_current_date() -> int:
    cst = timezone('America/Chicago')
    return int(datetime.datetime.now(cst).strftime("%Y%m%d")) - 1

def tally_transactions(transactions: list[Transaction]) -> float:
    total = sum(t.amount for t in transactions if t.amount is not None)
    return float(f"{total:.2f}")

def get_today_transactions() -> TodayTransactions:
    config = load_actual_config()
    current_date = get_current_date()
    new_transactions: list[Transaction] = []

    with Actual(
            base_url=config["url"],
            password=config["password"],
            file=config["sync_id"],
    ) as actual:
        transactions = get_transactions(actual.session)
        for t in transactions:
            if t.date == current_date and t.amount and t.amount < 0:
                new_transactions.append(Transaction(amount=t.amount / 100 if t.amount else None, payee=t.payee.name if t.payee else None))

    return TodayTransactions(transactions=new_transactions, total=tally_transactions(new_transactions))


def email_todays_transactions(transactions: TodayTransactions) -> None:
    transaction_html = ""
    for t in transactions.transactions:
        transaction_html += f"<tr><td>{t.payee}</td><td>{t.amount:.2f}</td></tr>"

    html = f"""
    <html>
        <body>
            <h1>Today's Transactions: {transactions.total:.2f}</h1>
            <table>
                <tr>
                    <th>Payee</th>
                    <th>Amount</th>
                </tr>
                {transaction_html}
            </table>
        </body>
    </html>
    """

    send_email("jaydenpyles0524@gmail.com", "Today's Transactions", html, is_html=True)

def actual():
    transactions = get_today_transactions()
    email_todays_transactions(transactions)


