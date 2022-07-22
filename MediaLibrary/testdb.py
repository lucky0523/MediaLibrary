# -*- coding: utf-8 -*-

from django.http import HttpResponse

from MovieModel.models import Movie


# 数据库操作
def testdb(request):
    test1 = Movie(douban_id='firstmovie')
    test1.save()
    return HttpResponse("<p>数据添加成功！</p>")


# 数据库操作
def read_db(request):
    # 初始化
    response = ""
    response1 = ""

    # 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM
    list = Movie.objects.all()

    # 输出所有数据
    for var in list:
        response1 += var.douban_id + " "
    response = response1
    return HttpResponse("<p>" + response + "</p>")