document.addEventListener("DOMContentLoaded", function() {
    function fetchAndRenderMovies(url) {
        fetch(url)
        .then(response => response.json())
        .then(data => {
            document.getElementById("movieContainer").innerHTML = '';

            data.forEach(movie => {
                var movieDiv = document.createElement("div");
                movieDiv.classList.add("movie");
                movieDiv.dataset.id = movie.id;

                var title = document.createElement("h3");
                title.textContent = movie.title;

                var genre = document.createElement("p");
                genre.textContent = "Genre: " + (movie.genre || "N/A");

                var rating = document.createElement("p");
                rating.textContent = "Rating: " + (movie.rating || "N/A");

                var year = document.createElement("p");
                year.textContent = "Year: " + (movie.year || "N/A");

                var detailsButton = document.createElement("button");
                detailsButton.textContent = "View Details";
                detailsButton.addEventListener("click", function() {
                    showMovieDetails(movie.id);
                });

                movieDiv.appendChild(title);
                movieDiv.appendChild(genre);
                movieDiv.appendChild(rating);
                movieDiv.appendChild(year);
                movieDiv.appendChild(detailsButton);

                document.getElementById("movieContainer").appendChild(movieDiv);
            });
        })
        .catch(error => {
            console.error("Error fetching movie data:", error);
        });
    }

    function showMovieDetails(movieId) {
        fetch(`http://127.0.0.1:5000/movie/${movieId}`)
        .then(response => response.json())
        .then(movie => {
            // Display movie details in HTML
            const movieContainer = document.getElementById("movieContainer");
            movieContainer.innerHTML = `
                <h2>${movie.title}</h2>
                <p><strong>Genre:</strong> ${movie.genre || "N/A"}</p>
                <p><strong>Rating:</strong> ${movie.rating || "N/A"}</p>
                <p><strong>Year:</strong> ${movie.year || "N/A"}</p>
            `;
        })
        .catch(error => {
            console.error("Error fetching movie details:", error);
        });
    }

    document.getElementById("searchInput").addEventListener("input", function() {
        const searchTerm = encodeURIComponent(this.value.trim()); // Encode the search term
        
        fetch(`http://127.0.0.1:5000/search?q=${searchTerm}`)
        .then(response => response.json())
        .then(data => {
            fetchAndRenderMovies(`http://127.0.0.1:5000/search?q=${searchTerm}`);
        })
        .catch(error => {
            console.error("Error fetching search results:", error);
        });
    });

    fetchAndRenderMovies("http://127.0.0.1:5000/search?q=");
});
