from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Sum
from munro_app.models import Munro, ClimbRecord, Photo, UserProfile
from munro_app.forms import UserForm, UserProfileForm, UserEditForm, ClimbRecordForm

def index(request):
    top_munros = Munro.objects.order_by('-height')[:10]
    latest_climb = None
    
    if request.user.is_authenticated:
        latest_climb = ClimbRecord.objects.filter(user=request.user).order_by('-climb_date').first()
        
    search_query = request.GET.get('search', '')
    if search_query:
        # Simple search for now, could redirect to list view
        return redirect(f'/munros/?search={search_query}')

    context = {
        'top_munros': top_munros,
        'latest_climb': latest_climb,
    }
    return render(request, 'munro/index.html', context)

def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            login(request, user)
            return redirect('munro_app:index')
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'munro/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('munro_app:index')
    else:
        form = AuthenticationForm()
    return render(request, 'munro/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('munro_app:index')

@login_required
def user_profile(request):
    user = request.user
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)

    # Stats
    climbs = ClimbRecord.objects.filter(user=user).order_by('-climb_date')
    total_climbed = climbs.count()
    total_distance = climbs.aggregate(Sum('total_distance'))['total_distance__sum'] or 0
    latest_climb = climbs.first()
    
    # Forms for editing
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('munro_app:user_profile')
    else:
        user_form = UserEditForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    context = {
        'profile': profile,
        'climbs': climbs,
        'total_climbed': total_climbed,
        'total_distance': total_distance,
        'latest_climb': latest_climb,
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'munro/user_profile.html', context)

@login_required
def add_climb(request):
    munro_id = request.GET.get('munro_id')
    initial_data = {}
    if munro_id:
        munro = get_object_or_404(Munro, id=munro_id)
        initial_data['munro'] = munro

    if request.method == 'POST':
        form = ClimbRecordForm(request.POST, request.FILES)
        if form.is_valid():
            climb = form.save(commit=False)
            climb.user = request.user
            climb.save()
            
            # Handle photos
            photos = request.FILES.getlist('photos')
            for photo_file in photos:
                Photo.objects.create(record=climb, image=photo_file)
                
            messages.success(request, "Climb added successfully!")
            return redirect('munro_app:user_profile')
    else:
        form = ClimbRecordForm(initial=initial_data)

    return render(request, 'munro/add_climb.html', {'form': form})

def munro_list(request):
    munros = Munro.objects.all().order_by('name')
    search_query = request.GET.get('search')
    region_filter = request.GET.get('region')
    
    if search_query:
        munros = munros.filter(name__icontains=search_query)
    
    if region_filter:
        munros = munros.filter(region=region_filter)
        
    regions = Munro.objects.values_list('region', flat=True).distinct()

    return render(request, 'munro/munro_list.html', {
        'munros': munros,
        'regions': regions,
        'search_query': search_query
    })

def munro_detail(request, munro_id):
    munro = get_object_or_404(Munro, id=munro_id)
    is_completed = False
    if request.user.is_authenticated:
        is_completed = ClimbRecord.objects.filter(user=request.user, munro=munro).exists()
        
    return render(request, 'munro/munro_detail.html', {
        'munro': munro,
        'is_completed': is_completed
    })
