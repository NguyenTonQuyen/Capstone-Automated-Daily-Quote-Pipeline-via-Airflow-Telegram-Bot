# file name: welcome_dag.py

## Ver 3
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta
import pendulum
import requests

# --- Def Python ---
def print_welcome():
    print("Welcome to Airflow!")

def print_date():
    print("Today is {}".format(datetime.today().date()))

def print_random_quote():
    url = "https://zenquotes.io/api/random"
    try:
        response = requests.get(url, timeout=10, verify=True)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                quote = data[0].get("q")
                author = data[0].get("a")
                result = f'"{quote}" — {author}'
                print(f"Quote of the day: {result}")
                return result  # Save result in Xcom
            else:
                print("Wrong API Format.")
        else:
            print(f"Failed status code: {response.status_code}")
    except Exception as e:
        print(f"Error fetching quote: {e}")
        raise 

def send_to_telegram(ti):
    # 1. Fetch data from the previous step
    quote_content = ti.xcom_pull(task_ids='print_random_quote')
    
    # 2. Change the information of your bot
    token = "814xxxxxxxx:AAFWhvZa6Wxxxxxxx"  # Change your token telegram here
    chat_id = "871xxxxx" # change your chat id from telegram
    
    if not quote_content:
        print("Nothing to send!")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": f"🌟 *Daily Inspiration* 🌟\n\n{quote_content}",
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print("Send your quote completely!")
        else:
            print(f"Error Telegram: {response.text}")
    except Exception as e:
        print(f"Error connection to Telegram: {e}")

# --- Def DAG ---
local_tz = pendulum.timezone("Asia/Ho_Chi_Minh")

with DAG(
    dag_id="welcome_dag",
    start_date=datetime(2026, 1, 2, tzinfo=local_tz),
    schedule="0 23 * * *",
    catchup=False,
    tags=["example"],
    default_args={
        'retries': 2,
        'retry_delay': timedelta(minutes=5),
    }
) as dag:

    # --- Tasks ---
    print_welcome_task = PythonOperator(
        task_id="print_welcome",
        python_callable=print_welcome,
    )

    print_date_task = PythonOperator(
        task_id="print_date",
        python_callable=print_date,
    )

    print_random_quote_task = PythonOperator(
        task_id="print_random_quote",
        python_callable=print_random_quote,
    )

    send_telegram_task = PythonOperator(
        task_id="send_to_telegram",
        python_callable=send_to_telegram,
    )

    # --- Dependencies ---
    print_welcome_task >> print_date_task >> print_random_quote_task >> send_telegram_task