// Function to create a new card
        function createCard(url, imageUrl, title, location, allergen) {
            var cardContainer = document.getElementById("cards-container");

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

        window.onclick = function(event) {
          if (!event.target.matches('.dropbtn')) {
            var dropdowns = document.getElementsByClassName("dropdown-content");
            for (var i = 0; i < dropdowns.length; i++) {
              var openDropdown = dropdowns[i];
              if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
              }
            }
          }
        }