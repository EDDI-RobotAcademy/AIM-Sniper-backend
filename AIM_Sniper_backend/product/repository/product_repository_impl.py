import os
from product.entity.models import Product
from product.repository.product_repository import ProductRepository
from AIM_Sniper_backend import settings




class ProductRepositoryImpl(ProductRepository):
    __instance = None
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def list(self):
        return Product.objects.all().order_by('productName')


    def create(self, productName, productPrice, productCategory, content, productTitleImage):
        uploadDirectory='../../AIM-Sniper-frontend/src/assets/images/uploadimages'
        print('업로드된 디렉토리 : ', uploadDirectory)
        os.makedirs(uploadDirectory, exist_ok=True)

        imagePath = os.path.join(uploadDirectory, productTitleImage.name)
        with open(imagePath, 'wb+') as destination:
            for chunk in productTitleImage.chunks():
                destination.write(chunk)
        print('이미지 경로: ',imagePath)


        product = Product(
            productName=productName,
            content=content,
            productPrice=productPrice,
            productCategory=productCategory,
            productTitleImage=productTitleImage.name
        )
        product.save()
        return product

    def findByProdictIdList(self, productIdList):
        try:
            return Product.objects.filter(productId__in=productIdList)
        except Product.DoesNotExist:
            return None

    def findAllByProductCategory(self, productCategory):
        try:
            return Product.objects.filter(productCategory=productCategory)
        except:
            return None

