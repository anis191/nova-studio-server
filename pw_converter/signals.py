# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.db import transaction
# from .models import Document

# @receiver(post_save, sender=Document)
# def cleanup_temp_files(sender, instance, created, **kwargs):
#     if not created:
#         return

#     # Define cleanup function
#     def cleanup():
#         if instance.pdf:
#             instance.pdf.delete(save=False)
#         if instance.word:
#             instance.word.delete(save=False)
#         instance.delete()
#         print("Deleted")

#     # Schedule cleanup after DB commit
#     transaction.on_commit(cleanup)
