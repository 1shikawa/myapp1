from django.urls import path,include
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views

app_name = 'ReadingRec'

urlpatterns = [
    # 書籍
    path('booklist/', views.IndexView.as_view(), name='index'),  # 一覧
    path('add/', views.AddView.as_view(), name='book_add'),  # 追加
    path('update/<int:pk>/', views.UpdateView.as_view(), name='book_update'),  # 編集
    path('delete/<int:pk>/', views.DeleteView.as_view(), name='book_delete'),  # 削除
    path('deleteAll/', views.deleteAll, name='deleteAll'),
    # 感想
    path('<int:pk>/impression/', views.ImpressionList.as_view(), name='impression_list'),  # 一覧
    path('<int:book_id>/impression/add/', views.ImpressionAddView.as_view(), name='impression_add'),  # 追加
    # path('<int:book_pk>/impression/<int:impression_id>/update/', views.ImpressionUpdateView.as_view(), name='impression_update'),  # 編集
    path('<int:book_id>/impression/<int:impression_id>/update/', views.impression_edit, name='impression_edit'),  # 編集
    # path('<int:pk>/impression/<int:impression_id>/', views.ImpressionDeleteView.as_view(), name='impression_delete'),
    path('<int:book_id>/impression/<int:impression_id>/', views.impression_delete, name='impression_delete'),
    # CSVインポート/エクスポート
    path('import/', views.BookImport.as_view(), name='import'),
    path('export/', views.BookExport, name='export'),

    # ログアウト
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]


