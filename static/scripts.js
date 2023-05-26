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
  var itemName = card.querySelector(".ItemName").textContent;
  var basket = document.getElementById("BasketList");
  var basketItem = document.createElement("li");
  basketItem.id = "basket-" + itemId;
  basketItem.innerHTML = `
  <span>${itemName}</span>
  <span class="RemoveItem" onclick="removeFromBasket('basket-${itemId}')">x</span>
`;
  basket.appendChild(basketItem);
}