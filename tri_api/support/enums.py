import os
from enum import Enum
from pathlib import Path
from datetime import date, timedelta


USER_AGENTS = [
    # Windows User Agents
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.102 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:113.0) Gecko/20100101 Firefox/113.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; AppleWebKit/537.36; KHTML, like Gecko) Edge/18.19041 Safari/537.36",
    # macOS User Agents
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.102 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.98 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",
    # Linux User Agents
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.102 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/605.1.15 (KHTML, like Gecko) Chrome/114.0.5735.133 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36",
    # Android User Agents
    "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.110 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-A536B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.92 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.125 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.127 Mobile Safari/537.36",
    # iOS User Agents
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPod touch; CPU iPhone OS 14_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.7 Mobile/15E148 Safari/604.1",
]


class ResponseCode(Enum):
    success = 200
    created = 201
    accepted = 202
    no_content = 204
    bad_request = 400
    unauthorized = 401
    forbidden = 403
    not_found = 404
    method_not_allowed = 405
    conflict = 409
    unprocessable_entity = 422
    internal_server_error = 500
    not_implemented = 501
    bad_gateway = 502
    service_unavailable = 503


class ScannerType(Enum):
    attack_surface_analysis = "asa"
    attack_surface_discovery = "asd"
    secret_exposure_analysis = "sea"
    attack_surface_management = "asm"
    software_bill_of_materials = "sbom"
    software_composition_analysis = "sca"
    cloud_security_posture_management = "cspm"
    static_application_security_testing = "sast"
    dynamic_application_security_testing = "dast"


class ScannerStatus(Enum):
    failed = "failed"
    aborted = "aborted"
    completed = "completed"
    scheduled = "scheduled"
    in_progress = "in_progress"


class TargetType(Enum):
    ip = "ip"
    url = "url"
    cidr = "cidr"
    cloud = "cloud"
    domain = "domain"
    repository = "repository"
    container_image = "container_image"


class ScannerExceptionMessage(Enum):
    incorrect_input = "Irregular input detected for the scanner."


class RouteEnum(Enum):
    api = "/api"
    mail = "/mail"
    user = "/user"
    tasks = "/tasks"
    token = "/token"
    login = "/login"
    tenant = "/tenant"
    verify = "/verify"
    refresh = "/refresh"
    activate = "/activate"
    add_invite = "/invite"
    register = "/register"
    super_user = "/super-user"
    fetch_task = "/fetch-task"
    update_task = "/update-task"
    update_member = "/update-member"
    verify_token = "/verify/{token}"
    authorization = "/authorization"
    forgot_password = "/forgot-password"
    populate_database = "/populate-database"
    reset_password = "/reset-password/{token}"


class TroveRouteEnum(Enum):
    trove = "/trove"
    cve = "/cve/{cve_id}"
    cwe = "/cwe/{cwe_id}"
    capec = "/capec/{capec_id}"


class ScannerRouteEnum(Enum):
    scanner = "/scanner"
    attack_surface_analysis = "/asa"
    attack_surface_discovery = "/asd"
    secret_exposure_analysis = "/sea"
    attack_surface_management = "/asm"
    software_bill_of_materials = "/sbom"
    software_composition_analysis = "/sca"
    cloud_security_posture_management = "/cspm"
    static_application_security_testing = "/sast"
    dynamic_application_security_testing = "/dast"


class ExceptionMessage(Enum):
    bad_request = "Bad request."
    not_a_member = "Not a member."
    item_not_found = "Item not found."
    task_id_needed = "Task ID is required."
    user_id_needed = "User ID is required."
    account_disabled = "Account is disabled."
    unconfirmed_email = "Email is not verified."
    email_already_exists = "Email already exists."
    invalid_invite_token = "Invalid invite token."
    user_not_found = "User not found with this email."
    auth_user_not_found = "Authorized user not found."
    account_already_active = "Account is already active."
    email_already_verified = "Email is already verified."
    invalid_credentials = "Invalid username or password."
    user_not_found_by_id = "User not found with this ID."
    task_not_found_by_id = "Task not found with this ID."
    undefined_state_choice = "Invalid user state choice."
    super_user_exception = "Missing appropriate credentials."
    no_auth_cred_found = "No authorization credentials found."
    user_already_exists = "User already exists with this email."


class Status(Enum):
    active = 1
    inactive = 0


class Access(Enum):
    access_expires = timedelta(minutes=15)
    refresh_expires = timedelta(days=30)


class APIenum(Enum):
    title = "My Server"
    description = """
This API powers whatever I want to make

It supports:

- Account sign-up and management
- Something really cool that will blow your socks off
"""
    contact = {
        "name": "My Server",
        "url": "https://myserver.dev",
        "email": "helloworld@myserver.dev",
    }
    env_file_path = Path(os.getenv("ENV_FILE_PATH", "/usr/src/app/dev.env"))


class MailEnum(Enum):
    verify_endpoint = "/mail/verify/"
    reset_endpoint = "/register/reset-password/"
    verify_subject = "MyServer Email Verification"
    reset_subject = "MyServer Password Reset"
    verify_body = (
        "Welcome to MyServer! We just need to verify your email to begin: {url}"
    )
    reset_body = "Click the link to reset your MyServer account password: {url}\nIf you did not request this, please ignore this email"


class MongoOption(Enum):
    port = int(os.getenv("MONGO_PORT", 27017))
    username = os.getenv("MONGO_INITDB_ROOT_USERNAME", "root")
    password = os.getenv("MONGO_INITDB_ROOT_PASSWORD", "example")
    host = os.getenv("MONGO_HOST", "mongodb")


class RabbitMQOption(Enum):
    port = os.getenv("RABBITMQ_PORT", 5672)
    schema = os.getenv("RABBITMQ_SCHEMA", "amqp")
    host = os.getenv("RABBITMQ_HOST", "rabbitmq")
    vhost = os.getenv("RABBITMQ_DEFAULT_VHOST", "/")
    password = os.getenv("RABBITMQ_DEFAULT_PASS", "example")
    username = os.getenv("RABBITMQ_DEFAULT_USER", "guest")


class AWSOption(Enum):
    file = str(date.today())
    download_dir = "/usr/src/app/temporary/"
    region = os.getenv("AWS_REGION", "us-east-1")
    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    s3_bucket = os.getenv("AWS_S3_BUCKET", "tri-db")
    cve_file = f"cve_trove_output_{str(date.today())}_.jsonl"
    cwe_file = f"cwe_trove_output_{str(date.today())}_.jsonl"
