######################################################################
# Copyright 2016, 2024 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################
# cspell:ignore userid postalcode
"""
Test Factory to make fake objects for testing
"""
from datetime import date

from factory import Factory, Faker, Sequence, SubFactory, post_generation
from factory.fuzzy import FuzzyChoice, FuzzyDate, FuzzyInteger

from service.models import Item, Order, OrderStatus


class OrderFactory(Factory):
    """Creates fake Orders"""

    # pylint: disable=too-few-public-methods
    class Meta:
        """Persistent class"""

        model = Order

    id = Sequence(lambda n: n)
    customer_name = Faker("name")
    status = FuzzyChoice(list(OrderStatus))
    created_at = FuzzyDate(date(2008, 1, 1))
    updated_at = FuzzyDate(date(2008, 9, 8))
    # the many side of relationships can be a little wonky in factory boy:
    # https://factoryboy.readthedocs.io/en/latest/recipes.html#simple-many-to-many-relationship

    @post_generation
    def items(
        self, create, extracted, **kwargs
    ):  # pylint: disable=method-hidden, unused-argument
        """Creates the items list"""
        if not create:
            return

        if extracted:
            self.items = extracted


class ItemFactory(Factory):
    """Creates fake Item"""

    # pylint: disable=too-few-public-methods
    class Meta:
        """Persistent class"""

        model = Item

    id = Sequence(lambda n: n)
    order_id = None
    product_name = FuzzyChoice(choices=["foo", "bar", "rolls", "cleaner", "hardware"])
    quantity = FuzzyInteger(1, 5)
    price = FuzzyInteger(10, 50)
    created_at = FuzzyDate(date(2008, 1, 1))
    updated_at = FuzzyDate(date(2008, 9, 8))
    order = SubFactory(OrderFactory)
