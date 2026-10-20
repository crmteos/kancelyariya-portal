import subprocess
import sys

def run_command(command):
    print(f"🚀 Виконується: {command}")
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='ignore')
    
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
            
    rc = process.poll()
    return rc

def deploy():
    project_id = "ukrainian-empire-portal"
    image_name = "gcr.io/ukrainian-empire-portal/imperial-portal-image"
    service_name = "imperial-portal"
    region = "us-central1"

    print("==================================================")
    print("👑 ПОЧАТОК ДЕПЛОЮ МЕДІЙНОГО ПОРТАЛУ УКРАЇНСЬКОЇ ІМПЕРІЇ")
    print("==================================================")

    # Крок 1: Встановлення активного проекту GCP
    print("\n👉 Налаштування проекту GCP...")
    if run_command(f"gcloud config set project {project_id}") != 0:
        print("❌ Помилка при виборі проекту GCP.")
        sys.exit(1)

    # Крок 2: Збирання образу та деплой через Cloud Build
    print("\n👉 Надсилання коду в Google Cloud Build...")
    deploy_cmd = (
        f"gcloud run deploy {service_name} "
        f"--source . "
        f"--region {region} "
        f"--platform managed "
        f"--allow-unauthenticated"
    )
    
    if run_command(deploy_cmd) == 0:
        print("\n==================================================")
        print("🎉 ДЕПЛОЙ УСПІШНО ЗАВЕРШЕНО!")
        print("👑 Оновлений портал та Адмін-Консоль уже в ефірі!")
        print("🔗 Адреса консолі: https://imperial-portal-210914528327.us-central1.run.app/admin")
        print("==================================================")
    else:
        print("\n❌ Помилка під час деплою. Перевірте статус Cloud Build та права доступу.")

if __name__ == "__main__":
    deploy()