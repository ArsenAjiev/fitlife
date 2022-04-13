# Testing plan

Тестируем то, что написали сами и что теоретически может пойти не так.

* models
* urls
* views
* forms

Не тестируем:

* код Django
* сторонние библиотеки

#APPS

## 1.membership

## models.py
### 1.1 Membership
```text
    class Membership(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        name = models.CharField(max_length=200, null=True)
        email = models.CharField(max_length=200)
    
        def __str__(self):
            return self.name
```

```text
 Membership:
    БД: Создаем экземпляр юзера.
    БД: Создаем тестовую запись.
    Проверяем:
    
    Атрибуты модели:
     - user == зарегистрированный пользователь в системе.
     - name: аргумент  max_length не более 200 символов.
     - email: аргумент  max_length не более 200 символов.
    
    Методы модели:
     - метод __str__: возвращает строку
  
```

### 1.2 Subscription
```text
class Subscription(models.Model):
    CHOICES = (
        ("1m", 'Subscription for 1 month'),
        ("2m", 'Subscription for 2 month'),
        ("3m", 'Subscription for 3 month'),
        ("4t", 'Subscription for 4 times'),
        ("8t", 'Subscription for 8 times'),
        ("12t", 'Subscription for 12 times'),
    )
    title = models.CharField(max_length=100, choices=CHOICES)
    description = models.CharField(max_length=255)
    is_limited = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.title

```


```text
 Subscription:
    БД: Создаем тестовую запись.
    Проверяем:
    
    Атрибуты модели:
     - title: аргумент  max_length не более 100 символов.
     - description: аргумент  max_length не более 255 символов.
     - price: аргумент  max_digits не более 5 символов, аргумент  decimal_places не более 2 символов
     - ???ПОЛЕ CHOICES???
    
    Методы модели:
     - метод __str__: возвращает строку
 
```


### 1.3 Order
```text
class Order(models.Model):
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    activation = models.BooleanField(default=False)
    date_activation = models.DateField(blank=True, null=True)
    paid_until = models.DateField(null=True, blank=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)

    @property
    def paid_limit(self, current_date=datetime.date.today()):
        if self.paid_until is None:
            return False
        if not self.is_limited:
            return False
        if self.is_limited:
            return current_date < self.paid_until

    @property
    def paid_quantity(self):
        if self.is_limited:
            return False
        else:
            return self.quantity > 0

    @property
    def expired(self):
        if self.paid_limit == 0 and self.paid_quantity == 0:
            return True
        else:
            return False

    @property
    def is_limited(self):
        return self.subscription.is_limited

    @property
    def diff_date(self):
        if self.is_limited and self.activation and self.paid_limit:
            return self.paid_until - datetime.date.today()

    def __str__(self):
        return f" id {self.pk}"

```


```text
 Order:
    БД: Создаем тестовую запись.
    Проверяем:
    
    Методы модели:
     - метод paid_limit: возвращает True если current_date < paid_until или paid_until is None, иначе False.
     - метод paid_quantity: возвращает True если quantity > 0, иначе False.     
     - метод expired: возвращает True  если paid_limit == 0 и paid_quantity == 0, иначе False. 
     - метод diff_date: возвращает количество дней между paid_until и сегодняшней датой.     
     - метод __str__: возвращает строку  вида  'id {pk}'    
```




