# Generated by Django 2.0.7 on 2018-07-27 08:34

import api.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('phone_no', models.BigIntegerField(blank=True, default=None, null=True, validators=[api.validators.validate_phoneno])),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Cart')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('added', models.DateTimeField(auto_now_add=True)),
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('category_name', models.CharField(choices=[('Fashion', 'Fashion'), ('Sports', 'Sports'), ('Books', 'Books'), ('Home & Kitchen', 'Home & Kitchen'), ('Computers, Laptops, Mobiles & Accessories', 'Computers, Laptops, Mobiles & Accessories'), ('Beauty', 'Beauty'), ('Automobile', 'Automobile'), ('Toys & Kids Stuff', 'Toys & Kids Stuff'), ('Grocery & Pantry', 'Grocery & Pantry')], default=None, max_length=50)),
                ('description', models.TextField()),
                ('buy_price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('sell_price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('quantity', models.IntegerField(validators=[api.validators.validate_quantity, api.validators.validate_neg_quantity])),
                ('rating', models.DecimalField(decimal_places=1, default=-1, max_digits=2)),
                ('buy_quantity', models.IntegerField(default=0, validators=[api.validators.validate_neg_quantity, api.validators.validate_max_quantity])),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[('-1', -1), ('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5)], default='-1')),
                ('buy_quantity', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Product')),
            ],
        ),
        migrations.AddField(
            model_name='orders',
            name='product',
            field=models.ManyToManyField(blank=True, to='api.Product'),
        ),
        migrations.AddField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(blank=True, to='api.Product'),
        ),
    ]