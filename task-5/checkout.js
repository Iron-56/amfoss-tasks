const productList = document.querySelector(".product-list")
const total = document.getElementById("total-amount")
cart = []
cprice = 0;

function main()
{

	cart = JSON.parse(sessionStorage.getItem("cart"))
	cart.forEach(item => {
		const product = document.createElement("div");
		const image = document.createElement("img");
		const title = document.createElement("h6");
		const price = document.createElement("h8");
		price.style = "text-align: center;";
		title.innerHTML = item.title;
		price.innerHTML = "$"+item.price.toString();
		if(item.quantity > 1)
		{
			price.innerHTML += "×"+item.quantity.toString();
		}
		product.classList.add("row");
		product.classList.add("product-price");
		product.classList.add("align-items-center");
		image.src = item.image;
		image.classList.add("col-sm");
		title.classList.add("col-sm");
		image.style.maxWidth = "25%";

		product.appendChild(image);
		product.appendChild(title);
		product.appendChild(price);
		productList.appendChild(product);

		cprice += item.price*item.quantity;
	});

	total.innerHTML = "$"+(Math.round((52.48+cprice)*100)/100).toString();
}

main()