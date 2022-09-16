from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import UsersSubscriptions
from posts.models import Post, Category
from django.db.models.signals import post_save

class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_not_author"] = not self.request.user.groups.filter(name='authors').exists()
        return context

@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/account/')

@login_required
def subscribe_me(request):
    category_id = request.GET.get('category_id')
    try:
        subscription = UsersSubscriptions.objects.get(
            user=request.user,
            category=Category.objects.get(pk=category_id)
            )
    except UsersSubscriptions.DoesNotExist:
        subscription = UsersSubscriptions.objects.create(
            user = request.user,
            category = Category.objects.get(pk = category_id)
            )
    return redirect(request.GET.get('path_info'))