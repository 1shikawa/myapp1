from django.shortcuts import get_object_or_404, redirect,render,reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib import messages  # メッセージフレームワーク
from django.urls import reverse_lazy
from ReadingRec.models import Book,Impression
from django.views import generic
from .forms import BookCreateForm,ImpressionCreateForm
from django.db.models import Q,Count,Sum


@method_decorator(login_required, name='dispatch')
class IndexView(generic.ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'book_list.html'
    paginate_by = 7

    def get_queryset(self):
        # 子数を親の感想数にセット
        # qs = Book.objects.filter(impressions__isnull=False).values('id').annotate(impre_count=Count('id'))
        # for i in qs:
        #     Book.objects.filter(id=i['id']).update(impressionCount=i['impre_count']) # 辞書型のキーを指定して更新
        queryset = Book.objects.all().order_by('-created_at')
        keyword = self.request.GET.get('keyword')
        if keyword:
            queryset = queryset.filter(
                Q(name__icontains=keyword) | Q(bookType__icontains=keyword)
            )
        return queryset


@method_decorator(login_required, name='dispatch')
class AddView(generic.CreateView):
    model = Book
    template_name = 'book_add.html'
    form_class = BookCreateForm
    success_url = reverse_lazy('ReadingRec:index')  # /ReadingRec/

    def form_valid(self, form):
        ''' バリデーションを通った時 '''
        book = form.save(commit=False)
        # book.editer = request.user.id
        form.instance.editer = str(self.request.user)
        book.save()
        # 追加のとき
        if 'save' in self.request.POST:
            messages.success(self.request, "追加しました")
            return redirect('ReadingRec:index')


            # 保存してもう一つ追加ボタンのとき
        elif 'save_and_add' in self.request.POST:
            messages.success(self.request, "追加しました")
            return redirect('ReadingRec:book_add')

        # 保存して編集を続けるボタンのとき
        elif 'save_and_edit' in self.request.POST:
            messages.success(self.request, "追加しました")
            return redirect('ReadingRec:book_update', pk=book.pk)

        # return super(AddView, self).form_valid(form)

    def form_invalid(self, form):
        ''' バリデーションに失敗した時 '''
        messages.warning(self.request, "追加できませんでした")
        return super().form_invalid(form)



@method_decorator(login_required, name='dispatch')
class UpdateView(generic.UpdateView):
    model = Book
    template_name = 'book_add.html'
    form_class = BookCreateForm
    success_url = reverse_lazy('ReadingRec:index')

    def form_valid(self, form):
        ''' バリデーションを通った時 '''
        book = form.save(commit=False)
        # book.editer = str(request.user)
        book.save()
        messages.success(self.request, "編集しました")
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class DeleteView(generic.DeleteView):
    model = Book
    template_name = 'book_delete.html'
    success_url = reverse_lazy('ReadingRec:index')

    def form_valid(self, form):
        ''' バリデーションを通った時 '''
        messages.success(self.request, "削除しました")
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ImpressionList(generic.ListView):
    """感想の一覧"""
    model = Impression
    context_object_name = 'impressions'
    template_name = 'impression_list.html'
    paginate_by = 7  # １ページは最大2件ずつでページングする

    def get(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=kwargs['pk'])  # 親の書籍を読む
        impressions = book.impressions.all().order_by('-created_at')  # 書籍の子供の、感想を読む
        self.object_list = impressions

        context = self.get_context_data(object_list=self.object_list, book=book)
        return self.render_to_response(context)


@method_decorator(login_required, name='dispatch')
class ImpressionAddView(generic.CreateView):
    model = Impression
    template_name = 'impression_add.html'
    form_class = ImpressionCreateForm

    def form_valid(self, form):
        book_pk = self.kwargs['book_id']
        impression = form.save(commit=False)  # コメントはDBに保存されていません
        impression.book = get_object_or_404(Book, pk=book_pk)
        form.instance.editer = str(self.request.user)
        impression.save()  # ここでDBに保存
        # Bookに紐づくコメント数更新
        b = Book.objects.filter(id=book_pk).filter(impressions__isnull=False).values('id').annotate(impre_count=Count('id'))[0]
        book = Book.objects.get(id=book_pk)
        book.impressionCount = b['impre_count']
        book.save()
        messages.success(self.request, "追加しました")
        return redirect('ReadingRec:impression_list', pk=book_pk)


@method_decorator(login_required, name='dispatch')
class ImpressionUpdateView(generic.UpdateView):
    model = Impression
    template_name = 'impression_add.html'
    form_class = ImpressionCreateForm
    success_url = reverse_lazy('ReadingRec:impression_list')

    def form_valid(self, form):
        ''' バリデーションを通った時 '''
        impression = form.save(commit=False)
        impression.book = book  # この感想の、親の書籍をセット
        impression.save()

        messages.success(self.request, "編集しました")
        return super().form_valid(form)
        # return redirect('impression_list', pk)



@login_required
def impression_edit(request, book_id, impression_id=None):
    """感想の編集"""
    book = get_object_or_404(Book, pk=book_id)  # 親の書籍を読む
    if impression_id:  # impression_id が指定されている (修正時)
        impression = get_object_or_404(Impression, pk=impression_id)
    else:  # impression_id が指定されていない (追加時)from django.db.models import Su
        impression = Impression()

    if request.method == 'POST':
        form = ImpressionCreateForm(request.POST, instance=impression)  # POST された request データからフォームを作成
        if form.is_valid():  # フォームのバリデーション
            impression = form.save(commit=False)
            impression.book = book  # この感想の、親の書籍をセット
            impression.editer = str(request.user)
            impression.save()
            return redirect('ReadingRec:impression_list', book_id)

    else:  # GET の時
        form = ImpressionCreateForm(instance=impression)  # impression インスタンスからフォームを作成

    return render(request,
                  'impression_edit.html',
                  dict(form=form, book_id=book_id, impression_id=impression_id))


@login_required
def impression_delete(request, book_id, impression_id):
    """感想の削除"""
    impression = get_object_or_404(Impression, pk=impression_id)
    impression.delete()
    messages.success(request, "削除しました")
    # Bookに紐づく感想数更新
    b = \
    Book.objects.filter(id=book_id).filter(impressions__isnull=False).values('id').annotate(impre_count=Count('id'))[0]
    book = Book.objects.get(id=book_id)
    book.impressionCount = b['impre_count']
    book.save()
    return redirect('ReadingRec:impression_list', pk=book_id)


# @method_decorator(login_required, name='dispatch')
# class ImpressionDeleteView(generic.DeleteView):
#     model = Impression
#     template_name = 'impression_delete.html'
#     success_url = reverse('ReadingRec:impression_list')
#
#     def form_valid(self, form):
#         ''' バリデーションを通った時 '''
#         messages.success(self.request, "削除しました")
#         return super().form_valid(form)

#CSVエクスポート/インポート
import csv
import io
from django.http import HttpResponse
from .forms import CSVUploadForm
from django.db import transaction

class InvalidColumnsExcepion(Exception):
    """CSVの列が足りなかったり多かったりしたらこのエラー"""
    pass

class InvalidSourceExcepion(Exception):
    """CSVの読みとり中にUnicodeDecordErrorが出たらこのエラー"""
    pass

class PostIndex(generic.ListView):
    model = Book

class BookImport(generic.FormView):
    template_name = 'import.html'
    success_url = reverse_lazy('ReadingRec:index')
    form_class = CSVUploadForm
    number_of_columns = 5  # 列の数を定義しておく。各行の列がこれかどうかを判断する

    def save_csv(self, form):
        # csv.readerに渡すため、TextIOWrapperでテキストモードなファイルに変換
        csvfile = io.TextIOWrapper(form.cleaned_data['file'],encoding='utf-8-sig')
        reader = csv.reader(csvfile)
        i = 1  # 1行目でのUnicodeDecodeError対策。for文の初回のnextでエラーになるとiの値がない為
        try:
            # iは、現在の行番号。エラーの際に補足情報として使う
            for i, row in enumerate(reader, 1):
                # 列数が違う場合
                if len(row) != self.number_of_columns:
                    raise InvalidColumnsExcepion(
                        '{0}行目が変です。本来の列数: {1}, {0}行目の列数: {2}'.format(i, self.number_of_columns, len(row)))

                # 問題なければ、この行は保存する。(実際には、form_validのwithブロック終了後に正式に保存される)
                book, created = Book.objects.get_or_create(pk=row[0])
                book.name = row[1]
                book.bookType = row[2]
                book.publisher = row[3]
                book.page = row[4]
                book.save()

        except UnicodeDecodeError:
            raise InvalidSourceExcepion('{}行目でデコードに失敗しました。ファイルのエンコーディングや、正しいCSVファイルか確認ください。'.format(i))

    def form_valid(self, form):
        try:
            # CSVの100行目でエラーがおきたら、前の99行分は保存されないようにする
            with transaction.atomic():
                self.save_csv(form)
        # 今のところは、この2つのエラーは同様に対処します。
        except InvalidSourceExcepion as e:
            form.add_error('file', e)
            return super().form_invalid(form)
        except InvalidColumnsExcepion as e:
            form.add_error('file', e)
            return super().form_invalid(form)
        else:
            return super().form_valid(form)  # うまくいったので、リダイレクトさせる


def BookExport(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="BookAll.csv"'
    # HttpResponseオブジェクトはファイルっぽいオブジェクトなので、csv.writerにそのまま渡せます。
    writer = csv.writer(response)
    for book in Book.objects.filter(editer=request.user):
        writer.writerow([book.pk, book.name,book.bookType,book.publisher,book.page])
    return response

#一括削除
from django.views.decorators.http import require_POST
@require_POST
def deleteAll(request):
    delete_ids = request.POST.getlist('delete_ids')
    if delete_ids:
        Book.objects.filter(id__in=delete_ids).delete()
    return redirect('ReadingRec:index')


