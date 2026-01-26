# test_burger.py

import pytest
from unittest.mock import Mock
from burger import Burger, Bun, Ingredient
import test_data as td # Импортируем наши тестовые данные

@pytest.fixture
def burger():
    """Фикстура для создания экземпляра Burger."""
    return Burger()

@pytest.fixture
def mock_bun():
    """
    Фикстура для создания и настройки мока булки.
    Вся настройка происходит здесь, как и советовал ревьюер.
    """
    bun = Mock(spec=Bun)
    bun.get_name.return_value = td.BUN_NAME
    bun.get_price.return_value = td.BUN_PRICE
    return bun

@pytest.fixture
def mock_ingredients():
    """
    Фикстура для создания и настройки моков ингредиентов.
    """
    ingredient1 = Mock(spec=Ingredient)
    ingredient1.get_type.return_value = td.INGREDIENT_SAUCE_TYPE
    ingredient1.get_name.return_value = td.INGREDIENT_SAUCE_NAME
    ingredient1.get_price.return_value = td.INGREDIENT_SAUCE_PRICE

    ingredient2 = Mock(spec=Ingredient)
    ingredient2.get_type.return_value = td.INGREDIENT_FILLING_TYPE
    ingredient2.get_name.return_value = td.INGREDIENT_FILLING_NAME
    ingredient2.get_price.return_value = td.INGREDIENT_FILLING_PRICE
    return [ingredient1, ingredient2]

class TestBurger:

    def test_set_buns_success(self, burger, mock_bun):
        burger.set_buns(mock_bun)
        assert burger.bun == mock_bun

    def test_add_ingredient_success(self, burger, mock_ingredients):
        burger.add_ingredient(mock_ingredients[0])
        burger.add_ingredient(mock_ingredients[1])
        assert len(burger.ingredients) == 2
        assert burger.ingredients[0] == mock_ingredients[0]
        assert burger.ingredients[1] == mock_ingredients[1]

    def test_remove_ingredient_success(self, burger, mock_ingredients):
        burger.add_ingredient(mock_ingredients[0])
        burger.add_ingredient(mock_ingredients[1])
        burger.remove_ingredient(0)
        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == mock_ingredients[1]

    def test_remove_ingredient_non_existent(self, burger, mock_ingredients):
        burger.add_ingredient(mock_ingredients[0])
        initial_ingredients = burger.ingredients[:]
        burger.remove_ingredient(5)
        assert burger.ingredients == initial_ingredients

    def test_move_ingredient_success(self, burger, mock_ingredients):
        burger.add_ingredient(mock_ingredients[0])
        burger.add_ingredient(mock_ingredients[1])
        burger.move_ingredient(0, 1)
        assert burger.ingredients == [mock_ingredients[1], mock_ingredients[0]]

    def test_get_price_success(self, burger, mock_bun, mock_ingredients):
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredients[0])
        burger.add_ingredient(mock_ingredients[1])
        
        assert burger.get_price() == td.EXPECTED_PRICE
        
        mock_bun.get_price.assert_called_once_with()
        mock_ingredients[0].get_price.assert_called_once_with()
        mock_ingredients[1].get_price.assert_called_once_with()

    def test_get_price_no_bun_negative(self, burger, mock_ingredients):
        burger.add_ingredient(mock_ingredients[0])
        assert burger.get_price() == 0.0

    def test_get_receipt_success(self, burger, mock_bun, mock_ingredients):
        """
        Позитивная проверка: формирование чека.
        Теперь с точной проверкой полного соответствия.
        """
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredients[0])
        burger.add_ingredient(mock_ingredients[1])

        # Создаем эталонную строку чека для сравнения
        expected_receipt = (
            f"(==== {td.BUN_NAME} ====)\n"
            f"= {td.INGREDIENT_SAUCE_TYPE.lower()} {td.INGREDIENT_SAUCE_NAME} =\n"
            f"= {td.INGREDIENT_FILLING_TYPE.lower()} {td.INGREDIENT_FILLING_NAME} =\n"
            f"(==== {td.BUN_NAME} ====)\n"
            f"\nPrice: {td.EXPECTED_PRICE}"
        )

        actual_receipt = burger.get_receipt()

        # Сравниваем фактический результат с эталоном
        assert actual_receipt == expected_receipt

    def test_get_receipt_no_bun_negative(self, burger, mock_ingredients):
        burger.add_ingredient(mock_ingredients[0])
        assert burger.get_receipt() == ""
