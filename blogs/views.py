from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import SignUpForm,ProfileForm,UserUpdateForm,ProfileUpdateForm
from .import models
from django.views.generic import CreateView,DeleteView,DetailView,ListView,UpdateView
from .models import Article
from django.core.paginator import Paginator

# Create your views here.


#homepage
class IndexView(ListView):
    context_object_name = 'article'
    model = models.Article
    template_name = 'blogs/index.html'
    paginate_by = 4


#register new user
def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            pro_form =ProfileForm(request.POST, request.FILES)
            if form.is_valid() and pro_form.is_valid():
               user= form.save()
               pf=pro_form.save(commit=False)
               pf.user=user
               pro_form.full_clean()
               pf.save()
               login(request, user)
               messages.success(request, 'your account is created successfully')
               return redirect('/')

        else:
            form = SignUpForm()
            pro_form = ProfileForm()
        return render(request, 'blogs/signup.html', {'form': form,'profile_form':pro_form})

    else:
        return redirect('/')

#logout current user
@login_required
def user_logout(request):
    logout(request)
    return redirect('/')


#create new post
class ArticleCreateView(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    fields = ('title','details','title_image')
    model = models.Article
    success_url = reverse_lazy("blogs:index")
    success_message = "Article was Created successfully"
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



#post update
class ArticleUpdateView(LoginRequiredMixin,UserPassesTestMixin,SuccessMessageMixin,UpdateView):
    fields = ('title', 'details','title_image')
    model = models.Article
    success_message = "Article was Updated successfully"

    def get_success_url(self):
        return reverse("blogs:user_profile", args=[self.object.user.id])



    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        else:
            return False

#post delete
class ArticleDeleteView(LoginRequiredMixin,UserPassesTestMixin,SuccessMessageMixin,DeleteView):
    model = models.Article
    success_message = "Article was deleted successfully"

    def get_success_url(self):
        return reverse("blogs:user_profile", args=[self.object.user.id])


    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        else:
            return False



#full post
class ArticleDetailView(DetailView):
    context_object_name = 'article_detail'
    model = models.Article
    template_name = 'blogs/detail.html'

#get total likes and unlike like logic
    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)

        like_unlike =  get_object_or_404(Article, id=self.kwargs['pk'])
        total_likes =  like_unlike.total_likes()

        is_like = False
        if like_unlike.likes.filter(id=self.request.user.id).exists():
            is_like = True
        context['is_like'] = is_like
        context['total_likes'] = total_likes
        return context


#get all details and post  of a particuler user
class UserProfileDetailView(DetailView):
    context_object_name = 'user_profile'
    model = models.User
    template_name = 'blogs/user_profile.html'
    def get_context_data(self, **kwargs):
        context = super(UserProfileDetailView, self).get_context_data(**kwargs)
        context['article_list'] = Article.objects.all()
        return context



#account update
@login_required()
def user_profile_Update(request):

    if request.method == 'POST':
        uform = UserUpdateForm(request.POST,instance=request.user)
        pform =ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if uform.is_valid() and pform.is_valid():
           uform.save()
           pform.save()
           messages.success(request, 'your account is updated successfully')
           return HttpResponseRedirect(reverse('blogs:user_profile', args=[request.user.pk]))


    else:
        uform = UserUpdateForm(instance=request.user)
        pform = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'blogs/account_update.html', {'uform': uform,'pform':pform})

def search(request):
    if request.method == 'POST':
        srch = request.POST['srch']
        if srch:
            find = User.objects.filter(Q(username__istartswith=srch)| Q(first_name__istartswith=srch))
            if find:
                #messages.success(request, f'{find}')
                match={'match':find}
                return render(request,'blogs/search.html',match)
            else:
                messages.error(request,'Not found')
                return render(request, 'blogs/search.html')
        else:
            return render(request, 'blogs/search.html')

    else:
        return render(request,'blogs/search.html')


#function for like and unlike button
@login_required()
def post_like(request):
    like = get_object_or_404(Article, id=request.POST.get('like'))

    is_like = False
    if like.likes.filter(id=request.user.id).exists():
        like.likes.remove(request.user)
        is_like = False
    else:
        like.likes.add(request.user)
        is_like = True

    pk = request.POST.get('like')
    return HttpResponseRedirect(reverse('blogs:detail', args=[pk]))

#function for list of all likes of a user on a article
def like_list(request, pk):
    like = get_object_or_404(Article, id=pk).likes.all()
    print(like[0])

    return render(request,'blogs/like_list.html',{'like':like})
