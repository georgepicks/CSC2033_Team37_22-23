// Function to create a new card
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

function filterCards(location) {
    var cards = document.getElementsByClassName('card');

    for (var i = 0; i < cards.length; i++) {
        var card = cards[i];
        var cardLocation = card.getAttribute('data-location');

        if (cardLocation.toLowerCase() === location.toLowerCase()) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    }
}
var searchInput = document.getElementById('location_search');
searchInput.addEventListener('input', function() {
    filterCards(searchInput.value);
});
