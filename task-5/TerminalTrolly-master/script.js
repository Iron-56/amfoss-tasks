//fix the errors and complete the code.

const terminalOutput = document.querySelector('.terminal-output').children[0];
const terminalInput = document.querySelector('input[type="text"]');
const productCatalog = document.querySelector('.product-catalog');
const totalPrice = document.getElementById('total-price');
const productList = productCatalog.children[0];

var products = [];
var cart = [];
var userId = 1;

terminalInput.addEventListener('keydown', (event) => {
	if (event.key === 'Enter') {
		handleInput(event.target.value);
	}
});

function displayList()
{
	out("Available products:")
	for(let i=0; i<products.length; ++i)
	{
		out((i+1).toString()+". "+products[i].title)
	}
}

function sort(param)
{
	const products = Array.from(productList.children);

	if(param == "name")
	{
		products.sort((a, b) => {
			const nameA = a.getAttribute("title");
			const nameB = b.getAttribute("title");
			return nameA.localeCompare(nameB);;
		});
	} else {
		products.sort((a, b) => {
			const priceA = parseFloat(a.getAttribute("price"));
			const priceB = parseFloat(b.getAttribute("price"));
			return priceA - priceB;
		});
	}

	products.sort();

	productList.innerHTML = '';
	products.forEach(product => productList.appendChild(product));
}

function search(keyword)
{
	hits = 0;
	products.forEach(element => {
		if(element.title.toLowerCase().includes(keyword))
		{
			hits++;
			out(hits.toString()+". "+element.title);
		}
	})
}

function showDetails(item)
{
	out("Name: "+item.title)
	out("Price: $"+item.price)
	out("Description: "+item.description)
}

function handleInput(command)
{
	terminalOutput.innerHTML += "<span class='terminalFont'>user@ubuntu:~$ </span>"+command+"\n"
	task = command.split(" ")

    switch (task[0]) {

        case 'help':
            viewCommand();
            break;
		
		case 'clear':
			terminalOutput.innerHTML = '';
			break;
		
		case 'list':
			displayList();
			break;
		
		case 'sort':
			sort(task[1]);
			break;
		
		case 'search':
			search(task[1].toLowerCase());
			break;
		
		case 'add':
			add(Number(task[1]));
			break;
		
		case 'remove':
			remove(Number(task[1]));
			break;
		
		case 'cart':
			showCart();
			break;
		
		case 'details':
			showDetails(products[Number(task[1])]);
			break;
		
		case 'buy':
			sessionStorage.setItem('cart', JSON.stringify(cart));
			window.location.href = "checkout.html";
			break;

        default:
            terminalOutput.innerHTML += `Invalid command: ${command}\n`;
            break;
    }

    terminalInput.value = '';
}

function out(string)
{
	terminalOutput.innerHTML += string+"\n";
}

function viewCommand() {
    out("Available Commands:");
	out("- list: List all products");
	out("- details [product_id]: View product details");
	out("- add [product_id]: Add a product to cart");
	out("- remove [product_id]: Remove a product from cart");
	out("- cart: View your cart");
	out("- buy: Buy all products in the cart");
	out("- clear: Clear the screen");
	out("- search [query]: Search products by name");
	out("- sort [price/name]: Sort products by price or name");
}

function showCart()
{
	out("Your Cart:");
	for(var i=0; i<cart.length; i++)
	{
		out((i+1).toString()+". "+cart[i].title);
	}
}

function remove(item)
{
	for(var i=0; i<cart.length; i++)
	{
		if(cart[i].id == item)
		{
			found = true
			cart.splice(i, 1);
			updateCart();
			break;
		}
	}

	out("No matching product found!")
}

function updateCart()
{
	price = 0
	cart.forEach(product => {
		price += product.price*product.quantity;
	})
	price = Math.round(price*100)/100
	totalPrice.innerHTML = "$"+price.toString()
}

function add(productId)
{
	var product = cart.find(item => item.id == productId);
	if (product) {
		product.quantity++;
	} else {
		product = products.find(item => item.id == productId);
		cart.push({ ...product, quantity: 1 });
	}

	updateCart();
	
	out(product.title + "\n--Added to cart");
}

async function addProductElements()
{
	var colors = [
		'rgb(244, 197, 193)',
		'rgb(194, 228, 169)',
		'rgb(175, 221, 225)',
		'rgb(230, 201, 234)'
	]

	products.forEach(element => {
		const div = document.createElement('div');
		//div.classList.add("title", "pt-4", "pb-1");
		const nameTag = document.createElement('div');
		const img = document.createElement('img');

		img.src = element.image;
		img.classList.add("card-img-top")
		div.classList.add(
			"col-lg-3",
			"col-sm-6",
			"d-flex",
			"flex-column",
			"align-items-center",
			"justify-content-center",
			"product-item",
			"card",
			"my-3"
		);
		div.style.background = colors[Math.floor(Math.random()*colors.length)];
		productList.style.padding = "10px";
		nameTag.classList.add("title", "pt-4", "pb-1");
		nameTag.textContent = element.title;
		//nameTag.classList.add("card-img-top");
		//nameTag.style.position = "relative";
		//nameTag.style.paddingBottom = "50px";
		div.setAttribute("title", element.title);
		div.setAttribute("price", element.price);
		div.appendChild(img);
		div.appendChild(nameTag);
		productList.appendChild(div);
	});
}

async function fetchData() {
	try {
		const response = await fetch('https://fakestoreapi.com/products');
		products = await response.json();
		addProductElements();
	} catch (error) {
		console.error('Error:', error);
	}
}

function main()
{

	fetchData();
}

main()
