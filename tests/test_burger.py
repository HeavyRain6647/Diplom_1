import pytest
from unittest.mock import Mock
from praktikum.burger import Burger
from praktikum.ingredient_types import INGREDIENT_TYPE_SAUCE

class TestBurger:

    def test_set_buns(self):
        burger = Burger()
        mock_bun = Mock()
        burger.set_buns(mock_bun)
        assert burger.bun == mock_bun

    def test_add_ingredient(self):
        burger = Burger()
        mock_ingredient = Mock()
        burger.add_ingredient(mock_ingredient)
        assert mock_ingredient in burger.ingredients
        assert len(burger.ingredients) == 1

    def test_remove_ingredient(self):
        burger = Burger()
        mock_ingredient = Mock()
        burger.add_ingredient(mock_ingredient)
        burger.remove_ingredient(0)
        assert len(burger.ingredients) == 0

    def test_move_ingredient(self):
        burger = Burger()
        mock_1 = Mock()
        mock_2 = Mock()
        burger.add_ingredient(mock_1)
        burger.add_ingredient(mock_2)
        # Перемещаем первый ингредиент в конец
        burger.move_ingredient(0, 1)
        assert burger.ingredients[1] == mock_1
        assert burger.ingredients[0] == mock_2

    @pytest.mark.parametrize("bun_price, ing_price, expected_total", [
        (100, 50, 250),   # (100 * 2) + 50 = 250
        (200, 100, 500),  # (200 * 2) + 100 = 500
        (0, 0, 0)         # Проверка на нулевые значения
    ])
    def test_get_price(self, bun_price, ing_price, expected_total):
        burger = Burger()
        # Создаем мок булки с ценой
        mock_bun = Mock()
        mock_bun.get_price.return_value = bun_price
        burger.set_buns(mock_bun)
        
        # Создаем мок ингредиента с ценой
        mock_ingredient = Mock()
        mock_ingredient.get_price.return_value = ing_price
        burger.add_ingredient(mock_ingredient)
        
        assert burger.get_price() == expected_total

    def test_get_receipt(self):
        burger = Burger()
        # Настраиваем мок булки
        mock_bun = Mock()
        mock_bun.get_name.return_value = "black bun"
        mock_bun.get_price.return_value = 100
        burger.set_buns(mock_bun)

        # Настраиваем мок ингредиента
        mock_ingredient = Mock()
        mock_ingredient.get_type.return_value = INGREDIENT_TYPE_SAUCE
        mock_ingredient.get_name.return_value = "hot sauce"
        mock_ingredient.get_price.return_value = 100
        burger.add_ingredient(mock_ingredient)

        receipt = burger.get_receipt()
        
        # Проверяем, что в чеке есть все нужные части
        assert "black bun" in receipt
        assert "sauce hot sauce" in receipt  # метод делает .lower()
        assert "Price: 300" in receipt       # (100*2) + 100

    def test_remove_ingredient_out_of_range_raises_error(self):
        # Негативный тест: удаление по несуществующему индексу
        burger = Burger()
        with pytest.raises(IndexError):
            burger.remove_ingredient(0)