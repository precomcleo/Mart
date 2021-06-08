from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Product, Order
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from django.db.models import Sum
from django.db import transaction

from .forms import OrderModelForm

# --檢查是否符合vip身份--
def check_customer(func):
    def check_custome_vip(request):
        # 來源資料驗證
        product_id = request.POST.get('product_id','')          #商品vip屬性
        customer_is_vip = bool(request.POST.get('is_vip',0))    #訂單vip屬性

        if any(not request.POST[k] for k in request.POST) or product_id == 'Select Product':
            messages.error(request,'* 有空白欄位，請不要留空')
            return product_list(request)

        # 判斷身份
        product_vip = Product.objects.get(product_id=product_id).vip
        if product_vip == True and customer_is_vip == False:
            messages.error(request, '非vip不可訂購vip商品!')
            return product_list(request)
        else:
            return func(request)
    return check_custome_vip

# --撿查庫存--
def check_stock(func):
    def check_stock_pcs(request):
        # 來源資料驗證
        product_id = request.POST.get('product_id','')  #商品庫存屬性
        order_qty = request.POST.get('qty','0')         #訂單數量屬性

        # 判斷庫存
        product_stock_pcs = Product.objects.get(product_id=product_id).stock_pcs
        if int(order_qty) > int(product_stock_pcs):
            messages.error(request, '庫存不足!')
            return product_list(request)
        else:
            return func(request)
    return check_stock_pcs

# --列表頁--
def product_list(request):
    context = {
        # 商品列表
        'product_field_name': [field.name for field in Product._meta.fields],
        'product_list': Product.objects.all(),
        # 訂單記錄
        'order_field_name': [field.name for field in Order._meta.fields],
        'order_list': Order.objects.all(),
        } 
    return render(request, 'product/product_list.html', context)

# --新增訂單--
@check_customer
@check_stock
@require_http_methods(['POST'])
@transaction.atomic
def order_create(request):
    # 來源資料驗證
    product_id = request.POST.get('product_id','')
    order_qty = int(request.POST.get('qty','0'))
    customer_id = request.POST.get('customer_id','')

    # 更新庫存
    product_detail = Product.objects.get(product_id=product_id)
    product_detail.stock_pcs = product_detail.stock_pcs - order_qty
    product_detail.save()

    # 寫入訂單
    Order.objects.create(
        product_id=product_detail.product_id,
        qty=order_qty,
        price=product_detail.price,
        shop_id=product_detail.shop_id
        )

    return product_list(request)

# --刪除訂單--
def order_delete(request, pk):
    order = Order.objects.get(pk=pk)

    # 庫存更新
    product_original = Product.objects.get(product_id=order.product_id)
    product_original_stock = product_original.stock_pcs
    product_original.stock_pcs = product_original.stock_pcs + order.qty
    product_original.save()

    # 刪除訂單
    order.delete()

    # 到貨提醒
    product_new = Product.objects.get(product_id=product_original.product_id)
    product_new_stock = product_new.stock_pcs
    print(product_new_stock)
    if product_original_stock == 0 and product_new_stock > 0 :
        messages.success(request, '[%s] 商品到貨!' %product_new.product_id)

    return product_list(request)


# --銷售量Top3--
def top_three(request):
    # Order表,商品銷售數量合計,依銷售量降冪,取前三名
    top = Order.objects.values_list('product_id').annotate(qty_sum=Sum('qty')).order_by('-qty_sum')[:3]
    
    toplist = []
    for i in top:
        toplist.append(i[0])

    return HttpResponse('銷售 Top3 product_id：%s' %','.join(str(e) for e in toplist))


'''
每日排程任務
'''
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger

from django.core.mail import send_mail
from django.conf import settings

def job_function():
    #1.總銷售金額 2.總銷售數量 3.總訂單數量
    sell = Order.objects.raw('''
    SELECT 
        id, 
        shop_id, 
        qty*price AS sell_price, 
        sum(qty) AS qty, 
        count() AS count 
    FROM Product_order 
    GROUP BY shop_id
    ''')

    message = ''
    for p in sell:
        message = message + ('館別[%s] 總銷售金額:%s, 總銷售數量:%s, 總訂單數量:%s \n' %(p.shop_id, p.sell_price, p.qty, p.count))

    #發送訊息
    send_mail(
        '每日訂單報告',                   #信件標題
        message,                        #信件內容
        settings.EMAIL_HOST_USER,       #寄件信箱
        [settings.EMAIL_RECEIVE_USER],  #收件人
        fail_silently=False
        )

scheduler = BackgroundScheduler(timezone='MST')
scheduler.add_job(job_function, 'interval', hours=24, start_date='2021-06-07 00:00:00')
scheduler.start()
