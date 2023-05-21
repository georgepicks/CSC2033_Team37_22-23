function createCard(url, imageUrl, title, location, allergen) {
    var cardContainer = document.getElementById("cards_container");

    var cardLink = document.createElement("a");
    cardLink.href = url;

    var cardDiv = document.createElement("div");
    cardDiv.classList.add("card");

    var imageElement = document.createElement("img");
    imageElement.src = imageUrl;
    imageElement.alt = "Food";

    var titleElement = document.createElement("h2");
    titleElement.textContent = title;

    var locationElement = document.createElement("p");
    locationElement.textContent = location;

    var allergenElement = document.createElement("p");
    allergenElement.classList.add("allergen-warning");
    allergenElement.textContent = allergen;

    cardDiv.appendChild(imageElement);
    cardDiv.appendChild(titleElement);
    cardDiv.appendChild(locationElement);
    cardDiv.appendChild(allergenElement);

    cardLink.appendChild(cardDiv);

    cardContainer.appendChild(cardLink);
}

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