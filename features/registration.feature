Feature: Регистрация

  Scenario: Успешная регистрация
    Given Я открыл страницу "Регистрации"
    When Я ввожу текст "user1" в поле "username"
    And Я ввожу текст "user1" в поле "password1"
    And Я ввожу текст "user1" в поле "password2"
    And Я ввожу текст "1999-01-01" в поле "birth_date"
    And Я отправляю форму
    Then Я должен быть на главной странице

  Scenario: Не успешный регистрация
    Given Я открыл страницу "Регистрации"
    When Я ввожу текст "admin" в поле "username"
    And Я ввожу текст "admin" в поле "password1"
    And Я ввожу текст "admin" в поле "password2"
    And Я ввожу текст "1999-01-01" в поле "birth_date"
    When Я отправляю форму
    Then Я должен быть на странице регистрации
    And Я должен видеть сообщение об ошибке с текстом "A user with that username already exists."