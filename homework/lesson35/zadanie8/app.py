import os


def check_aws_environment_variables():
    aws_variables = [
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "AWS_DEFAULT_REGION",
    ]

    for variable in aws_variables:
        if os.environ.get(variable):
            print(f"{variable}: ustawiona")
        else:
            print(f"OSTRZEŻENIE: zmienna {variable} nie jest ustawiona")


if __name__ == "__main__":
    check_aws_environment_variables()
