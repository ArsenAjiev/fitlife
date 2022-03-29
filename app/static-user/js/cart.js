// в store.html и cart.html добавляем class 'update-cart'  элементу button, что бы затем к нему  обратится
// <button data-product="{{ product.id }}" data-action="add" class=" ... update-cart...">Add to Cart</button>

// data-* атрибуты позволяют хранить дополнительную информацию в стандартных элементах HTML.
// Синтаксис прост — любой атрибут, чьё имя начинается с data-, является data-* атрибутом.
// Чтобы получить data-атрибут можно взять свойство объекта dataset с именем, равным части имени атрибута после data-*.

var updateBtns = document.getElementsByClassName('update-cart');
for ( i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		// присваиваем переменным значения полученных data-атрибутов.
		var product_id = this.dataset.product;
		var action = this.dataset.action;
		console.log('product_id:', product_id, 'Action:', action);
        console.log('USER', user);
        // если USER не авторизован, вызываем функцию addCookieItem
        if (user === 'AnonymousUser') {
            console.log('User not auth');
			addCookieItem(product_id, action)
        // если USER авторизован, вызываем функцию updateUserOrder
        }else {
			console.log('User is auth!!!');
            updateUserOrder(product_id, action)

        }
	})
}



// если User не авторизован, записываем полученные данные в cookie файлы.
function addCookieItem(product_id, action) {
	console.log('User is not authenticated');
	// action === 'add', если в cart[product_id] нет значений, то присваиваем цифру - 1,
	// если есть значения, то увеличиваем на 1.
	if (action === 'add') {
		if (cart[product_id] == undefined) {
			cart[product_id] = {'quantity': 1};

		} else {
			cart[product_id]['quantity'] += 1;
		}
	}
	// action === 'remove', уменьшаем значение в cart[product_id] на 1,
	// если значений нет, то удаляем cart[product_id] .
	if (action === 'remove') {
		cart[product_id]['quantity'] -= 1;
		if (cart[product_id]['quantity'] <= 0) {
			console.log('Item should be deleted')
			delete cart[product_id];
		}
	}
	console.log('CART_js:', cart);
	// сохраняем значения в cookie файле
	document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
	// перезагружаем страницу
	location.reload();
}


// если User авторизован, отправляем полученные данные на контроллер "update_item" используя метод fetch.
function updateUserOrder(product_id, action){
	console.log('User is authenticated, sending data...');
        // ссылка на контроллер, который будет обрабатывать полученные данные.
		var url = '/store/update_item/';

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
              	'X-CSRFToken':csrftoken,
			},
			body:JSON.stringify({'product_id':product_id, 'action':action})
		})
		.then((response) => {
			return response.json();

		})
		.then((data) => {
			// data -  это ответ сервера после POST запроса на url = '/store/update_item/'
			// пример:  return JsonResponse('Item was added!', safe=False)
		    console.log('data:', data);
			location.reload();
		});
}