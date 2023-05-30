/**
 * File: scripts.js.html
 *
 * Authors: George Pickard
 *
 * Description: This JavaScript file contains functions for filtering producers based on their name and location. Filtering items based on the item's name or any allergens the user should be aware of.
 * Redirecting to A producer's order page based on the id of the producer. Adding and removing items from the order basket.
 *
 */


// This function filters the suppliers based on the search input
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
            supplier[i].style.display = ''; // Show the supplier
        } else {
            supplier[i].style.display = 'none'; // Hide the supplier
        }
    }
}

// This function filters the items based on the search input
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
      inventory[i].style.display = ''; // Show the item
    } else {
      inventory[i].style.display = 'none'; // Hide the item
    }
  }
}

// This function redirects to the supplier's order page
function redirectToSupplier(supplierId) {
    window.location.href = "http://127.0.0.1:5000/order?supplier_id=" + supplierId;
}

// This function removes an item from the basket
function removeFromBasket(itemId) {
  var basketItem = document.getElementById(itemId);
  basketItem.style.opacity = 0; // Apply fade-out effect
  setTimeout(function () {
    basketItem.remove(); // Remove the item from the DOM after the fade-out
  }, 500); // Adjust the duration (in milliseconds) of the fade-out effect
}

// This function adds an item to the order basket
function addToOrder(itemId) {
  var card = document.getElementById(itemId);
  var itemName = card.querySelector(".item-name").textContent;
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
    basketItem.id = "basket-" + itemId; // Set the ID of the basket item
    basketItem.innerHTML = `
      <span class="basket-item-name">${itemName}</span>
      <span class="basket-item-quantity">1</span>
      <span class="RemoveItem" onclick="removeFromBasket('basket-${itemId}')">x</span>
      <input type="hidden" name="item[]" value="${itemName}">
      <input type="hidden" name="quantity[]" value="1">
    `;
    basket.appendChild(basketItem);
  }
}