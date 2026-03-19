from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Sum
from munro_app.models import Munro, ClimbRecord, Photo, UserProfile, UserFavouriteMunro
from munro_app.forms import UserForm, UserProfileForm, UserEditForm, ClimbRecordForm
from django.conf import settings

def index(request):
    # print("INDEX DB ENGINE:", settings.DATABASES['default'].get('ENGINE'))
    top_munros = Munro.objects.order_by('-height')[:15]
    latest_climb = None
    latest_climb_photos = []
    
    if request.user.is_authenticated:
        latest_climb = ClimbRecord.objects.filter(user=request.user).order_by('-climb_date', '-created_at').first()
        if latest_climb:
            latest_climb_photos = latest_climb.photos.all()

    search_query = request.GET.get('search', '')
    if search_query:
        # Simple search for now, could redirect to list view
        return redirect(f'/munros/?search={search_query}')

    context = {
        'top_munros': top_munros,
        'latest_climb': latest_climb,
        'latest_climb_photos': latest_climb_photos,
    }

    print(top_munros)
    for m in top_munros:
        print(m.name, m.height)

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

    return render(request, 'registration/register_form.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def user_login(request):
    # print("DB ENGINE:", settings.DATABASES['default'].get('ENGINE'))
    # print("DB NAME:", settings.DATABASES['default'].get('NAME'))
    # print("DB HOST:", settings.DATABASES['default'].get('HOST'))
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('munro_app:index')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

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
    # Order by climb_date descending, then by created_at descending to ensure the most recently added records appear first
    climbs = ClimbRecord.objects.filter(user=user).order_by('-climb_date', '-created_at')
    total_climbed = climbs.count()
    total_distance = climbs.aggregate(Sum('total_distance'))['total_distance__sum'] or 0
    
    # We must evaluate the queryset to a list to properly slice it and avoid issues with re-evaluating querysets after changes
    climbs_list = list(climbs)
    latest_climb = climbs_list[0] if climbs_list else None
    previously_hiked = climbs_list[1:] if len(climbs_list) > 1 else []
    
    # Get favourite munro
    try:
        fav_munro = UserFavouriteMunro.objects.get(user=user).munro
    except UserFavouriteMunro.DoesNotExist:
        fav_munro = None
    
    climb_modal_open = False
    
    # Forms for editing
    if request.method == 'POST' and 'profile_submit' in request.POST:
        user_form = UserEditForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        climb_form = ClimbRecordForm()
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('munro_app:user_profile')
    elif request.method == 'POST' and 'climb_submit' in request.POST:
        user_form = UserEditForm(instance=user)
        profile_form = UserProfileForm(instance=profile)
        climb_form = ClimbRecordForm(request.POST, request.FILES)
        
        if climb_form.is_valid():
            climb = climb_form.save(commit=False)
            climb.user = request.user
            
            # Convert hr and min to total hours
            hr = climb_form.cleaned_data.get('time_hr', 0)
            min = climb_form.cleaned_data.get('time_min', 0)
            climb.completion_time_hours = (hr or 0) + ((min or 0) / 60.0)
            
            climb.save()
            
            # Handle photos
            photos = request.FILES.getlist('photos')
            for photo_file in photos:
                Photo.objects.create(record=climb, image=photo_file)
                
            # Handle favourite
            is_favourite = climb_form.cleaned_data.get('is_favourite')
            if is_favourite == 'yes':
                UserFavouriteMunro.objects.update_or_create(
                    user=request.user,
                    defaults={'munro': climb.munro}
                )
                
            messages.success(request, "Climb added successfully!")
            return redirect('munro_app:user_profile')
        else:
            # If the form is invalid, we don't redirect so we can show errors
            climb_modal_open = True
            print("Form errors:", climb_form.errors)
    else:
        user_form = UserEditForm(instance=user)
        profile_form = UserProfileForm(instance=profile)
        climb_form = ClimbRecordForm()

    # Re-evaluate stats after potential POST save to ensure fresh data is shown if we didn't redirect
    climbs = ClimbRecord.objects.filter(user=user).order_by('-climb_date', '-created_at')
    total_climbed = climbs.count()
    total_distance = climbs.aggregate(Sum('total_distance'))['total_distance__sum'] or 0
    climbs_list = list(climbs)
    latest_climb = climbs_list[0] if climbs_list else None
    previously_hiked = climbs_list[1:] if len(climbs_list) > 1 else []

    # Refresh favourite munro in case it changed
    try:
        fav_munro = UserFavouriteMunro.objects.get(user=user).munro
    except UserFavouriteMunro.DoesNotExist:
        fav_munro = None

    context = {
        'profile': profile,
        'climbs': climbs,
        'total_climbed': total_climbed,
        'total_distance': total_distance,
        'fav_munro': fav_munro,
        'latest_climb': latest_climb,
        'previously_hiked': previously_hiked,
        'user_form': user_form,
        'profile_form': profile_form,
        'form': climb_form,
        'climb_modal_open': climb_modal_open
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

    return render(request, 'munro/user_profile.html', {'form': form})

def munro_list(request):
    munros = Munro.objects.all().order_by('region', 'name')
    search_query = request.GET.get('search')
    region_filter = request.GET.get('region')
    
    if search_query:
        munros = munros.filter(name__icontains=search_query)
    
    if region_filter:
        munros = munros.filter(region=region_filter)
        
    regions = Munro.objects.values_list('region', flat=True).distinct().order_by('region')

    climbed_ids = set()
    if request.user.is_authenticated:
        climbed_ids = set(
            ClimbRecord.objects.filter(user=request.user).values_list('munro_id',flat=True)
        )

    return render(request, 'munro/munro_list.html', {
        'munros': munros,
        'regions': regions,
        'search_query': search_query,
        'region_filter': region_filter,
        'climbed_ids': climbed_ids,
    })

@login_required
def climb_detail(request, climb_id):
    climb = get_object_or_404(ClimbRecord, id=climb_id, user=request.user)
    return render(request, 'munro/climb_detail.html', {'climb': climb})

def munro_detail(request, munro_id):
    munro = get_object_or_404(Munro, id=munro_id)
    is_completed = False
    if request.user.is_authenticated:
        is_completed = ClimbRecord.objects.filter(user=request.user, munro=munro).exists()
        
    return render(request, 'munro/munro_detail.html', {
        'munro': munro,
        'is_completed': is_completed
    })