import logging
import click
import dotenv
from . import email as em
from . import bigquery
from . import edge_web
from . import user as us
from . import plan as p

dotenv.load_dotenv()

LOGGER = logging.getLogger(__name__)


@click.group()
@click.option("-v", "--verbose", is_flag=True)
def main(verbose: bool):
    logging.basicConfig(format="%(levelname)s:%(asctime)s:%(name)s:%(message)s")
    logging.getLogger(__name__).setLevel(logging.DEBUG if verbose else logging.INFO)


@main.group()
def email():
    pass


@email.command("raw")
@click.argument("output")
def fetch_email_raw_events(output: str):
    """ """
    client = bigquery.create_client()
    em.fetch_raw_events(client, output)


@email.command("format")
@click.argument("input")
@click.argument("output")
def format_raw_events(input: str, output: str):
    """ """
    em.format_raw_events(input, output)


@email.command("open")
@click.argument("events_file")
@click.argument("users_file")
@click.argument("plan_file")
@click.argument("output")
def email_open(events_file: str, users_file: str, plan_file: str, output: str):
    plans = p.create_plan(plan_file)
    em.filter_email_open_events(events_file, users_file, plans, output)


@main.group()
def web():
    pass


@web.command("raw")
@click.argument("output")
def fetch_raw_requests(output: str):
    client = bigquery.create_client()
    edge_web.fetch_raw_events(client, output)


@main.group()
def user():
    pass


@user.command("master")
@click.argument("user")
@click.argument("user_plan")
@click.argument("plan_history")
@click.argument("output")
def user_master(user: str, user_plan: str, plan_history: str, output: str):
    us.user_master(user, user_plan, plan_history, output)
