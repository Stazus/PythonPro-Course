import subprocess
import sys
import time

import requests


REPOSITORY_URL = "git@github.com:Stazus/PythonPro-Course.git"
PROJECT_DIR = "deploy_project"

ECR_REPOSITORY = "lesson35-app"
AWS_REGION = "eu-central-1"

EC2_HOST = "EC2_PUBLIC_IP"
EC2_USER = "ubuntu"
SSH_KEY = "key.pem"

HEALTHCHECK_URL = "http://EC2_PUBLIC_IP:8000/"


def run_command(command, cwd=None):
    print(f"\nUruchamiam: {' '.join(command)}")
    result = subprocess.run(command, cwd=cwd)

    if result.returncode != 0:
        raise RuntimeError(
            f"Polecenie zakończyło się błędem: {' '.join(command)}"
        )


def clone_or_pull_repository():
    try:
        run_command(["git", "clone", REPOSITORY_URL, PROJECT_DIR])
    except RuntimeError:
        print("Repozytorium już istnieje - wykonuję git pull.")
        run_command(["git", "pull"], cwd=PROJECT_DIR)


def run_tests():
    run_command(
        [sys.executable, "-m", "pytest"],
        cwd=PROJECT_DIR,
    )


def build_docker_image():
    run_command(
        ["docker", "build", "-t", "lesson35-app:latest", "."],
        cwd=PROJECT_DIR,
    )


def push_to_ecr():
    account_id = subprocess.check_output(
        [
            "aws",
            "sts",
            "get-caller-identity",
            "--query",
            "Account",
            "--output",
            "text",
        ],
        text=True,
    ).strip()

    ecr_url = (
        f"{account_id}.dkr.ecr.{AWS_REGION}.amazonaws.com/"
        f"{ECR_REPOSITORY}"
    )

    login_process = subprocess.Popen(
        [
            "aws",
            "ecr",
            "get-login-password",
            "--region",
            AWS_REGION,
        ],
        stdout=subprocess.PIPE,
    )

    subprocess.run(
        [
            "docker",
            "login",
            "--username",
            "AWS",
            "--password-stdin",
            f"{account_id}.dkr.ecr.{AWS_REGION}.amazonaws.com",
        ],
        stdin=login_process.stdout,
        check=True,
    )

    run_command(
        [
            "docker",
            "tag",
            "lesson35-app:latest",
            f"{ecr_url}:latest",
        ]
    )

    run_command(
        [
            "docker",
            "push",
            f"{ecr_url}:latest",
        ]
    )

    return ecr_url


def deploy_to_ec2(ecr_url):
    remote_command = (
        f"docker pull {ecr_url}:latest && "
        "docker stop lesson35-app || true && "
        "docker rm lesson35-app || true && "
        f"docker run -d --name lesson35-app -p 8000:8000 "
        f"{ecr_url}:latest"
    )

    run_command(
        [
            "ssh",
            "-i",
            SSH_KEY,
            f"{EC2_USER}@{EC2_HOST}",
            remote_command,
        ]
    )


def health_check():
    time.sleep(5)

    try:
        response = requests.get(
            HEALTHCHECK_URL,
            timeout=10,
        )
        return response.status_code == 200

    except requests.RequestException:
        return False


def rollback():
    print("Health check nieudany - wykonuję rollback.")

    remote_command = (
        "docker stop lesson35-app || true && "
        "docker rm lesson35-app || true"
    )

    run_command(
        [
            "ssh",
            "-i",
            SSH_KEY,
            f"{EC2_USER}@{EC2_HOST}",
            remote_command,
        ]
    )


def deployment_pipeline():
    clone_or_pull_repository()
    run_tests()
    build_docker_image()

    ecr_url = push_to_ecr()
    deploy_to_ec2(ecr_url)

    if health_check():
        print("Deployment zakończony sukcesem.")
    else:
        rollback()
        print("Deployment nieudany.")
        sys.exit(1)


if __name__ == "__main__":
    deployment_pipeline()
