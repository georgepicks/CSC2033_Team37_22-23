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

function toggleDropdown() {
    var dropdownContent = document.getElementById("dropdownContent");
    dropdownContent.classList.toggle("show");
}


function filterSuppliers() {
    var input, filter, suppliers, supplier, name, address, allergens;
    input = document.getElementById('search-input');
    filter = input.value.toUpperCase();
    suppliers = document.getElementById('suppliers');
    supplier = suppliers.getElementsByClassName('supplier');

    for (var i = 0; i < supplier.length; i++) {
        name = supplier[i].getElementsByTagName('h3')[0];
        address = supplier[i].getElementsByTagName('p')[0];
        allergens = supplier[i].getElementsByClassName('allergens')[0];

        if (
            name.innerHTML.toUpperCase().indexOf(filter) > -1 ||
            address.innerHTML.toUpperCase().indexOf(filter) > -1 ||
            allergens.innerHTML.toUpperCase().indexOf(filter) > -1
        ) {
            supplier[i].style.display = '';
        } else {
            supplier[i].style.display = 'none';
        }
    }
}

function redirectToSupplier(supplierId) {
    window.location.href = 'https://example.com/pasta'; // Replace with the actual URL for the supplier page
}

function toggleSelected(itemId) {
    var card = document.getElementById(itemId);
    card.classList.toggle("selected");
    var checkbox = card.querySelector("input[type='checkbox']");
    checkbox.checked = !checkbox.checked;

    var basket = document.getElementById("basket");
    var itemName = card.querySelector(".item-name").textContent;
    var basketItem = document.createElement("li");
    basketItem.textContent = itemName;
    if (card.classList.contains("selected")) {
        basket.appendChild(basketItem);
    } else {
        var items = basket.getElementsByTagName("li");
        for (var i = 0; i < items.length; i++) {
            if (items[i].textContent === basketItem.textContent) {
                basket.removeChild(items[i]);
                break;
            }
        }
    }
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
  var itemName = card.querySelector(".item-name").textContent;
  var basket = document.getElementById("basket-list");
  var basketItem = document.createElement("li");
  basketItem.id = "basket-" + itemId;
  basketItem.innerHTML = `
    <span>${itemName}</span>
    <span class="remove-item" onclick="removeFromBasket('basket-${itemId}')">x</span>
  `;
  basket.appendChild(basketItem);
}
