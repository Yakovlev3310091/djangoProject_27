#from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count, Avg, Q, F
from django.http import JsonResponse
import json

from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from authentication.models import User
from djangoProject_27 import settings
from vacancies.models import Vacancy, Skill
from vacancies.permissions import VacancyCreatePermission
from vacancies.serializers import VacancyListSerializer, VacancyDetailSerializer, VacancyCreateSerializer, \
    VacancyUpdateSerializer, VacancyDestroySerializer, SkillSerializer


@extend_schema_view(
    list=extend_schema(
        description="Retrieve skill list",
        summary="Skill list",
    ),
    create=extend_schema(
       description="Create new skill object",
        summary="Create skill",
    ),
)
class SkillsViewSet(ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class VacancyListView(ListAPIView):
    #model = Vacancy
    queryset = Vacancy.objects.all()
    serializer_class = VacancyListSerializer

    @extend_schema(
        description="Retrieve vacancy list",
        summary="Vacancy list"
    )
    def get(self, request, *args, **kwargs):
        vacancy_text = request.GET.get('text', None)
        if vacancy_text:
            self.queryset = self.queryset.filter(text__icontains=vacancy_text)

        skills = request.GET.getlist('skill', None)
        skills_q = None

        for skill in skills:
            if skills_q is None:
                skills_q = Q(skills__name__icontains=skill)
            else:
                skills_q |= Q(skills__name__icontains=skill)

        if skills_q:
            self.queryset = self.queryset.filter(skills_q)

        return super().get(request, *args, **kwargs)


    # def get(self, request, *args, **kwargs):
    #     super().get(request, *args, **kwargs)
    #
    #     search_text = request.GET.get('text', None)
    #     if search_text:
    #         self.object_list = self.object_list.filter(text=search_text)
    #
    #     self.object_list = self.object_list.select_related('user').prefetch_related('skills').order_by("text", "slug")  # Сортировка
    #
    #     """
    #     Пагинация
    #     1 - 0:10
    #     2 - 10:20
    #     3 - 20:30
    #
    #     total = self.object_list.count()                    количество страниц всего
    #     page_number = int(request.GET.get("page", 1))       запрос пользователя по странице, берем из реквеста
    #                                                         если запрос пустой, то делаем страницу 1
    #     offset = (page_number-1) * settings.TOTAL_ON_PAGE   отступ (насколько отступаем, чтобы вытащить следующую страницу
    #
    #     if offset < total:
    #         self.object_list = self.object_list[offset:offset + settings.TOTAL_ON_PAGE]
    #     else:
    #         self.object_list = self.object_list[offset:offset + total]
    #     """
    #
    #     paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
    #     page_number = request.GET.get("page")
    #     page_obj = paginator.get_page(page_number)
    #
    #     # vacancies = []
    #     # for vacancy in page_obj:
    #     #     vacancies.append({
    #     #         'id': vacancy.id,
    #     #         'text': vacancy.text,
    #     #         'slug': vacancy.slug,
    #     #         'status': vacancy.status,
    #     #         'created': vacancy.created,
    #     #         'user': vacancy.user.username,
    #     #         'skills': list(map(str, vacancy.skills.all())),
    #     #     })
    #     list(map(lambda x: setattr(x, 'username', x.user.username if x.user else None), page_obj))
    #
    #     response = {
    #         "items": VacancyListSerializer(page_obj, many=True).data,
    #         "num_pages": paginator.num_pages,
    #         "total": paginator.count
    #     }
    #
    #     return JsonResponse(response, safe=False)

class VacancyDetailView(RetrieveAPIView):
    #model = Vacancy
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDetailSerializer
    permission_classes = [IsAuthenticated]

    # def get(self, request, *args, **kwargs):
    #     vacancy = self.get_object()
    #
    #     # return JsonResponse({
    #     #     'id': vacancy.id,
    #     #     'text': vacancy.text,
    #     #     'slug': vacancy.slug,
    #     #     'status': vacancy.status,
    #     #     'created': vacancy.created,
    #     #     'user': vacancy.user_id,
    #     #     'skills': list(map(str, vacancy.skills.all())),
    #     # })
    #     return JsonResponse(VacancyDetailSerializer(vacancy).data)

#@method_decorator(csrf_exempt, name='dispatch')
class VacancyCreateView(CreateAPIView):
    #model = Vacancy
    #fields = ['user', 'slug', 'text', 'status', 'created', 'skills']
    queryset = Vacancy.objects.all()
    serializer_class = VacancyCreateSerializer
    permission_classes = [IsAuthenticated, VacancyCreatePermission]

    # def post(self, request, *args, **kwargs):
    #     #vacancy_data = json.loads(request.body)
    #     vacancy_data = VacancyCreateSerializer(data=json.loads(request.body))
    #     if vacancy_data.is_valid():
    #         vacancy_data.save()
    #     else:
    #         return JsonResponse(vacancy_data.errors)
    #
    #     # vacancy = Vacancy.objects.create(
    #     #     slug=vacancy_data['slug'],
    #     #     text=vacancy_data['text'],
    #     #     status=vacancy_data['status']
    #     # )
    #     # vacancy.user = get_object_or_404(User, pk=vacancy_data['user_id'])
    #     #
    #     # for skill in vacancy_data['skills']:
    #     #     """
    #     #     try:
    #     #         skill_obj = Skill.objects.get(name=skill)
    #     #     except Skill.DoesNotExist:
    #     #         skill_obj = Skill.objects.create(name=skill)
    #     #     """
    #     #     skill_obj, created = Skill.objects.get_or_create(
    #     #         name=skill,
    #     #         defaults={
    #     #             "is_active": True
    #     #         }
    #     #     )
    #     #     vacancy.skills.add(skill_obj)
    #     #
    #     # vacancy.save()
    #     #
    #     # return JsonResponse({
    #     #     'id': vacancy.id,
    #     #     'text': vacancy.text,
    #     #     'slug': vacancy.slug,
    #     #     'status': vacancy.status,
    #     #     'created': vacancy.created,
    #     #     'user': vacancy.user_id,
    #     # })
    #     return JsonResponse(vacancy_data.data)


#@method_decorator(csrf_exempt, name='dispatch')
class VacancyUpdateView(UpdateAPIView):
    # model = Vacancy
    # fields = ['slug', 'text', 'status', 'skills']
    queryset = Vacancy.objects.all()
    serializer_class = VacancyUpdateSerializer
    http_method_names = ["put"]

    # def patch(self, request, *args, **kwargs):
    #     super().post(request, *args, **kwargs)
    #
    #     vacancy_data = json.loads(request.body)
    #     self.object.slug = vacancy_data['slug']
    #     self.object.text = vacancy_data['text']
    #     self.object.status = vacancy_data['status']
    #
    #     for skill in vacancy_data['skills']:
    #         try:
    #             skill_obj = Skill.objects.get(name=skill)
    #         except Skill.DoesNotExist:
    #             return JsonResponse({'error': 'Skill not found'}, status=404)
    #         self.object.skills.add(skill_obj)
    #
    #     self.object.save()
    #
    #     return JsonResponse({
    #         'id': self.object.id,
    #         'text': self.object.text,
    #         'slug': self.object.slug,
    #         'status': self.object.status,
    #         'created': self.object.created,
    #         'user': self.object.user_id,
    #         'skills': list(self.object.skills.all().values_list('name', flat=True))
    #     })


#@method_decorator(csrf_exempt, name='dispatch')
class VacancyDeleteView(DestroyAPIView):
    # model = Vacancy
    # success_url = "/"
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDestroySerializer

    # def delete(self, request, *args, **kwargs):
    #     super().delete(request, *args, **kwargs)
    #
    #     return JsonResponse({'status': 'ok'}, status=200)


# class UserVacancyDetailView(View):  # Группировка
#     def get(self, request):
#         user_qs = User.objects.annotate(vacancies=Count('vacancy'))  # Объект который создает ORM-запрос в базу данных
#
#         paginator = Paginator(user_qs, settings.TOTAL_ON_PAGE)
#         page_number = request.GET.get("page")
#         page_obj = paginator.get_page(page_number)
#
#         users = []
#
#         for user in page_obj:
#             users.append({
#                 "id": user.id,
#                 "name": user.username,
#                 "vacancies": user.vacancies
#             })
#
#         response = {
#             "items": users,
#             "total": paginator.count,
#             "num_pages": paginator.num_pages,
#             "avg": user_qs.aggregate(avg=Avg('vacancies'))["avg"]  # Среднее количество вакансий на пользователя
#         }
#
#         return JsonResponse(response)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_vacancies(request): # меняем предыдущий класс на эту функцию:
    user_qs = User.objects.annotate(vacancies=Count('vacancy'))  # Объект который создает ORM-запрос в базу данных

    paginator = Paginator(user_qs, settings.TOTAL_ON_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    users = []

    for user in page_obj:
        users.append({
            "id": user.id,
            "name": user.username,
            "vacancies": user.vacancies
        })

    response = {
        "items": users,
        "total": paginator.count,
        "num_pages": paginator.num_pages,
        "avg": user_qs.aggregate(avg=Avg('vacancies'))["avg"]  # Среднее количество вакансий на пользователя
    }

    return JsonResponse(response)



class VacancyLikeView(UpdateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDetailSerializer
    http_method_names = ["put"]

    @extend_schema(deprecated=True)
    def put(self, request, *args, **kwargs):
        Vacancy.objects.filter(pk__in=request.data).update(likes=F('likes') + 1)

        return JsonResponse(VacancyDetailSerializer(Vacancy.objects.filter(pk__in=request.data),
                                                    many=True).data, safe=False)
