const endpoint=//paste madu
document.addEventListener("DOMContentLoaded", function() {
    async function fetchMovies() {
        try {
            const response = await fetch(endpoint); 
            if (!response.ok) {
                throw new Error('Failed to fetch movies');
            }
            const movies = await response.json();
            return movies;
        } catch (error) {
            console.error("Error fetching movies:", error);
            return [];
        }
    }

    function displayMovies() {
        const movieList = document.getElementById("movie-list");

        fetchMovies().then(movies => {
            movies.forEach(movie => {
                const movieDiv = document.createElement("div");
                movieDiv.classList.add("movie");

                const title = document.createElement("h2");
                title.textContent = movie.title;
                movieDiv.appendChild(title);

                const genre = document.createElement("h2");
                genre.textContent = movie.genre; 
                movieDiv.appendChild(genre); 

                movieList.appendChild(movieDiv);
            });
        });
    }

    displayMovies();
});
