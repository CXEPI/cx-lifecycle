import base64

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn
import requests
from cli.config import CONFIG_FILE, PLATFORM_SERVICES, IAM_BASE_URL, ENVIRONMENTS
from cli.helpers.api_client import APIClient
from cli.helpers.errors import handle_request_error
from cli.helpers.file import load_config, save_config


def create_application(api, config):
    """
    Create a new application in IAM and return application details.
    """
    typer.secho("🚀 Starting Create Application...", fg=typer.colors.BRIGHT_MAGENTA)
    create_application_url = "/cxp-iam/api/v1/applications"

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("Creating application...", start=True)

        try:
            application_metadata = config.get("application", {})
            application_name = (
                application_metadata.get("display_name")
                .strip()
                .lower()
                .replace(" ", "-")
            )
            response = api.post(
                create_application_url,
                json={
                    "name": application_name,
                    "displayName": application_metadata.get("display_name"),
                    "description": application_metadata.get("description"),
                    "contact": application_metadata.get("lead_developer_email"),
                    "version": application_metadata.get("app_version"),
                    "git": application_metadata.get("github_url"),
                },
                timeout=10,
            )
            response.raise_for_status()
            typer.secho("✅ Application created successfully!")
            return response.json()

        except requests.exceptions.RequestException as error:
            typer.secho("❌ Failed to create application.", fg=typer.colors.RED)
            handle_request_error(error)
            raise typer.Exit(code=1)


def assign_roles(api, application_details):
    """
    Assign roles for platform services to the application.
    """
    client_id = application_details.get("clientId")
    assign_roles_url = f"/cxp-iam/api/v1/tenants/users/{client_id}/assignRoles"
    typer.secho(
        f"🔑 Assigning Roles for Platform services {', '.join(service['name'] for service in PLATFORM_SERVICES)}...",
        fg=typer.colors.CYAN,
    )
    for service in PLATFORM_SERVICES:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task = progress.add_task(
                f"Assigning Roles for Platform service {service['name']}...", start=True
            )

            try:
                response = api.post(
                    assign_roles_url,
                    json=[{"id": service["role_id"], "name": service["role_name"]}],
                    timeout=10,
                )
                response.raise_for_status()
                typer.secho(f"✅ Assigned role for {service['name']} successfully!")

            except requests.exceptions.RequestException as error:
                progress.update(task, description=f"❌ Failed to assign role.")
                handle_request_error(error)
                raise typer.Exit(code=1)


def generate_service_credentials(application_details):
    """
    Generate and display service credentials for the application.
    """
    credentials_raw = (
        f"{application_details.get('clientId')}:{application_details.get('secret')}"
    )
    credentials = base64.b64encode(credentials_raw.encode("utf-8")).decode("utf-8")
    typer.secho(
        f"🔒 Your Service account secret is: {credentials}", fg=typer.colors.GREEN
    )
    typer.secho("⚠️ The secret will be shown only once.", fg=typer.colors.BRIGHT_YELLOW)


def register(
    env: str = typer.Argument(
        ...,
        help=f"Environment (one of: {', '.join(ENVIRONMENTS)})",
        show_default=False,
        case_sensitive=False,
    )
):
    """
    Register the app in IAM and return service credentials.
    """
    if env not in ENVIRONMENTS:
        typer.secho(
            f"Error: env must be one of: {', '.join(ENVIRONMENTS)}",
            fg=typer.colors.RED,
            bold=True,
        )
        raise typer.Exit(code=1)
    typer.secho("📦 Registering a new application...", fg=typer.colors.BRIGHT_BLUE)
    config = load_config()
    api = APIClient(base_url=IAM_BASE_URL[env], env=env)
    print("base url:", api.base_url)
    print("env: ", api.env)
    application_details = create_application(api, config)

    config["application"][f"application_uid_{env}"] = application_details.get("id")
    save_config(config)
    typer.secho(
        f"📄 Updated application_uid in config file: {CONFIG_FILE}",
        fg=typer.colors.GREEN,
    )

    assign_roles(api, application_details)
    generate_service_credentials(application_details)
