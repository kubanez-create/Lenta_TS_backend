"""Custom manage.py command for loading csv files into project database."""
import csv
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from products.models import DataPoint, Product, Sales, Shops

COMMANDS = {"product": Product, "shop": Shops, "sales": None}


class Command(BaseCommand):
    help = (
        "The command for loading csv files into projects db."
        " Takes command-line arguments. For example to load"
        "file genre.csv you need to enter the following command:"
        " python manage.py loadcsv review"
        " /home/kubanez/Dev/api_yamdb/api_yamdb/static/data/review.csv."
    )

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument("command", nargs="+", type=str)
        parser.add_argument("filename", nargs="+", type=str)

    def handle(self, *args, **options):
        command: str = options["command"][0]
        filename: str = options["filename"][0]

        try:
            model = COMMANDS.get(command)
            with open(filename) as f:
                reader = csv.reader(f)
                field_names = next(reader)

                for row in reader:
                    data_to_insert = dict(zip(field_names, row))

                    if command == "product":
                        model.objects.create(
                            sku=data_to_insert.get("pr_sku_id"),
                            uom=data_to_insert.get("pr_uom_id"),
                            group=data_to_insert.get("pr_group_id"),
                            category=data_to_insert.get("pr_cat_id"),
                            subcategory=data_to_insert.get("pr_subcat_id"),
                        )
                    elif command == "shop":
                        model.objects.create(
                            title=data_to_insert.get("st_id"),
                            city=data_to_insert.get("st_city_id"),
                            division=data_to_insert.get("st_division_code"),
                            type_format=data_to_insert.get("st_type_format_id"),
                            loc=data_to_insert.get("st_type_loc_id"),
                            size=data_to_insert.get("st_type_size_id"),
                            is_active=data_to_insert.get("st_is_active"),
                        )
                    elif command == "sales":
                        sales_obj, _ = Sales.objects.get_or_create(
                            store=Shops.objects.get(title=data_to_insert.get("st_id")),
                            SKU=Product.objects.get(
                                sku=data_to_insert.get("pr_sku_id")
                            ),
                        )
                        DataPoint.objects.create(
                            date=datetime.strptime(
                                data_to_insert.get("date"), "%m/%d/%Y"
                            ),
                            sales_type=data_to_insert.get("pr_sales_type_id"),
                            sales_units=data_to_insert.get("pr_sales_in_units"),
                            sales_units_promo=data_to_insert.get(
                                "pr_promo_sales_in_units"
                            ),
                            sales_rub=data_to_insert.get("pr_sales_in_rub"),
                            sales_rub_promo=data_to_insert.get("pr_promo_sales_in_rub"),
                            sale=sales_obj,
                        )

            self.stdout.write(
                self.style.SUCCESS('Successfully loaded the file "%s"' % filename)
            )
        except IOError as ex:
            raise CommandError("File '%s' does not exist" % filename) from ex
