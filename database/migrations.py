import subprocess


def run_alembic_command(command):
    # Запустить команду Alembic
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        print(f"Ошибка при выполнении команды Alembic: {stderr.decode()}")
    else:
        print(stdout.decode())


def upgrade_database():
    # Применить последние миграции
    run_alembic_command(["alembic", "upgrade", "head"])
    print(["alembic", "upgrade", "head"])


def check_for_migrations():
    # Проверить наличие новых миграций
    run_alembic_command(["alembic", "revision", "--autogenerate"])
