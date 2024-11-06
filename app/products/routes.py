from app.products import bp
from flask import render_template, request, current_app
from werkzeug.utils import secure_filename
import os
from app.products.forms import NewProductForm


@bp.route('/')
def index():
    return render_template('products.html')


@bp.route('/new', methods=['GET', 'POST'])
def new_product():
    if request.method == 'GET':
        print('new product request: ', request.args)
        if request.args.get('shop_id'):
            form = NewProductForm()
            form.shop_id.process_data(request.args.get('shop_id'))

    elif request.method == 'POST':
        print('new product request: ', request.form)
        form = NewProductForm(request.form)
        if form.validate_on_submit():
            from app.shops.models import Shop
            shop = Shop.query.get(form.shop_id.data)
            print('shop: ', shop)
            if shop:
                shop_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'admins', str(shop.admin_id), 'shops', str(shop.id))
                if shop_folder:
                    products_folder = os.path.join(shop_folder, 'products')
                    if not os.path.exists(products_folder):
                        os.makedirs(products_folder)
                    if form.main_image.data:
                        main_image = form.main_image.data
                        main_image_filename = secure_filename(main_image.filename)
                        main_image.save(os.path.join(products_folder, f'main_{main_image_filename}'))
                    
                    from app.products.models import Product
                    product = Product.add(
                        name = form.name.data,
                        points_cost = form.points_cost.data,
                        short_description = form.short_description.data,
                        description = form.description.data,
                        shop_id = shop.id,
                        type = form.type.data,
                        standart_cost = form.standart_cost.data,
                        currency = form.currency.data,
                        available_quantity = form.available_quantity.data,
                        end_date = form.end_date.data,
                        category_id = form.category.data,
                        subcategory_id = form.subcategory.data
                    )
                    return render_template('new_product_success.html', product=product)

    return render_template('new_product.html', form=form)
                    
