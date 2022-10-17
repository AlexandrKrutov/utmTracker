import datetime

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render

from .models import UserName, UserProjects, ProjectsUTM, UTMTracker

# https://vk.com/alalkrutov
"""  

UTM tags is a specialized tool for convenient targeting. In fact, this is a GET request.
It looks like basic GET request: https://some_site.ru/?utm_source=url&utm_campaign=some_name&...

Utm_source is the main tag. It should contain the URL where lead is going to be redirected to.
https://some_site.ru/?utm_source=https://tg.me/SomeTgBot <-- this the the url to redirect

Other tags need only for get some necessary/unnecessary statistic.

"""
def utm_check(request):
    request_get = request.GET
    utm_source = request_get.get('utm_source')
    utm_medium = request_get.get('utm_medium')
    utm_campaign = request_get.get('utm_campaign')

    """ check if there are utm tags """
    if utm_source is not None and utm_medium is not None and utm_campaign is not None:  # if it`s tag

        tracker = UTMTracker()
        tracker.utm_campaign = ProjectsUTM.objects.get(utm_campaign=utm_campaign)
        tracker.date_time = datetime.datetime.now()
        tracker.save()  # save

        return HttpResponseRedirect(utm_source)  # redirect to needed url

    else:  # if it`s not, so it`s a user
        request.session['main_url'] = request.build_absolute_uri()
        return render(request, 'index.html')

def miniUserAuth(request):
    """ something like auth """
    if request.method == 'POST':
        username = UserName()
        username.user_name = request.POST.get('user_name')
        request.session['user_name'] = username.user_name
        if username.user_name != '':
            try:
                username.save()
                return HttpResponseRedirect('/user/projects')
            except:
                return HttpResponseRedirect('/user/projects')
        else:
            return render(request, 'create_user.html', {'error_message': 'Придумайте username'})
    else:
        return render(request, 'create_user.html', {'error_message': ''})

def createProject(request):
    """ Projects creation """
    username = request.session['user_name']
    # table of user projects
    user_projects = UserProjects.objects.filter(user_name=UserName.objects.get(user_name=username).id)
    # saved url of 'user/projects/' page (it needs in order to return from the page that is further away)
    request.session['back_to_projects_url'] = request.build_absolute_uri()

    if request.method == 'POST' and request.POST.get('project_name') != '':
        project_name = UserProjects()
        project_name.project_name = request.POST.get('project_name')
        project_name.user_name = UserName.objects.get(user_name=request.session['user_name'])
        project_name.save()

        return render(request, 'user_projects.html', {'user_name': username, 'user_projects': user_projects})

    return render(request, 'user_projects.html', {'user_name': username, 'user_projects': user_projects})

def deleteProject(request, id):
    """ deleting user projects """
    try:
        project_name = UserProjects.objects.get(id=id)
        project_name.delete()
        return HttpResponseRedirect('/user/projects')
    except UserProjects.DoesNotExist:
        return HttpResponseNotFound('<h2>Project not found</h2>')

def setUpProject(request, id):
    """ setting up the user project utm tags """
    if request.method == 'POST':

        if request.POST.get('utm_campaign') != '' and request.POST.get('utm_source') != '' and request.POST.get('utm_medium') != '':
            try:
                project_utm = ProjectsUTM()
                project_utm.project_name = UserProjects.objects.get(id=id)
                project_utm.utm_campaign = request.POST.get('utm_campaign')
                project_utm.utm_source = request.POST.get('utm_source')
                project_utm.utm_medium = request.POST.get('utm_medium')

                project_utm.utm_content = request.POST.get('utm_content')
                project_utm.utm_term = request.POST.get('utm_term')

                utm_content = f'&utm_content={project_utm.utm_content}' if project_utm.utm_content != '' else ''
                utm_term = f'&utm_term={project_utm.utm_term}' if project_utm.utm_term != '' else ''
                utm_link = f"""?utm_source={project_utm.utm_source}&utm_medium={project_utm.utm_medium}&utm_campaign={project_utm.utm_campaign}{utm_content}{utm_term}"""
                project_utm.utm_url = request.session['main_url'] + utm_link

                project_utm.save()
            except:
                pass

    # getting all utm tags related to a specific project
    project_utms = ProjectsUTM.objects.filter(project_name=UserProjects.objects.get(id=id))
    project_utms_track = dict()
    for i in range(len(project_utms)):
        try:  # if there is at least 1 tag, get it
            utm_track = UTMTracker.objects.filter(utm_campaign=ProjectsUTM.objects.get(utm_campaign=project_utms[i].utm_campaign))
        except:  # if not, so just make an empty list
            utm_track = list()
        project_utms_track[project_utms[i]] = len(utm_track)  # dict: {utm_tag_info : list length, ...}

    return render(request, 'setup_project.html',
                  {'project_utms_track': project_utms_track, 'back_url': request.session['back_to_projects_url']})

def deleteUTM(request, id, utm_campaign):
    """ deleting utm tag """
    try:
        utm = ProjectsUTM.objects.get(utm_campaign=utm_campaign)
        utm.delete()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    except ProjectsUTM.DoesNotExist:
        return HttpResponseNotFound('<h2>UTM not found</h2>')