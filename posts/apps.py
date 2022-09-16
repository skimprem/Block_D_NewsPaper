from django.apps import AppConfig


class PostsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'posts'
    
    def ready(self):
        import posts.signals

        # from .tasks import send_mails
        # from .scheduler import subscribe_scheduler
        # print('started')

        # subscribe_scheduler.add_job(
        #     id='mail send',
        #     func=send_mails,
        #     trigger='interval',
        #     seconds=10,
        # )
        # subscribe_scheduler.start()