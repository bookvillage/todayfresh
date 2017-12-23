from django.shortcuts import render
from django.views.generic import View
from apps.goods.models import GoodsType,IndexGoodsBanner,IndexTypeGoodsBanner,IndexPromotionBanner
from django_redis import get_redis_connection

# Create your views here.
class IndexViews(View):
    def get(self, requset):
        # 获取商品分类信息
        types = GoodsType.objects.all()
        # 获取首页轮播商品
        index_banner = IndexGoodsBanner.objects.all().order_by('index')
        # 促销活动表的信息
        promotion_banner = IndexPromotionBanner.objects.all().order_by('index')
        # 首页的分类商品展示的商品信息
        # types_goods_banner = IndexTypeGoodsBanner.objects.all()
        for type in types:
            title_banner = IndexTypeGoodsBanner.objects.filter(type = type,display_type = 0).order_by('index')
            image_banner = IndexTypeGoodsBanner.objects.filter(type = type,display_type = 1).order_by('index')
            type.title_banner = title_banner
            type.image_banner = image_banner
        # 我的购物车的中商品的数目
        cart_count = 0

        user = requset.user
        if user.is_authenticated():
            conn = get_redis_connection('default')
            cart_id = 'cart_%d'%user.id
            cart_count = conn.hlen(cart_id)
        # 组织模板上下文
        context = {'types':types,
                   'index_banner':index_banner,
                   'promotion_banner':promotion_banner,
                   # 'types_goods_banner':types_goods_banner,

                   'cart_count':cart_count}

        return render(requset, 'index.html',context)