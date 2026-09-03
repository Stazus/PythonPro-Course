from django.http import JsonResponse

from .tasks import process_task


def create_task(request):
    message = request.GET.get("message", "Przykładowe zadanie")

    task = process_task.delay(message)

    return JsonResponse(
        {
            "status": "Zadanie przekazane do Celery",
            "task_id": task.id,
            "message": message,
        }
    )
