//fetch("https://example.com/api/businesses") // Replace with your backend endpoint to retrieve business data-
            //.then(response => response.json())
            //.then(data => {
               // data.forEach(business => {
                    //createCard(
                       // business.url,
                        //business.imageUrl,
                        //business.title,
                       // business.location,
                       // business.allergen
                   // );
                //});
           // })
           // .catch(error => {
              //  console.error("Error:", error);
           // });

function filterSuppliers() {
    var input, filter, suppliers, supplier, name, address1, postcode;
    input = document.getElementById('SearchInput');
    filter = input.value.toUpperCase();
    suppliers = document.getElementById('suppliers');
    supplier = suppliers.getElementsByClassName('supplier');

    for (var i = 0; i < supplier.length; i++) {
        name = supplier[i].getElementsByTagName('h3')[0];
        address1 =supplier[i].getElementsByTagName('p')[0];
        postcode =supplier[i].getElementsByTagName('p')[3];

        if (
            name.innerHTML.toUpperCase().indexOf(filter) > -1 ||
            address1.innerHTML.toUpperCase().indexOf(filter) > -1 ||
            postcode.innerHTML.toUpperCase().indexOf(filter) > -1
        ) {
            supplier[i].style.display = '';
        } else {
            supplier[i].style.display = 'none';
        }
    }
}

function filterItems() {
  var input, filter, inventory, name, dietary;
  input = document.getElementById('SearchInput');
  filter = input.value.toUpperCase();
  inventory = document.getElementsByClassName('InventoryCard');

  for (var i = 0; i < inventory.length; i++) {
    name = inventory[i].getElementsByClassName('item-name')[0];
    dietary = inventory[i].getElementsByClassName('item_dietary')[0];

    if (
      name.innerHTML.toUpperCase().indexOf(filter) > -1 ||
      dietary.innerHTML.toUpperCase().indexOf(filter) > -1
    ) {
      inventory[i].style.display = '';
    } else {
      inventory[i].style.display = 'none';
    }
  }
}


function redirectToSupplier(supplierId) {
    window.location.href = "http://127.0.0.1:5000/order?supplier_id=" + supplierId
}


function removeFromBasket(itemId) {
  var basketItem = document.getElementById(itemId);
  basketItem.style.opacity = 0; // Apply fade-out effect
  setTimeout(function () {
    basketItem.remove(); // Remove the item from the DOM after the fade-out
  }, 500); // Adjust the duration (in milliseconds) of the fade-out effect
}

function addToOrder(itemId) {
  var card = document.getElementById(itemId);
  var itemName = card.querySelector(".item-name").textContent; // Updated class name
  var itemQuantity = parseInt(card.querySelector(".item-quantity").textContent.split(":")[1].trim());
  var basket = document.getElementById("BasketList");
  var basketItems = basket.getElementsByClassName("basket-item");
  var existingItem = null;

  // Check if the item already exists in the basket
  for (var i = 0; i < basketItems.length; i++) {
    var name = basketItems[i].querySelector(".basket-item-name").textContent;
    if (name === itemName) {
      existingItem = basketItems[i];
      break;
    }
  }

  if (existingItem) {
    // If the item already exists, increment the quantity counter
    var quantityElement = existingItem.querySelector(".basket-item-quantity");
    var quantity = parseInt(quantityElement.textContent);
    if (quantity < itemQuantity) {
      quantity++;
      quantityElement.textContent = quantity;
    } else {
      alert("You cannot add more than the available quantity.");
    }
  } else {
    // If the item doesn't exist, add a new item with quantity 1
    var basketItem = document.createElement("li");
    basketItem.className = "basket-item";
    basketItem.innerHTML = `
      <span class="basket-item-name">${itemName}</span>
      <span class="basket-item-quantity"> 1</span>
      <span class="RemoveItem" onclick="removeFromBasket('basket-${itemId}')">x</span>
    `;
    basket.appendChild(basketItem);
  }
}