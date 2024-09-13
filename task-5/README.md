# TerminalTrolly

## Running Server

```
sudo chmod +x server.sh
```
Run the above command in a terminal to allow permission.

```
./server.sh
```
The above command is to run the program.

## Script.js

* displayList function displays every available product
* sort function sorts on the basis of name (using localeCompare) or price
* search function loops through products and prints to terminal if condition is met.
* showDetails function shows the corresponding product details
* out function writes to the interactive terminal using innerHTML
* showCart function displays products in cart by looping through cart
* remove function removes product from cart by using splice. 
* updateCart function updates the price and innerHTML of totalPrice element.
* add function adds product to cart and also check if product exists (if exists, quantity is updated).
* addProductElements creates elements for each product to be appended to the document.
* fetchData function retrieves daata from web and calls addProductElements to create elements.

I used setItem function of sessionStorage to store cart details to be used when the page gets updated.

## Checkout.js

getItem function of sessionStorage is used to retrieve back the cart details and passed to JSON parser. The total price is calculated using the product price, product quantity and total tax.