import datapane as dp
from prefect import flow, task
from prefect_shell import shell_run_command
from prefect.blocks.system import Secret


@task
def get_dp_token():
    secret_block = Secret.load("datapane-token")

    # Access the stored secret
    return secret_block.get()


@flow
def login_into_datapane():
    token = get_dp_token()
    return shell_run_command(f"datapane login --token {token}")


# @task
# def task_upload_report(report_elements: list, keyword: str):
#     dp.Report(*report_elements).upload(
#         name=f"{keyword.title()} Report", publicly_visible=False
#     )


@task
def task_upload_report(report_elements: list, keyword: str):
    print("report_elements: ", *report_elements)
    print("name: ", f"{keyword.title()} Report")
    dp.upload_report(
        *report_elements, name=f"{keyword.title()} Report", publicly_visible=False
    )


@flow(name="Create a Report")
def create_report(report_elements: list, keyword: str):
    login_into_datapane()
    task_upload_report(report_elements, keyword)
